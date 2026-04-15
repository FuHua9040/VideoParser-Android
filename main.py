#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoParser-Android v2.0
视频解析助手 - 重构版

采用 MVC 架构重新设计：
- Model: models.py (数据模型)
- View: views.py (UI 组件)
- Controller: 此类 (业务协调)
- Service: services.py (核心逻辑)
- Config: config.py (配置管理)
- Utils: utils.py (工具函数)

相比 v1.0 的改进：
1. 分层架构：代码职责清晰，易于维护
2. 依赖注入：服务通过构造函数传入，便于测试
3. 事件驱动：UI 与业务逻辑通过回调解耦
4. 类型注解：增强代码可读性和 IDE 支持
5. 丰富注释：每个类和方法都有详细文档
6. 单例服务：确保全局状态一致性
7. 工厂模式：统一 UI 控件创建

作者: FuHua9040 / AI Assistant
日期: 2026-04-15
版本: 2.0
"""

from kivy.app import App
from kivy.core.window import Window

from config import AppConfig
from views import MainLayout
from services import VideoParserService, HistoryService
from models import HistoryItem, ParseResult
from utils import URLUtils


class VideoParserController:
    """
    视频解析控制器
    
    MVC 架构中的 Controller 层，负责：
    - 协调 View（UI）和 Service（业务逻辑）
    - 处理用户交互事件
    - 管理应用状态
    
    采用依赖注入设计，服务通过构造函数传入，
    便于单元测试和 mock
    """
    
    def __init__(
        self,
        view: MainLayout,
        parser_service: VideoParserService,
        history_service: HistoryService
    ):
        """
        初始化控制器
        
        Args:
            view: 主界面视图
            parser_service: 视频解析服务
            history_service: 历史记录服务
        """
        self._view = view
        self._parser_service = parser_service
        self._history_service = history_service
        
        # 绑定 UI 事件
        self._bind_events()
        
        # 加载历史记录
        self._load_history()
    
    def _bind_events(self) -> None:
        """
        绑定 UI 事件
        
        将用户的界面操作（点击按钮等）绑定到控制器方法
        """
        # 播放按钮点击 -> 处理播放
        self._view.play_button.bind(on_press=lambda x: self._on_play())
        
        # 历史记录点击 -> 从历史播放
        # （通过 view 的回调设置）
    
    def _load_history(self) -> None:
        """
        加载历史记录
        
        从 HistoryService 获取最近记录并显示在 UI 上
        """
        recent_items = self._history_service.get_recent(
            AppConfig.MAX_HISTORY_DISPLAY
        )
        self._view.load_history(recent_items)
    
    def _on_play(self) -> None:
        """
        处理播放按钮点击
        
        这是核心的用户交互处理逻辑：
        1. 获取 URL 和通道
        2. 验证输入
        3. 调用异步解析
        4. 更新 UI 状态
        """
        # 获取输入
        url = self._view.get_url()
        channel = self._view.get_channel()
        
        # 验证输入
        if not URLUtils.is_valid(url):
            self._view.set_status(AppConfig.STATUS_ERROR + "：请输入视频链接")
            return
        
        # 更新状态为解析中
        self._view.set_status(AppConfig.STATUS_PARSING)
        
        # 调用异步解析服务
        self._parser_service.parse_async(
            video_url=url,
            channel=channel,
            on_success=lambda result: self._on_parse_success(result, url, channel),
            on_error=self._on_parse_error
        )
    
    def _on_history_click(self, url: str) -> None:
        """
        处理历史记录点击
        
        从历史记录中选择 URL 并播放
        
        Args:
            url: 选中的历史 URL
        """
        # 填入输入框
        self._view.set_url(url)
        # 触发播放
        self._on_play()
    
    def _on_parse_success(self, result: ParseResult, 
                          original_url: str, channel: str) -> None:
        """
        解析成功回调
        
        在 UI 线程更新界面（Kivy 自动处理线程安全）
        
        Args:
            result: 解析结果
            original_url: 原始视频 URL
            channel: 使用的通道
        """
        # 更新状态
        status = AppConfig.STATUS_SUCCESS.format(channel)
        self._view.set_status(status)
        
        # 保存历史记录
        self._history_service.add(original_url, channel)
        
        # 添加历史记录到界面
        new_item = HistoryItem.now(original_url, channel)
        self._view.add_history_item(new_item)
    
    def _on_parse_error(self, error: str) -> None:
        """
        解析失败回调
        
        在 UI 显示错误信息
        
        Args:
            error: 错误信息
        """
        self._view.set_status(f"{AppConfig.STATUS_ERROR}：{error}")


class VideoParserApp(App):
    """
    视频解析应用主类
    
    Kivy 应用的入口点，负责：
    - 初始化服务和控制器
    - 构建界面
    - 配置应用级设置
    
    采用依赖注入容器模式，所有依赖在此组装
    """
    
    def build(self) -> MainLayout:
        """
        构建应用
        
        Kivy 框架的回调方法，返回根 Widget
        
        Returns:
            主界面布局
        """
        # 设置窗口背景色
        Window.clearcolor = AppConfig.WINDOW_BG_COLOR
        
        # 初始化服务（单例）
        parser_service = VideoParserService()
        history_service = HistoryService(max_store=AppConfig.MAX_HISTORY_STORE)
        
        # 构建视图
        view = MainLayout()
        view.build(
            channel_names=parser_service.get_available_channels(),
            default_channel=parser_service.get_default_channel(),
            on_play=lambda x: None,  # 占位，实际由控制器绑定
            on_history_click=lambda url: None  # 占位
        )
        
        # 创建控制器，注入依赖
        controller = VideoParserController(
            view=view,
            parser_service=parser_service,
            history_service=history_service
        )
        
        # 重新绑定历史记录点击（需要 controller 实例）
        view.history_view.on_item_click = controller._on_history_click
        
        return view


if __name__ == '__main__':
    # 应用入口
    VideoParserApp().run()
