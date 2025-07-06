#!/bin/bash

echo "🚀 启动 Samantha AI 助手..."

# 检查是否安装了必要的工具
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到 Docker，请先安装 Docker"
    exit 1
fi

# 设置环境变量
export OPENAI_API_KEY=${OPENAI_API_KEY:-"your-openai-api-key-here"}

echo "📋 环境变量设置:"
echo "   OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}..."

# 启动后端服务
echo "🔧 启动后端服务..."
cd backend

# 检查是否已安装依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 启动后端服务
echo "🚀 启动FastAPI服务..."
python main.py &

# 等待后端服务启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 检查后端服务是否正常运行
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 后端服务启动成功!"
else
    echo "❌ 后端服务启动失败，请检查日志"
    exit 1
fi

echo ""
echo "🎉 Samantha AI 助手启动完成!"
echo ""
echo "📱 后端API地址: http://localhost:8000"
echo "📖 API文档: http://localhost:8000/docs"
echo ""
echo "📱 接下来请在Android Studio中打开 android-app 项目并运行应用"
echo ""
echo "💡 提示: 确保在Android模拟器中运行应用，以便连接到本地后端服务"
