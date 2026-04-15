# VideoParser-Android v2.0

视频解析助手 Android 版 - 重构版

## 项目结构

```
VideoParser-Android/
├── main.py          # 应用入口 (MVC Controller)
├── config.py        # 配置管理
├── models.py        # 数据模型
├── views.py         # UI 组件
├── services.py      # 业务逻辑
├── utils.py         # 工具函数
├── requirements.txt # 依赖列表
└── README.md        # 项目说明
```

## 架构设计

采用 **MVC + Service** 分层架构：

- **Model** (`models.py`): 定义 `HistoryItem`, `ParseResult` 等数据类
- **View** (`views.py`): 封装所有 UI 控件，使用工厂模式统一创建
- **Controller** (`main.py`): 协调 View 和 Service，处理用户交互
- **Service** (`services.py`): 核心业务逻辑（视频解析、历史记录管理）
- **Config** (`config.py`): 集中管理配置参数
- **Utils** (`utils.py`): 通用工具函数

## 相比 v1.0 的改进

1. **分层架构**: 代码职责清晰，易于维护扩展
2. **依赖注入**: 服务通过构造函数传入，便于单元测试
3. **事件驱动**: UI 与业务逻辑解耦
4. **类型注解**: 增强代码可读性和 IDE 支持
5. **丰富注释**: 每个类和方法都有详细文档
6. **单例模式**: 确保全局服务状态一致性
7. **工厂模式**: 统一 UI 控件创建，样式一致

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py

# Android 打包
buildozer android debug deploy run
```

## 配置说明

编辑 `config.py` 修改：
- 解析通道 URL
- UI 样式颜色
- 历史记录数量限制

## 作者

FuHua9040
