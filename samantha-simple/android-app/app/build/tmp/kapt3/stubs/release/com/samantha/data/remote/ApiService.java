package com.samantha.data.remote;

@kotlin.Metadata(mv = {1, 8, 0}, k = 1, xi = 48, d1 = {"\u00006\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\b\n\u0002\b\u0003\n\u0002\u0010$\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\bf\u0018\u00002\u00020\u0001J+\u0010\u0002\u001a\b\u0012\u0004\u0012\u00020\u00040\u00032\b\b\u0001\u0010\u0005\u001a\u00020\u00062\b\b\u0003\u0010\u0007\u001a\u00020\u0006H\u00a7@\u00f8\u0001\u0000\u00a2\u0006\u0002\u0010\bJ\u001d\u0010\t\u001a\u000e\u0012\u0004\u0012\u00020\u000b\u0012\u0004\u0012\u00020\u000b0\nH\u00a7@\u00f8\u0001\u0000\u00a2\u0006\u0002\u0010\fJ\u001b\u0010\r\u001a\u00020\u000e2\b\b\u0001\u0010\u000f\u001a\u00020\u0010H\u00a7@\u00f8\u0001\u0000\u00a2\u0006\u0002\u0010\u0011\u0082\u0002\u0004\n\u0002\b\u0019\u00a8\u0006\u0012"}, d2 = {"Lcom/samantha/data/remote/ApiService;", "", "getHistory", "", "Lcom/samantha/domain/model/HistoryResponse;", "userId", "", "limit", "(IILkotlin/coroutines/Continuation;)Ljava/lang/Object;", "healthCheck", "", "", "(Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "sendMessage", "Lcom/samantha/domain/model/ChatResponse;", "request", "Lcom/samantha/domain/model/ChatRequest;", "(Lcom/samantha/domain/model/ChatRequest;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_release"})
public abstract interface ApiService {
    
    @retrofit2.http.POST(value = "chat")
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object sendMessage(@retrofit2.http.Body
    @org.jetbrains.annotations.NotNull
    com.samantha.domain.model.ChatRequest request, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super com.samantha.domain.model.ChatResponse> $completion);
    
    @retrofit2.http.GET(value = "history/{user_id}")
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object getHistory(@retrofit2.http.Path(value = "user_id")
    int userId, @retrofit2.http.Query(value = "limit")
    int limit, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super java.util.List<com.samantha.domain.model.HistoryResponse>> $completion);
    
    @retrofit2.http.GET(value = "health")
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object healthCheck(@org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super java.util.Map<java.lang.String, java.lang.String>> $completion);
    
    @kotlin.Metadata(mv = {1, 8, 0}, k = 3, xi = 48)
    public static final class DefaultImpls {
    }
}