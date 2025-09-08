# 🎤 Voice-Enabled Telegram Bot Setup Guide

This guide will help you set up your personal system Telegram bot with voice command capabilities and automation script integration.

## 🚀 Quick Start

### 1. Create Telegram Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Save the bot token securely

### 2. Get OpenAI API Key (for Voice Transcription)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Go to API Keys section
4. Create a new API key
5. Save the key securely

### 3. Environment Setup

**Option A: Quick Install (Recommended)**
```bash
# Navigate to bot directory
cd projects/personal_telegram_bot

# Run installation script
./install.sh
```

**Option B: Manual Install**
```bash
# Navigate to bot directory
cd projects/personal_telegram_bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Note:** The requirements.txt has been updated to resolve dependency conflicts with httpx and supabase.

### 4. Configuration
1. Copy `config/config.yaml.sample` to `config/config.yaml`
2. Edit the configuration file:

```yaml
# Telegram Bot Settings
telegram:
  bot_token: "YOUR_BOT_TOKEN_HERE"
  allowed_users: [YOUR_TELEGRAM_USER_ID]  # Get from @userinfobot
  admin_users: [YOUR_TELEGRAM_USER_ID]

# Personal System Paths
paths:
  base_path: "../../../"  # Path to your personal system root
  automation_scripts: "../../../automation/scripts/"

# OpenAI Configuration
openai:
  api_key: "YOUR_OPENAI_API_KEY_HERE"
  model: "whisper-1"
  enable_voice_transcription: true
```

### 5. Run the Bot
```bash
python main.py
```

**🎉 Startup Notification:**
When the bot starts, it will automatically send you a welcome message with:
- Bot status confirmation
- Available features overview
- Quick start guide
- Voice command examples

**🧪 Test Notifications:**
You can test the notification system anytime by sending:
- `/test_notification` - Test the bot's messaging system

## 🎤 Voice Commands Setup

### Supported Voice Commands

**Opportunity Management:**
- "Create a new opportunity for [description]"
- "Create business opportunity for [description]"
- "Show my opportunities"
- "List business opportunities"
- "Check upcoming deadlines"
- "Evaluate opportunity [ID]"

**Shadow Work:**
- "Daily shadow work check-in"
- "Log shadow work insight: [insight]"
- "Get shadow work prompt"
- "Show shadow work progress"
- "Set shadow work focus: [aspect]"

**Daily Operations:**
- "Generate daily summary"
- "Get morning routine"
- "Log health metrics"
- "Log learning activity"
- "Add task: [task description]"
- "Capture idea: [idea]"

**System Management:**
- "Create system backup"
- "Sync with Google Drive"
- "Show system statistics"
- "Check prosperity course status"

### Voice Command Flow
1. **Send Voice Message**: Record and send voice message to bot
2. **Transcription**: Bot transcribes using OpenAI Whisper
3. **Action Parsing**: Bot parses command and extracts parameters
4. **Confirmation**: Bot shows confirmation with extracted details
5. **Execution**: After approval, bot executes the automation script
6. **Results**: Bot shows execution results and output

## 📱 Interactive Menus

### Main Menu Categories
- **📊 Daily Operations**: Health, learning, summaries
- **🧠 Shadow Work**: Check-ins, insights, prompts
- **📝 Journal & Notes**: Entries, ideas, tasks
- **💼 Opportunities**: Career and business opportunities
- **⚙️ System Management**: Backup, sync, statistics
- **🎤 Voice Commands**: Examples and help
- **❓ Help & Examples**: Comprehensive guidance

### Menu Navigation
- Use `/start` or `/menu` to access main menu
- Click buttons to navigate through categories
- Each category has specific actions available
- Actions execute your automation scripts directly

## 🔧 Automation Script Integration

### Available Scripts
The bot integrates with these automation scripts:

1. **Shadow Work Tracker** (`shadow_work_tracker.py`)
   - Daily check-ins
   - Insight logging
   - Progress reports
   - Reminders

2. **Opportunity Manager** (`opportunity_manager.py`)
   - Create opportunities
   - List and evaluate
   - Check deadlines
   - Archive opportunities

3. **Business Opportunity Manager** (`business_opportunity_manager.py`)
   - Business opportunity tracking
   - Investment opportunities
   - Business evaluation

4. **Daily Summary Generator** (`daily_summary.py`)
   - Automated daily summaries
   - Health and productivity insights

5. **Prosperity Course Manager** (`prosperity-course-manager.py`)
   - Course progress tracking
   - Status updates

6. **Google Drive Sync** (`google_drive_sync.py`)
   - Automated data synchronization
   - Cloud backup

7. **System Backup** (`create_backup.py`)
   - Automated backup creation
   - Data protection

### Script Execution
- Scripts are executed with appropriate parameters
- Output is captured and displayed in Telegram
- Error handling provides clear feedback
- Timeout protection prevents hanging

## 🔒 Security & Privacy

### Authentication
- User-based access control
- Admin vs regular user permissions
- Secure token storage

### Data Protection
- Local data storage
- Encrypted sensitive data
- Privacy markers respected
- No data sent to external services (except OpenAI for transcription)

### Voice Data
- Voice files are temporarily downloaded for transcription
- Files are deleted after processing
- Only transcribed text is processed
- No voice data is stored permanently

## 🛠️ Troubleshooting

### Common Issues

**Voice Transcription Not Working:**
- Check OpenAI API key is correct
- Verify API key has sufficient credits
- Ensure voice file is clear and not too long

**Scripts Not Executing:**
- Verify script paths in config
- Check script permissions
- Ensure Python environment is correct
- Check script dependencies

**Menu Buttons Not Working:**
- Restart the bot
- Check callback query handlers are registered
- Verify inline keyboard markup

**Authentication Issues:**
- Check user ID is correct
- Verify bot token is valid
- Ensure user is in allowed_users list

### Debug Mode
Enable debug logging by setting:
```yaml
logging:
  level: "DEBUG"
```

### Logs
Check logs in `logs/bot.log` for detailed information about errors and execution.

## 🚀 Advanced Features

### Custom Voice Commands
You can extend the voice command parser by modifying `voice_handlers.py`:

```python
# Add new action patterns
self.action_patterns["custom_action"] = [
    "custom command", "new action", "special task"
]
```

### Custom Automation Scripts
Add new scripts by:
1. Creating the script in `automation/scripts/`
2. Adding mapping in `automation_handlers.py`
3. Updating menu handlers if needed

### Integration with External Services
The bot can be extended to integrate with:
- Calendar systems
- Health tracking APIs
- Financial data sources
- Learning platforms

## 📞 Support

For issues or questions:
1. Check the logs in `logs/bot.log`
2. Verify configuration settings
3. Test individual automation scripts
4. Check Telegram bot permissions

## 🔄 Updates

To update the bot:
1. Pull latest changes
2. Update dependencies: `pip install -r requirements.txt`
3. Restart the bot
4. Test voice commands and menus

---

**Enjoy your voice-controlled personal system! 🎤✨**
