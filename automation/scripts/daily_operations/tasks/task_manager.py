#!/usr/bin/env python3
"""
Task Manager - Manage personal tasks and todos
Part of the Personal System automation suite.
"""

import json
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class TaskManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.data_file = self.data_dir / "tasks.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load tasks data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict[str, Any]]):
        """Save tasks data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_task_id(self, data: List[Dict[str, Any]]) -> str:
        """Generate a unique task ID."""
        existing_ids = [task.get('id', '') for task in data]
        counter = 1
        while f"task_{counter:04d}" in existing_ids:
            counter += 1
        return f"task_{counter:04d}"
    
    def add_task(self, title: str, description: str = "", priority: str = "medium", 
                due_date: str = "", category: str = "", tags: List[str] = None) -> Dict[str, Any]:
        """Add a new task."""
        data = self._load_data()
        
        task_id = self._generate_task_id(data)
        
        task = {
            'id': task_id,
            'title': title,
            'description': description,
            'priority': priority.lower(),
            'status': 'pending',
            'created_date': date.today().isoformat(),
            'created_timestamp': datetime.now().isoformat(),
            'due_date': due_date,
            'category': category,
            'tags': tags or [],
            'completed_date': None,
            'completed_timestamp': None,
            'notes': []
        }
        
        data.append(task)
        self._save_data(data)
        
        return {
            'success': True,
            'message': f"Task added: {title}",
            'task': task
        }
    
    def complete_task(self, task_id: str, notes: str = "") -> Dict[str, Any]:
        """Mark a task as completed."""
        data = self._load_data()
        
        for task in data:
            if task['id'] == task_id:
                if task['status'] == 'completed':
                    return {
                        'success': False,
                        'message': f"Task {task_id} is already completed"
                    }
                
                task['status'] = 'completed'
                task['completed_date'] = date.today().isoformat()
                task['completed_timestamp'] = datetime.now().isoformat()
                
                if notes:
                    task['notes'].append({
                        'timestamp': datetime.now().isoformat(),
                        'note': notes
                    })
                
                self._save_data(data)
                
                return {
                    'success': True,
                    'message': f"Task completed: {task['title']}",
                    'task': task
                }
        
        return {
            'success': False,
            'message': f"Task {task_id} not found"
        }
    
    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update a task."""
        data = self._load_data()
        
        for task in data:
            if task['id'] == task_id:
                # Update allowed fields
                allowed_fields = ['title', 'description', 'priority', 'due_date', 'category', 'tags']
                for field, value in kwargs.items():
                    if field in allowed_fields:
                        task[field] = value
                
                task['updated_timestamp'] = datetime.now().isoformat()
                self._save_data(data)
                
                return {
                    'success': True,
                    'message': f"Task updated: {task['title']}",
                    'task': task
                }
        
        return {
            'success': False,
            'message': f"Task {task_id} not found"
        }
    
    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        data = self._load_data()
        
        for i, task in enumerate(data):
            if task['id'] == task_id:
                deleted_task = data.pop(i)
                self._save_data(data)
                
                return {
                    'success': True,
                    'message': f"Task deleted: {deleted_task['title']}",
                    'task': deleted_task
                }
        
        return {
            'success': False,
            'message': f"Task {task_id} not found"
        }
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a specific task."""
        data = self._load_data()
        
        for task in data:
            if task['id'] == task_id:
                return {
                    'success': True,
                    'message': f"Task found: {task['title']}",
                    'task': task
                }
        
        return {
            'success': False,
            'message': f"Task {task_id} not found"
        }
    
    def list_tasks(self, status: str = "all", priority: str = "all", 
                  category: str = "all", due_soon: bool = False) -> Dict[str, Any]:
        """List tasks with optional filters."""
        data = self._load_data()
        
        # Apply filters
        filtered_tasks = []
        for task in data:
            # Status filter
            if status != "all" and task['status'] != status:
                continue
            
            # Priority filter
            if priority != "all" and task['priority'] != priority:
                continue
            
            # Category filter
            if category != "all" and task['category'] != category:
                continue
            
            # Due soon filter
            if due_soon and task['due_date']:
                try:
                    due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                    if due_date <= date.today() + timedelta(days=3):
                        filtered_tasks.append(task)
                except ValueError:
                    pass
            else:
                filtered_tasks.append(task)
        
        # Sort by priority and due date
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        filtered_tasks.sort(key=lambda x: (
            priority_order.get(x['priority'], 0),
            x['due_date'] or '9999-12-31'
        ), reverse=True)
        
        # Generate summary
        summary = []
        if filtered_tasks:
            pending_count = sum(1 for task in filtered_tasks if task['status'] == 'pending')
            completed_count = sum(1 for task in filtered_tasks if task['status'] == 'completed')
            
            summary.append(f"📋 Total tasks: {len(filtered_tasks)}")
            summary.append(f"⏳ Pending: {pending_count}")
            summary.append(f"✅ Completed: {completed_count}")
            
            if pending_count > 0:
                high_priority = sum(1 for task in filtered_tasks 
                                  if task['status'] == 'pending' and task['priority'] == 'high')
                if high_priority > 0:
                    summary.append(f"🔴 High priority: {high_priority}")
        else:
            summary.append("📋 No tasks found")
        
        return {
            'success': True,
            'message': f"Tasks list ({len(filtered_tasks)} found)",
            'tasks': filtered_tasks,
            'summary': summary,
            'filters': {
                'status': status,
                'priority': priority,
                'category': category,
                'due_soon': due_soon
            }
        }
    
    def get_today_tasks(self) -> Dict[str, Any]:
        """Get tasks due today or overdue."""
        data = self._load_data()
        today = date.today().isoformat()
        
        today_tasks = []
        overdue_tasks = []
        
        for task in data:
            if task['status'] == 'pending' and task['due_date']:
                if task['due_date'] == today:
                    today_tasks.append(task)
                elif task['due_date'] < today:
                    overdue_tasks.append(task)
        
        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        today_tasks.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        overdue_tasks.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        
        summary = []
        if today_tasks:
            summary.append(f"📅 Due today: {len(today_tasks)}")
        if overdue_tasks:
            summary.append(f"⚠️ Overdue: {len(overdue_tasks)}")
        if not today_tasks and not overdue_tasks:
            summary.append("📅 No tasks due today")
        
        return {
            'success': True,
            'message': "Today's tasks",
            'date': today,
            'today_tasks': today_tasks,
            'overdue_tasks': overdue_tasks,
            'summary': summary
        }
    
    def get_task_stats(self) -> Dict[str, Any]:
        """Get task statistics."""
        data = self._load_data()
        
        if not data:
            return {
                'success': True,
                'message': "No tasks found",
                'stats': {
                    'total': 0,
                    'pending': 0,
                    'completed': 0,
                    'completion_rate': 0
                }
            }
        
        total = len(data)
        pending = sum(1 for task in data if task['status'] == 'pending')
        completed = sum(1 for task in data if task['status'] == 'completed')
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        # Priority breakdown
        priority_stats = {'high': 0, 'medium': 0, 'low': 0}
        for task in data:
            if task['status'] == 'pending':
                priority_stats[task['priority']] += 1
        
        # Category breakdown
        categories = {}
        for task in data:
            category = task.get('category', 'Uncategorized')
            if category not in categories:
                categories[category] = {'pending': 0, 'completed': 0}
            categories[category][task['status']] += 1
        
        # Recent activity (last 7 days)
        recent_completed = 0
        week_ago = (date.today() - timedelta(days=7)).isoformat()
        for task in data:
            if (task['status'] == 'completed' and 
                task.get('completed_date', '') >= week_ago):
                recent_completed += 1
        
        summary = []
        summary.append(f"📊 Total tasks: {total}")
        summary.append(f"⏳ Pending: {pending}")
        summary.append(f"✅ Completed: {completed}")
        summary.append(f"📈 Completion rate: {completion_rate:.1f}%")
        summary.append(f"📅 Completed this week: {recent_completed}")
        
        return {
            'success': True,
            'message': "Task statistics",
            'stats': {
                'total': total,
                'pending': pending,
                'completed': completed,
                'completion_rate': completion_rate,
                'priority_breakdown': priority_stats,
                'category_breakdown': categories,
                'recent_completed': recent_completed
            },
            'summary': summary
        }

def main():
    """Main entry point."""
    manager = TaskManager()
    
    if len(sys.argv) < 2:
        print("Usage: python task_manager.py <action> [args...]")
        print("Actions:")
        print("  add <title> [description] [priority] [due_date] [category] - Add a new task")
        print("  complete <task_id> [notes] - Mark task as completed")
        print("  update <task_id> <field> <value> - Update a task field")
        print("  delete <task_id> - Delete a task")
        print("  get <task_id> - Get a specific task")
        print("  list [status] [priority] [category] [due_soon] - List tasks")
        print("  today - Get today's tasks")
        print("  stats - Get task statistics")
        return
    
    action = sys.argv[1]
    
    if action == "add":
        if len(sys.argv) < 3:
            print("Usage: python task_manager.py add <title> [description] [priority] [due_date] [category]")
            return
        
        title = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        due_date = sys.argv[5] if len(sys.argv) > 5 else ""
        category = sys.argv[6] if len(sys.argv) > 6 else ""
        
        result = manager.add_task(title, description, priority, due_date, category)
        print(json.dumps(result, indent=2))
    
    elif action == "complete":
        if len(sys.argv) < 3:
            print("Usage: python task_manager.py complete <task_id> [notes]")
            return
        
        task_id = sys.argv[2]
        notes = sys.argv[3] if len(sys.argv) > 3 else ""
        
        result = manager.complete_task(task_id, notes)
        print(json.dumps(result, indent=2))
    
    elif action == "update":
        if len(sys.argv) < 5:
            print("Usage: python task_manager.py update <task_id> <field> <value>")
            return
        
        task_id = sys.argv[2]
        field = sys.argv[3]
        value = sys.argv[4]
        
        result = manager.update_task(task_id, **{field: value})
        print(json.dumps(result, indent=2))
    
    elif action == "delete":
        if len(sys.argv) < 3:
            print("Usage: python task_manager.py delete <task_id>")
            return
        
        task_id = sys.argv[2]
        result = manager.delete_task(task_id)
        print(json.dumps(result, indent=2))
    
    elif action == "get":
        if len(sys.argv) < 3:
            print("Usage: python task_manager.py get <task_id>")
            return
        
        task_id = sys.argv[2]
        result = manager.get_task(task_id)
        print(json.dumps(result, indent=2))
    
    elif action == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else "all"
        priority = sys.argv[3] if len(sys.argv) > 3 else "all"
        category = sys.argv[4] if len(sys.argv) > 4 else "all"
        due_soon = sys.argv[5] == "true" if len(sys.argv) > 5 else False
        
        result = manager.list_tasks(status, priority, category, due_soon)
        print(json.dumps(result, indent=2))
    
    elif action == "today":
        result = manager.get_today_tasks()
        print(json.dumps(result, indent=2))
    
    elif action == "stats":
        result = manager.get_task_stats()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
