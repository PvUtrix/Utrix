#!/usr/bin/env python3
"""
Daily Task Reminder
Simple script to check for pending high-priority tasks and send reminders.
This can be run manually or scheduled as a cron job.
"""

import sys
import logging
from pathlib import Path

# Add task manager to path
task_manager_path = Path(__file__).parent.parent / "tools" / "task_manager"
sys.path.append(str(task_manager_path))

from main import TaskManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_remind():
    """Check for pending tasks and send reminder if needed."""
    try:
        manager = TaskManager()
        
        # Get high priority pending tasks
        high_priority_tasks = manager.list_tasks(status="pending", priority="high")
        
        if high_priority_tasks:
            print(f"\n🔴 HIGH PRIORITY TASKS PENDING: {len(high_priority_tasks)}")
            print("=" * 50)
            
            for task in high_priority_tasks:
                print(f"⏳ {task['id']}: {task['title']}")
                if task.get('description'):
                    print(f"   {task['description'][:100]}...")
            
            print("\n💡 Quick Actions:")
            print("   python3 automation/tools/task_manager/main.py --list --priority high")
            print("   python3 automation/tools/task_manager/main.py --complete task_XXX")
            print("   python3 automation/tools/task_manager/main.py --report")
            
            return True
        else:
            print("✅ No high priority tasks pending!")
            return False
            
    except Exception as e:
        logger.error(f"Error checking tasks: {e}")
        return False

if __name__ == "__main__":
    has_pending = check_and_remind()
    
    if has_pending:
        # Exit with code 1 to indicate there are pending tasks
        # This can be used by cron jobs or other automation
        sys.exit(1)
    else:
        sys.exit(0)
