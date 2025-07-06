#!/bin/bash

# Samantha AI 后端启动脚本

echo "启动 Samantha AI 后端服务..."

# 设置环境变量
export GEMINI_API_KEY="your-gemini-api-key-here"
export ENVIRONMENT="development"
export LOG_LEVEL="INFO"
export BACKEND_PORT="8000"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
fi

# 安装依赖
echo "检查依赖..."
pip install -r requirements.txt

# 启动服务
echo "启动 FastAPI 服务..."
echo "服务地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "按 Ctrl+C 停止服务"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
