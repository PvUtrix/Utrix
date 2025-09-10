# Start Scripts for Personal System

This directory contains start scripts for all Python applications and tools in the Personal System that require a virtual environment and have dependencies.

## 🚀 Quick Start

### Master Script
Use the master script to see all available options:
```bash
./start_all.sh
```

### Individual Scripts
Run any specific script directly:
```bash
./start_script_name.sh [arguments...]
```

## 📋 Available Scripts

### Core Applications

#### `start_main_api.sh`
- **Purpose**: Starts the Personal System API Server
- **Port**: 8000 (default)
- **URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Requirements**: Main project requirements

#### `start_telegram_bot.sh`
- **Purpose**: Starts the Personal System Telegram Bot
- **Requirements**: Telegram bot token in environment variables
- **Features**: Voice commands, interactive menus, automation scripts

### Projects

#### `start_habit_tracker.sh`
- **Purpose**: Starts the Habit Tracker Flask Web App
- **Port**: 5000 (default)
- **URL**: http://localhost:5000
- **Features**: Habit tracking, streak management, statistics

#### `start_presentation_analyzer.sh`
- **Purpose**: Analyzes presentations from Google Drive
- **Features**: Text extraction, keyword analysis, knowledge base integration
- **Requirements**: Google Drive API credentials

### Automation Tools

#### `start_task_manager.sh`
- **Purpose**: Manages codebase improvement tasks
- **Usage Examples**:
  ```bash
  ./start_task_manager.sh --add "Fix authentication bug" --priority high
  ./start_task_manager.sh --list
  ./start_task_manager.sh --complete task_001
  ./start_task_manager.sh --report
  ```

#### `start_daily_summary.sh`
- **Purpose**: Generates daily summaries with reflections
- **Features**: Health data, productivity metrics, learning progress, financial data
- **Output**: Markdown summary and JSON data

#### `start_cleanup_tool.sh`
- **Purpose**: Cleans up temporary files and optimizes system
- **Features**: Automated cleanup, file organization, system optimization

#### `start_code_quality_checker.sh`
- **Purpose**: Analyzes code for quality issues
- **Features**: Linting, code analysis, quality metrics

#### `start_lab_analyzer.sh`
- **Purpose**: Analyzes lab results and health data
- **Features**: Health data processing, trend analysis

#### `start_reminder_system.sh`
- **Purpose**: Manages reminders and notifications
- **Features**: Automated reminders, notification scheduling

## 🔧 Setup Requirements

### Virtual Environment
All scripts automatically:
1. Check for existing virtual environment in `venv/`
2. Create one if it doesn't exist
3. Activate the environment
4. Install/update requirements

### Environment Variables
Scripts automatically load environment variables from `.env` file if present.

### Required Environment Variables
- **Telegram Bot**: `TELEGRAM_BOT_TOKEN`
- **Google Drive**: `GOOGLE_DRIVE_CREDENTIALS_PATH`
- **Database**: `CORE_SUPABASE_URL`
- **AI Services**: `ELEVENLABS_API_KEY`, `OPENAI_API_KEY`

## 📁 Directory Structure

```
personal-system/
├── start_all.sh                    # Master script
├── start_main_api.sh              # API server
├── start_telegram_bot.sh          # Telegram bot
├── start_habit_tracker.sh         # Habit tracker app
├── start_presentation_analyzer.sh # Presentation analyzer
├── start_task_manager.sh          # Task manager tool
├── start_daily_summary.sh         # Daily summary generator
├── start_cleanup_tool.sh          # Cleanup tool
├── start_code_quality_checker.sh  # Code quality checker
├── start_lab_analyzer.sh          # Lab analyzer
├── start_reminder_system.sh       # Reminder system
└── START_SCRIPTS_README.md        # This file
```

## 🛠️ Customization

### Adding New Scripts
1. Create a new `.sh` file following the naming pattern `start_[tool_name].sh`
2. Use the template structure from existing scripts
3. Update `start_all.sh` to include the new script
4. Make the script executable: `chmod +x start_[tool_name].sh`

### Script Template
```bash
#!/bin/bash
# Start script for [Tool Name]
# This script sets up the virtual environment and runs [tool]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
TOOL_DIR="$PROJECT_ROOT/path/to/tool"

echo -e "${BLUE}🚀 Starting [Tool Name]${NC}"

# Virtual environment setup
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    cd "$PROJECT_ROOT"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Install requirements
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    pip install -r "$PROJECT_ROOT/requirements.txt"
fi

# Create necessary directories
mkdir -p "$PROJECT_ROOT/logs"

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Run the tool
cd "$TOOL_DIR"
python main.py "$@"
```

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x start_*.sh
   ```

2. **Virtual Environment Issues**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Missing Dependencies**
   - Check if `requirements.txt` exists in the tool directory
   - Ensure all required environment variables are set

4. **Port Already in Use**
   - Check what's running on the port: `lsof -i :8000`
   - Kill the process or change the port in the script

### Logs
Check the `logs/` directory for application logs and error messages.

## 📞 Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Verify environment variables are set correctly
3. Ensure all requirements are installed
4. Check the individual tool documentation

---

*Last updated: $(date)*
