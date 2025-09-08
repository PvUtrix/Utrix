#!/usr/bin/env python3
"""
Task Manager
Simple task management tool for tracking codebase improvement tasks.
"""

import json
import argparse
import logging
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskManager:
    """Manage and track tasks for codebase improvements."""
    
    def __init__(self, tasks_file: str = "automation/outputs/tasks.json"):
        """Initialize the task manager."""
        self.tasks_file = Path(tasks_file)
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict]:
        """Load tasks from file."""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading tasks: {e}")
                return []
        return []
    
    def _save_tasks(self) -> None:
        """Save tasks to file."""
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2, default=str)
        except IOError as e:
            logger.error(f"Error saving tasks: {e}")
    
    def add_task(self, title: str, priority: str = "medium", due_date: Optional[str] = None, 
                 category: str = "improvement", description: str = "") -> str:
        """Add a new task."""
        task_id = f"task_{len(self.tasks) + 1:03d}"
        
        task = {
            "id": task_id,
            "title": title,
            "priority": priority.lower(),
            "status": "pending",
            "category": category,
            "description": description,
            "created": datetime.now().isoformat(),
            "due_date": due_date,
            "completed": None
        }
        
        self.tasks.append(task)
        self._save_tasks()
        
        logger.info(f"Added task: {task_id} - {title}")
        return task_id
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed"] = datetime.now().isoformat()
                self._save_tasks()
                logger.info(f"Completed task: {task_id} - {task['title']}")
                return True
        
        logger.warning(f"Task not found: {task_id}")
        return False
    
    def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, 
                   category: Optional[str] = None) -> List[Dict]:
        """List tasks with optional filtering."""
        filtered_tasks = self.tasks
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status.lower()]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority.lower()]
        
        if category:
            filtered_tasks = [t for t in filtered_tasks if t["category"] == category.lower()]
        
        return filtered_tasks
    
    def get_task_stats(self) -> Dict:
        """Get task statistics."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "completed"])
        pending = len([t for t in self.tasks if t["status"] == "pending"])
        
        priorities = {}
        for task in self.tasks:
            priority = task["priority"]
            priorities[priority] = priorities.get(priority, 0) + 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "by_priority": priorities
        }
    
    def generate_report(self) -> str:
        """Generate a task progress report."""
        stats = self.get_task_stats()
        
        report = ["# Task Progress Report\n"]
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Summary statistics
        report.append("## Summary")
        report.append(f"- **Total Tasks**: {stats['total']}")
        report.append(f"- **Completed**: {stats['completed']}")
        report.append(f"- **Pending**: {stats['pending']}")
        report.append(f"- **Completion Rate**: {stats['completion_rate']:.1f}%\n")
        
        # Tasks by priority
        report.append("## Tasks by Priority")
        for priority, count in stats['by_priority'].items():
            report.append(f"- **{priority.title()}**: {count}")
        report.append("")
        
        # Pending tasks
        pending_tasks = self.list_tasks(status="pending")
        if pending_tasks:
            report.append("## Pending Tasks")
            for task in pending_tasks:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
                report.append(f"- {priority_emoji} **{task['title']}** ({task['priority']})")
                if task.get("due_date"):
                    report.append(f"  - Due: {task['due_date']}")
            report.append("")
        
        # Recent completions
        completed_tasks = [t for t in self.tasks if t["status"] == "completed"]
        if completed_tasks:
            recent_completed = sorted(completed_tasks, key=lambda x: x.get("completed", ""), reverse=True)[:5]
            report.append("## Recent Completions")
            for task in recent_completed:
                completed_date = task.get("completed", "")
                if completed_date:
                    try:
                        date_obj = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))
                        formatted_date = date_obj.strftime('%Y-%m-%d')
                    except:
                        formatted_date = completed_date
                    report.append(f"- ✅ **{task['title']}** (completed {formatted_date})")
            report.append("")
        
        return "\n".join(report)
    
    def save_report(self, output_path: str = "automation/outputs/task_progress_report.md"):
        """Save the task progress report."""
        report = self.generate_report()
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        logger.info(f"Task report saved to {output_path}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Manage codebase improvement tasks")
    parser.add_argument("--add", help="Add a new task")
    parser.add_argument("--complete", help="Mark a task as completed")
    parser.add_argument("--list", action="store_true", help="List tasks")
    parser.add_argument("--status", choices=["pending", "completed"], help="Filter by status")
    parser.add_argument("--priority", choices=["high", "medium", "low"], help="Filter by priority")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--report", action="store_true", help="Generate progress report")
    parser.add_argument("--due", help="Due date for new task (YYYY-MM-DD)")
    parser.add_argument("--description", help="Description for new task")
    
    args = parser.parse_args()
    
    manager = TaskManager()
    
    if args.add:
        task_id = manager.add_task(
            title=args.add,
            priority=args.priority or "medium",
            due_date=args.due,
            description=args.description or ""
        )
        print(f"Added task: {task_id}")
    
    elif args.complete:
        if manager.complete_task(args.complete):
            print(f"Completed task: {args.complete}")
        else:
            print(f"Task not found: {args.complete}")
    
    elif args.list:
        tasks = manager.list_tasks(
            status=args.status,
            priority=args.priority,
            category=args.category
        )
        
        if not tasks:
            print("No tasks found.")
            return
        
        print(f"\nFound {len(tasks)} tasks:")
        for task in tasks:
            status_emoji = "✅" if task["status"] == "completed" else "⏳"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
            print(f"{status_emoji} {priority_emoji} {task['id']}: {task['title']}")
    
    elif args.report:
        report = manager.generate_report()
        print(report)
        manager.save_report()
    
    else:
        # Show summary if no specific action
        stats = manager.get_task_stats()
        print(f"Task Summary: {stats['completed']}/{stats['total']} completed ({stats['completion_rate']:.1f}%)")

if __name__ == "__main__":
    main()
