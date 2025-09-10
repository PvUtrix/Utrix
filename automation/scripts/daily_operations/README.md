# Daily Operations Scripts

Core scripts for daily productivity, tracking, and life management.

## 📁 Structure

```
daily_operations/
├── health/                   # Health and wellness tracking
│   └── health_logger.py     # Track health metrics
├── learning/                 # Learning and skill development
│   └── learning_tracker.py  # Track learning activities
├── notes/                    # Note-taking and knowledge capture
│   └── quick_note.py        # Rapid note capture
├── routines/                 # Daily routines and habits
│   └── morning_routine.py   # Generate morning routines
├── tasks/                    # Task and project management
│   └── task_manager.py      # Task management system
├── daily_summary.py          # Daily summary generation
└── daily_task_reminder.py    # Task reminder system
```

## 🎯 Scripts Overview

### 💪 Health Tracking (`health/`)

**health_logger.py** - Comprehensive health metrics tracking
- **Features**: Steps, sleep, water, mood, workout, weight, calories, meditation, stress, energy
- **Capabilities**: Daily tracking, weekly statistics, health summaries
- **Usage**: `python3 health_logger.py log steps 8500 "Morning walk"`
- **Integration**: Telegram buttons `action_log_health`, `action_health_stats`

### 📚 Learning Management (`learning/`)

**learning_tracker.py** - Learning activities and progress tracking
- **Features**: Reading, video, course, practice, research, writing, discussion, project, review, experiment
- **Capabilities**: Duration tracking, course progress, skill development, learning reports
- **Usage**: `python3 learning_tracker.py log reading 30 "Python docs"`
- **Integration**: Telegram button `action_log_learning`

### ✅ Task Management (`tasks/`)

**task_manager.py** - Complete task and project management
- **Features**: Add, view, update, delete, complete tasks with priorities and due dates
- **Capabilities**: Priority management, category organization, task statistics, completion tracking
- **Usage**: `python3 task_manager.py add "Complete project" "Finish the project"`
- **Integration**: Telegram buttons `action_add_task`, `action_view_tasks`

### 📝 Note Taking (`notes/`)

**quick_note.py** - Rapid note capture and organization
- **Features**: Auto-categorization, auto-tagging, search functionality, note statistics
- **Capabilities**: Smart categorization, tag extraction, note search, today's notes
- **Usage**: `python3 quick_note.py capture "Great idea for new feature"`
- **Integration**: Telegram button `action_quick_note`

### 🌅 Daily Routines (`routines/`)

**morning_routine.py** - Personalized morning routine generation
- **Features**: Weather context, motivational quotes, health check-ins, task priorities, shadow work prompts
- **Capabilities**: Personalized routines, daily intentions, progress integration
- **Usage**: `python3 morning_routine.py generate`
- **Integration**: Telegram button `action_morning_routine`

### 📊 Daily Summary (`daily_summary.py`)

**daily_summary.py** - Comprehensive daily summary generation
- **Features**: Health, learning, task, and productivity summaries
- **Capabilities**: Data aggregation, trend analysis, daily insights
- **Usage**: `python3 daily_summary.py`
- **Integration**: Telegram button `action_daily_summary`

### 🔔 Task Reminders (`daily_task_reminder.py`)

**daily_task_reminder.py** - Automated task reminder system
- **Features**: Due date tracking, priority reminders, overdue notifications
- **Capabilities**: Automated reminders, task prioritization, deadline management
- **Usage**: `python3 daily_task_reminder.py`
- **Integration**: Automated system reminders

## 🚀 Quick Start

### Health Tracking
```bash
# Log health metrics
python3 health/health_logger.py log steps 8500 "Morning walk"
python3 health/health_logger.py log sleep 8 "Good night's rest"
python3 health/health_logger.py log mood great "Feeling energetic"

# View today's health stats
python3 health/health_logger.py today

# View weekly health stats
python3 health/health_logger.py weekly
```

### Learning Tracking
```bash
# Log learning activities
python3 learning/learning_tracker.py log reading 30 "Python documentation"
python3 learning/learning_tracker.py log course 45 "Machine Learning Course"
python3 learning/learning_tracker.py log practice 60 "Coding exercises"

# View today's learning stats
python3 learning/learning_tracker.py today

# View course progress
python3 learning/learning_tracker.py course "Python Programming"
```

### Task Management
```bash
# Add tasks
python3 tasks/task_manager.py add "Complete project" "Finish the project" "high" "2024-12-20" "development"

# View tasks
python3 tasks/task_manager.py list
python3 tasks/task_manager.py today

# Complete tasks
python3 tasks/task_manager.py complete task_0001 "Finished successfully"
```

### Quick Notes
```bash
# Capture notes
python3 notes/quick_note.py capture "Great idea for new feature" "development" "idea,feature" "high"

# Search notes
python3 notes/quick_note.py search "feature"

# View today's notes
python3 notes/quick_note.py today
```

### Morning Routine
```bash
# Generate morning routine
python3 routines/morning_routine.py generate

# Generate without certain sections
python3 routines/morning_routine.py generate --no-health --no-tasks
```

## 📊 Data Integration

All daily operations scripts share data and integrate with each other:

- **Health data** feeds into morning routine generation
- **Task data** appears in daily summaries and morning routines
- **Learning data** contributes to daily summaries
- **Notes** can be categorized and searched across all activities

## 🔧 Telegram Bot Integration

All scripts are fully integrated with the Telegram bot:

### Daily Operations Menu
- 📈 **Daily Summary** - Generate comprehensive daily summaries
- 🌅 **Morning Routine** - Get personalized morning routines
- 💪 **Log Health** - Track health metrics
- 📚 **Log Learning** - Track learning activities
- ⚡ **Quick Note** - Capture quick notes
- 📊 **Health Stats** - View health statistics

### Voice Commands
All daily operations support voice commands:
- "Log 8500 steps from my morning walk"
- "Add task: Complete project by Friday"
- "Capture idea: New feature for the app"
- "Generate my morning routine"
- "Show today's health stats"

## 📋 Data Storage

All daily operations data is stored in `automation/outputs/`:

- `health_data.json` - Health metrics and statistics
- `learning_data.json` - Learning activities and progress
- `tasks.json` - Task management data
- `quick_notes.json` - Quick notes and ideas
- `morning_routines.json` - Generated morning routines

## 🎯 Best Practices

### Daily Workflow
1. **Morning**: Generate morning routine, log health metrics
2. **Throughout day**: Log learning activities, capture notes, add tasks
3. **Evening**: Review daily summary, plan tomorrow's tasks

### Data Consistency
- Use consistent categories and tags
- Log activities promptly for accurate tracking
- Regular review of data for insights

### Integration
- Leverage cross-script data integration
- Use voice commands for hands-free logging
- Regular backup of data files

---

*Last Updated: 2024-12-19*
*Status: All daily operations scripts fully functional and integrated*
