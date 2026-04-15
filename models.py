#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型模块 - 业务实体定义

此模块定义应用中的核心数据模型：
- 历史记录项
- 解析结果

采用 dataclass 简化模型定义，提供类型安全和序列化支持

作者: AI Assistant
日期: 2026-04-15
版本: 2.0
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass
class HistoryItem:
    """
    历史记录项数据类
    
    表示一条视频解析历史记录，包含：
    - 时间戳：记录创建时间
    - URL：视频原始链接
    - 通道：使用的解析通道
    
    Attributes:
        timestamp: Unix 时间戳（秒）
        url: 视频 URL
        channel: 解析通道名称
    """
    timestamp: int
    url: str
    channel: str
    
    @classmethod
    def now(cls, url: str, channel: str) -> 'HistoryItem':
        """
        创建当前时间的记录项
        
        工厂方法，自动使用当前时间创建记录
        
        Args:
            url: 视频 URL
            channel: 解析通道
            
        Returns:
            新的 HistoryItem 实例
        """
        return cls(
            timestamp=int(time.time()),
            url=url,
            channel=channel
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        用于 JSON 序列化
        
        Returns:
            字典表示
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HistoryItem':
        """
        从字典创建实例
        
        用于 JSON 反序列化
        
        Args:
            data: 字典数据
            
        Returns:
            HistoryItem 实例
        """
        return cls(**data)
    
    def get_display_text(self, max_length: int = 50) -> str:
        """
        获取用于界面显示的文本
        
        截断过长的 URL
        
        Args:
            max_length: 最大显示长度
            
        Returns:
            显示文本
        """
        if len(self.url) > max_length:
            return self.url[:max_length] + "..."
        return self.url
    
    def get_formatted_time(self) -> str:
        """
        获取格式化的时间字符串
        
        Returns:
            格式如 "2026-04-15 13:30:00"
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))


@dataclass
class ParseResult:
    """
    解析结果数据类
    
    表示视频解析操作的结果
    
    Attributes:
        success: 是否成功
        url: 解析后的播放 URL（失败时为空字符串）
        channel: 使用的解析通道（失败时为空字符串）
        error_message: 错误信息（失败时）
    """
    success: bool
    url: str = ""
    channel: str = ""
    error_message: Optional[str] = None
    
    @classmethod
    def success(cls, url: str, channel: str) -> 'ParseResult':
        """
        创建成功结果
        
        Args:
            url: 解析后的 URL
            channel: 使用的通道
            
        Returns:
            成功的 ParseResult
        """
        return cls(success=True, url=url, channel=channel)
    
    @classmethod
    def failure(cls, error: str, url: str = "", channel: str = "") -> 'ParseResult':
        """
        创建失败结果
        
        Args:
            error: 错误信息
            url: 原始 URL
            channel: 尝试的通道
            
        Returns:
            失败的 ParseResult
        """
        return cls(success=False, url=url, channel=channel, error_message=error)
    
    def is_success(self) -> bool:
        """
        检查是否成功
        
        Returns:
            操作是否成功
        """
        return self.success


class HistoryCollection:
    """
    历史记录集合类
    
    管理多条历史记录，提供增删改查和序列化功能
    """
    
    def __init__(self, items: Optional[List[HistoryItem]] = None):
        """
        初始化
        
        Args:
            items: 初始记录列表
        """
        self._items: List[HistoryItem] = items or []
    
    def add(self, item: HistoryItem) -> None:
        """
        添加记录
        
        新记录添加到列表末尾
        
        Args:
            item: 要添加的记录项
        """
        self._items.append(item)
    
    def get_all(self) -> List[HistoryItem]:
        """
        获取所有记录
        
        Returns:
            记录项列表
        """
        return self._items.copy()
    
    def get_recent(self, count: int) -> List[HistoryItem]:
        """
        获取最近 N 条记录
        
        Args:
            count: 数量
            
        Returns:
            最近的记录列表（最新的在后）
        """
        return self._items[-count:]
    
    def trim(self, max_count: int) -> None:
        """
        裁剪记录数量
        
        只保留最近的 N 条
        
        Args:
            max_count: 最大保留数量
        """
        if len(self._items) > max_count:
            self._items = self._items[-max_count:]
    
    def to_json_list(self) -> List[Dict[str, Any]]:
        """
        转换为 JSON 可序列化的列表
        
        Returns:
            字典列表
        """
        return [item.to_dict() for item in self._items]
    
    @classmethod
    def from_json_list(cls, data: List[Dict[str, Any]]) -> 'HistoryCollection':
        """
        从 JSON 列表创建
        
        Args:
            data: 字典列表
            
        Returns:
            HistoryCollection 实例
        """
        items = []
        for item_data in data:
            try:
                items.append(HistoryItem.from_dict(item_data))
            except Exception:
                # 跳过无效数据
                continue
        return cls(items)
    
    def __len__(self) -> int:
        """
        获取记录数量
        
        Returns:
            记录总数
        """
        return len(self._items)
    
    def __iter__(self):
        """
        迭代器支持
        
        Yields:
            HistoryItem
        """
        return iter(self._items)
