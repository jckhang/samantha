# Samantha AI 项目笔记

## 项目概述

Samantha AI 是一个智能聊天助手项目，包含Android客户端和Python后端。

## 技术栈

- **前端**: Android (Kotlin + Jetpack Compose)
- **后端**: Python (FastAPI + SQLite)
- **AI服务**: Google Gemini (google-genai库)
- **架构**: MVVM + Repository Pattern
- **部署**: Vercel (美国节点)

## 最近解决的问题

### Android 网络通信问题 (2025-07-06)

**问题描述**: Android应用无法连接到后端API，出现错误：

```
CLEARTEXT communication to 10.0.2.2 not permitted by network security policy
```

**根本原因**: Android 9.0+ **默认禁止明文HTTP通信**

**解决方案**:

1. 创建网络安全配置文件 `network_security_config.xml`
2. 在 `AndroidManifest.xml` 中引用配置
3. 在 `NetworkModule.kt` 中添加 `ConnectionSpec.CLEARTEXT` 支持

**具体步骤**:

```xml
<!-- network_security_config.xml -->
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">127.0.0.1</domain>
    </domain-config>
</network-security-config>
```

```xml
<!-- AndroidManifest.xml -->
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```

```kotlin
// NetworkModule.kt
.connectionSpecs(listOf(
    ConnectionSpec.CLEARTEXT,  // 允许明文连接
    ConnectionSpec.MODERN_TLS,
    ConnectionSpec.COMPATIBLE_TLS
))
```

**验证结果**:

- 后端API测试通过 (4/4)
- Android应用重新构建成功
- 网络通信问题已解决

### API服务替换 (2025-07-06)

**问题描述**: 将OpenAI API替换为Google Gemini API

**替换内容**:

1. **依赖更新**: `openai==1.3.0` → `google-genai==1.24.0`
2. **代码修改**:
   - 导入: `import openai` → `import google.genai as genai`
   - 配置: `openai.api_key` → `client = genai.Client(api_key=...)`
   - 模型: `gpt-3.5-turbo` → `gemini-1.5-flash`
   - API调用: `openai.ChatCompletion.create()` → `client.models.generate_content()`

**具体修改**:

```python
# 旧代码 (OpenAI)
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[...]
)

# 新代码 (Gemini - google-genai库)
import google.genai as genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=prompt
)
```

**环境变量更新**:

- `OPENAI_API_KEY` → `GEMINI_API_KEY`

**文档更新**:

- README.md, TROUBLESHOOTING.md, 环境变量示例文件
- 所有OpenAI相关引用替换为Gemini

**验证结果**:

- ✅ 依赖安装成功
- ✅ 代码修改完成
- ✅ API测试通过 (4/4)
- ✅ 文档更新完成

### Vercel海外部署 (2025-07-06)

**问题描述**: 本地环境无法访问Google Gemini API，出现地区限制错误

**根本原因**:

- 错误信息: `User location is not supported for the API use`
- 本地网络环境不被Google Gemini API支持

**解决方案**: 部署到Vercel美国节点

**部署过程**:

1. **初始部署失败**: 文件大小超限 (2641个文件 > 250MB)
2. **创建精简部署**: 只包含必要文件 (3个文件)
3. **成功部署**: 美国华盛顿特区节点

**部署结果**:

- ✅ 项目名称: `vercel-deploy`
- ✅ 生产环境: `https://samantha-ai-dev.vercel.app`
- ✅ 部署地区: 美国华盛顿特区
- ✅ 构建时间: 8秒
- ✅ 访问保护: 已配置环境变量并禁用访问保护
- ✅ API测试: 5/5 通过

**部署文件结构**:

```
vercel-deploy/
├── api/
│   └── index.py          # FastAPI主入口
├── requirements.txt      # Python依赖
└── vercel.json          # Vercel配置
```

**优势**:

- 解决地区限制问题
- 免费额度充足
- 全球CDN，低延迟
- 自动部署，无需服务器管理

## 项目结构

```
samantha-simple/
├── android-app/          # Android客户端
├── backend/             # Python后端
├── vercel-deploy/       # Vercel部署目录
├── docs/               # 文档
├── notes/              # 笔记
├── test_api.py         # API测试脚本
├── test_gemini.py      # Gemini API测试脚本 (google-genai)
├── test_vercel_new.py  # Vercel API测试脚本
├── diagnose_gemini.py  # Gemini API诊断脚本
└── VERCEL_DEPLOYMENT.md # Vercel部署文档
```

## 开发环境设置

### 后端启动

```bash
cd backend
./start_backend.sh
```

### Android构建

```bash
cd android-app
./gradlew assembleDebug
```

### Vercel部署

```bash
cd vercel-deploy
vercel --prod
```

## 关键文件

- `backend/main.py` - FastAPI后端服务
- `vercel-deploy/api/index.py` - Vercel部署的FastAPI入口
- `android-app/app/src/main/java/com/samantha/di/NetworkModule.kt` - 网络配置
- `android-app/app/src/main/AndroidManifest.xml` - Android清单文件
- `android-app/app/src/main/res/xml/network_security_config.xml` - 网络安全配置
- `backend/requirements.txt` - Python依赖
- `vercel-deploy/vercel.json` - Vercel配置

## 注意事项

- 开发环境使用HTTP，生产环境需要HTTPS
- Android模拟器使用 `10.0.2.2` 访问主机
- 需要配置Google Gemini API密钥才能正常使用AI功能
- Gemini API使用 `gemini-1.5-flash` 模型 (google-genai库)
- API调用方式与OpenAI不同，使用 `client.models.generate_content()` 方法
- Vercel部署在美国，解决地区限制问题
- Vercel访问保护已配置并禁用
- Android端API地址已更新为 `https://samantha-ai-dev.vercel.app/`

## 下一步计划

1. ✅ 配置Vercel环境变量 `GEMINI_API_KEY`
2. ✅ 禁用Vercel访问保护
3. ✅ 更新Android应用使用Vercel API地址
4. ✅ 测试完整的聊天功能
5. 优化UI/UX
6. 添加语音识别功能
7. 测试Gemini API的完整功能
