# Gemini API 配置指南

## 获取 Gemini API 密钥

### 1. 访问 Google AI Studio

1. 打开 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用Google账户登录

### 2. 创建 API 密钥

1. 点击 "Create API Key" 按钮
2. 选择 "Create API Key in new project" 或现有项目
3. 复制生成的API密钥

### 3. 设置环境变量

#### 方法1: 在启动脚本中设置

编辑 `backend/start_backend.sh`:

```bash
export GEMINI_API_KEY="your-actual-gemini-api-key-here"
```

#### 方法2: 在系统环境变量中设置

```bash
# macOS/Linux
export GEMINI_API_KEY="your-actual-gemini-api-key-here"

# Windows
set GEMINI_API_KEY=your-actual-gemini-api-key-here
```

#### 方法3: 创建 .env 文件

在 `backend/` 目录下创建 `.env` 文件:

```
GEMINI_API_KEY=your-actual-gemini-api-key-here
```

## 测试配置

### 1. 测试 Gemini API

```bash
cd backend
python ../test_gemini.py
```

### 2. 测试完整API

```bash
cd backend
python ../test_api.py
```

### 3. 启动后端服务

```bash
cd backend
./start_backend.sh
```

## API 使用说明

### 模型选择

- **gemini-pro**: 文本生成模型（推荐）
- **gemini-pro-vision**: 支持图像和文本的多模态模型

### 基本用法

```python
import google.generativeai as genai

# 配置API密钥
genai.configure(api_key="your-api-key")

# 创建模型
model = genai.GenerativeModel('gemini-pro')

# 生成内容
response = model.generate_content("你好，请介绍一下自己。")
print(response.text)
```

### 参数配置

```python
# 设置生成参数
response = model.generate_content(
    "写一个短故事",
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        top_p=0.8,
        top_k=40,
        max_output_tokens=2048,
    )
)
```

## 错误处理

### 常见错误

1. **API_KEY_INVALID**: API密钥无效
   - 检查API密钥是否正确
   - 确认API密钥已激活

2. **QUOTA_EXCEEDED**: 配额超限
   - 检查API使用量
   - 等待配额重置或升级计划

3. **SAFETY_BLOCKED**: 内容被安全过滤器阻止
   - 修改提示词
   - 避免敏感内容

### 调试技巧

```python
try:
    response = model.generate_content(prompt)
    print(response.text)
except Exception as e:
    print(f"错误: {e}")
    print(f"错误类型: {type(e).__name__}")
```

## 成本控制

### 定价

- Gemini Pro: $0.0005 / 1K characters (输入)
- Gemini Pro Vision: $0.0025 / 1K characters (输入)

### 优化建议

1. 限制输入长度
2. 使用缓存机制
3. 设置合理的max_output_tokens
4. 监控API使用量

## 安全注意事项

1. **保护API密钥**
   - 不要在代码中硬编码
   - 使用环境变量
   - 不要提交到版本控制

2. **内容过滤**
   - 实施输入验证
   - 监控输出内容
   - 设置安全策略

3. **访问控制**
   - 限制API访问
   - 监控异常使用
   - 定期轮换密钥

## 相关链接

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API 文档](https://ai.google.dev/docs)
- [Python SDK 文档](https://ai.google.dev/tutorials/python_quickstart)
- [API 参考](https://ai.google.dev/api/python/google/generativeai)
