#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务模块 - 核心业务逻辑

此模块包含应用的核心业务逻辑：
- 视频解析服务
- 历史记录服务

采用服务层模式，将业务逻辑与 UI 分离

作者: AI Assistant
日期: 2026-04-15
版本: 2.0
"""

import json
import webbrowser
from typing import Callable, Optional, List
from concurrent.futures import ThreadPoolExecutor

from config import ParserConfig
from utils import URLUtils, PathUtils
from models import HistoryItem, HistoryCollection, ParseResult


class VideoParserService:
    """
    视频解析服务
    
    负责处理视频解析的核心逻辑：
    - 根据通道选择构建解析 URL
    - 在浏览器中打开
    - 异步执行避免阻塞 UI
    
    使用单例模式确保全局唯一实例
    """
    
    _instance: Optional['VideoParserService'] = None
    _executor = ThreadPoolExecutor(max_workers=1)
    
    def __new__(cls) -> 'VideoParserService':
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def parse_async(
        self,
        video_url: str,
        channel: str,
        on_success: Callable[[ParseResult], None],
        on_error: Callable[[str], None]
    ) -> None:
        """
        异步解析视频
        
        在后台线程执行解析操作，完成后回调 UI 更新
        
        Args:
            video_url: 视频原始 URL
            channel: 解析通道名称
            on_success: 成功回调，接收 ParseResult
            on_error: 失败回调，接收错误信息
        """
        def _do_parse():
            try:
                result = self._parse_sync(video_url, channel)
                if result.is_success():
                    on_success(result)
                else:
                    on_error(result.error_message or "解析失败")
            except Exception as e:
                on_error(str(e))
        
        # 提交到线程池执行
        self._executor.submit(_do_parse)
    
    def _parse_sync(self, video_url: str, channel: str) -> ParseResult:
        """
        同步解析（内部方法）
        
        实际执行解析操作，构建 URL 并在浏览器打开
        
        Args:
            video_url: 视频 URL
            channel: 解析通道
            
        Returns:
            ParseResult 解析结果
        """
        try:
            # 获取解析通道 URL
            base_url = ParserConfig.get_channel_url(channel)
            
            # 构建完整解析 URL
            full_url = URLUtils.build_parser_url(base_url, video_url)
            
            # 在浏览器中打开
            webbrowser.open(full_url)
            
            return ParseResult.success(full_url, channel)
            
        except Exception as e:
            return ParseResult.failure(str(e), video_url, channel)
    
    def get_available_channels(self) -> List[str]:
        """
        获取可用通道列表
        
        Returns:
            通道名称列表
        """
        return ParserConfig.get_channel_names()
    
    def get_default_channel(self) -> str:
        """
        获取默认通道
        
        Returns:
            默认通道名称
        """
        return ParserConfig.DEFAULT_CHANNEL


class HistoryService:
    """
    历史记录服务
    
    负责历史记录的持久化和查询：
    - 加载/保存历史记录
    - 添加新记录
    - 获取最近记录
    
    同样使用单例模式
    """
    
    _instance: Optional['HistoryService'] = None
    
    def __new__(cls) -> 'HistoryService':
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, max_store: int = 20):
        """
        初始化（仅首次有效）
        
        Args:
            max_store: 最大存储数量
        """
        if self._initialized:
            return
        
        self._max_store = max_store
        self._collection = HistoryCollection()
        self._file_path = PathUtils.get_history_path()
        self._initialized = True
        
        # 初始化时加载历史记录
        self._load()
    
    def add(self, url: str, channel: str) -> None:
        """
        添加历史记录
        
        创建新记录，裁剪数量，并保存到文件
        
        Args:
            url: 视频 URL
            channel: 使用的通道
        """
        # 创建新记录
        item = HistoryItem.now(url, channel)
        
        # 添加到集合
        self._collection.add(item)
        
        # 裁剪数量
        self._collection.trim(self._max_store)
        
        # 保存到文件
        self._save()
    
    def get_recent(self, count: int) -> List[HistoryItem]:
        """
        获取最近 N 条记录
        
        Args:
            count: 数量
            
        Returns:
            历史记录列表
        """
        return self._collection.get_recent(count)
    
    def get_all(self) -> List[HistoryItem]:
        """
        获取所有记录
        
        Returns:
            所有历史记录
        """
        return self._collection.get_all()
    
    def _load(self) -> None:
        """
        从文件加载历史记录（内部方法）
        """
        try:
            if not PathUtils.file_exists(self._file_path):
                return
            
            with open(self._file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self._collection = HistoryCollection.from_json_list(data)
                    
        except json.JSONDecodeError:
            # JSON 格式错误，清空
            self._collection = HistoryCollection()
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            self._collection = HistoryCollection()
    
    def _save(self) -> None:
        """
        保存历史记录到文件（内部方法）
        """
        try:
            PathUtils.ensure_dir(self._file_path)
            
            with open(self._file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    self._collection.to_json_list(),
                    f,
                    indent=2,
                    ensure_ascii=False
                )
                
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def clear(self) -> None:
        """
        清空历史记录
        """
        self._collection = HistoryCollection()
        self._save()
