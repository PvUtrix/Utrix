#!/usr/bin/env python3
"""
Reminder System
Automated reminder system for task management and system maintenance.
"""

import os
import json
import argparse
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReminderSystem:
    """Manage reminders for tasks and system maintenance."""
    
    def __init__(self, config_path: str = "automation/tools/reminder_system/reminder_config.yaml"):
        """Initialize the reminder system."""
        self.config_path = config_path
        self.config = self._load_config()
        self.reminders_file = Path("automation/outputs/reminders.json")
        self.reminders = self._load_reminders()
    
    def _load_config(self) -> Dict:
        """Load reminder configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            return self._get_default_config()
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'reminders': {
                'daily_task_check': {
                    'enabled': True,
                    'time': '09:00',
                    'message': 'Daily task check - review and update progress',
                    'command': 'python3 automation/tools/task_manager/main.py --list --priority high'
                },
                'weekly_review': {
                    'enabled': True,
                    'day': 'monday',
                    'time': '10:00',
                    'message': 'Weekly task review - generate progress report',
                    'command': 'python3 automation/tools/task_manager/main.py --report'
                },
                'overdue_tasks': {
                    'enabled': True,
                    'check_interval_hours': 24,
                    'message': 'You have overdue tasks that need attention'
                }
            },
            'notifications': {
                'desktop': True,
                'file': True,
                'email': False
            },
            'task_thresholds': {
                'high_priority_pending': 2,
                'overdue_days': 7
            }
        }
    
    def _load_reminders(self) -> List[Dict]:
        """Load existing reminders."""
        if self.reminders_file.exists():
            try:
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading reminders: {e}")
                return []
        return []
    
    def _save_reminders(self) -> None:
        """Save reminders to file."""
        self.reminders_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f, indent=2, default=str)
        except IOError as e:
            logger.error(f"Error saving reminders: {e}")
    
    def add_reminder(self, title: str, message: str, due_date: str, 
                    priority: str = "medium", reminder_type: str = "task") -> str:
        """Add a new reminder."""
        reminder_id = f"reminder_{len(self.reminders) + 1:03d}"
        
        reminder = {
            "id": reminder_id,
            "title": title,
            "message": message,
            "due_date": due_date,
            "priority": priority,
            "type": reminder_type,
            "created": datetime.now().isoformat(),
            "completed": None,
            "notified": False
        }
        
        self.reminders.append(reminder)
        self._save_reminders()
        
        logger.info(f"Added reminder: {reminder_id} - {title}")
        return reminder_id
    
    def check_overdue_reminders(self) -> List[Dict]:
        """Check for overdue reminders."""
        overdue = []
        now = datetime.now()
        
        for reminder in self.reminders:
            if reminder.get("completed"):
                continue
            
            try:
                due_date = datetime.fromisoformat(reminder["due_date"])
                if now > due_date:
                    overdue.append(reminder)
            except ValueError:
                logger.warning(f"Invalid due date format: {reminder['due_date']}")
        
        return overdue
    
    def check_pending_tasks(self) -> Dict:
        """Check for pending high-priority tasks."""
        try:
            # Import task manager
            import sys
            task_manager_path = Path(__file__).parent.parent / "task_manager"
            sys.path.append(str(task_manager_path))
            
            from main import TaskManager
            manager = TaskManager()
            
            high_priority_tasks = manager.list_tasks(status="pending", priority="high")
            stats = manager.get_task_stats()
            
            return {
                "high_priority_pending": len(high_priority_tasks),
                "total_pending": stats["pending"],
                "completion_rate": stats["completion_rate"],
                "tasks": high_priority_tasks
            }
        except Exception as e:
            logger.error(f"Error checking tasks: {e}")
            return {"error": str(e)}
    
    def send_notification(self, title: str, message: str, priority: str = "medium") -> bool:
        """Send notification using available methods."""
        success = True
        
        # Desktop notification
        if self.config.get('notifications', {}).get('desktop', True):
            try:
                self._send_desktop_notification(title, message)
            except Exception as e:
                logger.error(f"Desktop notification failed: {e}")
                success = False
        
        # File notification
        if self.config.get('notifications', {}).get('file', True):
            try:
                self._save_notification_to_file(title, message, priority)
            except Exception as e:
                logger.error(f"File notification failed: {e}")
                success = False
        
        return success
    
    def _send_desktop_notification(self, title: str, message: str) -> None:
        """Send desktop notification."""
        try:
            # Try different notification methods based on OS
            if os.name == 'posix':  # macOS/Linux
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "{message}" with title "{title}"'
                ], check=True, capture_output=True)
            else:  # Windows
                # You could implement Windows toast notifications here
                logger.info(f"Desktop notification: {title} - {message}")
        except subprocess.CalledProcessError:
            # Fallback to simple print
            logger.info(f"NOTIFICATION: {title} - {message}")
    
    def _save_notification_to_file(self, title: str, message: str, priority: str) -> None:
        """Save notification to file."""
        notification_file = Path("automation/outputs/notifications.md")
        notification_file.parent.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
        
        notification = f"""
## {priority_emoji} {title}
**Time**: {timestamp}  
**Priority**: {priority}  
**Message**: {message}

---
"""
        
        # Append to file
        with open(notification_file, 'a') as f:
            f.write(notification)
    
    def setup_daily_reminder(self) -> str:
        """Set up daily task check reminder."""
        tomorrow = datetime.now() + timedelta(days=1)
        due_date = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return self.add_reminder(
            title="Daily Task Check",
            message="Review high-priority tasks and update progress",
            due_date=due_date.isoformat(),
            priority="high",
            reminder_type="daily"
        )
    
    def setup_weekly_reminder(self) -> str:
        """Set up weekly task review reminder."""
        # Find next Monday
        today = datetime.now()
        days_ahead = 0 - today.weekday()  # Monday is 0
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        next_monday = today + timedelta(days=days_ahead)
        due_date = next_monday.replace(hour=10, minute=0, second=0, microsecond=0)
        
        return self.add_reminder(
            title="Weekly Task Review",
            message="Generate progress report and plan next week's tasks",
            due_date=due_date.isoformat(),
            priority="medium",
            reminder_type="weekly"
        )
    
    def check_and_notify(self) -> None:
        """Check for overdue reminders and pending tasks, then notify."""
        # Check overdue reminders
        overdue = self.check_overdue_reminders()
        if overdue:
            for reminder in overdue:
                self.send_notification(
                    title=f"Overdue: {reminder['title']}",
                    message=reminder['message'],
                    priority=reminder['priority']
                )
                reminder['notified'] = True
        
        # Check pending high-priority tasks
        task_info = self.check_pending_tasks()
        if not task_info.get('error'):
            high_priority_count = task_info.get('high_priority_pending', 0)
            threshold = self.config.get('task_thresholds', {}).get('high_priority_pending', 2)
            
            if high_priority_count >= threshold:
                self.send_notification(
                    title="High Priority Tasks Pending",
                    message=f"You have {high_priority_count} high-priority tasks pending. Consider reviewing them soon.",
                    priority="high"
                )
        
        self._save_reminders()
    
    def generate_reminder_report(self) -> str:
        """Generate a reminder status report."""
        overdue = self.check_overdue_reminders()
        task_info = self.check_pending_tasks()
        
        report = ["# Reminder System Report\n"]
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Overdue reminders
        if overdue:
            report.append("## 🔴 Overdue Reminders")
            for reminder in overdue:
                report.append(f"- **{reminder['title']}**: {reminder['message']}")
            report.append("")
        else:
            report.append("## ✅ No Overdue Reminders\n")
        
        # Task status
        if not task_info.get('error'):
            report.append("## 📋 Task Status")
            report.append(f"- **High Priority Pending**: {task_info.get('high_priority_pending', 0)}")
            report.append(f"- **Total Pending**: {task_info.get('total_pending', 0)}")
            report.append(f"- **Completion Rate**: {task_info.get('completion_rate', 0):.1f}%\n")
        
        # Upcoming reminders
        upcoming = []
        now = datetime.now()
        for reminder in self.reminders:
            if reminder.get("completed"):
                continue
            try:
                due_date = datetime.fromisoformat(reminder["due_date"])
                if due_date > now:
                    upcoming.append((due_date, reminder))
            except ValueError:
                continue
        
        if upcoming:
            upcoming.sort(key=lambda x: x[0])
            report.append("## 📅 Upcoming Reminders")
            for due_date, reminder in upcoming[:5]:  # Show next 5
                report.append(f"- **{reminder['title']}**: {due_date.strftime('%Y-%m-%d %H:%M')}")
            report.append("")
        
        return "\n".join(report)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Manage reminders for tasks and system maintenance")
    parser.add_argument("--setup-daily", action="store_true", help="Set up daily task check reminder")
    parser.add_argument("--setup-weekly", action="store_true", help="Set up weekly task review reminder")
    parser.add_argument("--check", action="store_true", help="Check for overdue reminders and pending tasks")
    parser.add_argument("--remind", action="store_true", help="Send reminder notifications")
    parser.add_argument("--report", action="store_true", help="Generate reminder report")
    parser.add_argument("--add", help="Add a custom reminder")
    parser.add_argument("--message", help="Reminder message")
    parser.add_argument("--due", help="Due date (YYYY-MM-DD HH:MM)")
    parser.add_argument("--priority", choices=["high", "medium", "low"], default="medium", help="Reminder priority")
    
    args = parser.parse_args()
    
    reminder_system = ReminderSystem()
    
    if args.setup_daily:
        reminder_id = reminder_system.setup_daily_reminder()
        print(f"Daily reminder set up: {reminder_id}")
    
    elif args.setup_weekly:
        reminder_id = reminder_system.setup_weekly_reminder()
        print(f"Weekly reminder set up: {reminder_id}")
    
    elif args.check:
        overdue = reminder_system.check_overdue_reminders()
        task_info = reminder_system.check_pending_tasks()
        
        print(f"Overdue reminders: {len(overdue)}")
        if not task_info.get('error'):
            print(f"High priority tasks pending: {task_info.get('high_priority_pending', 0)}")
    
    elif args.remind:
        reminder_system.check_and_notify()
        print("Reminder notifications sent")
    
    elif args.report:
        report = reminder_system.generate_reminder_report()
        print(report)
        
        # Save report
        report_file = Path("automation/outputs/reminder_report.md")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {report_file}")
    
    elif args.add:
        if not args.due:
            print("Error: --due date required when adding reminder")
            return
        
        reminder_id = reminder_system.add_reminder(
            title=args.add,
            message=args.message or "Custom reminder",
            due_date=args.due,
            priority=args.priority
        )
        print(f"Added reminder: {reminder_id}")
    
    else:
        # Show status
        overdue = reminder_system.check_overdue_reminders()
        task_info = reminder_system.check_pending_tasks()
        
        print(f"Reminder System Status:")
        print(f"- Overdue reminders: {len(overdue)}")
        if not task_info.get('error'):
            print(f"- High priority tasks: {task_info.get('high_priority_pending', 0)}")
            print(f"- Completion rate: {task_info.get('completion_rate', 0):.1f}%")

if __name__ == "__main__":
    main()
