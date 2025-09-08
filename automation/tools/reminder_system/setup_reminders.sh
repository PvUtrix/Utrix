#!/bin/bash

# Setup Reminders for Task Management
# This script helps you set up automatic reminders for your codebase improvement tasks

echo "🔔 Setting up Task Reminders"
echo "=============================="

# Get the project root directory
PROJECT_ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$PROJECT_ROOT"

echo "📁 Project root: $PROJECT_ROOT"

# Create necessary directories
mkdir -p automation/outputs
mkdir -p logs

echo "✅ Created output directories"

# Set up daily reminder
echo ""
echo "📅 Setting up daily task reminder..."
python3 automation/tools/reminder_system/main.py --setup-daily

# Set up weekly reminder
echo ""
echo "📅 Setting up weekly task review reminder..."
python3 automation/tools/reminder_system/main.py --setup-weekly

# Test the reminder system
echo ""
echo "🧪 Testing reminder system..."
python3 automation/tools/reminder_system/main.py --check

echo ""
echo "📋 Current task status:"
python3 automation/tools/task_manager/main.py --list --priority high

echo ""
echo "🎯 Setup Complete!"
echo ""
echo "📝 What was set up:"
echo "   ✅ Daily task check reminder (9:00 AM)"
echo "   ✅ Weekly task review reminder (Monday 10:00 AM)"
echo "   ✅ Reminder system configuration"
echo ""
echo "🚀 Next steps:"
echo "   1. Run daily reminder manually:"
echo "      python3 automation/scripts/daily_task_reminder.py"
echo ""
echo "   2. Check reminder status:"
echo "      python3 automation/tools/reminder_system/main.py --check"
echo ""
echo "   3. Set up cron job (optional):"
echo "      crontab -e"
echo "      # Add this line for daily 9 AM reminder:"
echo "      0 9 * * * cd $PROJECT_ROOT && python3 automation/scripts/daily_task_reminder.py"
echo ""
echo "   4. View reminder report:"
echo "      python3 automation/tools/reminder_system/main.py --report"
echo ""
echo "📁 Files created:"
echo "   - automation/outputs/reminders.json"
echo "   - automation/outputs/notifications.md"
echo "   - automation/outputs/reminder_report.md"
echo ""
echo "💡 Tip: Run 'python3 automation/scripts/daily_task_reminder.py' daily to stay on top of tasks!"
