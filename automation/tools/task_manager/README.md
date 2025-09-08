# Task Manager

## Purpose
A simple task management tool for tracking and managing codebase improvement tasks and other system maintenance activities.

## Quick Start
```bash
# View all tasks
python3 automation/tools/task_manager/main.py --list

# Mark task as completed
python3 automation/tools/task_manager/main.py --complete "Task 1"

# Add new task
python3 automation/tools/task_manager/main.py --add "Fix type hints in daily_summary.py" --priority high

# View tasks by priority
python3 automation/tools/task_manager/main.py --list --priority high
```

## Configuration
Edit `task_manager_config.yaml` to customize task management:
- Task categories and priorities
- Default due dates and reminders
- Integration with external tools
- Reporting and notification settings

## Usage Examples
```bash
# List pending tasks
python3 automation/tools/task_manager/main.py --list --status pending

# Add task with due date
python3 automation/tools/task_manager/main.py --add "Implement unit tests" --priority high --due "2024-12-26"

# Generate progress report
python3 automation/tools/task_manager/main.py --report
```

## Troubleshooting
- **File not found**: Ensure task file exists in automation/outputs/
- **Permission errors**: Check file write permissions
- **Date format errors**: Use YYYY-MM-DD format for dates

## Integration
This tool integrates with the broader system:
- Uses automation/outputs/ for task storage
- Generates reports in markdown format
- Integrates with code quality checker
- Supports automated task creation
