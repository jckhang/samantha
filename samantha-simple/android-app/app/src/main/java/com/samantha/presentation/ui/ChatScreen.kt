package com.samantha.presentation.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.samantha.domain.model.Message
import com.samantha.presentation.viewmodel.ChatUiState
import com.samantha.presentation.viewmodel.ChatViewModel

@OptIn(ExperimentalMaterial3Api::class)
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
                IconButton(onClick = { viewModel.clearMessages() }) {
                    Icon(
                        imageVector = Icons.Default.Clear,
                        contentDescription = "清空对话"
                    )
                }
            }
        )

        // 错误提示
        uiState.error?.let { error ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.errorContainer
                )
            ) {
                Text(
                    text = error,
                    modifier = Modifier.padding(16.dp),
                    color = MaterialTheme.colorScheme.onErrorContainer
                )
            }
        }

        // 对话列表
        LazyColumn(
            modifier = Modifier.weight(1f),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(uiState.messages) { message ->
                MessageItem(message = message)
            }

            // 加载指示器
            if (uiState.isLoading) {
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Start
                    ) {
                        Card(
                            colors = CardDefaults.cardColors(
                                containerColor = MaterialTheme.colorScheme.surfaceVariant
                            )
                        ) {
                            Row(
                                modifier = Modifier.padding(12.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(16.dp),
                                    strokeWidth = 2.dp
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("Samantha正在思考...")
                            }
                        }
                    }
                }
            }
        }

        // 输入区域
        InputArea(
            onSendMessage = { viewModel.sendMessage(it) },
            isVoiceMode = uiState.isVoiceMode,
            isLoading = uiState.isLoading
        )
    }
}

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
            Column(
                modifier = Modifier.padding(12.dp)
            ) {
                Text(
                    text = message.content,
                    color = if (isUser)
                        MaterialTheme.colorScheme.onPrimary
                    else
                        MaterialTheme.colorScheme.onSurfaceVariant
                )

                // 显示情感标签
                message.emotion?.let { emotion ->
                    if (!isUser) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "情感: $emotion",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                        )
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InputArea(
    onSendMessage: (String) -> Unit,
    isVoiceMode: Boolean,
    isLoading: Boolean
) {
    var text by remember { mutableStateOf("") }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 语音按钮
            IconButton(
                onClick = { /* TODO: 实现语音输入 */ },
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
                placeholder = {
                    Text(
                        if (isVoiceMode) "点击麦克风开始语音输入..."
                        else "输入消息..."
                    )
                },
                enabled = !isLoading && !isVoiceMode,
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = MaterialTheme.colorScheme.primary,
                    unfocusedBorderColor = MaterialTheme.colorScheme.outline
                )
            )

            // 发送按钮
            IconButton(
                onClick = {
                    if (text.isNotBlank()) {
                        onSendMessage(text)
                        text = ""
                    }
                },
                enabled = text.isNotBlank() && !isLoading && !isVoiceMode
            ) {
                Icon(
                    imageVector = Icons.Default.Send,
                    contentDescription = "发送"
                )
            }
        }
    }
}
