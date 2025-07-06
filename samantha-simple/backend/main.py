from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.genai as genai
import sqlite3
from datetime import datetime
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Samantha AI API", version="1.0.0")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini客户端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here"))

# 数据模型
class ChatRequest(BaseModel):
    message: str
    user_id: int = 1

class ChatResponse(BaseModel):
    response: str
    emotion: str

class HistoryResponse(BaseModel):
    message: str
    response: str
    emotion: str
    created_at: str

# 数据库初始化
def init_db():
    """初始化SQLite数据库"""
    try:
        conn = sqlite3.connect("samantha.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT,
                response TEXT,
                emotion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建默认用户
        cursor.execute("""
            INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Default User')
        """)

        conn.commit()
        conn.close()
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")

# 情感分析
def analyze_emotion(text: str) -> str:
    """分析文本情感"""
    try:
        prompt = f"分析以下文本的情感，只返回：happy, sad, angry, calm, neutral\n\n文本：{text}"

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        emotion = response.text.strip().lower()
        logger.info(f"情感分析结果: {emotion}")
        return emotion
    except Exception as e:
        logger.error(f"情感分析失败: {e}")
        return "neutral"

# 生成回复
def generate_response(message: str, emotion: str) -> str:
    """生成AI回复"""
    try:
        prompt = f"""
你是Samantha，一个智能、温暖的AI助手。
用户当前情感状态：{emotion}

请根据用户的情感状态提供合适的回应：
- 如果用户情绪低落，提供温暖和支持
- 如果用户情绪积极，分享快乐
- 如果用户情绪愤怒，保持冷静和理解
- 始终保持友好、有帮助的态度

回复要简洁、自然，不超过100字。

用户消息：{message}
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        ai_response = response.text.strip()
        logger.info(f"AI回复生成成功: {ai_response[:50]}...")
        return ai_response
    except Exception as e:
        logger.error(f"AI回复生成失败: {e}")
        return f"抱歉，我现在无法回应。请稍后再试。"

# 保存对话
def save_conversation(user_id: int, message: str, response: str, emotion: str):
    """保存对话到数据库"""
    try:
        conn = sqlite3.connect("samantha.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations (user_id, message, response, emotion)
            VALUES (?, ?, ?, ?)
        """, (user_id, message, response, emotion))

        conn.commit()
        conn.close()
        logger.info(f"对话已保存到数据库")
    except Exception as e:
        logger.error(f"保存对话失败: {e}")

# API端点
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        logger.info(f"收到聊天请求: {request.message[:50]}...")

        # 情感分析
        emotion = analyze_emotion(request.message)

        # 生成回复
        response = generate_response(request.message, emotion)

        # 保存对话
        save_conversation(request.user_id, request.message, response, emotion)

        return ChatResponse(response=response, emotion=emotion)
    except Exception as e:
        logger.error(f"处理聊天请求失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}", response_model=list[HistoryResponse])
async def get_history(user_id: int, limit: int = 50):
    """获取对话历史"""
    try:
        conn = sqlite3.connect("samantha.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT message, response, emotion, created_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))

        results = cursor.fetchall()
        conn.close()

        history = [
            HistoryResponse(
                message=row[0],
                response=row[1],
                emotion=row[2],
                created_at=row[3]
            )
            for row in results
        ]

        logger.info(f"获取用户 {user_id} 的历史记录: {len(history)} 条")
        return history
    except Exception as e:
        logger.error(f"获取历史记录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Samantha AI API",
        "version": "1.0.0",
        "status": "running"
    }

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("Samantha AI API 启动中...")
    init_db()
    logger.info("Samantha AI API 启动完成")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
