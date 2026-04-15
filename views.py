#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视图模块 - UI 组件定义

此模块包含所有的 UI 组件：
- 主界面布局
- 历史记录列表
- 各种控件工厂

使用工厂模式创建控件，统一样式

作者: AI Assistant
日期: 2026-04-15
版本: 2.0
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from typing import Callable, List, Optional

from config import AppConfig
from models import HistoryItem


class WidgetFactory:
    """
    控件工厂类
    
    统一创建各种 UI 控件，确保样式一致性
    使用工厂模式避免重复样式代码
    """
    
    @staticmethod
    def create_title(text: str) -> Label:
        """
        创建标题标签
        
        Args:
            text: 标题文本
            
        Returns:
            配置好的 Label
        """
        return Label(
            text=text,
            font_size=24,
            bold=True,
            color=AppConfig.WINDOW_TITLE_COLOR,
            size_hint_y=0.1
        )
    
    @staticmethod
    def create_label(text: str, size_hint_y: float = 0.1, 
                     italic: bool = False) -> Label:
        """
        创建普通标签
        
        Args:
            text: 标签文本
            size_hint_y: 垂直尺寸比例
            italic: 是否斜体
            
        Returns:
            配置好的 Label
        """
        return Label(
            text=text,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=size_hint_y,
            italic=italic
        )
    
    @staticmethod
    def create_text_input(multiline: bool = False, 
                         height: int = None) -> TextInput:
        """
        创建文本输入框
        
        Args:
            multiline: 是否多行
            height: 固定高度（None 表示自适应）
            
        Returns:
            配置好的 TextInput
        """
        kwargs = {
            'multiline': multiline,
            'background_color': (1, 1, 1, 1),
            'foreground_color': (0, 0, 0, 1)
        }
        if height:
            kwargs['size_hint_y'] = None
            kwargs['height'] = height
        return TextInput(**kwargs)
    
    @staticmethod
    def create_spinner(values: List[str], default: str, 
                     size: tuple = None) -> Spinner:
        """
        创建下拉选择器
        
        Args:
            values: 选项列表
            default: 默认值
            size: 固定尺寸 (width, height)
            
        Returns:
            配置好的 Spinner
        """
        kwargs = {
            'values': values,
            'text': default,
            'background_color': AppConfig.SPINNER_BG_COLOR
        }
        if size:
            kwargs['size_hint'] = (None, None)
            kwargs['size'] = size
        return Spinner(**kwargs)
    
    @staticmethod
    def create_primary_button(text: str, height: int = 50,
                             on_press: Callable = None) -> Button:
        """
        创建主按钮（蓝色）
        
        Args:
            text: 按钮文本
            height: 固定高度
            on_press: 点击回调
            
        Returns:
            配置好的 Button
        """
        btn = Button(
            text=text,
            size_hint_y=None,
            height=height,
            background_color=AppConfig.PRIMARY_BTN_COLOR,
            color=AppConfig.PRIMARY_BTN_TEXT_COLOR
        )
        if on_press:
            btn.bind(on_press=on_press)
        return btn
    
    @staticmethod
    def create_history_button(text: str, height: int = 40,
                             on_press: Callable = None) -> Button:
        """
        创建历史记录按钮
        
        Args:
            text: 按钮文本
            height: 固定高度
            on_press: 点击回调
            
        Returns:
            配置好的 Button
        """
        btn = Button(
            text=text,
            size_hint_y=None,
            height=height,
            background_color=AppConfig.HISTORY_BTN_COLOR,
            color=AppConfig.HISTORY_BTN_TEXT_COLOR
        )
        if on_press:
            btn.bind(on_press=on_press)
        return btn


class HistoryListView(BoxLayout):
    """
    历史记录列表视图
    
    封装历史记录的显示逻辑：
    - 滚动容器
    - 动态添加/清除记录
    - 点击回调
    """
    
    def __init__(self, on_item_click: Callable[[str], None], **kwargs):
        """
        初始化
        
        Args:
            on_item_click: 记录点击回调，接收 URL
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.on_item_click = on_item_click
        self._buttons: List[Button] = []
        
        # 创建标签
        self.add_widget(WidgetFactory.create_label("历史记录:", size_hint_y=0.1))
        
        # 创建滚动区域
        self.scroll_view = ScrollView(size_hint=(1, 0.3))
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll_view.add_widget(self.grid)
        self.add_widget(self.scroll_view)
    
    def add_item(self, item: HistoryItem) -> None:
        """
        添加一条历史记录
        
        Args:
            item: 历史记录项
        """
        display_text = item.get_display_text(AppConfig.URL_DISPLAY_MAX_LEN)
        url = item.url
        
        btn = WidgetFactory.create_history_button(
            display_text,
            height=AppConfig.HISTORY_ITEM_HEIGHT,
            on_press=lambda x: self.on_item_click(url)
        )
        
        self.grid.add_widget(btn)
        self._buttons.append(btn)
    
    def add_items(self, items: List[HistoryItem]) -> None:
        """
        批量添加历史记录
        
        Args:
            items: 历史记录列表
        """
        for item in items:
            self.add_item(item)
    
    def clear(self) -> None:
        """
        清空所有记录
        """
        self.grid.clear_widgets()
        self._buttons.clear()


class MainLayout(BoxLayout):
    """
    主界面布局
    
    组装所有 UI 组件成完整界面
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = AppConfig.MAIN_PADDING
        self.spacing = AppConfig.MAIN_SPACING
        
        # 初始化控件引用（供外部访问）
        self.url_input: Optional[TextInput] = None
        self.channel_spinner: Optional[Spinner] = None
        self.status_label: Optional[Label] = None
        self.history_view: Optional[HistoryListView] = None
        self.play_button: Optional[Button] = None
    
    def build(self, 
              channel_names: List[str],
              default_channel: str,
              on_play: Callable,
              on_history_click: Callable[[str], None]) -> 'MainLayout':
        """
        构建界面
        
        Args:
            channel_names: 可用通道名称列表
            default_channel: 默认通道
            on_play: 播放按钮点击回调
            on_history_click: 历史记录点击回调
            
        Returns:
            自身实例（链式调用）
        """
        # 标题
        self.add_widget(WidgetFactory.create_title(AppConfig.APP_NAME))
        
        # 内容区域
        content = BoxLayout(orientation='vertical', spacing=AppConfig.CONTENT_SPACING)
        
        # URL 输入
        content.add_widget(WidgetFactory.create_label("请输入视频链接:"))
        self.url_input = WidgetFactory.create_text_input(
            height=AppConfig.INPUT_HEIGHT
        )
        content.add_widget(self.url_input)
        
        # 通道选择
        content.add_widget(WidgetFactory.create_label("选择解析通道:"))
        self.channel_spinner = WidgetFactory.create_spinner(
            channel_names,
            default_channel,
            size=AppConfig.SPINNER_SIZE
        )
        content.add_widget(self.channel_spinner)
        
        # 播放按钮
        self.play_button = WidgetFactory.create_primary_button(
            "播放视频",
            height=AppConfig.BUTTON_HEIGHT,
            on_press=on_play
        )
        content.add_widget(self.play_button)
        
        # 状态标签
        self.status_label = WidgetFactory.create_label(
            AppConfig.STATUS_READY,
            size_hint_y=0.1,
            italic=True
        )
        content.add_widget(self.status_label)
        
        # 历史记录列表
        self.history_view = HistoryListView(on_history_click)
        content.add_widget(self.history_view)
        
        self.add_widget(content)
        
        return self
    
    def get_url(self) -> str:
        """
        获取输入的 URL
        
        Returns:
            输入框中的文本（已去除首尾空白）
        """
        if self.url_input:
            return self.url_input.text.strip()
        return ""
    
    def set_url(self, url: str) -> None:
        """
        设置输入框 URL
        
        Args:
            url: 要设置的 URL
        """
        if self.url_input:
            self.url_input.text = url
    
    def get_channel(self) -> str:
        """
        获取选中的通道
        
        Returns:
            当前选中的通道名称
        """
        if self.channel_spinner:
            return self.channel_spinner.text
        return ""
    
    def set_status(self, text: str) -> None:
        """
        设置状态文本
        
        Args:
            text: 状态信息
        """
        if self.status_label:
            self.status_label.text = text
    
    def add_history_item(self, item: HistoryItem) -> None:
        """
        添加历史记录到视图
        
        Args:
            item: 历史记录项
        """
        if self.history_view:
            self.history_view.add_item(item)
    
    def load_history(self, items: List[HistoryItem]) -> None:
        """
        加载历史记录列表
        
        Args:
            items: 历史记录列表
        """
        if self.history_view:
            self.history_view.clear()
            self.history_view.add_items(items)
