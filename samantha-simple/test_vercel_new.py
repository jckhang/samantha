#!/usr/bin/env python3
"""
测试Vercel部署的最新更改 - 使用google-genai
"""

import requests
import json
import time

# Vercel部署URL
VERCEL_URL = "https://samantha-ai-dev.vercel.app"

def test_health():
    """测试健康检查"""
    print("=== 健康检查测试 ===")
    try:
        response = requests.get(f"{VERCEL_URL}/health", timeout=10)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_root():
    """测试根路径"""
    print("\n=== 根路径测试 ===")
    try:
        response = requests.get(f"{VERCEL_URL}/", timeout=10)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 根路径成功: {data}")
            return True
        else:
            print(f"❌ 根路径失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 根路径异常: {e}")
        return False

def test_chat():
    """测试聊天功能"""
    print("\n=== 聊天功能测试 ===")
    try:
        chat_data = {
            "message": "你好，Samantha！",
            "user_id": 1
        }

        response = requests.post(
            f"{VERCEL_URL}/chat",
            json=chat_data,
            timeout=30
        )
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 聊天成功:")
            print(f"  用户消息: {chat_data['message']}")
            print(f"  AI回复: {data['response']}")
            print(f"  情感分析: {data['emotion']}")
            return True
        else:
            print(f"❌ 聊天失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 聊天异常: {e}")
        return False

def test_history():
    """测试历史记录"""
    print("\n=== 历史记录测试 ===")
    try:
        response = requests.get(f"{VERCEL_URL}/history/1?limit=5", timeout=10)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 历史记录成功: 获取到 {len(data)} 条记录")
            if len(data) > 0:
                latest = data[0]
                print(f"  最新记录: {latest['message']} -> {latest['response'][:50]}...")
            return True
        else:
            print(f"❌ 历史记录失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 历史记录异常: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n=== 错误处理测试 ===")
    try:
        # 测试无效的聊天请求
        invalid_data = {
            "message": "",  # 空消息
            "user_id": 1
        }

        response = requests.post(
            f"{VERCEL_URL}/chat",
            json=invalid_data,
            timeout=10
        )
        print(f"空消息测试状态码: {response.status_code}")

        if response.status_code in [400, 422]:
            print("✅ 错误处理正常 (空消息被拒绝)")
        else:
            print(f"⚠️  意外响应: {response.text}")

        return True
    except Exception as e:
        print(f"❌ 错误处理测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 测试Vercel部署的最新更改")
    print("=" * 50)

    tests = [
        ("健康检查", test_health),
        ("根路径", test_root),
        ("聊天功能", test_chat),
        ("历史记录", test_history),
        ("错误处理", test_error_handling)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 测试 {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)  # 避免请求过快

    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！Vercel部署工作正常")
    else:
        print("⚠️  部分测试失败，请检查部署配置")

    print(f"\n🌐 Vercel URL: {VERCEL_URL}")

if __name__ == "__main__":
    main()
