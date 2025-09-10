# Automation Scripts

This directory contains all automation scripts for the Personal System, organized by category for easy navigation and maintenance.

## 📁 Directory Structure

```
automation/scripts/
├── daily_operations/          # Daily productivity and tracking scripts
│   ├── health/               # Health and wellness tracking
│   ├── learning/             # Learning and skill development
│   ├── notes/                # Note-taking and knowledge capture
│   ├── routines/             # Daily routines and habits
│   ├── tasks/                # Task and project management
│   ├── daily_summary.py      # Daily summary generation
│   └── daily_task_reminder.py # Task reminder system
├── shadow_work/              # Shadow work and self-development
├── opportunities/            # Career and business opportunities
├── system_management/        # System maintenance and utilities
├── custom/                   # Custom scripts and utilities
└── legacy/                   # Deprecated or old scripts
```

## 🎯 Script Categories

### 📊 Daily Operations
Core scripts for daily productivity and life management:

- **Health Tracking** (`daily_operations/health/`)
  - `health_logger.py` - Track health metrics (steps, sleep, mood, etc.)
  
- **Learning Management** (`daily_operations/learning/`)
  - `learning_tracker.py` - Track learning activities and progress
  
- **Task Management** (`daily_operations/tasks/`)
  - `task_manager.py` - Create, manage, and track tasks
  
- **Note Taking** (`daily_operations/notes/`)
  - `quick_note.py` - Rapid note capture and organization
  
- **Daily Routines** (`daily_operations/routines/`)
  - `morning_routine.py` - Generate personalized morning routines
  
- **Daily Summary** (`daily_operations/`)
  - `daily_summary.py` - Generate comprehensive daily summaries
  - `daily_task_reminder.py` - Automated task reminders

### 🧠 Shadow Work
Self-development and inner work scripts:

- **Shadow Work Tracker** (`shadow_work/`)
  - `shadow_work_tracker.py` - Track shadow work insights and progress

### 💼 Opportunities
Career and business opportunity management:

- **Opportunity Management** (`opportunities/`)
  - `opportunity_manager.py` - Manage career opportunities
  - `business_opportunity_manager.py` - Manage business opportunities

### ⚙️ System Management
System maintenance and utility scripts:

- **System Utilities** (`system_management/`)
  - `create_backup.py` - Create system backups
  - `google_drive_sync.py` - Sync with Google Drive
  - `prosperity-course-manager.py` - Manage prosperity course progress

### 🔧 Custom Scripts
Custom utilities and integrations:

- **Custom Utilities** (`custom/`)
  - `setup_gitea_sync.sh` - Setup Gitea synchronization
  - `update_intro_reminder.py` - Update introduction reminders

### 📦 Legacy Scripts
Deprecated or old scripts for reference:

- **Legacy Scripts** (`legacy/`)
  - `manual_input_example.py` - Example manual input script
  - `morning_routine.py` - Old morning routine script
  - `weekly/` - Weekly review scripts

## 🚀 Usage

### Running Scripts Directly

Each script can be run directly from the command line:

```bash
# Health logging
python3 daily_operations/health/health_logger.py log steps 8500 "Morning walk"

# Learning tracking
python3 daily_operations/learning/learning_tracker.py log reading 30 "Python docs"

# Task management
python3 daily_operations/tasks/task_manager.py add "Complete project" "Finish the project"

# Quick notes
python3 daily_operations/notes/quick_note.py capture "Great idea for new feature"

# Morning routine
python3 daily_operations/routines/morning_routine.py generate
```

### Integration with Telegram Bot

All scripts are integrated with the Telegram bot through the automation handlers. Users can access them through:

- **Daily Operations Menu** - Health, learning, tasks, notes, routines
- **Shadow Work Menu** - Shadow work tracking and insights
- **Opportunities Menu** - Career and business opportunities
- **System Management Menu** - Backups, sync, system utilities

## 📋 Script Standards

All scripts follow these standards:

### File Structure
- **Shebang**: `#!/usr/bin/env python3`
- **Docstring**: Clear description of purpose
- **Imports**: Standard library first, then local imports
- **Class-based**: Main functionality in classes
- **Main function**: Command-line interface
- **Error handling**: Comprehensive error handling

### Data Storage
- **JSON format**: All data stored in JSON files
- **Structured data**: Consistent data structure across scripts
- **Backup support**: Data can be easily backed up
- **Privacy**: All data stored locally

### Command Line Interface
- **Action-based**: `python script.py <action> [args...]`
- **Help text**: Built-in help for all actions
- **JSON output**: Structured output for integration
- **Error messages**: Clear error messages

### Integration
- **Telegram bot**: All scripts integrated with bot
- **Automation handlers**: Proper error handling and logging
- **Voice commands**: Support for voice command integration
- **Confirmation system**: User confirmation for actions

## 🔧 Development

### Adding New Scripts

1. **Choose category**: Place script in appropriate category folder
2. **Follow standards**: Use the established file structure
3. **Update handlers**: Add script to automation handlers
4. **Test integration**: Test with Telegram bot
5. **Update documentation**: Update relevant README files

### Script Template

```python
#!/usr/bin/env python3
"""
[Script Name] - [Description]
Part of the Personal System automation suite.
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent.parent))

class [ScriptName]:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "outputs"
        self.data_file = self.data_dir / "[data_file].json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def [main_method](self, *args, **kwargs):
        """Main functionality."""
        # Implementation here
        pass

def main():
    """Main entry point."""
    script = [ScriptName]()
    
    if len(sys.argv) < 2:
        print("Usage: python [script_name].py <action> [args...]")
        print("Actions:")
        print("  [action1] - [description]")
        print("  [action2] - [description]")
        return
    
    action = sys.argv[1]
    
    if action == "[action1]":
        # Handle action1
        pass
    elif action == "[action2]":
        # Handle action2
        pass
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
```

## 📊 Data Files

All scripts store data in the `automation/outputs/` directory:

- `health_data.json` - Health metrics and statistics
- `learning_data.json` - Learning activities and progress
- `tasks.json` - Task management data
- `quick_notes.json` - Quick notes and ideas
- `morning_routines.json` - Generated morning routines
- `shadow_work_data.json` - Shadow work insights
- `opportunities.json` - Career opportunities
- `business_opportunities.json` - Business opportunities

## 🔒 Privacy & Security

- **Local storage**: All data stored locally
- **No external APIs**: Scripts don't send data externally
- **Encryption ready**: Data structure supports encryption
- **Backup friendly**: Easy to backup and restore
- **Privacy markers**: Respects `.private` file markers

## 🧪 Testing

### Manual Testing
```bash
# Test each script with various inputs
python3 daily_operations/health/health_logger.py list
python3 daily_operations/health/health_logger.py log steps 10000
python3 daily_operations/health/health_logger.py today
```

### Integration Testing
- Test through Telegram bot interface
- Verify data persistence
- Check error handling
- Validate output formatting

## 📚 Related Documentation

- [Telegram Bot Integration](../core/telegram_interface/README.md)
- [Automation Handlers](../core/telegram_interface/bot/handlers/automation_handlers.py)
- [Button Integration Map](../core/telegram_interface/BUTTON_INTEGRATION_MAP.md)
- [Implementation Roadmap](../core/telegram_interface/IMPLEMENTATION_ROADMAP.md)

---

*Last Updated: 2024-12-19*
*Organization: Complete - All scripts properly categorized and documented*