#!/usr/bin/env python3
"""
Gemini API 测试脚本
"""

import os
import google.generativeai as genai

def test_gemini_connection():
    """测试Gemini连接"""
    try:
        # 配置API密钥
        api_key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
        genai.configure(api_key=api_key)

        # 创建模型
        model = genai.GenerativeModel('gemini-pro')

        # 测试简单对话
        response = model.generate_content("你好，请简单介绍一下自己。")

        print("✅ Gemini连接测试成功")
        print(f"回复: {response.text[:100]}...")
        return True

    except Exception as e:
        print(f"❌ Gemini连接测试失败: {e}")
        return False

def test_emotion_analysis():
    """测试情感分析"""
    try:
        api_key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-pro')

        # 测试情感分析
        prompt = "分析以下文本的情感，只返回：happy, sad, angry, calm, neutral\n\n文本：我今天很开心！"
        response = model.generate_content(prompt)

        print("✅ 情感分析测试成功")
        print(f"情感: {response.text.strip()}")
        return True

    except Exception as e:
        print(f"❌ 情感分析测试失败: {e}")
        return False

def test_chat_response():
    """测试聊天回复"""
    try:
        api_key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-pro')

        # 测试聊天回复
        prompt = """
你是Samantha，一个智能、温暖的AI助手。
用户当前情感状态：happy

请根据用户的情感状态提供合适的回应：
- 如果用户情绪低落，提供温暖和支持
- 如果用户情绪积极，分享快乐
- 如果用户情绪愤怒，保持冷静和理解
- 始终保持友好、有帮助的态度

回复要简洁、自然，不超过100字。

用户消息：你好，Samantha！
"""
        response = model.generate_content(prompt)

        print("✅ 聊天回复测试成功")
        print(f"回复: {response.text.strip()}")
        return True

    except Exception as e:
        print(f"❌ 聊天回复测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== Gemini API 测试 ===")
    print()

    tests = [
        ("Gemini连接", test_gemini_connection),
        ("情感分析", test_emotion_analysis),
        ("聊天回复", test_chat_response)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"测试 {test_name}...")
        if test_func():
            passed += 1
        print()

    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有Gemini测试通过！")
        print("💡 提示: 要获得完整功能，请设置GEMINI_API_KEY环境变量")
    else:
        print("⚠️  部分测试失败，请检查Gemini API配置")

if __name__ == "__main__":
    main()
