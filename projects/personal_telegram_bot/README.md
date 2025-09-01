# Personal System Telegram Bot

A Telegram bot interface for your personal knowledge management and automation system. This bot provides quick access to your system's features, data collection, and insights through natural language commands.

## Features

### Core Functionality
- **Daily Summary**: Get your daily health, productivity, learning, and finance summary
- **Morning Routine**: Voice-guided morning routine with automatic delivery at 6:00 AM
- **Shadow Work Tracking**: Log shadow work insights and get prompts
- **Quick Notes**: Capture thoughts and ideas on the go
- **System Status**: Check various system metrics and status
- **Journal Entries**: Create quick journal entries
- **Task Management**: Add and track tasks
- **Health Tracking**: Log health metrics
- **Learning Progress**: Track learning activities

### Privacy & Security
- End-to-end encryption for sensitive data
- Local data storage with optional cloud sync
- Privacy markers respected (.private files)
- Secure authentication

### Integration
- Connects with existing automation scripts
- Integrates with your knowledge base
- Syncs with your journal system
- Connects to your shadow work tracking

## Setup Instructions

### 1. Create Telegram Bot
1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Save the bot token securely

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
1. Copy `config.yaml.sample` to `config.yaml`
2. Add your bot token and other settings
3. Configure paths to your personal system

### 4. Run the Bot
```bash
python main.py
```

## Commands

### Basic Commands
- `/start` - Welcome message and help
- `/help` - Show available commands
- `/status` - System status overview

### Daily Operations
- `/summary` - Get daily summary
- `/morning_routine` - Get voice-guided morning routine
- `/log_health` - Log health metrics
- `/log_learning` - Log learning activity
- `/quick_note` - Capture a quick thought

### Shadow Work
- `/shadow_checkin` - Daily shadow work check-in
- `/shadow_log` - Log shadow work insight
- `/shadow_prompt` - Get shadow work prompt

### Journal & Notes
- `/journal` - Create journal entry
- `/idea` - Capture new idea
- `/task` - Add new task

### System Management
- `/backup` - Create system backup
- `/sync` - Sync data across devices
- `/stats` - View system statistics

## Architecture

```
personal_telegram_bot/
├── main.py                 # Main bot entry point
├── bot/
│   ├── __init__.py
│   ├── handlers/           # Command handlers
│   ├── middleware/         # Custom middleware
│   └── utils/             # Utility functions
├── integrations/
│   ├── personal_system.py  # Integration with your system
│   ├── journal.py         # Journal integration
│   └── shadow_work.py     # Shadow work integration
├── data/
│   ├── storage/           # Local data storage
│   └── cache/            # Temporary cache
├── config/
│   └── config.yaml       # Configuration file
└── tests/                # Test files
```

## Privacy Considerations

- All sensitive data is encrypted locally
- Bot only stores necessary session data
- Integration respects your privacy markers
- Data can be exported/deleted on demand

## Future Enhancements

- Voice message support
- Image analysis for health tracking
- AI-powered insights and recommendations
- Integration with external APIs (health, finance)
- Advanced natural language processing
- Multi-language support

## Contributing

This bot is designed for personal use but can be extended. Follow the existing code patterns and respect privacy guidelines.
