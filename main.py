from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import webbrowser
import urllib.parse
import time

class VideoParserApp(App):
    def build(self):
        # 创建主布局
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title = Label(text="视频解析助手", font_size=24, bold=True)
        layout.add_widget(title)
        
        # URL输入框
        layout.add_widget(Label(text="请输入视频链接:"))
        self.url_input = TextInput(multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.url_input)
        
        # 解析通道选择
        layout.add_widget(Label(text="选择解析通道:"))
        self.channel_spinner = Spinner(
            values=['高清通道1', '超清通道2', '蓝光通道3', 'VIP通道4'],
            size_hint=(None, None),
            size=(300, 40),
            text='高清通道1'
        )
        layout.add_widget(self.channel_spinner)
        
        # 播放按钮
        play_btn = Button(text="播放视频", size_hint_y=None, height=50)
        play_btn.bind(on_press=self.play_video)
        layout.add_widget(play_btn)
        
        # 状态标签
        self.status_label = Label(text="就绪", italic=True)
        layout.add_widget(self.status_label)
        
        return layout
    
    def play_video(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "错误：请输入视频链接"
            return
            
        # 更新状态
        self.status_label.text = "正在解析..."
        
        # 解析逻辑（简化版）
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
            
            # 添加历史记录（简化）
            with open("history.txt", "a") as f:
                f.write(f"{time.time()}:{url}\n")
                
        except Exception as e:
            self.status_label.text = f"错误：{str(e)}"

if __name__ == '__main__':
    VideoParserApp().run()
