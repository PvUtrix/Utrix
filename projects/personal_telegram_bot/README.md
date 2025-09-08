# Personal System Telegram Bot

A comprehensive Telegram bot interface for your personal knowledge management and automation system. This bot provides voice-controlled access to all your automation scripts, interactive menus, and natural language commands.

## 🚀 Features

### 🎤 Voice Commands
- **Voice Transcription**: Send voice messages for hands-free interaction
- **Action Parsing**: Automatically parse voice commands into actionable items
- **Confirmation System**: Review and approve actions before execution
- **Natural Language**: Use natural speech patterns for commands

### 📱 Interactive Menus
- **Categorized Navigation**: Organized menus for all system features
- **Quick Access**: One-tap access to automation scripts
- **Visual Interface**: Clean, intuitive button-based navigation
- **Context-Aware**: Smart menus that adapt to your needs

### ⚡ Automation Integration
- **Shadow Work Tracker**: Daily check-ins, insights, prompts, and reports
- **Opportunity Manager**: Create, evaluate, and manage career opportunities
- **Business Opportunity Manager**: Track business and investment opportunities
- **Daily Summary Generator**: Automated daily summaries and insights
- **Prosperity Course Manager**: Track course progress and status
- **Google Drive Sync**: Automated data synchronization
- **System Backup**: Automated backup creation and management

### 🔒 Privacy & Security
- **End-to-End Encryption**: All sensitive data encrypted locally
- **Privacy Markers**: Respects .private file markers
- **Secure Authentication**: User-based access control
- **Local Storage**: Data stored locally with optional cloud sync

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

## 🎯 Usage

### 🎤 Voice Commands
Send voice messages for natural interaction:

**Opportunity Management:**
- "Create a new opportunity for software engineer role at Google"
- "Show my pending opportunities"
- "Evaluate opportunity [ID]"
- "Check upcoming deadlines"

**Shadow Work:**
- "Log shadow work insight: I noticed I avoid difficult conversations"
- "Daily shadow work check-in"
- "Get shadow work prompt"
- "Show shadow work progress"

**Daily Operations:**
- "Generate daily summary"
- "Add task: Review quarterly goals"
- "Log health metrics"
- "Capture idea: New app concept"

**System Management:**
- "Backup my system"
- "Sync with Google Drive"
- "Show system statistics"

### 📱 Interactive Menus
Use `/start` or `/menu` to access the main menu with categorized options:

- **📊 Daily Operations**: Summary, health tracking, learning logs
- **🧠 Shadow Work**: Check-ins, insights, prompts, reports
- **📝 Journal & Notes**: Entries, ideas, tasks
- **💼 Opportunities**: Career and business opportunity management
- **⚙️ System Management**: Backup, sync, statistics
- **🎤 Voice Commands**: Examples and help
- **❓ Help & Examples**: Comprehensive guidance

### ⚡ Quick Commands
- `/start` - Main menu with interactive buttons
- `/menu` - Show main navigation menu
- `/help` - Detailed help and examples
- `/status` - System status overview

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
