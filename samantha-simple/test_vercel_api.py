#!/usr/bin/env python3
"""
Vercel API 测试脚本
"""

import requests
import json

# Vercel部署的API地址
VERCEL_API_URL = "https://vercel-deploy-yuxiang-jckhangs-projects-5b6d8741.vercel.app"

def test_vercel_api():
    """测试Vercel API"""
    print("=== Vercel API 测试 ===")
    print(f"API地址: {VERCEL_API_URL}")
    print()

    # 测试根路径
    try:
        response = requests.get(f"{VERCEL_API_URL}/")
        print(f"根路径测试: {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.json()}")
        else:
            print(f"响应: {response.text[:200]}...")
    except Exception as e:
        print(f"根路径测试失败: {e}")

    print()

    # 测试健康检查
    try:
        response = requests.get(f"{VERCEL_API_URL}/health")
        print(f"健康检查测试: {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.json()}")
        else:
            print(f"响应: {response.text[:200]}...")
    except Exception as e:
        print(f"健康检查测试失败: {e}")

    print()

    # 测试聊天功能
    try:
        data = {
            "message": "你好，Samantha！",
            "user_id": 1
        }
        response = requests.post(f"{VERCEL_API_URL}/chat", json=data)
        print(f"聊天功能测试: {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.json()}")
        else:
            print(f"响应: {response.text[:200]}...")
    except Exception as e:
        print(f"聊天功能测试失败: {e}")

if __name__ == "__main__":
    test_vercel_api()
