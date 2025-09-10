# Personal System Telegram Bot - Setup Guide

## Quick Start

### 1. Create Your Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. **Save the bot token** - you'll need it for configuration

### 2. Get Your User ID

1. Send a message to `@userinfobot` on Telegram
2. It will reply with your user ID
3. **Save your user ID** - you'll need it for admin access

### 3. Setup the Bot

```bash
# Navigate to the bot directory
cd projects/personal_telegram_bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure the Bot

```bash
# Copy the sample configuration
cp config/config.yaml.sample config/config.yaml

# Edit the configuration file
nano config/config.yaml  # or use your preferred editor
```

**Update these settings in `config.yaml`:**

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
  allowed_users: []  # Leave empty to allow all users, or add specific user IDs
  admin_users: [YOUR_USER_ID]  # Add your user ID here for admin access

paths:
  base_path: "../../../"  # Path to your personal system root
  automation_scripts: "../../../automation/scripts/"
  journal: "../../../knowledge/journal/"
  notes: "../../../knowledge/notes/"
```

### 5. Run the Bot

```bash
# Start the bot
python main.py
```

### 6. Test the Bot

1. Open Telegram and search for your bot
2. Send `/start` to begin
3. Try `/help` to see all available commands

## Features Overview

### Daily Operations
- **`/summary`** - Get your daily health, productivity, learning, and finance summary
- **`/log_health`** - Log health metrics (steps, sleep, water, workout, etc.)
- **`/log_learning`** - Log learning activity and progress
- **`/quick_note`** - Capture thoughts and ideas quickly

### Shadow Work Integration
- **`/shadow_checkin`** - Daily shadow work check-in with prompts
- **`/shadow_log`** - Log shadow work insights and observations
- **`/shadow_prompt`** - Get random shadow work reflection prompts

### Journal & Notes
- **`/journal`** - Create journal entries
- **`/idea`** - Capture new ideas and inspirations
- **`/task`** - Add tasks to your system

### System Management
- **`/status`** - Check system status and health
- **`/stats`** - View detailed system statistics
- **`/backup`** - Create system backup (admin only)
- **`/sync`** - Sync data across devices

## Privacy & Security

- All data is stored locally in the `data/` directory
- User authentication prevents unauthorized access
- Privacy markers from your system are respected
- All interactions are logged for your reference

## Troubleshooting

### Common Issues

**Bot doesn't respond:**
- Check that your bot token is correct
- Ensure the bot is running (`python main.py`)
- Verify your user ID is in the allowed_users list

**Configuration errors:**
- Make sure `config.yaml` exists and is properly formatted
- Check that all paths point to valid directories
- Verify YAML syntax (use a YAML validator)

**Import errors:**
- Ensure you're in the correct directory
- Activate the virtual environment
- Install all dependencies: `pip install -r requirements.txt`

**Permission errors:**
- Check that the bot has write permissions to the `data/` directory
- Ensure your personal system paths are accessible

### Getting Help

1. Check the logs in `logs/bot.log`
2. Verify your configuration in `config/config.yaml`
3. Test individual components using the admin commands

## Advanced Configuration

### OpenAI Voice Transcription Setup

To enable voice message transcription:

1. **Get an OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set the API key securely** using the bot:
   ```
   /admin set_openai_key YOUR_API_KEY_HERE
   ```
3. **Test the configuration**:
   ```bash
   python test_openai_config.py
   ```
4. **Send voice messages** to your bot for transcription

**Note**: Your API key is encrypted and stored securely. Never share it in plain text.

### Customizing Prompts

Edit `integrations/shadow_work.py` to customize shadow work prompts.

### Adding New Commands

1. Create a new handler in `bot/handlers/`
2. Register it in `bot/bot.py`
3. Update the help text

### Integration with External Services

The bot is designed to be extensible. You can add integrations for:
- Health tracking APIs (Fitbit, Apple Health)
- Calendar systems
- Task management tools
- Cloud storage services

## Next Steps

1. **Test all commands** to ensure they work with your system
2. **Customize prompts** and responses to match your preferences
3. **Set up automated reminders** using the notification system
4. **Integrate with external services** as needed
5. **Backup your configuration** and data regularly

Your personal system now has a powerful Telegram interface! 🚀
