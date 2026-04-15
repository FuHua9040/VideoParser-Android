#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块 - 集中管理应用配置

此模块包含所有可配置的参数，便于修改和扩展：
- 解析通道配置
- UI 样式配置
- 应用常量

作者: AI Assistant
日期: 2026-04-15
版本: 2.0
"""

from typing import Dict, Tuple


class AppConfig:
    """
    应用配置类
    
    集中管理所有应用级别的配置项，避免硬编码分散在代码各处
    """
    
    # ==================== 应用基本信息 ====================
    APP_NAME: str = "视频解析助手"
    APP_VERSION: str = "2.0"
    APP_AUTHOR: str = "FuHua9040"
    
    # ==================== 窗口配置 ====================
    WINDOW_BG_COLOR: Tuple[float, float, float, float] = (0.95, 0.95, 1, 1)  # 淡蓝色背景
    WINDOW_TITLE_COLOR: Tuple[float, float, float, float] = (0.1, 0.2, 0.6, 1)  # 深蓝色标题
    
    # ==================== UI 样式配置 ====================
    # 主按钮样式
    PRIMARY_BTN_COLOR: Tuple[float, float, float, float] = (0.3, 0.5, 1, 1)  # 蓝色按钮
    PRIMARY_BTN_TEXT_COLOR: Tuple[float, float, float, float] = (1, 1, 1, 1)  # 白色文字
    
    # 历史记录按钮样式
    HISTORY_BTN_COLOR: Tuple[float, float, float, float] = (0.95, 0.95, 1, 1)  # 淡蓝色背景
    HISTORY_BTN_TEXT_COLOR: Tuple[float, float, float, float] = (0.2, 0.2, 0.2, 1)  # 深灰色文字
    
    # 下拉选择器样式
    SPINNER_BG_COLOR: Tuple[float, float, float, float] = (0.9, 0.9, 1, 1)  # 淡紫蓝色
    
    # 状态标签颜色
    STATUS_READY: str = "就绪"
    STATUS_ERROR: str = "错误"
    STATUS_PARSING: str = "正在解析..."
    STATUS_SUCCESS: str = "已通过 {} 打开视频"
    
    # ==================== 布局配置 ====================
    # 内边距和间距
    MAIN_PADDING: int = 20
    MAIN_SPACING: int = 15
    CONTENT_SPACING: int = 10
    
    # 控件尺寸
    INPUT_HEIGHT: int = 40
    BUTTON_HEIGHT: int = 50
    HISTORY_ITEM_HEIGHT: int = 40
    SPINNER_SIZE: Tuple[int, int] = (300, 40)
    
    # 历史记录显示限制
    MAX_HISTORY_DISPLAY: int = 10  # 界面最多显示条数
    MAX_HISTORY_STORE: int = 20    # 文件最多存储条数
    URL_DISPLAY_MAX_LEN: int = 50  # URL 截断长度
    
    # ==================== 文件配置 ====================
    HISTORY_FILENAME: str = "history.json"


class ParserConfig:
    """
    解析器配置类
    
    管理视频解析通道的配置信息
    支持动态添加新的解析通道
    """
    
    # 解析通道映射表
    # key: 显示名称
    # value: 解析接口 URL 模板（需要在末尾拼接视频 URL）
    CHANNELS: Dict[str, str] = {
        '高清通道1': 'https://jx.bozrc.com:4433/player/?url=',
        '超清通道2': 'https://www.ckplayer.vip/jiexi/?url=',
        '蓝光通道3': 'https://jx.playerjy.com/?url=',
        'VIP通道4': 'https://www.playm3u8.cn/jiexi.php?url='
    }
    
    # 默认通道
    DEFAULT_CHANNEL: str = '高清通道1'
    
    @classmethod
    def get_channel_url(cls, channel_name: str) -> str:
        """
        获取指定通道的解析 URL
        
        Args:
            channel_name: 通道显示名称
            
        Returns:
            解析接口 URL 模板，如果不存在则返回默认通道
        """
        return cls.CHANNELS.get(channel_name, cls.CHANNELS[cls.DEFAULT_CHANNEL])
    
    @classmethod
    def get_channel_names(cls) -> list:
        """
        获取所有通道名称列表
        
        Returns:
            通道名称字符串列表
        """
        return list(cls.CHANNELS.keys())
    
    @classmethod
    def add_channel(cls, name: str, url: str) -> None:
        """
        动态添加新通道
        
        Args:
            name: 通道显示名称
            url: 解析接口 URL 模板
        """
        cls.CHANNELS[name] = url
