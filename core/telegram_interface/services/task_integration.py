#!/usr/bin/env python3
"""
Task Integration Service
Integrates with various task management systems to provide top priority tasks
"""

import json
import logging
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

logger = logging.getLogger(__name__)

class TaskIntegrationService:
    """Service to integrate with task management systems and get top priority tasks."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Task data sources
        self.task_sources = [
            self._get_automation_tasks,
            self._get_startup_tasks,
            self._get_general_tasks
        ]
    
    def get_top_3_tasks(self) -> Dict[str, Any]:
        """Get the top 3 priority tasks for today."""
        try:
            all_tasks = []
            
            # Collect tasks from all sources
            for source_func in self.task_sources:
                try:
                    tasks = source_func()
                    if tasks:
                        all_tasks.extend(tasks)
                except Exception as e:
                    self.logger.warning(f"Failed to get tasks from {source_func.__name__}: {e}")
            
            if not all_tasks:
                return {
                    'success': True,
                    'message': 'No tasks found',
                    'tasks': [],
                    'count': 0
                }
            
            # Sort by priority and select top 3
            priority_order = {'high': 3, 'medium': 2, 'low': 1, 'urgent': 4, 'critical': 5}
            all_tasks.sort(key=lambda x: priority_order.get(x.get('priority', 'low').lower(), 0), reverse=True)
            
            top_3_tasks = all_tasks[:3]
            
            return {
                'success': True,
                'message': f'Top {len(top_3_tasks)} priority tasks',
                'tasks': top_3_tasks,
                'count': len(top_3_tasks),
                'total_available': len(all_tasks)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting top 3 tasks: {e}")
            return {
                'success': False,
                'message': f'Error getting tasks: {str(e)}',
                'tasks': [],
                'count': 0
            }
    
    def _get_automation_tasks(self) -> List[Dict[str, Any]]:
        """Get tasks from automation task manager."""
        try:
            tasks_file = project_root / "automation" / "outputs" / "tasks.json"
            self.logger.info(f"Looking for automation tasks at: {tasks_file}")
            
            if not tasks_file.exists():
                self.logger.warning(f"Automation tasks file does not exist: {tasks_file}")
                return []
            
            with open(tasks_file, 'r') as f:
                tasks = json.load(f)
            
            self.logger.info(f"Loaded {len(tasks)} tasks from automation file")
            
            # Filter for pending tasks
            pending_tasks = [task for task in tasks if task.get('status') == 'pending']
            self.logger.info(f"Found {len(pending_tasks)} pending tasks")
            
            # Add source information
            for task in pending_tasks:
                task['source'] = 'automation'
                task['category'] = task.get('category', 'improvement')
            
            return pending_tasks
            
        except Exception as e:
            self.logger.error(f"Error loading automation tasks: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return []
    
    def _get_startup_tasks(self) -> List[Dict[str, Any]]:
        """Get tasks from startup project manager."""
        try:
            # Look for startup project files
            startup_dir = project_root / "domains" / "my-startups"
            if not startup_dir.exists():
                return []
            
            tasks = []
            
            # Check for Tango.Vision project tasks
            tango_dir = startup_dir / "Tango.Vision" / "projects"
            if tango_dir.exists():
                # Look for project files
                for project_file in tango_dir.glob("*.json"):
                    try:
                        with open(project_file, 'r') as f:
                            project_data = json.load(f)
                        
                        # Extract tasks from project
                        if 'tasks' in project_data:
                            for task in project_data['tasks']:
                                if task.get('status') != 'completed':
                                    task['source'] = 'startup'
                                    task['project'] = project_data.get('name', 'Unknown Project')
                                    tasks.append(task)
                    except Exception as e:
                        self.logger.warning(f"Error loading project {project_file}: {e}")
            
            return tasks
            
        except Exception as e:
            self.logger.warning(f"Error loading startup tasks: {e}")
            return []
    
    def _get_general_tasks(self) -> List[Dict[str, Any]]:
        """Get general tasks from various sources."""
        try:
            tasks = []
            
            # Check for daily operations tasks
            daily_tasks_file = project_root / "automation" / "scripts" / "daily_operations" / "outputs" / "tasks.json"
            if daily_tasks_file.exists():
                with open(daily_tasks_file, 'r') as f:
                    daily_tasks = json.load(f)
                
                for task in daily_tasks:
                    if task.get('status') == 'pending':
                        task['source'] = 'daily_operations'
                        tasks.append(task)
            
            # Check for health tracking tasks
            health_file = project_root / "automation" / "outputs" / "health_data.json"
            if health_file.exists():
                try:
                    with open(health_file, 'r') as f:
                        health_data = json.load(f)
                    
                    # Add health-related tasks if any
                    if 'pending_tasks' in health_data:
                        for task in health_data['pending_tasks']:
                            task['source'] = 'health'
                            task['category'] = 'health'
                            tasks.append(task)
                except:
                    pass
            
            return tasks
            
        except Exception as e:
            self.logger.warning(f"Error loading general tasks: {e}")
            return []
    
    def format_tasks_for_morning_routine(self, tasks: List[Dict[str, Any]]) -> str:
        """Format tasks for inclusion in morning routine message."""
        if not tasks:
            return "📝 **No priority tasks found for today**\n\nTake this opportunity to plan your day or work on long-term goals!"
        
        formatted_tasks = ["📝 **Your Top 3 Priority Tasks Today:**\n"]
        
        for i, task in enumerate(tasks, 1):
            priority_emoji = {
                'high': '🔴', 'urgent': '🚨', 'critical': '⚡',
                'medium': '🟡', 'low': '🟢'
            }.get(task.get('priority', 'medium').lower(), '⚪')
            
            title = task.get('title', 'Untitled Task')
            category = task.get('category', 'general')
            source = task.get('source', 'unknown')
            
            # Format task with priority and category
            task_line = f"**{i}.** {priority_emoji} **{title}**"
            
            # Add category if not generic
            if category not in ['general', 'improvement']:
                task_line += f" *({category})*"
            
            # Add due date if available
            if task.get('due_date'):
                task_line += f" - Due: {task['due_date']}"
            
            formatted_tasks.append(task_line)
        
        # Add motivational message
        formatted_tasks.append(f"\n💪 **Focus on these {len(tasks)} tasks today to make progress toward your goals!**")
        
        return "\n".join(formatted_tasks)
    
    def get_task_summary(self) -> str:
        """Get a brief summary of all available tasks."""
        try:
            all_tasks = []
            for source_func in self.task_sources:
                try:
                    tasks = source_func()
                    if tasks:
                        all_tasks.extend(tasks)
                except:
                    pass
            
            if not all_tasks:
                return "📊 **Task Summary:** No tasks found"
            
            # Count by priority
            priority_counts = {}
            for task in all_tasks:
                priority = task.get('priority', 'low').lower()
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            summary_parts = ["📊 **Task Summary:**"]
            for priority in ['critical', 'urgent', 'high', 'medium', 'low']:
                count = priority_counts.get(priority, 0)
                if count > 0:
                    emoji = {'critical': '⚡', 'urgent': '🚨', 'high': '🔴', 'medium': '🟡', 'low': '🟢'}[priority]
                    summary_parts.append(f"{emoji} {priority.title()}: {count}")
            
            return " | ".join(summary_parts)
            
        except Exception as e:
            return f"📊 **Task Summary:** Error loading tasks ({str(e)})"


# Global instance
task_service = None

def initialize_task_service(config: Dict[str, Any] = None):
    """Initialize the global task service."""
    global task_service
    task_service = TaskIntegrationService(config)

def get_top_3_tasks() -> Dict[str, Any]:
    """Get top 3 tasks using the global service."""
    global task_service
    if not task_service:
        task_service = TaskIntegrationService()
    return task_service.get_top_3_tasks()

def format_tasks_for_morning_routine(tasks: List[Dict[str, Any]]) -> str:
    """Format tasks for morning routine using the global service."""
    global task_service
    if not task_service:
        task_service = TaskIntegrationService()
    return task_service.format_tasks_for_morning_routine(tasks)
