#!/usr/bin/env python3
"""
Gemini API 诊断脚本
"""

import os
import requests
import json

def check_api_key_format():
    """检查API密钥格式"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    print("=== API密钥格式检查 ===")
    print(f"API密钥长度: {len(api_key)}")
    print(f"API密钥前缀: {api_key[:10]}...")
    print(f"API密钥后缀: ...{api_key[-4:]}")

    if api_key.startswith("AIza"):
        print("✅ API密钥格式正确 (以AIza开头)")
    else:
        print("❌ API密钥格式不正确")

    if len(api_key) == 39:
        print("✅ API密钥长度正确 (39字符)")
    else:
        print(f"❌ API密钥长度不正确 (期望39字符，实际{len(api_key)}字符)")

    print()

def test_gemini_api_directly():
    """直接测试Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    print("=== 直接API测试 ===")

    # 测试API密钥是否有效
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            print("✅ API密钥有效，可以访问模型列表")
            models = response.json()
            print(f"可用模型数量: {len(models.get('models', []))}")
            for model in models.get('models', [])[:3]:  # 显示前3个模型
                print(f"  - {model.get('name', 'Unknown')}")
        elif response.status_code == 400:
            print("❌ API密钥无效")
            error_data = response.json()
            print(f"错误详情: {json.dumps(error_data, indent=2)}")
        elif response.status_code == 403:
            print("❌ API密钥有效但权限不足")
            error_data = response.json()
            print(f"错误详情: {json.dumps(error_data, indent=2)}")
        else:
            print(f"❌ 未知错误: {response.status_code}")
            print(f"响应: {response.text[:200]}...")

    except Exception as e:
        print(f"❌ 请求失败: {e}")

    print()

def test_generate_content():
    """测试生成内容API"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    print("=== 生成内容API测试 ===")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Hello, please respond with 'OK' if you can see this message."
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            print("✅ 生成内容API工作正常")
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"响应: {text}")
        else:
            print(f"❌ 生成内容API失败: {response.status_code}")
            error_data = response.json()
            print(f"错误详情: {json.dumps(error_data, indent=2)}")

    except Exception as e:
        print(f"❌ 请求失败: {e}")

    print()

def provide_solutions():
    """提供解决方案"""
    print("=== 解决方案建议 ===")
    print("1. 检查API密钥来源:")
    print("   - 确保从 https://makersuite.google.com/app/apikey 获取")
    print("   - 不要从Google Cloud Console获取")
    print()
    print("2. 检查项目设置:")
    print("   - 确保项目已启用Generative Language API")
    print("   - 检查API配额和限制")
    print()
    print("3. 检查API密钥权限:")
    print("   - 确保API密钥有正确的权限")
    print("   - 检查是否启用了必要的API")
    print()
    print("4. 重新生成API密钥:")
    print("   - 删除现有密钥")
    print("   - 重新创建新的API密钥")
    print()
    print("5. 检查网络环境:")
    print("   - 确保网络可以访问Google API")
    print("   - 考虑使用VPN或代理")

def main():
    """主函数"""
    print("🔍 Gemini API 诊断工具")
    print("=" * 50)

    check_api_key_format()
    test_gemini_api_directly()
    test_generate_content()
    provide_solutions()

if __name__ == "__main__":
    main()
