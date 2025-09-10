# Personal System Telegram Bot

The Personal System Telegram Bot is the primary interface for your personal knowledge management and automation system. It provides voice transcription, daily operations, and system management through a convenient Telegram interface.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Telegram Bot Token (from @BotFather)
- API keys for voice transcription services

### Running the Bot

#### Option 1: Using the Run Script (Recommended)
```bash
./run_bot.sh
```

This script will:
- ✅ Check Python installation
- ✅ Create/activate virtual environment
- ✅ Install all required dependencies
- ✅ Verify configuration
- ✅ Start the bot

#### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install python-telegram-bot==20.7 pyyaml aiohttp requests

# Start the bot
python3 main.py
```

### Stopping the Bot
```bash
./stop_bot.sh
```

## 🎤 Voice Transcription

The bot supports voice message transcription using:

- **Primary**: ElevenLabs Scribe (speech-to-text)
- **Fallback**: OpenAI Whisper

### Voice Commands
Send voice messages to the bot and it will:
1. Transcribe your voice using serverless functions
2. Process voice commands like:
   - "log health" - Track health metrics
   - "add task" - Add a new task
   - "quick note" - Capture a quick note
   - "morning routine" - Get daily routine
   - "daily summary" - Get daily summary

## 📋 Daily Operations

### Available Commands
- `/summary` - Daily summary with interactive buttons
- `/log_health` - Log health metrics
- `/log_learning` - Track learning progress
- `/quick_note` - Capture quick notes
- `/morning_routine` - Get morning routine
- `/shadow_checkin` - Shadow work reflection
- `/journal` - Journal entry
- `/task` - Task management
- `/backup` - System backup
- `/sync` - Data synchronization

### Interactive Buttons
The bot provides interactive buttons for:
- Daily operations (health, learning, tasks, notes)
- Quick actions from daily summary
- System management functions

## ⚙️ Configuration

### Bot Configuration (`config/config.yaml`)
```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  allowed_users: [YOUR_USER_ID]
  admin_users: [YOUR_USER_ID]

serverless:
  transcription_url: "YOUR_SERVERLESS_URL"
  enable_serverless_transcription: true

elevenlabs:
  api_key: "YOUR_ELEVENLABS_API_KEY"
  enable_speech_to_text: true

openai:
  api_key: "YOUR_OPENAI_API_KEY"
  enable_voice_transcription: true
```

### Required API Keys
1. **Telegram Bot Token**: Get from @BotFather
2. **ElevenLabs API Key**: For voice transcription
3. **OpenAI API Key**: For fallback transcription

## 🔧 Troubleshooting

### Common Issues

#### Bot Won't Start
```bash
# Check Python version
python3 --version

# Recreate virtual environment
rm -rf venv
./run_bot.sh
```

#### Voice Transcription Not Working
1. Check serverless function is deployed
2. Verify API keys are set in serverless environment
3. Test serverless function directly

#### Missing Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Logs
Bot logs are written to:
- Console output (when running in foreground)
- `logs/bot.log` (if configured)

## 🏗️ Architecture

### Components
- **Bot Core** (`bot/bot.py`) - Main bot application
- **Handlers** (`bot/handlers/`) - Command and message handlers
- **Serverless Integration** - Voice transcription via AWS Lambda
- **Configuration** (`config/`) - Bot and system configuration

### Voice Processing Flow
1. User sends voice message
2. Bot downloads voice file
3. Sends to serverless transcription function
4. Receives transcription
5. Processes voice commands
6. Sends response to user

## 📁 File Structure
```
core/telegram_interface/
├── run_bot.sh              # Bot startup script
├── stop_bot.sh             # Bot stop script
├── main.py                 # Bot entry point
├── requirements.txt        # Python dependencies
├── config/
│   └── config.yaml        # Bot configuration
├── bot/
│   ├── bot.py             # Main bot class
│   └── handlers/          # Message handlers
├── venv/                  # Virtual environment
└── logs/                  # Bot logs
```

## 🔄 Updates

To update the bot:
1. Stop the bot: `./stop_bot.sh`
2. Pull latest changes
3. Restart: `./run_bot.sh`

## 📞 Support

For issues or questions:
1. Check the logs for error messages
2. Verify configuration settings
3. Test individual components
4. Check serverless function status

---

**Note**: This bot is part of your personal system and should be kept secure. Never share your bot token or API keys.
