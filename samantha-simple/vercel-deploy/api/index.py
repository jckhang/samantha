import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.genai as genai
import sqlite3
from datetime import datetime

# Gemini客户端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here"))

app = FastAPI(title="Samantha AI API", version="1.0.0")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 数据库路径（Vercel建议用内存或外部DB，演示用本地文件）
DB_PATH = "/tmp/samantha.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
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
        cursor.execute("""
            INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Default User')
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"数据库初始化失败: {e}")

init_db()

def analyze_emotion(text: str) -> str:
    try:
        prompt = f"分析以下文本的情感，只返回：happy, sad, angry, calm, neutral\n\n文本：{text}"
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        emotion = response.text.strip().lower()
        return emotion
    except Exception as e:
        print(f"情感分析失败: {e}")
        return "neutral"

def generate_response(message: str, emotion: str) -> str:
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
        return ai_response
    except Exception as e:
        print(f"AI回复生成失败: {e}")
        return f"抱歉，我现在无法回应。请稍后再试。"

def save_conversation(user_id: int, message: str, response: str, emotion: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (user_id, message, response, emotion)
            VALUES (?, ?, ?, ?)
        """, (user_id, message, response, emotion))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"保存对话失败: {e}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        emotion = analyze_emotion(request.message)
        response = generate_response(request.message, emotion)
        save_conversation(request.user_id, request.message, response, emotion)
        return ChatResponse(response=response, emotion=emotion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}", response_model=list[HistoryResponse])
async def get_history(user_id: int, limit: int = 50):
    try:
        conn = sqlite3.connect(DB_PATH)
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
            ) for row in results
        ]
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    return {"message": "Samantha AI API (Vercel)", "version": "1.0.0", "status": "running"}
