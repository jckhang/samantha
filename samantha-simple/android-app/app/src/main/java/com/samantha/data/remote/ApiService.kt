package com.samantha.data.remote

import com.samantha.domain.model.ChatRequest
import com.samantha.domain.model.ChatResponse
import com.samantha.domain.model.HistoryResponse
import retrofit2.http.*

interface ApiService {

    @POST("chat")
    suspend fun sendMessage(@Body request: ChatRequest): ChatResponse

    @GET("history/{user_id}")
    suspend fun getHistory(
        @Path("user_id") userId: Int,
        @Query("limit") limit: Int = 50
    ): List<HistoryResponse>

    @GET("health")
    suspend fun healthCheck(): Map<String, String>
}
