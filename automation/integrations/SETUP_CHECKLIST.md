# n8n Integration Setup Checklist

## 🚀 Quick Setup (Recommended)

Run the automated setup script:

```bash
cd /Users/PvUtrix_1/Apps/_cursor/personal-system/automation/integrations
python quick_setup.py
```

This will guide you through the entire setup process.

---

## 📋 Manual Setup Checklist

### ✅ Prerequisites
- [ ] n8n instance is running and accessible
- [ ] You have n8n API key or username/password
- [ ] You have OpenAI API key
- [ ] Python environment is set up

### ✅ Configuration
- [ ] Update `services/telegram-bot/config/config.yaml` with n8n details
- [ ] Add n8n base URL
- [ ] Add n8n API key or username/password
- [ ] Add OpenAI API key for n8n workflow

### ✅ Dependencies
- [ ] Install httpx: `pip install httpx`
- [ ] Install pyyaml: `pip install pyyaml`
- [ ] Verify imports work: `python -c "import httpx, yaml"`

### ✅ n8n Connection
- [ ] Test connection: `python automation/integrations/n8n_cli.py test`
- [ ] Verify n8n instance is accessible
- [ ] Check API authentication works

### ✅ Workflow Deployment
- [ ] Deploy multilingual workflow: `python automation/integrations/n8n_cli.py deploy multilingual_intent`
- [ ] Verify workflow appears in n8n UI
- [ ] Ensure workflow is active (green status)

### ✅ OpenAI Configuration
- [ ] Open n8n UI in browser
- [ ] Navigate to "Multilingual Intent Detection" workflow
- [ ] Click on "AI Intent Detection" node
- [ ] Add your OpenAI API key
- [ ] Save and activate workflow

### ✅ Testing
- [ ] Test Russian message: "Какие у меня задачи на сегодня?"
- [ ] Test English message: "What tasks do I have today?"
- [ ] Verify intent detection works
- [ ] Check response quality

### ✅ Bot Integration
- [ ] Update AI assistant to use new integration
- [ ] Restart Telegram bot
- [ ] Test with actual voice messages
- [ ] Verify fallback works when n8n is down

---

## 🧪 Test Commands

### Test Connection
```bash
cd services/telegram-bot
python automation/integrations/n8n_cli.py test --service telegram-bot
```

### Test Multilingual Processing
```bash
cd services/telegram-bot
python test_n8n_multilingual.py
```

### Test Webhook
```bash
cd services/telegram-bot
python automation/integrations/n8n_cli.py test-webhook --service telegram-bot multilingual_intent
```

---

## 🚨 Troubleshooting

### Connection Issues
- Check n8n URL is correct
- Verify API key or username/password
- Ensure n8n instance is running

### Workflow Issues
- Check workflow is active in n8n UI
- Verify OpenAI API key is configured
- Check n8n execution logs

### Bot Issues
- Check bot logs for errors
- Verify configuration is correct
- Test with simple messages first

---

## ✅ Success Criteria

The setup is complete when:
- [ ] Russian voice message "Какие у меня задачи на сегодня?" works
- [ ] English message "What tasks do I have today?" works
- [ ] Intent detection returns correct results
- [ ] Fallback processing works when n8n is unavailable
- [ ] No errors in bot logs

---

## 🎯 Expected Results

After successful setup:
1. **Russian Voice Message**: "Какие у меня задачи на сегодня?" → Returns task recommendations
2. **English Message**: "What tasks do I have today?" → Returns task recommendations
3. **High Confidence**: Intent detection with confidence > 0.7
4. **Multilingual Support**: Works in both Russian and English
5. **Fallback**: Works even when n8n is unavailable

Your original multilingual voice command issue should now be completely resolved! 🎉
