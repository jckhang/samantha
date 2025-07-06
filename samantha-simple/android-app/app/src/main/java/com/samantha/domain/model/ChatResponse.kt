package com.samantha.domain.model

data class ChatResponse(
    val response: String,
    val emotion: String
)

data class ChatRequest(
    val message: String,
    val user_id: Int = 1
)

data class HistoryResponse(
    val message: String,
    val response: String,
    val emotion: String,
    val created_at: String
)
