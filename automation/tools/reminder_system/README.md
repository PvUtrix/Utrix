# Reminder System

## Purpose
Automated reminder system to ensure you don't forget to work on codebase improvement tasks and other system maintenance activities.

## Quick Start
```bash
# Set up daily reminders
python3 automation/tools/reminder_system/main.py --setup-daily

# Check for pending reminders
python3 automation/tools/reminder_system/main.py --check

# Send reminder notification
python3 automation/tools/reminder_system/main.py --remind
```

## Configuration
Edit `reminder_config.yaml` to customize reminder settings:
- Reminder frequency and timing
- Notification methods (email, desktop, file)
- Task priority thresholds
- Custom reminder messages

## Usage Examples
```bash
# Set up weekly task review reminder
python3 automation/tools/reminder_system/main.py --setup-weekly --message "Weekly task review due"

# Check overdue tasks
python3 automation/tools/reminder_system/main.py --check-overdue

# Generate reminder report
python3 automation/tools/reminder_system/main.py --report
```

## Troubleshooting
- **Permission errors**: Ensure write access to reminder files
- **Notification failures**: Check system notification settings
- **Schedule conflicts**: Review existing cron jobs or scheduled tasks

## Integration
This tool integrates with the broader system:
- Uses task manager for task data
- Integrates with system scheduling
- Generates reminder reports
- Supports multiple notification methods
