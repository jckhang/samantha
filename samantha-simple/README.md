# Samantha AI 助手 - 最简化版本

一个基于LLM的智能AI助手Android应用，专注于核心功能，提供简洁而强大的AI交互体验。

## 🎯 核心功能

- **智能对话**: 基于GPT-3.5的智能问答
- **语音交互**: 语音识别和合成（待实现）
- **情感回应**: 基础情感分析和情感化回复

## 🏗️ 技术架构

```
Android App (Kotlin + Compose) ↔ FastAPI (Python) ↔ OpenAI GPT-3.5
```

### 技术栈

**前端 (Android)**
- Kotlin + Jetpack Compose
- MVVM架构 + Hilt依赖注入
- Room本地数据库
- Retrofit网络请求

**后端 (Python)**
- FastAPI框架
- SQLite数据库
- OpenAI GPT-3.5集成

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Android Studio Arctic Fox+
- OpenAI API密钥

### 1. 克隆项目

```bash
git clone <repository-url>
cd samantha-simple
```

### 2. 配置环境变量

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. 启动后端服务

```bash
# 使用启动脚本
./start.sh

# 或手动启动
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 4. 运行Android应用

1. 在Android Studio中打开 `android-app` 项目
2. 确保Android模拟器正在运行
3. 点击运行按钮

## 📱 应用界面

```
┌─────────────────────────┐
│     Samantha AI         │
├─────────────────────────┤
│                         │
│    对话区域             │
│                         │
│                         │
├─────────────────────────┤
│  [🎤] [输入框] [发送]   │
└─────────────────────────┘
```

## 🔧 开发指南

### 项目结构

```
samantha-simple/
├── android-app/          # Android应用
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/samantha/
│   │   │   │   ├── data/          # 数据层
│   │   │   │   ├── domain/        # 业务逻辑层
│   │   │   │   ├── presentation/  # 表现层
│   │   │   │   └── di/            # 依赖注入
│   │   │   └── res/               # 资源文件
│   │   └── build.gradle
│   └── gradle/
├── backend/              # 后端服务
│   ├── main.py          # FastAPI主文件
│   ├── requirements.txt # Python依赖
│   └── Dockerfile       # Docker配置
├── docker-compose.yml   # Docker Compose
├── start.sh            # 启动脚本
└── README.md
```

### API端点

- `POST /chat` - 发送消息
- `GET /history/{user_id}` - 获取对话历史
- `GET /health` - 健康检查

### 测试API

```bash
# 发送消息
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "你好", "user_id": 1}'

# 获取历史
curl "http://localhost:8000/history/1"

# 健康检查
curl "http://localhost:8000/health"
```

## 🐳 Docker部署

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📊 功能状态

| 功能 | 状态 | 说明 |
|------|------|------|
| 基础对话 | ✅ 完成 | GPT-3.5集成，情感分析 |
| 语音识别 | 🔄 待实现 | 计划使用Android Speech API |
| 语音合成 | 🔄 待实现 | 计划使用Android TTS |
| 本地存储 | ✅ 完成 | Room数据库 |
| 网络请求 | ✅ 完成 | Retrofit + OkHttp |

## 🔮 后续计划

### 第二阶段 (2-3周)
- [ ] 语音识别集成
- [ ] 语音合成功能
- [ ] 语音/文字切换

### 第三阶段 (1周)
- [ ] 优化情感分析
- [ ] 改进用户界面
- [ ] 性能优化

## 🐛 故障排除

### 常见问题

1. **后端服务无法启动**
   - 检查Python版本 (需要3.9+)
   - 检查OpenAI API密钥是否正确
   - 查看后端日志

2. **Android应用无法连接后端**
   - 确保后端服务在运行
   - 检查网络配置 (模拟器使用10.0.2.2)
   - 查看Android日志

3. **API调用失败**
   - 检查OpenAI API配额
   - 检查网络连接
   - 查看API响应日志

### 日志查看

```bash
# 后端日志
cd backend
tail -f logs/app.log

# Docker日志
docker-compose logs -f backend
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**专注核心，简单有效！** 🎯
