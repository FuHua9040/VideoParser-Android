#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块测试脚本 - 验证重构后各模块功能

运行方式: python test_modules.py
"""

import sys


def test_models():
    """测试数据模型模块"""
    print("\n" + "="*50)
    print("测试 models.py 模块")
    print("="*50)
    
    try:
        from models import HistoryItem, ParseResult, HistoryCollection
        
        # 测试 HistoryItem
        item = HistoryItem.now("https://example.com/video.mp4", "测试通道")
        print(f"  [OK] HistoryItem 创建成功: {item.get_display_text()}")
        print(f"  [OK] 时间格式化: {item.get_formatted_time()}")
        
        # 测试 ParseResult
        success_result = ParseResult.success("https://play.com/video", "VIP通道")
        print(f"  [OK] ParseResult 成功: {success_result.is_success()}")
        
        fail_result = ParseResult.failure("网络错误", "https://test.com", "通道A")
        print(f"  [OK] ParseResult 失败: {fail_result.error_message}")
        
        # 测试 HistoryCollection
        collection = HistoryCollection()
        collection.add(item)
        print(f"  [OK] HistoryCollection: 共 {len(collection)} 条记录")
        
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_utils():
    """测试工具模块"""
    print("\n" + "="*50)
    print("测试 utils.py 模块")
    print("="*50)
    
    try:
        from utils import URLUtils, StringUtils, PathUtils
        
        # 测试 URLUtils
        valid = URLUtils.is_valid("https://example.com/video.mp4")
        invalid = URLUtils.is_valid("not-a-url")
        print(f"  [OK] URL验证: 有效={valid}, 无效={invalid}")
        
        # 测试 URL 编码
        encoded = URLUtils.encode_url("https://test.com?a=1&b=2")
        print(f"  [OK] URL编码: {encoded}")
        
        # 测试 StringUtils
        truncated = StringUtils.truncate("这是一段很长的文本用于测试截断功能", 10)
        print(f"  [OK] 字符串截断: {truncated}")
        
        # 测试 PathUtils
        history_path = PathUtils.get_history_path()
        print(f"  [OK] 历史记录路径: {history_path}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_services():
    """测试服务模块"""
    print("\n" + "="*50)
    print("测试 services.py 模块")
    print("="*50)
    
    try:
        from services import VideoParserService, HistoryService
        from config import APP_NAME, HISTORY_MAX_ITEMS
        
        # 测试配置加载
        print(f"  [OK] 应用名称: {APP_NAME}")
        print(f"  [OK] 最大历史记录: {HISTORY_MAX_ITEMS}")
        
        # 测试 VideoParserService
        parser = VideoParserService()
        channels = parser.get_all_channels()
        print(f"  [OK] 解析服务: 共 {len(channels)} 个通道")
        
        default_channel = parser.get_default_channel()
        print(f"  [OK] 默认通道: {default_channel}")
        
        # 测试 HistoryService
        history = HistoryService()
        print(f"  [OK] 历史服务初始化成功")
        
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_config():
    """测试配置模块"""
    print("\n" + "="*50)
    print("测试 config.py 模块")
    print("="*50)
    
    try:
        from config import (
            APP_NAME, APP_VERSION, WINDOW_SIZE,
            HISTORY_FILE, HISTORY_MAX_ITEMS,
            DEFAULT_CHANNEL, CHANNELS
        )
        
        print(f"  [OK] APP_NAME: {APP_NAME}")
        print(f"  [OK] APP_VERSION: {APP_VERSION}")
        print(f"  [OK] WINDOW_SIZE: {WINDOW_SIZE}")
        print(f"  [OK] HISTORY_FILE: {HISTORY_FILE}")
        print(f"  [OK] HISTORY_MAX_ITEMS: {HISTORY_MAX_ITEMS}")
        print(f"  [OK] DEFAULT_CHANNEL: {DEFAULT_CHANNEL}")
        print(f"  [OK] CHANNELS: {len(CHANNELS)} 个通道")
        
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "#"*50)
    print("# VideoParser-Android v2.0 模块测试")
    print("#"*50)
    
    results = []
    
    # 运行各模块测试
    results.append(("config", test_config()))
    results.append(("models", test_models()))
    results.append(("utils", test_utils()))
    results.append(("services", test_services()))
    
    # 总结
    print("\n" + "#"*50)
    print("# 测试结果汇总")
    print("#"*50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n所有模块测试通过!")
        return 0
    else:
        print("\n部分模块测试失败，请检查")
        return 1


if __name__ == "__main__":
    sys.exit(main())
