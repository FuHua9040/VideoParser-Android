#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块 - 通用功能函数

此模块包含项目中使用的各种工具函数：
- URL 处理
- 文件路径操作
- 字符串处理

作者: AI Assistant
日期: 2026-04-15
版本: 2.0
"""

import os
import urllib.parse
from typing import Optional


class URLUtils:
    """
    URL 工具类
    
    处理与 URL 相关的各种操作
    """
    
    @staticmethod
    def encode_url(url: str) -> str:
        """
        对 URL 进行编码
        
        将特殊字符转换为 URL 安全格式，确保解析接口能正确接收
        
        Args:
            url: 原始 URL 字符串
            
        Returns:
            编码后的 URL 字符串
        """
        return urllib.parse.quote_plus(url)
    
    @staticmethod
    def build_parser_url(base_url: str, video_url: str) -> str:
        """
        构建完整的解析 URL
        
        将基础解析接口和视频 URL 拼接成完整的请求地址
        
        Args:
            base_url: 解析接口基础 URL
            video_url: 视频原始 URL
            
        Returns:
            完整的解析请求 URL
        """
        encoded_video = URLUtils.encode_url(video_url)
        return base_url + encoded_video
    
    @staticmethod
    def truncate(url: str, max_length: int = 50, suffix: str = "...") -> str:
        """
        截断 URL 用于显示
        
        当 URL 过长时，截断显示以保持界面整洁
        
        Args:
            url: 原始 URL
            max_length: 最大显示长度
            suffix: 截断后缀
            
        Returns:
            截断后的字符串
        """
        if len(url) > max_length:
            return url[:max_length] + suffix
        return url
    
    @staticmethod
    def is_valid(url: str) -> bool:
        """
        简单验证 URL 是否有效
        
        检查 URL 是否为空或仅包含空白字符
        
        Args:
            url: 待验证的 URL
            
        Returns:
            URL 是否有效
        """
        return bool(url and url.strip())


class PathUtils:
    """
    路径工具类
    
    处理文件路径相关操作，适配不同平台（Windows/Android）
    """
    
    @staticmethod
    def get_history_path(filename: str = "history.json") -> str:
        """
        获取历史记录文件路径
        
        根据运行环境自动选择合适的路径：
        - Android: 使用应用私有目录
        - 其他: 使用当前工作目录
        
        Args:
            filename: 历史记录文件名
            
        Returns:
            完整的历史记录文件路径
        """
        # Android 环境使用私有目录
        if 'ANDROID_PRIVATE' in os.environ:
            return os.path.join(os.environ['ANDROID_PRIVATE'], filename)
        
        # 普通环境使用当前目录
        return filename
    
    @staticmethod
    def ensure_dir(path: str) -> None:
        """
        确保目录存在
        
        如果目录不存在则创建
        
        Args:
            path: 目录路径
        """
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            path: 文件路径
            
        Returns:
            文件是否存在
        """
        return os.path.exists(path)


class StringUtils:
    """
    字符串工具类
    
    处理字符串相关操作
    """
    
    @staticmethod
    def safe_strip(text: Optional[str]) -> str:
        """
        安全地去除字符串首尾空白
        
        处理 None 值的情况，避免异常
        
        Args:
            text: 输入字符串，可能为 None
            
        Returns:
            处理后的字符串
        """
        if text is None:
            return ""
        return str(text).strip()
    
    @staticmethod
    def format_status(template: str, *args) -> str:
        """
        格式化状态消息
        
        安全地格式化状态字符串
        
        Args:
            template: 模板字符串
            *args: 格式化参数
            
        Returns:
            格式化后的字符串
        """
        try:
            return template.format(*args)
        except Exception:
            return template
