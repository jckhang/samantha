package com.samantha.data.repository

import com.samantha.data.local.MessageDao
import com.samantha.data.remote.ApiService
import com.samantha.domain.model.ChatRequest
import com.samantha.domain.model.Message
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ChatRepository @Inject constructor(
    private val apiService: ApiService,
    private val messageDao: MessageDao
) {

    fun getAllMessages(): Flow<List<Message>> {
        return messageDao.getAllMessages()
    }

    suspend fun sendMessage(message: String): Message {
        // 保存用户消息到本地
        val userMessage = Message(
            content = message,
            isFromUser = true
        )
        messageDao.insertMessage(userMessage)

        try {
            // 发送到API
            val response = apiService.sendMessage(ChatRequest(message = message))

            // 保存AI回复到本地
            val aiMessage = Message(
                content = response.response,
                isFromUser = false,
                emotion = response.emotion
            )
            messageDao.insertMessage(aiMessage)

            return aiMessage
        } catch (e: Exception) {
            // 如果API调用失败，返回错误消息
            val errorMessage = Message(
                content = "抱歉，我现在无法回应。请检查网络连接。",
                isFromUser = false,
                emotion = "neutral"
            )
            messageDao.insertMessage(errorMessage)
            return errorMessage
        }
    }

    suspend fun getRecentMessages(limit: Int = 50): List<Message> {
        return messageDao.getRecentMessages(limit)
    }

    suspend fun clearMessages() {
        messageDao.deleteAllMessages()
    }
}
