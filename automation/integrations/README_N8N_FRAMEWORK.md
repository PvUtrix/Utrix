# n8n Integration Framework

A comprehensive, reusable framework for integrating with n8n workflows across the Personal System. This framework provides tools for creating, managing, and deploying n8n workflows programmatically.

## 🚀 Features

- **Workflow Builder**: Programmatic workflow creation with type-safe node definitions
- **Template System**: Reusable workflow templates for common use cases
- **Configuration Management**: Centralized configuration management across services
- **CLI Tools**: Command-line interface for workflow management
- **Multi-Service Support**: Support for multiple n8n instances and services
- **Webhook Management**: Easy webhook URL generation and testing
- **Error Handling**: Comprehensive error handling and logging

## 📁 Framework Structure

```
automation/integrations/
├── n8n_framework.py          # Core framework classes
├── n8n_config_manager.py     # Configuration management
├── n8n_cli.py               # Command-line interface
├── n8n_templates/           # Workflow templates
│   ├── multilingual_intent.json
│   ├── data_processor.json
│   └── api_integration.json
└── configs/                 # Configuration files
    ├── n8n_default.yaml
    └── n8n_configs.yaml
```

## 🛠️ Core Components

### 1. N8nWorkflowBuilder

Programmatically create n8n workflows:

```python
from automation.integrations.n8n_framework import N8nWorkflowBuilder, N8nNodeType

# Create a new workflow
builder = N8nWorkflowBuilder("My Workflow")

# Add nodes
webhook_id = builder.add_webhook_trigger("my-webhook")
processor_id = builder.add_code_node("Data Processor", "return $input.first().json;", [460, 300])
response_id = builder.add_webhook_response()

# Connect nodes
builder.connect_nodes(webhook_id, processor_id)
builder.connect_nodes(processor_id, response_id)

# Build the workflow
workflow_data = builder.build()
```

### 2. N8nClient

Interact with n8n API:

```python
from automation.integrations.n8n_framework import N8nClient

client = N8nClient(
    base_url="http://localhost:5678",
    api_key="your_api_key"
)

# Test connection
await client.test_connection()

# Create workflow
workflow_id = await client.create_workflow(workflow_data)

# Call webhook
result = await client.call_webhook("my-webhook", {"data": "test"})
```

### 3. N8nWorkflowManager

Manage workflows and templates:

```python
from automation.integrations.n8n_framework import N8nWorkflowManager

manager = N8nWorkflowManager(client)

# Create multilingual intent workflow
workflow_data = manager.create_multilingual_intent_workflow()

# Save as template
manager.save_workflow_template("multilingual-intent", workflow_data)

# Deploy template
workflow_id = await manager.deploy_template("multilingual-intent")
```

### 4. N8nIntegrationManager

Centralized integration management:

```python
from automation.integrations.n8n_config_manager import N8nIntegrationManager

manager = N8nIntegrationManager()

# Setup integration
config = manager.setup_integration(
    "telegram-bot", 
    "http://localhost:5678",
    api_key="your_api_key"
)

# Register workflow
manager.register_workflow("multilingual-intent", "workflow_id", "multilingual-intent")

# Get webhook URL
url = manager.get_workflow_url("telegram-bot", "multilingual-intent")
```

## 🎯 Use Cases

### 1. Multilingual Intent Detection

Perfect for chatbots and voice assistants:

```python
# Create multilingual intent workflow
workflow = manager.create_multilingual_intent_workflow()

# Deploy to n8n
workflow_id = await client.create_workflow(workflow)

# Use in your bot
result = await client.call_webhook("multilingual-intent", {
    "text": "Какие у меня задачи на сегодня?",
    "user_id": 12345,
    "context": {"language": "ru"}
})
```

### 2. Data Processing

Process data through n8n workflows:

```python
# Create data processor workflow
workflow = manager.create_data_processor_workflow(
    "Health Data Processor",
    "// Process health data\nreturn $input.first().json;"
)

# Deploy and use
workflow_id = await client.create_workflow(workflow)
```

### 3. API Integration

Integrate with external APIs:

```python
# Create API integration workflow
workflow = manager.create_api_integration_workflow(
    "Weather API",
    "https://api.weather.com/current",
    {"Authorization": "Bearer your_token"}
)

# Deploy and use
workflow_id = await client.create_workflow(workflow)
```

## 🖥️ CLI Usage

The framework includes a powerful CLI for managing n8n integrations:

### Setup Integration

```bash
python automation/integrations/n8n_cli.py setup telegram-bot http://localhost:5678 --api-key your_key
```

### Deploy Workflow

```bash
python automation/integrations/n8n_cli.py deploy --service telegram-bot multilingual_intent
```

### Test Connection

```bash
python automation/integrations/n8n_cli.py test --service telegram-bot
```

### List Workflows

```bash
python automation/integrations/n8n_cli.py list --service telegram-bot
```

### Test Webhook

```bash
python automation/integrations/n8n_cli.py test-webhook --service telegram-bot multilingual_intent --data test_data.json
```

## 📋 Available Templates

### 1. Multilingual Intent Detection

- **Purpose**: Detect user intent in multiple languages
- **Input**: Text, user context, language hint
- **Output**: Intent, confidence, response, language
- **Use Case**: Chatbots, voice assistants

### 2. Data Processor

- **Purpose**: Process data through custom logic
- **Input**: Any JSON data
- **Output**: Processed data
- **Use Case**: Data transformation, validation

### 3. API Integration

- **Purpose**: Integrate with external APIs
- **Input**: Data to send to API
- **Output**: API response
- **Use Case**: External service integration

## 🔧 Configuration

### Service Configuration

```yaml
# automation/integrations/configs/n8n_default.yaml
base_url: "http://localhost:5678"
api_key: "your_api_key"
timeout: 30
webhook_base_path: "webhook"
openai_api_key: "your_openai_key"
openai_model: "gpt-4o"
openai_temperature: 0.3
openai_max_tokens: 1000
```

### Service-Specific Configuration

```yaml
# automation/integrations/configs/n8n_configs.yaml
telegram-bot:
  base_url: "http://localhost:5678"
  api_key: "telegram_bot_api_key"
  timeout: 30

health-dashboard:
  base_url: "http://n8n.health.com"
  username: "health_user"
  password: "health_pass"
  timeout: 60
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install httpx pyyaml
```

### 2. Setup Integration

```python
from automation.integrations.n8n_framework import N8nIntegration

# Create integration
integration = N8nIntegration({
    "base_url": "http://localhost:5678",
    "api_key": "your_api_key"
})

# Test connection
await integration.test_connection()

# Setup multilingual intent
await integration.setup_multilingual_intent()
```

### 3. Use in Your Service

```python
# Call webhook
result = await integration.call_webhook("multilingual-intent", {
    "text": "What tasks do I have today?",
    "user_id": 12345,
    "context": {"language": "en"}
})

print(f"Intent: {result['intent']}")
print(f"Response: {result['response']}")
```

## 🔄 Workflow Lifecycle

1. **Create**: Use N8nWorkflowBuilder to create workflow
2. **Template**: Save as template for reuse
3. **Deploy**: Deploy to n8n instance
4. **Register**: Register in workflow registry
5. **Use**: Call webhook endpoints
6. **Monitor**: Track usage and performance
7. **Update**: Modify and redeploy as needed

## 🐛 Troubleshooting

### Connection Issues

```bash
# Test connection
python automation/integrations/n8n_cli.py test --service telegram-bot

# Check configuration
python automation/integrations/n8n_cli.py configs
```

### Workflow Issues

```bash
# List workflows
python automation/integrations/n8n_cli.py list --service telegram-bot

# Test webhook
python automation/integrations/n8n_cli.py test-webhook --service telegram-bot multilingual_intent
```

### Template Issues

```bash
# Create new template
python automation/integrations/n8n_cli.py create-template my_template multilingual

# Deploy template
python automation/integrations/n8n_cli.py deploy --service telegram-bot my_template
```

## 📊 Monitoring

### Logs

The framework logs important events:
- Connection status
- Workflow deployments
- Webhook calls
- Errors and warnings

### Metrics

Track these metrics:
- Webhook response times
- Success/failure rates
- Workflow execution counts
- Error rates

## 🔮 Future Enhancements

- **Workflow Versioning**: Version control for workflows
- **A/B Testing**: Test different workflow versions
- **Performance Monitoring**: Built-in performance tracking
- **Auto-scaling**: Automatic workflow scaling
- **Workflow Marketplace**: Share and discover workflows

## 🤝 Contributing

1. Add new workflow templates in `n8n_templates/`
2. Extend `N8nWorkflowBuilder` for new node types
3. Add new CLI commands in `n8n_cli.py`
4. Update documentation

## 📚 Examples

See the `examples/` directory for complete examples:
- Multilingual chatbot integration
- Health data processing pipeline
- API integration patterns
- Custom workflow templates

This framework provides everything you need to integrate n8n workflows into any part of your personal system!
