from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import webbrowser
import urllib.parse
import time
import os
import threading
import json

class VideoParserApp(App):
    def build(self):
        # 设置窗口背景颜色
        Window.clearcolor = (0.95, 0.95, 1, 1)  # 淡蓝色背景
        
        # 创建主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title = Label(
            text="视频解析助手", 
            font_size=24, 
            bold=True, 
            color=(0.1, 0.2, 0.6, 1),  # 深蓝色
            size_hint_y=0.1
        )
        main_layout.add_widget(title)
        
        # 内容区域
        content_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # URL输入框
        url_label = Label(
            text="请输入视频链接:", 
            color=(0.1, 0.1, 0.1, 1),  # 深灰色
            size_hint_y=0.1
        )
        content_layout.add_widget(url_label)
        
        self.url_input = TextInput(
            multiline=False, 
            size_hint_y=None, 
            height=40,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        content_layout.add_widget(self.url_input)
        
        # 解析通道选择
        channel_label = Label(
            text="选择解析通道:", 
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=0.1
        )
        content_layout.add_widget(channel_label)
        
        self.channel_spinner = Spinner(
            values=['高清通道1', '超清通道2', '蓝光通道3', 'VIP通道4'],
            size_hint=(None, None),
            size=(300, 40),
            text='高清通道1',
            background_color=(0.9, 0.9, 1, 1)
        )
        content_layout.add_widget(self.channel_spinner)
        
        # 播放按钮
        play_btn = Button(
            text="播放视频", 
            size_hint_y=None, 
            height=50,
            background_color=(0.3, 0.5, 1, 1),  # 蓝色按钮
            color=(1, 1, 1, 1)  # 白色文字
        )
        play_btn.bind(on_press=self.play_video)
        content_layout.add_widget(play_btn)
        
        # 状态标签
        self.status_label = Label(
            text="就绪", 
            italic=True, 
            color=(0.3, 0.3, 0.3, 1),  # 灰色
            size_hint_y=0.1
        )
        content_layout.add_widget(self.status_label)
        
        # 历史记录区域
        history_label = Label(
            text="历史记录:", 
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=0.1
        )
        content_layout.add_widget(history_label)
        
        # 滚动区域
        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.history_layout = GridLayout(
            cols=1, 
            spacing=5, 
            size_hint_y=None
        )
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll_view.add_widget(self.history_layout)
        content_layout.add_widget(scroll_view)
        
        main_layout.add_widget(content_layout)
        
        # 加载历史记录
        self.load_history()
        
        return main_layout
    
    def play_video(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "错误：请输入视频链接"
            return
            
        # 更新状态
        self.status_label.text = "正在解析..."
        
        # 使用线程避免界面卡顿
        threading.Thread(target=self._play_video, args=(url,), daemon=True).start()
    
    def _play_video(self, url):
        try:
            # 选择解析通道
            channel_map = {
                '高清通道1': 'https://jx.bozrc.com:4433/player/?url=',
                '超清通道2': 'https://www.ckplayer.vip/jiexi/?url=',
                '蓝光通道3': 'https://jx.playerjy.com/?url=',
                'VIP通道4': 'https://www.playm3u8.cn/jiexi.php?url='
            }
            
            channel = self.channel_spinner.text
            base_url = channel_map.get(channel, channel_map['高清通道1'])
            full_url = base_url + urllib.parse.quote_plus(url)
            
            # 在浏览器中打开
            webbrowser.open(full_url)
            self.status_label.text = f"已通过 {channel} 打开视频"
            
            # 保存历史记录
            self.save_history(url)
            
            # 添加历史记录项
            self.add_history_button(url)
                
        except Exception as e:
            self.status_label.text = f"错误：{str(e)}"
    
    def get_history_path(self):
        """获取历史记录文件路径"""
        # 在Android上使用应用私有目录
        if 'ANDROID_PRIVATE' in os.environ:
            return os.path.join(os.environ['ANDROID_PRIVATE'], 'history.json')
        # 在普通环境下使用当前目录
        return 'history.json'
    
    def save_history(self, url):
        """保存历史记录到文件"""
        try:
            history_path = self.get_history_path()
            history = []
            
            # 加载现有历史记录
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    try:
                        history = json.load(f)
                    except:
                        history = []
            
            # 添加新记录
            timestamp = int(time.time())
            history.append({
                "timestamp": timestamp,
                "url": url,
                "channel": self.channel_spinner.text
            })
            
            # 只保留最近的20条记录
            history = history[-20:]
            
            # 保存文件
            with open(history_path, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def load_history(self):
        """加载历史记录"""
        try:
            history_path = self.get_history_path()
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    history = json.load(f)
                    
                    # 只显示最近的10条记录
                    for item in history[-10:]:
                        self.add_history_button(item['url'])
        except Exception as e:
            print(f"加载历史记录失败: {e}")
    
    def add_history_button(self, url):
        """添加一个历史记录按钮到界面"""
        # 创建历史记录按钮
        history_btn = Button(
            text=url[:50] + "..." if len(url) > 50 else url, 
            size_hint_y=None, 
            height=40,
            background_color=(0.95, 0.95, 1, 1),  # 淡蓝色背景
            color=(0.2, 0.2, 0.2, 1)  # 深灰色文字
        )
        history_btn.bind(on_press=lambda x: self.play_from_history(url))
        self.history_layout.add_widget(history_btn)
    
    def play_from_history(self, url):
        """从历史记录播放"""
        self.url_input.text = url
        self.play_video(None)

if __name__ == '__main__':
    VideoParserApp().run()
