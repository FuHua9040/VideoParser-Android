[app]
title = 视频解析助手
package.name = videoparser
package.domain = org.videoparser
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy==2.2.1,urllib3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.ndk = 25.2.9519653
android.sdk = 34.0.0
p4a.branch = master
android.arch = arm64-v8a

# 日志设置
[buildozer]
log_level = 2
