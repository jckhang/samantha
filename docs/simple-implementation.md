# Samantha AI助手 - 最简化实现方案

## 项目结构 (简化版)

```
samantha-simple/
├── android-app/          # Android应用
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/samantha/
│   │   │   │   ├── data/
│   │   │   │   │   ├── local/      # Room数据库
│   │   │   │   │   ├── remote/     # API调用
│   │   │   │   │   └── repository/ # 数据仓库
│   │   │   │   ├── domain/
│   │   │   │   │   ├── model/      # 数据模型
│   │   │   │   │   └── usecase/    # 用例
│   │   │   │   ├── presentation/
│   │   │   │   │   ├── ui/         # UI组件
│   │   │   │   │   └── viewmodel/  # ViewModel
│   │   │   │   └── di/             # 依赖注入
│   │   │   └── res/
│   │   └── build.gradle
│   └── gradle/
├── backend/              # 简化后端
│   ├── main.py          # FastAPI主文件
│   ├── database.py      # SQLite数据库
│   ├── models.py        # 数据模型
│   ├── services.py      # 业务逻辑
│   └── requirements.txt
└── README.md
```

## Android端实现

### 1. 主界面 (MainActivity)

```kotlin
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SamanthaTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    ChatScreen()
                }
            }
        }
    }
}
```

### 2. 聊天界面 (ChatScreen)

```kotlin
@Composable
fun ChatScreen(
    viewModel: ChatViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize()
    ) {
        // 标题栏
        TopAppBar(
            title = { Text("Samantha AI") },
            actions = {
                IconButton(onClick = { viewModel.toggleVoiceMode() }) {
                    Icon(
                        imageVector = if (uiState.isVoiceMode) Icons.Default.Mic else Icons.Default.Chat,
                        contentDescription = "语音模式"
                    )
                }
            }
        )

        // 对话列表
        LazyColumn(
            modifier = Modifier.weight(1f),
            contentPadding = PaddingValues(16.dp)
        ) {
            items(uiState.messages) { message ->
                MessageItem(message = message)
                Spacer(modifier = Modifier.height(8.dp))
            }
        }

        // 输入区域
        InputArea(
            onSendMessage = { viewModel.sendMessage(it) },
            onVoiceInput = { viewModel.startVoiceRecognition() },
            isVoiceMode = uiState.isVoiceMode,
            isLoading = uiState.isLoading
        )
    }
}
```

### 3. 消息组件 (MessageItem)

```kotlin
@Composable
fun MessageItem(message: Message) {
    val isUser = message.isFromUser

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Card(
            modifier = Modifier.widthIn(max = 280.dp),
            colors = CardDefaults.cardColors(
                containerColor = if (isUser)
                    MaterialTheme.colorScheme.primary
                else
                    MaterialTheme.colorScheme.surfaceVariant
            )
        ) {
            Text(
                text = message.content,
                modifier = Modifier.padding(12.dp),
                color = if (isUser)
                    MaterialTheme.colorScheme.onPrimary
                else
                    MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
```

### 4. 输入区域 (InputArea)

```kotlin
@Composable
fun InputArea(
    onSendMessage: (String) -> Unit,
    onVoiceInput: () -> Unit,
    isVoiceMode: Boolean,
    isLoading: Boolean
) {
    var text by remember { mutableStateOf("") }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // 语音按钮
        IconButton(
            onClick = onVoiceInput,
            enabled = !isLoading
        ) {
            Icon(
                imageVector = Icons.Default.Mic,
                contentDescription = "语音输入"
            )
        }

        // 输入框
        OutlinedTextField(
            value = text,
            onValueChange = { text = it },
            modifier = Modifier.weight(1f),
            placeholder = { Text("输入消息...") },
            enabled = !isLoading && !isVoiceMode,
            singleLine = true
        )

        // 发送按钮
        IconButton(
            onClick = {
                if (text.isNotBlank()) {
                    onSendMessage(text)
                    text = ""
                }
            },
            enabled = text.isNotBlank() && !isLoading
        ) {
            Icon(
                imageVector = Icons.Default.Send,
                contentDescription = "发送"
            )
        }
    }
}
```

### 5. ViewModel

```kotlin
@HiltViewModel
class ChatViewModel @Inject constructor(
    private val chatRepository: ChatRepository,
    private val voiceRepository: VoiceRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(ChatUiState())
    val uiState: StateFlow<ChatUiState> = _uiState.asStateFlow()

    fun sendMessage(message: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)

            try {
                val response = chatRepository.sendMessage(message)
                _uiState.value = _uiState.value.copy(
                    messages = _uiState.value.messages + response,
                    isLoading = false
                )
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    error = e.message,
                    isLoading = false
                )
            }
        }
    }

    fun startVoiceRecognition() {
        viewModelScope.launch {
            voiceRepository.startRecognition { text ->
                sendMessage(text)
            }
        }
    }

    fun toggleVoiceMode() {
        _uiState.value = _uiState.value.copy(
            isVoiceMode = !_uiState.value.isVoiceMode
        )
    }
}
```

### 6. 数据模型

```kotlin
@Entity(tableName = "messages")
data class Message(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val content: String,
    val isFromUser: Boolean,
    val emotion: String? = null,
    val timestamp: Long = System.currentTimeMillis()
)

data class ChatUiState(
    val messages: List<Message> = emptyList(),
    val isLoading: Boolean = false,
    val isVoiceMode: Boolean = false,
    val error: String? = null
)
```

## 后端实现

### 1. 主应用 (main.py)

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import sqlite3
from datetime import datetime
import os

app = FastAPI(title="Samantha AI API")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI配置
openai.api_key = os.getenv("OPENAI_API_KEY")

# 数据模型
class ChatRequest(BaseModel):
    message: str
    user_id: int = 1

class ChatResponse(BaseModel):
    response: str
    emotion: str

# 数据库初始化
def init_db():
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

    conn.commit()
    conn.close()

# 情感分析
def analyze_emotion(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "分析以下文本的情感，只返回：happy, sad, angry, calm, neutral"},
                {"role": "user", "content": text}
            ],
            max_tokens=10
        )
        return response.choices[0].message.content.strip().lower()
    except:
        return "neutral"

# 生成回复
def generate_response(message: str, emotion: str) -> str:
    try:
        system_prompt = f"""
        你是Samantha，一个智能、温暖的AI助手。
        用户当前情感状态：{emotion}
        请根据用户的情感状态提供合适的回应，保持温暖和理解的态度。
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"抱歉，我现在无法回应。错误：{str(e)}"

# 保存对话
def save_conversation(user_id: int, message: str, response: str, emotion: str):
    conn = sqlite3.connect("samantha.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (user_id, message, response, emotion)
        VALUES (?, ?, ?, ?)
    """, (user_id, message, response, emotion))

    conn.commit()
    conn.close()

# API端点
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 情感分析
        emotion = analyze_emotion(request.message)

        # 生成回复
        response = generate_response(request.message, emotion)

        # 保存对话
        save_conversation(request.user_id, request.message, response, emotion)

        return ChatResponse(response=response, emotion=emotion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}")
async def get_history(user_id: int):
    conn = sqlite3.connect("samantha.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response, emotion, created_at
        FROM conversations
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 50
    """, (user_id,))

    results = cursor.fetchall()
    conn.close()

    return [
        {
            "message": row[0],
            "response": row[1],
            "emotion": row[2],
            "created_at": row[3]
        }
        for row in results
    ]

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. 依赖文件 (requirements.txt)

```txt
fastapi==0.104.1
uvicorn==0.24.0
openai==1.3.0
pydantic==2.5.0
python-multipart==0.0.6
```

## 部署配置

### 1. Docker配置 (docker-compose.yml)

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
      - sqlite_data:/app/data

volumes:
  sqlite_data:
```

### 2. 后端Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 启动指南

### 1. 后端启动
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. Android应用
```bash
cd android-app
./gradlew assembleDebug
```

### 3. Docker启动
```bash
docker-compose up -d
```

## 功能测试

### 1. 基础对话测试
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "你好", "user_id": 1}'
```

### 2. 历史记录测试
```bash
curl "http://localhost:8000/history/1"
```

## 总结

最简化版本的Samantha AI助手包含：

### 核心功能
1. **智能对话** - 基于GPT-3.5的问答
2. **语音交互** - 语音识别和合成
3. **情感回应** - 简单的情感分析

### 技术特点
- **轻量级架构** - SQLite + 简单API
- **快速开发** - 6周完成
- **易于维护** - 代码结构简单
- **成本低廉** - 最小化资源需求

### 开发优势
- 功能专注，体验简洁
- 开发周期短，风险可控
- 易于扩展和迭代
- 用户上手简单

这个简化版本保留了Samantha的核心特色，同时大大降低了开发复杂度和成本，是一个理想的MVP方案。

---

**专注核心，简单有效！** 🎯
