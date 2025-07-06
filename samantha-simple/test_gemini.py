#!/usr/bin/env python3
"""
Gemini API 测试脚本 - 使用 google-genai
"""

import os
import google.genai as genai

# 创建Gemini客户端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

def test_gemini_connection():
    """测试Gemini连接"""
    print("测试 Gemini连接...")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Hello, please respond with 'OK'"
        )
        if response.text.strip():
            print("✅ Gemini连接测试成功")
            return True
        else:
            print("❌ Gemini连接测试失败: 空响应")
            return False
    except Exception as e:
        print(f"❌ Gemini连接测试失败: {e}")
        return False

def test_emotion_analysis():
    """测试情感分析"""
    print("测试 情感分析...")
    try:
        prompt = "分析以下文本的情感，只返回：happy, sad, angry, calm, neutral\n\n文本：我今天很开心！"

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        emotion = response.text.strip().lower()

        valid_emotions = ['happy', 'sad', 'angry', 'calm', 'neutral']
        if any(valid in emotion for valid in valid_emotions):
            print(f"✅ 情感分析测试成功: {emotion}")
            return True
        else:
            print(f"❌ 情感分析测试失败: 无效情感 {emotion}")
            return False
    except Exception as e:
        print(f"❌ 情感分析测试失败: {e}")
        return False

def test_chat_response():
    """测试聊天回复"""
    print("测试 聊天回复...")
    try:
        prompt = """
你是Samantha，一个智能、温暖的AI助手。
用户当前情感状态：happy

请根据用户的情感状态提供合适的回应：
- 如果用户情绪低落，提供温暖和支持
- 如果用户情绪积极，分享快乐
- 如果用户情绪愤怒，保持冷静和理解
- 始终保持友好、有帮助的态度

回复要简洁、自然，不超过100字。

用户消息：你好！
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        ai_response = response.text.strip()

        if len(ai_response) > 0:
            print(f"✅ 聊天回复测试成功: {ai_response[:50]}...")
            return True
        else:
            print("❌ 聊天回复测试失败: 空响应")
            return False
    except Exception as e:
        print(f"❌ 聊天回复测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=== Gemini API 测试 ===")
    print()

    # 检查API密钥
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        print("❌ 未设置 GEMINI_API_KEY 环境变量")
        return

    # 运行测试
    tests = [
        test_gemini_connection,
        test_emotion_analysis,
        test_chat_response
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    # 输出结果
    print(f"测试结果: {passed}/{len(tests)} 通过")
    if passed == len(tests):
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查Gemini API配置")

if __name__ == "__main__":
    main()
