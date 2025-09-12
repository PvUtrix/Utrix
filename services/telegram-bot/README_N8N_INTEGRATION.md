# n8n Multilingual Integration

This integration connects your Personal System Telegram Bot to an existing n8n instance for advanced multilingual intent detection and response generation.

## 🚀 Features

- **Multilingual Support**: Handles Russian, English, and other languages
- **AI-Powered Intent Detection**: Uses GPT-4o for intelligent intent classification
- **Fallback Processing**: Local processing when n8n is unavailable
- **User Context**: Incorporates personal system data for better responses
- **Voice & Text**: Works with both voice messages and text input

## 📁 Files Created

- `integrations/n8n_multilingual_agent.py` - Main n8n integration service
- `config/n8n_config.yaml` - n8n configuration template
- `scripts/setup_n8n_integration.py` - Interactive setup script
- `scripts/test_n8n_integration.py` - Test script
- Updated `integrations/ai_assistant.py` - Now uses n8n integration
- Updated `config/config.yaml` - Added n8n configuration

## 🔧 Setup Instructions

### 1. Configure n8n Connection

Edit `config/config.yaml` and update the n8n section:

```yaml
n8n:
  base_url: "http://your-n8n-instance.com"  # Your n8n URL
  api_key: "your_api_key"  # Your n8n API key
  webhook_path: "multilingual-intent"
  timeout: 10
  fallback_enabled: true
  openai:
    api_key: "your_openai_key"  # For n8n workflow
    model: "gpt-4o"
```

### 2. Run Setup Script

```bash
cd services/telegram-bot
python scripts/setup_n8n_integration.py
```

This will:
- Test connection to your n8n instance
- Create the multilingual intent detection workflow
- Test the webhook endpoint

### 3. Configure OpenAI in n8n

1. Open your n8n instance
2. Go to the "Multilingual Intent Detection" workflow
3. Click on the "AI Intent Detection" node
4. Add your OpenAI API key
5. Save and activate the workflow

### 4. Test the Integration

```bash
python scripts/test_n8n_integration.py
```

## 🔄 How It Works

### Message Flow

```
Voice/Text Message
        ↓
Transcription (if voice)
        ↓
n8n Multilingual Agent
        ↓
┌─────────────────┬─────────────────┐
│   n8n Workflow  │  Fallback       │
│   (AI Intent)   │  (Local Logic)  │
└─────────────────┴─────────────────┘
        ↓
Intent Classification
        ↓
Response Generation
        ↓
User Response
```

### n8n Workflow

The workflow includes:
1. **Webhook Trigger** - Receives messages from the bot
2. **Data Extractor** - Processes input data
3. **AI Intent Detection** - Uses GPT-4o for intent classification
4. **Response Processor** - Structures the response
5. **Webhook Response** - Returns structured data

### Supported Intents

- `tasks` - Questions about tasks, projects, priorities
- `health` - Health tracking, fitness, wellness
- `learning` - Learning progress, courses, education
- `shadow_work` - Shadow work, archetypes, personal development
- `journal` - Journal entries, patterns, insights
- `goals` - Goals, progress, achievements
- `values` - Core values, life direction
- `help` - General help and capabilities

## 🌐 Multilingual Support

### Russian Examples
- "Какие у меня задачи на сегодня?" → `tasks` intent
- "Как дела с моим здоровьем?" → `health` intent
- "Что я изучал сегодня?" → `learning` intent

### English Examples
- "What tasks do I have for today?" → `tasks` intent
- "How is my health progress?" → `health` intent
- "What should I learn today?" → `learning` intent

## 🔧 Configuration Options

### n8n Settings

```yaml
n8n:
  base_url: "http://localhost:5678"  # Your n8n instance URL
  api_key: ""  # API key (recommended)
  username: ""  # Username (alternative to API key)
  password: ""  # Password (alternative to API key)
  webhook_path: "multilingual-intent"  # Webhook endpoint
  timeout: 10  # Request timeout in seconds
  fallback_enabled: true  # Enable local fallback
```

### OpenAI Settings (for n8n workflow)

```yaml
openai:
  api_key: ""  # Your OpenAI API key
  model: "gpt-4o"  # Model to use
  temperature: 0.3  # Response creativity
  max_tokens: 1000  # Maximum response length
```

## 🐛 Troubleshooting

### Connection Issues

1. **Check n8n URL**: Ensure the base_url is correct
2. **Verify Authentication**: Check API key or username/password
3. **Test Connection**: Run the setup script to test connectivity

### Workflow Issues

1. **Check OpenAI API Key**: Ensure it's configured in n8n
2. **Verify Webhook**: Check that the webhook is active
3. **Check Logs**: Look at n8n execution logs for errors

### Fallback Issues

1. **Enable Fallback**: Set `fallback_enabled: true`
2. **Check Local Processing**: Verify the original AI assistant works
3. **Review Logs**: Check bot logs for fallback activation

## 📊 Monitoring

### Logs

The integration logs important events:
- ✅ Successful n8n processing
- 🔄 Fallback activation
- ⚠️ Low confidence results
- ❌ Connection errors

### Metrics

Track these metrics:
- n8n success rate
- Fallback usage
- Intent detection accuracy
- Response time

## 🔄 Updates

To update the integration:

1. Update the n8n workflow in your n8n instance
2. Modify the workflow JSON in the setup script
3. Run the setup script to update the workflow
4. Test the integration

## 🆘 Support

If you encounter issues:

1. Check the logs in `logs/bot.log`
2. Run the test script to identify problems
3. Verify n8n workflow is active and configured
4. Test with simple messages first

## 🎯 Next Steps

1. **Configure your n8n instance** with the provided settings
2. **Run the setup script** to create the workflow
3. **Test with your Russian voice message** - it should now work!
4. **Customize the workflow** in n8n as needed
5. **Monitor performance** and adjust as necessary

The integration should now handle your Russian voice command "Какие у меня задачи на сегодня?" correctly!
