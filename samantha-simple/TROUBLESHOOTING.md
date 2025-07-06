# Samantha AI 故障排除指南

## Android 网络通信问题

### 问题描述
如果遇到以下错误：
```
CLEARTEXT communication to 10.0.2.2 not permitted by network security policy
```

这是因为 Android 9.0 (API 28) 及以上版本默认禁止明文 HTTP 通信。

### 解决方案

#### 方案1：网络安全配置（推荐）
1. 创建网络安全配置文件：`app/src/main/res/xml/network_security_config.xml`
2. 在 `AndroidManifest.xml` 中添加配置引用
3. 重新构建应用

#### 方案2：OkHttpClient 配置
在 `NetworkModule.kt` 中添加 `ConnectionSpec.CLEARTEXT` 支持

#### 方案3：临时禁用网络安全策略（仅开发环境）
在 `AndroidManifest.xml` 中添加：
```xml
android:usesCleartextTraffic="true"
```

### 验证步骤

1. **检查后端服务**
   ```bash
   cd backend
   python test_api.py
   ```

2. **重新构建Android应用**
   ```bash
   cd android-app
   ./gradlew clean assembleDebug
   ```

3. **安装应用到模拟器**
   ```bash
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```

### 常见问题

#### Q: 后端服务无法启动
A: 检查端口是否被占用，确保安装了所有依赖

#### Q: API调用返回错误
A: 检查Google Gemini API密钥配置，确保网络连接正常

#### Q: 模拟器无法访问localhost
A: 使用 `10.0.2.2` 而不是 `localhost` 或 `127.0.0.1`

### 开发环境设置

1. **启动后端服务**
   ```bash
   cd backend
   ./start_backend.sh
   ```

2. **配置环境变量**
   - 设置 `GEMINI_API_KEY`
   - 确保端口 8000 可用

3. **运行Android应用**
   - 使用Android Studio或命令行构建
   - 在模拟器中测试

### 生产环境注意事项

- 不要在生产环境中使用明文HTTP
- 配置HTTPS证书
- 使用适当的网络安全策略
- 移除调试配置
