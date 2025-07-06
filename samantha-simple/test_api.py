#!/usr/bin/env python3
"""
Samantha AI API 测试脚本
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查端点"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_root():
    """测试根端点"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"根端点: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"根端点测试失败: {e}")
        return False

def test_chat():
    """测试聊天端点"""
    try:
        data = {
            "message": "你好，Samantha！",
            "user_id": 1
        }
        response = requests.post(f"{BASE_URL}/chat", json=data)
        print(f"聊天测试: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"聊天测试失败: {e}")
        return False

def test_history():
    """测试历史记录端点"""
    try:
        response = requests.get(f"{BASE_URL}/history/1?limit=5")
        print(f"历史记录测试: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"历史记录测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== Samantha AI API 测试 ===")
    print()

    tests = [
        ("健康检查", test_health),
        ("根端点", test_root),
        ("聊天功能", test_chat),
        ("历史记录", test_history)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"测试 {test_name}...")
        if test_func():
            print(f"✅ {test_name} 通过")
            passed += 1
        else:
            print(f"❌ {test_name} 失败")
        print()

    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！API运行正常。")
    else:
        print("⚠️  部分测试失败，请检查API服务。")

if __name__ == "__main__":
    main()
