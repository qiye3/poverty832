# AI 配置说明

本项目支持多种AI服务来生成SQL查询。你可以根据需要配置不同的AI服务。

## 配置方法

### 方法1：使用环境变量（推荐）

在项目根目录创建 `.env` 文件，添加以下配置：

```env
# AI服务类型：doubao（豆包）、openai（OpenAI）、custom（自定义）
AI_SERVICE_TYPE=doubao

# AI API密钥（必需）
AI_API_KEY=your_api_key_here

# AI API基础URL（可选，如果不设置则使用默认值）
AI_API_BASE=https://ark.cn-beijing.volces.com/api/v3

# AI模型名称/Endpoint（可选，如果不设置则使用默认值）
AI_MODEL=ep-20250118102936-tdz6m
```

### 方法2：直接在 settings.py 中配置

在 `poverty832/settings.py` 文件中直接修改：

```python
# AI 配置
AI_SERVICE_TYPE = "doubao"  # 或 "openai" 或 "custom"
AI_API_KEY = "your_api_key_here"
AI_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
AI_MODEL = "ep-20250118102936-tdz6m"
```

## 支持的AI服务

### 1. 豆包（Doubao / 火山方舟）

**配置示例：**
```env
AI_SERVICE_TYPE=doubao
AI_API_KEY=your_doubao_api_key
AI_API_BASE=https://ark.cn-beijing.volces.com/api/v3
AI_MODEL=ep-你的endpoint-id
```

**获取API密钥和Endpoint：**
1. 访问 [火山方舟控制台](https://console.volcengine.com/ark/)
2. 创建应用并获取API密钥（Access Key ID 和 Secret Access Key）
3. **重要**：创建模型endpoint并获取endpoint ID（格式如：`ep-20250118102936-tdz6m`）
4. 在 `.env` 文件中设置：
   ```env
   AI_SERVICE_TYPE=doubao
   AI_API_KEY=你的API密钥
   AI_MODEL=ep-你的endpoint-id  # ⚠️ 必须替换为你的实际endpoint ID
   ```

**⚠️ 重要提示：**
- 代码中的 `ep-20250118102936-tdz6m` 只是示例，**必须替换为你自己的endpoint ID**
- 如果遇到404错误，说明endpoint不存在或配置错误
- 确保endpoint在控制台中已创建并处于可用状态

### 2. OpenAI

**配置示例：**
```env
AI_SERVICE_TYPE=openai
AI_API_KEY=sk-your_openai_api_key
AI_API_BASE=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo
```

**获取API密钥：**
1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册账号并获取API密钥
3. 选择模型（gpt-3.5-turbo 或 gpt-4）

### 3. 自定义AI服务（OpenAI兼容API）

如果你使用其他支持OpenAI兼容API的服务（如：
- 通义千问
- 文心一言
- Claude
- 本地部署的模型等）

**配置示例：**
```env
AI_SERVICE_TYPE=custom
AI_API_KEY=your_api_key
AI_API_BASE=https://your-api-endpoint.com/v1
AI_MODEL=your-model-name
```

## 常见问题

### Q: 如何测试AI配置是否正确？

A: 启动Django服务器后，访问智能查询页面，输入一个问题测试。如果配置正确，AI会生成SQL；如果配置错误，会显示错误信息。

### Q: 支持哪些AI模型？

A: 理论上支持所有提供OpenAI兼容API的模型服务。只要API格式兼容OpenAI的ChatCompletion接口即可。

### Q: 如何切换不同的AI服务？

A: 只需修改 `AI_SERVICE_TYPE` 环境变量或设置，然后重启Django服务器即可。

### Q: API密钥安全吗？

A: 建议使用环境变量（.env文件）存储API密钥，不要将密钥提交到Git仓库。`.env` 文件应该添加到 `.gitignore` 中。

## 注意事项

1. **API密钥安全**：不要将API密钥提交到版本控制系统
2. **API费用**：使用AI服务可能会产生费用，请注意API调用次数和费用
3. **网络连接**：确保服务器能够访问AI服务的API地址
4. **模型选择**：不同模型的性能和价格不同，请根据需求选择

