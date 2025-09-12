# n8n Integration Setup Tasks

## 🎯 Overview
This document provides step-by-step tasks to set up the n8n integration framework for your personal system.

## 📋 Setup Tasks

### Task 1: Configure n8n Instance Connection Details
**Status**: ⏳ Pending  
**Priority**: High  
**Estimated Time**: 5 minutes

**Description**: Update configuration files with your n8n instance details.

**Steps**:
1. Open `services/telegram-bot/config/config.yaml`
2. Update the n8n section with your actual n8n instance details:
   ```yaml
   n8n:
     base_url: "http://your-n8n-instance.com"  # Your actual n8n URL
     api_key: "your_actual_api_key"  # Your n8n API key
     webhook_path: "multilingual-intent"
     timeout: 10
     fallback_enabled: true
     openai:
       api_key: "your_openai_api_key"  # For n8n workflow
       model: "gpt-4o"
       temperature: 0.3
       max_tokens: 1000
   ```

**Verification**: Configuration file contains your actual n8n instance URL and API key.

---

### Task 2: Install Required Dependencies
**Status**: ⏳ Pending  
**Priority**: High  
**Estimated Time**: 2 minutes

**Description**: Install Python packages required for the n8n framework.

**Steps**:
1. Navigate to the project root:
   ```bash
   cd /Users/PvUtrix_1/Apps/_cursor/personal-system
   ```

2. Install required packages:
   ```bash
   pip install httpx pyyaml
   ```

3. Verify installation:
   ```bash
   python -c "import httpx, yaml; print('Dependencies installed successfully')"
   ```

**Verification**: No import errors when running the verification command.

---

### Task 3: Test Connection to n8n Instance
**Status**: ⏳ Pending  
**Priority**: High  
**Estimated Time**: 3 minutes

**Description**: Verify that the framework can connect to your n8n instance.

**Steps**:
1. Navigate to the telegram bot directory:
   ```bash
   cd services/telegram-bot
   ```

2. Run the connection test:
   ```bash
   python automation/integrations/n8n_cli.py test --service telegram-bot
   ```

3. Alternative: Run the test script directly:
   ```bash
   python scripts/test_n8n_integration.py
   ```

**Expected Output**: "✅ Connection successful!"

**Verification**: Connection test passes without errors.

---

### Task 4: Deploy Multilingual Intent Detection Workflow
**Status**: ⏳ Pending  
**Priority**: High  
**Estimated Time**: 5 minutes

**Description**: Deploy the multilingual intent detection workflow to your n8n instance.

**Steps**:
1. Deploy the workflow using CLI:
   ```bash
   python automation/integrations/n8n_cli.py deploy --service telegram-bot multilingual_intent
   ```

2. Alternative: Use the setup script:
   ```bash
   python scripts/setup_n8n_integration.py
   ```

3. Verify deployment in n8n UI:
   - Open your n8n instance in browser
   - Check that "Multilingual Intent Detection" workflow is created
   - Ensure it's active (green status)

**Verification**: Workflow appears in n8n UI and is active.

---

### Task 5: Configure OpenAI API Key in n8n Workflow
**Status**: ⏳ Pending  
**Priority**: High  
**Estimated Time**: 3 minutes

**Description**: Add your OpenAI API key to the n8n workflow for AI processing.

**Steps**:
1. Open your n8n instance in browser
2. Navigate to the "Multilingual Intent Detection" workflow
3. Click on the "AI Intent Detection" node
4. In the OpenAI configuration:
   - Add your OpenAI API key
   - Verify model is set to "gpt-4o"
   - Save the node configuration
5. Save and activate the workflow

**Verification**: Workflow executes without OpenAI API errors.

---

### Task 6: Test Multilingual Processing
**Status**: ⏳ Pending  
**Priority**: High  
**Estimated Time**: 5 minutes

**Description**: Test the multilingual processing with your Russian voice message.

**Steps**:
1. Create a test script:
   ```bash
   cat > test_russian.py << 'EOF'
   import asyncio
   import sys
   from pathlib import Path
   sys.path.append(str(Path(__file__).parent))
   
   from integrations.n8n_multilingual_agent_v2 import N8nMultilingualAgent
   import yaml
   
   async def test():
       with open('config/config.yaml', 'r') as f:
           config = yaml.safe_load(f)
       
       agent = N8nMultilingualAgent(config)
       
       # Test Russian message
       result = await agent.process_message(
           "Какие у меня задачи на сегодня?",
           12345,
           "voice"
       )
       
       print(f"Intent: {result['intent']}")
       print(f"Confidence: {result['confidence']}")
       print(f"Response: {result['response_text']}")
   
   asyncio.run(test())
   EOF
   ```

2. Run the test:
   ```bash
   python test_russian.py
   ```

**Expected Output**: Intent should be "tasks" with high confidence.

**Verification**: Russian message is processed correctly and returns task recommendations.

---

### Task 7: Update Telegram Bot to Use New Integration
**Status**: ⏳ Pending  
**Priority**: Medium  
**Estimated Time**: 3 minutes

**Description**: Update the Telegram bot to use the new n8n integration.

**Steps**:
1. Update the AI assistant import in `integrations/ai_assistant.py`:
   ```python
   # Change this line:
   from .n8n_multilingual_agent import N8nMultilingualAgent
   
   # To this:
   from .n8n_multilingual_agent_v2 import N8nMultilingualAgent
   ```

2. Restart the Telegram bot:
   ```bash
   # Stop current bot if running
   pkill -f "python.*bot"
   
   # Start bot with new integration
   python main.py
   ```

**Verification**: Bot starts without errors and uses n8n integration.

---

### Task 8: Verify Fallback Processing
**Status**: ⏳ Pending  
**Priority**: Medium  
**Estimated Time**: 3 minutes

**Description**: Ensure fallback processing works when n8n is unavailable.

**Steps**:
1. Temporarily stop n8n or change the URL in config
2. Test with a message:
   ```bash
   python test_russian.py
   ```

3. Verify that:
   - Fallback processing is used
   - Message is still processed correctly
   - Response indicates fallback source

**Expected Output**: Message processed with fallback, source shows "fallback".

**Verification**: Fallback processing works when n8n is unavailable.

---

## 🧪 Testing Checklist

After completing all tasks, verify:

- [ ] n8n connection test passes
- [ ] Multilingual workflow is deployed and active
- [ ] OpenAI API key is configured in n8n
- [ ] Russian voice message "Какие у меня задачи на сегодня?" works
- [ ] English message "What tasks do I have today?" works
- [ ] Fallback processing works when n8n is down
- [ ] Telegram bot uses new integration
- [ ] No errors in bot logs

## 🚨 Troubleshooting

### Connection Issues
- Verify n8n URL is correct
- Check API key or username/password
- Ensure n8n instance is running

### Workflow Issues
- Check OpenAI API key in n8n workflow
- Verify workflow is active
- Check n8n execution logs

### Fallback Issues
- Ensure `fallback_enabled: true` in config
- Check that original AI assistant still works
- Review bot logs for fallback activation

## 📞 Support

If you encounter issues:
1. Check the logs in `logs/bot.log`
2. Run the test script to identify problems
3. Verify n8n workflow configuration
4. Test with simple messages first

## 🎉 Success Criteria

The setup is complete when:
1. Your Russian voice message works correctly
2. n8n processes multilingual intent detection
3. Fallback works when n8n is unavailable
4. No errors in the system logs

Your multilingual voice command issue should now be completely resolved!
