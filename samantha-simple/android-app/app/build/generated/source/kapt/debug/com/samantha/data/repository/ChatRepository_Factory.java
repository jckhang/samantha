package com.samantha.data.repository;

import com.samantha.data.local.MessageDao;
import com.samantha.data.remote.ApiService;
import dagger.internal.DaggerGenerated;
import dagger.internal.Factory;
import dagger.internal.QualifierMetadata;
import dagger.internal.ScopeMetadata;
import javax.annotation.processing.Generated;
import javax.inject.Provider;

@ScopeMetadata("javax.inject.Singleton")
@QualifierMetadata
@DaggerGenerated
@Generated(
    value = "dagger.internal.codegen.ComponentProcessor",
    comments = "https://dagger.dev"
)
@SuppressWarnings({
    "unchecked",
    "rawtypes",
    "KotlinInternal",
    "KotlinInternalInJava"
})
public final class ChatRepository_Factory implements Factory<ChatRepository> {
  private final Provider<ApiService> apiServiceProvider;

  private final Provider<MessageDao> messageDaoProvider;

  public ChatRepository_Factory(Provider<ApiService> apiServiceProvider,
      Provider<MessageDao> messageDaoProvider) {
    this.apiServiceProvider = apiServiceProvider;
    this.messageDaoProvider = messageDaoProvider;
  }

  @Override
  public ChatRepository get() {
    return newInstance(apiServiceProvider.get(), messageDaoProvider.get());
  }

  public static ChatRepository_Factory create(Provider<ApiService> apiServiceProvider,
      Provider<MessageDao> messageDaoProvider) {
    return new ChatRepository_Factory(apiServiceProvider, messageDaoProvider);
  }

  public static ChatRepository newInstance(ApiService apiService, MessageDao messageDao) {
    return new ChatRepository(apiService, messageDao);
  }
}
