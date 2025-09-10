#!/usr/bin/env python3
"""
Interactive Task Manager for Telegram Bot
Provides a simple interface for managing tasks
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class InteractiveTaskManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.data_file = self.data_dir / "tasks.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump({"tasks": [], "next_id": 1}, f)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load task data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"tasks": [], "next_id": 1}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save task data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_task(self, title: str, description: str = "", priority: str = "medium", due_date: str = "", category: str = "") -> str:
        """Add a new task."""
        data = self._load_data()
        
        task = {
            "id": data["next_id"],
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "category": category,
            "status": "pending",
            "created": datetime.now().isoformat(),
            "completed": None
        }
        
        data["tasks"].append(task)
        data["next_id"] += 1
        
        self._save_data(data)
        
        response = f"✅ **Task Added**\n\n"
        response += f"📋 **Title**: {title}\n"
        if description:
            response += f"📝 **Description**: {description}\n"
        response += f"⚡ **Priority**: {priority.title()}\n"
        if due_date:
            response += f"📅 **Due Date**: {due_date}\n"
        if category:
            response += f"🏷️ **Category**: {category}\n"
        response += f"🆔 **ID**: {task['id']}"
        
        return response
    
    def list_tasks(self, status: str = "all") -> str:
        """List tasks with optional status filter."""
        data = self._load_data()
        tasks = data.get("tasks", [])
        
        if not tasks:
            return "📋 **Task List**\n\nNo tasks found.\n\n**Priority Levels:**\n- low: Low priority\n- medium: Medium priority (default)\n- high: High priority\n- urgent: Urgent priority"
        
        # Filter tasks by status
        if status != "all":
            tasks = [task for task in tasks if task.get("status") == status]
        
        if not tasks:
            return f"📋 **Task List** ({status.title()})\n\nNo {status} tasks found."
        
        # Sort by priority and creation date
        priority_order = {"urgent": 4, "high": 3, "medium": 2, "low": 1}
        tasks.sort(key=lambda x: (priority_order.get(x.get("priority", "medium"), 2), x.get("created", "")), reverse=True)
        
        response = f"📋 **Task List** ({len(tasks)} tasks)\n\n"
        
        for task in tasks:
            status_emoji = "✅" if task.get("status") == "completed" else "⏳"
            priority_emoji = {"urgent": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get("priority", "medium"), "🟡")
            
            response += f"{status_emoji} **{task['title']}** {priority_emoji}\n"
            response += f"   🆔 ID: {task['id']} | Status: {task['status'].title()}\n"
            if task.get("due_date"):
                response += f"   📅 Due: {task['due_date']}\n"
            if task.get("category"):
                response += f"   🏷️ Category: {task['category']}\n"
            response += "\n"
        
        return response
    
    def get_task_stats(self) -> str:
        """Get task statistics."""
        data = self._load_data()
        tasks = data.get("tasks", [])
        
        if not tasks:
            return "📊 **Task Statistics**\n\nNo tasks found."
        
        total = len(tasks)
        completed = len([t for t in tasks if t.get("status") == "completed"])
        pending = total - completed
        
        # Priority breakdown
        priorities = {"urgent": 0, "high": 0, "medium": 0, "low": 0}
        for task in tasks:
            if task.get("status") != "completed":
                priority = task.get("priority", "medium")
                priorities[priority] += 1
        
        response = f"📊 **Task Statistics**\n\n"
        response += f"📋 **Total Tasks**: {total}\n"
        response += f"✅ **Completed**: {completed} ({completed/total*100:.1f}%)\n"
        response += f"⏳ **Pending**: {pending} ({pending/total*100:.1f}%)\n\n"
        response += f"⚡ **Priority Breakdown:**\n"
        response += f"🚨 Urgent: {priorities['urgent']}\n"
        response += f"🔴 High: {priorities['high']}\n"
        response += f"🟡 Medium: {priorities['medium']}\n"
        response += f"🟢 Low: {priorities['low']}"
        
        return response
    
    def get_help(self) -> str:
        """Get help information."""
        return """📋 **Task Manager Help**

**Adding Tasks:**
• python task_manager_interactive.py add "Task Title" [description] [priority] [due_date] [category]

**Priority Levels:**
• low - Low priority (green)
• medium - Medium priority (yellow, default)
• high - High priority (red)
• urgent - Urgent priority (red with alert)

**Due Date Format:**
• today, tomorrow
• 2024-12-25 (YYYY-MM-DD)
• in 3 days, next week

**Categories:**
• work, personal, health, learning, finance, etc.

**Examples:**
• Add simple task: "Buy groceries"
• Add detailed task: "Complete project" "Finish the report" "high" "tomorrow" "work"
• Add urgent task: "Fix bug" "Critical issue" "urgent" "today" "work"

**Available Commands:**
• add - Add a new task
• list - List all tasks
• pending - List pending tasks
• completed - List completed tasks
• stats - Show task statistics"""

def main():
    """Main entry point for interactive task management."""
    manager = InteractiveTaskManager()
    
    if len(sys.argv) < 2:
        # Show help and current stats
        print("📋 **Task Manager - Quick Start**\n")
        print(manager.get_help())
        print("\n" + "="*50 + "\n")
        print(manager.get_task_stats())
        return
    
    action = sys.argv[1]
    
    if action == "add":
        if len(sys.argv) < 3:
            print("❌ **Usage:** python task_manager_interactive.py add <title> [description] [priority] [due_date] [category]")
            print("\n" + manager.get_help())
            return
        
        title = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        due_date = sys.argv[5] if len(sys.argv) > 5 else ""
        category = sys.argv[6] if len(sys.argv) > 6 else ""
        
        result = manager.add_task(title, description, priority, due_date, category)
        print(result)
        print("\n" + manager.get_task_stats())
    
    elif action == "list":
        print(manager.list_tasks("all"))
    
    elif action == "pending":
        print(manager.list_tasks("pending"))
    
    elif action == "completed":
        print(manager.list_tasks("completed"))
    
    elif action == "stats":
        print(manager.get_task_stats())
    
    elif action == "help":
        print(manager.get_help())
    
    else:
        print(f"❌ Unknown action: {action}")
        print("Available actions: add, list, pending, completed, stats, help")

if __name__ == "__main__":
    main()
