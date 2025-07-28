from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import webbrowser
import urllib.parse
import time
import os

class VideoParserApp(App):
    def build(self):
        # 创建主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title = Label(text="视频解析助手", font_size=24, bold=True, size_hint_y=0.1)
        main_layout.add_widget(title)
        
        # 内容区域
        content_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # URL输入框
        content_layout.add_widget(Label(text="请输入视频链接:"))
        self.url_input = TextInput(multiline=False, size_hint_y=None, height=40)
        content_layout.add_widget(self.url_input)
        
        # 解析通道选择
        content_layout.add_widget(Label(text="选择解析通道:"))
        self.channel_spinner = Spinner(
            values=['高清通道1', '超清通道2', '蓝光通道3', 'VIP通道4'],
            size_hint=(None, None),
            size=(300, 40),
            text='高清通道1'
        )
        content_layout.add_widget(self.channel_spinner)
        
        # 播放按钮
        play_btn = Button(text="播放视频", size_hint_y=None, height=50)
        play_btn.bind(on_press=self.play_video)
        content_layout.add_widget(play_btn)
        
        # 状态标签
        self.status_label = Label(text="就绪", italic=True, size_hint_y=0.1)
        content_layout.add_widget(self.status_label)
        
        # 历史记录区域
        history_label = Label(text="历史记录:", size_hint_y=0.1)
        content_layout.add_widget(history_label)
        
        # 滚动区域
        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.history_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll_view.add_widget(self.history_layout)
        content_layout.add_widget(scroll_view)
        
        # 加载历史记录
        self.load_history()
        
        main_layout.add_widget(content_layout)
        return main_layout
    
    def play_video(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "错误：请输入视频链接"
            return
            
        # 更新状态
        self.status_label.text = "正在解析..."
        
        # 解析逻辑
        try:
            # 选择解析通道
            channel_map = {
                '高清通道1': 'https://jx.bozrc.com:4433/player/?url=',
                '超清通道2': 'https://www.ckplayer.vip/jiexi/?url=',
                '蓝光通道3': 'https://jx.playerjy.com/?url=',
                'VIP通道4': 'https://www.playm3u8.cn/jiexi.php?url='
            }
            
            base_url = channel_map.get(self.channel_spinner.text, channel_map['高清通道1'])
            full_url = base_url + urllib.parse.quote_plus(url)
            
            # 在浏览器中打开
            webbrowser.open(full_url)
            self.status_label.text = f"已打开：{self.channel_spinner.text}"
            
            # 保存历史记录
            self.save_history(url)
            
            # 添加历史记录项
            history_btn = Button(text=url[:50] + "..." if len(url) > 50 else url, 
                                 size_hint_y=None, height=40)
            history_btn.bind(on_press=lambda x: self.play_from_history(url))
            self.history_layout.add_widget(history_btn)
                
        except Exception as e:
            self.status_label.text = f"错误：{str(e)}"
    
    def save_history(self, url):
        """保存历史记录到文件"""
        try:
            with open("history.txt", "a") as f:
                f.write(f"{time.time()}:{url}\n")
        except:
            pass
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists("history.txt"):
                with open("history.txt", "r") as f:
                    for line in f.readlines()[-10:]:  # 只显示最近10条
                        _, url = line.strip().split(":", 1)
                        history_btn = Button(text=url[:50] + "..." if len(url) > 50 else url, 
                                             size_hint_y=None, height=40)
                        history_btn.bind(on_press=lambda x, u=url: self.play_from_history(u))
                        self.history_layout.add_widget(history_btn)
        except:
            pass
    
    def play_from_history(self, url):
        """从历史记录播放"""
        self.url_input.text = url
        self.play_video(None)

if __name__ == '__main__':
    VideoParserApp().run()
