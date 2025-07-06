# Samantha AI助手

一个基于LLM的智能AI助手Android应用，灵感来源于电影《Her》中的Samantha。Samantha不仅是一个功能强大的助手，更是一个能够理解情感、建立深度连接的AI伙伴。

## 🌟 项目特色

- **情感智能**: 多模态情感识别，理解用户情绪状态
- **个性化交互**: 基于用户画像的定制化体验
- **自然语音**: 高质量语音识别和情感化语音合成
- **持续学习**: 从交互中学习用户偏好和行为模式
- **隐私保护**: 端到端加密，本地优先的数据处理

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Android App   │    │   Backend API   │    │   AI Services   │
│                 │    │                 │    │                 │
│ • Jetpack       │◄──►│ • FastAPI       │◄──►│ • LLM Models    │
│   Compose       │    │ • PostgreSQL    │    │ • Speech Models │
│ • MVVM          │    │ • Redis         │    │ • Emotion AI    │
│ • Hilt DI       │    │ • RabbitMQ      │    │ • TTS Engine    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 快速开始

### 环境要求

- Android Studio Arctic Fox 或更高版本
- Android SDK API 24+
- Kotlin 1.8+
- Python 3.9+ (后端服务)
- Node.js 16+ (可选，用于某些工具)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/samantha.git
   cd samantha
   ```

2. **配置Android项目**
   ```bash
   # 进入Android项目目录
   cd android-app

   # 配置环境变量
   cp .env.example .env
   # 编辑.env文件，添加必要的API密钥

   # 构建项目
   ./gradlew build
   ```

3. **配置后端服务**
   ```bash
   # 进入后端目录
   cd backend

   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或 venv\Scripts\activate  # Windows

   # 安装依赖
   pip install -r requirements.txt

   # 配置环境变量
   cp .env.example .env
   # 编辑.env文件

   # 启动服务
   uvicorn main:app --reload
   ```

4. **配置数据库**
   ```bash
   # 启动PostgreSQL
   docker-compose up -d postgres redis

   # 运行数据库迁移
   alembic upgrade head
   ```

## 📱 功能特性

### 核心功能
- ✅ 智能文本对话
- ✅ 语音识别和合成
- ✅ 情感状态识别
- ✅ 个性化回应生成
- ✅ 对话历史管理

### 高级功能
- 🔄 多模态交互 (开发中)
- 🔄 用户画像构建 (开发中)
- 🔄 智能推荐系统 (开发中)
- 🔄 AR集成 (计划中)
- 🔄 多设备同步 (计划中)

## 🛠️ 技术栈

### 前端 (Android)
- **语言**: Kotlin
- **UI框架**: Jetpack Compose
- **架构**: MVVM + Clean Architecture
- **依赖注入**: Hilt
- **异步处理**: Coroutines + Flow
- **本地存储**: Room + DataStore
- **网络**: Retrofit + OkHttp

### 后端
- **语言**: Python
- **框架**: FastAPI
- **数据库**: PostgreSQL + Redis
- **消息队列**: RabbitMQ
- **容器化**: Docker

### AI/ML
- **LLM**: OpenAI GPT-4, Anthropic Claude
- **语音**: OpenAI Whisper, Azure Speech Services
- **情感分析**: 自定义CNN + Transformer模型
- **TTS**: YourTTS, Azure TTS

## 📁 项目结构

```
samantha/
├── android-app/           # Android应用
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
├── backend/               # 后端服务
│   ├── app/
│   │   ├── api/           # API路由
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务服务
│   │   └── utils/         # 工具函数
│   ├── requirements.txt
│   └── main.py
├── ai-services/           # AI服务
│   ├── llm/               # 大语言模型
│   ├── speech/            # 语音处理
│   ├── emotion/           # 情感分析
│   └── tts/               # 语音合成
├── docs/                  # 文档
│   ├── architecture.md    # 架构设计
│   ├── features.md        # 功能特性
│   ├── roadmap.md         # 开发路线图
│   └── technical-implementation.md
├── docker-compose.yml     # Docker配置
└── README.md
```

## 🔧 开发指南

### 代码规范
- 遵循Kotlin官方编码规范
- 使用Ktlint进行代码格式化
- 提交前运行单元测试
- 使用语义化提交信息

### 测试
```bash
# 运行Android单元测试
./gradlew test

# 运行后端测试
cd backend
pytest

# 运行集成测试
./gradlew connectedAndroidTest
```

### 部署
```bash
# 构建Android APK
./gradlew assembleRelease

# 部署后端服务
docker-compose up -d

# 部署到Google Play Store
./gradlew bundleRelease
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

### 贡献流程
1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 🙏 致谢

- 感谢电影《Her》带来的灵感
- 感谢所有开源项目的贡献者
- 感谢社区的支持和反馈

## 📞 联系我们

- 项目主页: [https://github.com/your-username/samantha](https://github.com/your-username/samantha)
- 问题反馈: [Issues](https://github.com/your-username/samantha/issues)
- 讨论区: [Discussions](https://github.com/your-username/samantha/discussions)
- 邮箱: samantha@example.com

---

**让Samantha成为你的AI伙伴，一起探索智能交互的未来！** 🤖💫
