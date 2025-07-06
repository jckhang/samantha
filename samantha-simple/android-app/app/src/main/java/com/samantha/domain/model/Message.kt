package com.samantha.domain.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "messages")
data class Message(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val content: String,
    val isFromUser: Boolean,
    val emotion: String? = null,
    val timestamp: Long = System.currentTimeMillis()
)
