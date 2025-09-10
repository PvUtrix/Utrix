#!/usr/bin/env python3
"""
ClickUp Integrated Project Manager for Tango.Vision
Combines local project management with ClickUp synchronization.
"""

import json
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))
from project_manager import TangoVisionProjectManager, Priority, ProjectStatus, TaskStatus
from clickup_client import ClickUpClient, ClickUpProjectManager, load_clickup_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClickUpIntegratedManager:
    """Integrated project manager with ClickUp synchronization"""
    
    def __init__(self, projects_dir: str = None, clickup_config_file: str = None):
        """Initialize the integrated manager."""
        self.local_manager = TangoVisionProjectManager(projects_dir)
        
        # Initialize ClickUp integration
        self.clickup_enabled = False
        self.clickup_client = None
        self.clickup_project_manager = None
        self.project_mappings = {}  # Maps local project IDs to ClickUp folder IDs
        
        try:
            config = load_clickup_config(clickup_config_file)
            self.clickup_client = ClickUpClient(config)
            self.clickup_project_manager = ClickUpProjectManager(self.clickup_client)
            self.clickup_enabled = True
            logger.info("ClickUp integration enabled")
        except Exception as e:
            logger.warning(f"ClickUp integration disabled: {e}")
            self.clickup_enabled = False
    
    def create_project(self, name: str, description: str = "", priority: Priority = Priority.MEDIUM,
                      owner: str = "", budget: float = 0.0, revenue_potential: float = 0.0,
                      sync_to_clickup: bool = True) -> str:
        """Create a new project with optional ClickUp synchronization."""
        # Create local project
        project_id = self.local_manager.create_project(
            name=name,
            description=description,
            priority=priority,
            owner=owner,
            budget=budget,
            revenue_potential=revenue_potential
        )
        
        # Sync to ClickUp if enabled
        if self.clickup_enabled and sync_to_clickup:
            try:
                clickup_project = self.clickup_project_manager.create_project_in_clickup(
                    project_name=name,
                    project_description=description
                )
                
                # Store mapping
                self.project_mappings[project_id] = clickup_project['list']['id']
                self._save_project_mappings()
                
                logger.info(f"Project {project_id} synced to ClickUp: {clickup_project['list']['id']}")
                
                # Add financial information as custom fields if available
                if budget > 0 or revenue_potential > 0:
                    self._add_financial_fields_to_clickup(project_id, budget, revenue_potential)
                
            except Exception as e:
                logger.error(f"Failed to sync project to ClickUp: {e}")
                # Continue with local project creation even if ClickUp sync fails
        
        return project_id
    
    def add_task(self, project_id: str, title: str, description: str = "", 
                priority: Priority = Priority.MEDIUM, due_date: Optional[str] = None,
                estimated_hours: float = 0.0, daily_task: bool = False,
                sync_to_clickup: bool = True) -> str:
        """Add a task to a project with optional ClickUp synchronization."""
        # Add task locally
        task_id = self.local_manager.add_task(
            project_id=project_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            estimated_hours=estimated_hours,
            daily_task=daily_task
        )
        
        # Sync to ClickUp if enabled
        if self.clickup_enabled and sync_to_clickup and project_id in self.project_mappings:
            try:
                task_data = {
                    'title': title,
                    'description': description,
                    'priority': priority.value,
                    'due_date': due_date,
                    'estimated_hours': estimated_hours,
                    'daily_task': daily_task
                }
                
                # Add dependencies if the task has them
                dependencies = task_data.get('dependencies', [])
                
                clickup_task = self.clickup_project_manager.sync_task_to_clickup(
                    project_id=project_id,
                    task_data=task_data,
                    dependencies=dependencies
                )
                
                # Store task mapping
                self._store_task_mapping(project_id, task_id, clickup_task['id'])
                
                logger.info(f"Task {task_id} synced to ClickUp: {clickup_task['id']}")
                
            except Exception as e:
                logger.error(f"Failed to sync task to ClickUp: {e}")
                # Continue with local task creation even if ClickUp sync fails
        
        return task_id
    
    def complete_task(self, project_id: str, task_id: str, sync_to_clickup: bool = True) -> bool:
        """Complete a task with optional ClickUp synchronization."""
        # Complete task locally
        success = self.local_manager.complete_task(project_id, task_id)
        
        if success and self.clickup_enabled and sync_to_clickup:
            try:
                # Get ClickUp task ID
                clickup_task_id = self._get_clickup_task_id(project_id, task_id)
                if clickup_task_id:
                    # Update task status in ClickUp
                    self.clickup_client.update_task(clickup_task_id, status="complete")
                    logger.info(f"Task {task_id} marked as complete in ClickUp")
                
            except Exception as e:
                logger.error(f"Failed to sync task completion to ClickUp: {e}")
        
        return success
    
    def upload_document(self, project_id: str, file_path: str, 
                       task_name: str = "Document Upload") -> bool:
        """Upload a document to a project in ClickUp."""
        if not self.clickup_enabled:
            logger.warning("ClickUp integration not enabled")
            return False
        
        if project_id not in self.project_mappings:
            logger.error(f"Project {project_id} not found in ClickUp mappings")
            return False
        
        try:
            result = self.clickup_project_manager.upload_project_document(
                project_id=project_id,
                file_path=file_path,
                task_name=task_name
            )
            logger.info(f"Document uploaded to ClickUp: {result['attachment']['filename']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload document to ClickUp: {e}")
            return False
    
    def add_comment(self, project_id: str, comment: str, 
                   task_name: str = "Project Comment") -> bool:
        """Add a comment to a project in ClickUp."""
        if not self.clickup_enabled:
            logger.warning("ClickUp integration not enabled")
            return False
        
        if project_id not in self.project_mappings:
            logger.error(f"Project {project_id} not found in ClickUp mappings")
            return False
        
        try:
            result = self.clickup_project_manager.add_project_comment(
                project_id=project_id,
                comment=comment,
                task_name=task_name
            )
            logger.info(f"Comment added to ClickUp project: {result['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add comment to ClickUp: {e}")
            return False
    
    def sync_project_to_clickup(self, project_id: str) -> bool:
        """Manually sync an existing project to ClickUp."""
        if not self.clickup_enabled:
            logger.warning("ClickUp integration not enabled")
            return False
        
        if project_id not in self.local_manager.projects:
            logger.error(f"Project {project_id} not found locally")
            return False
        
        try:
            project = self.local_manager.projects[project_id]
            
            # Create project in ClickUp
            clickup_project = self.clickup_project_manager.create_project_in_clickup(
                project_name=project.name,
                project_description=project.description
            )
            
            # Store mapping
            self.project_mappings[project_id] = clickup_project['list']['id']
            self._save_project_mappings()
            
            # Sync all existing tasks
            for task in project.tasks:
                task_data = {
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
                    'due_date': task.due_date,
                    'estimated_hours': task.estimated_hours,
                    'daily_task': task.daily_task
                }
                
                # Add dependencies if the task has them
                dependencies = task_data.get('dependencies', [])
                
                clickup_task = self.clickup_project_manager.sync_task_to_clickup(
                    project_id=project_id,
                    task_data=task_data,
                    dependencies=dependencies
                )
                
                # Store task mapping
                self._store_task_mapping(project_id, task.id, clickup_task['id'])
            
            logger.info(f"Project {project_id} fully synced to ClickUp")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync project to ClickUp: {e}")
            return False
    
    def get_clickup_status(self, project_id: str) -> Optional[Dict]:
        """Get ClickUp status for a project."""
        if not self.clickup_enabled or project_id not in self.project_mappings:
            return None
        
        try:
            return self.clickup_project_manager.get_project_status(project_id)
        except Exception as e:
            logger.error(f"Failed to get ClickUp status: {e}")
            return None
    
    def _add_financial_fields_to_clickup(self, project_id: str, budget: float, revenue_potential: float):
        """Add financial custom fields to ClickUp project."""
        if project_id not in self.project_mappings:
            return
        
        try:
            list_id = self.project_mappings[project_id]
            
            # Create custom fields for financial tracking
            if budget > 0:
                self.clickup_client.create_custom_field(
                    list_id=list_id,
                    name="Budget",
                    field_type="currency"
                )
            
            if revenue_potential > 0:
                self.clickup_client.create_custom_field(
                    list_id=list_id,
                    name="Revenue Potential",
                    field_type="currency"
                )
            
        except Exception as e:
            logger.error(f"Failed to add financial fields to ClickUp: {e}")
    
    def _save_project_mappings(self):
        """Save project mappings to file."""
        mappings_file = Path(__file__).parent / "clickup_mappings.json"
        try:
            with open(mappings_file, 'w') as f:
                json.dump(self.project_mappings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save project mappings: {e}")
    
    def _load_project_mappings(self):
        """Load project mappings from file."""
        mappings_file = Path(__file__).parent / "clickup_mappings.json"
        if mappings_file.exists():
            try:
                with open(mappings_file, 'r') as f:
                    self.project_mappings = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load project mappings: {e}")
                self.project_mappings = {}
    
    def _store_task_mapping(self, project_id: str, local_task_id: str, clickup_task_id: str):
        """Store mapping between local and ClickUp task IDs."""
        mappings_file = Path(__file__).parent / "clickup_task_mappings.json"
        
        try:
            if mappings_file.exists():
                with open(mappings_file, 'r') as f:
                    task_mappings = json.load(f)
            else:
                task_mappings = {}
            
            if project_id not in task_mappings:
                task_mappings[project_id] = {}
            
            task_mappings[project_id][local_task_id] = clickup_task_id
            
            with open(mappings_file, 'w') as f:
                json.dump(task_mappings, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to store task mapping: {e}")
    
    def _get_clickup_task_id(self, project_id: str, local_task_id: str) -> Optional[str]:
        """Get ClickUp task ID for a local task ID."""
        mappings_file = Path(__file__).parent / "clickup_task_mappings.json"
        
        if not mappings_file.exists():
            return None
        
        try:
            with open(mappings_file, 'r') as f:
                task_mappings = json.load(f)
            
            return task_mappings.get(project_id, {}).get(local_task_id)
            
        except Exception as e:
            logger.error(f"Failed to get ClickUp task ID: {e}")
            return None
    
    def generate_integrated_report(self) -> str:
        """Generate a report that includes both local and ClickUp data."""
        local_report = self.local_manager.generate_report()
        
        if not self.clickup_enabled:
            return local_report + "\n\n## ClickUp Integration\n❌ ClickUp integration is disabled"
        
        clickup_section = "\n\n## ClickUp Integration\n✅ ClickUp integration is enabled\n\n"
        
        # Add ClickUp status for each project
        for project_id, project in self.local_manager.projects.items():
            clickup_status = self.get_clickup_status(project_id)
            if clickup_status:
                clickup_section += f"### {project.name} (ClickUp)\n"
                clickup_section += f"- **List ID**: {clickup_status['list_id']}\n"
                clickup_section += f"- **Total Tasks**: {clickup_status['total_tasks']}\n"
                clickup_section += f"- **Completed Tasks**: {clickup_status['completed_tasks']}\n"
                clickup_section += f"- **Pending Tasks**: {clickup_status['pending_tasks']}\n"
                clickup_section += f"- **Completion Rate**: {clickup_status['completion_rate']:.1f}%\n"
                clickup_section += f"- **Priority Breakdown**: Critical: {clickup_status['tasks_by_priority']['critical']}, High: {clickup_status['tasks_by_priority']['high']}, Medium: {clickup_status['tasks_by_priority']['medium']}, Low: {clickup_status['tasks_by_priority']['low']}\n\n"
            else:
                clickup_section += f"### {project.name} (ClickUp)\n❌ Not synced to ClickUp\n\n"
        
        return local_report + clickup_section

def main():
    """Main entry point for integrated manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ClickUp Integrated Project Manager")
    parser.add_argument("--projects-dir", help="Projects directory path")
    parser.add_argument("--clickup-config", help="ClickUp configuration file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create project with ClickUp sync
    create_parser = subparsers.add_parser("create", help="Create a new project with ClickUp sync")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--description", help="Project description")
    create_parser.add_argument("--priority", choices=["critical", "high", "medium", "low"], default="medium")
    create_parser.add_argument("--owner", help="Project owner")
    create_parser.add_argument("--budget", type=float, default=0.0, help="Project budget")
    create_parser.add_argument("--revenue", type=float, default=0.0, help="Revenue potential")
    create_parser.add_argument("--no-sync", action="store_true", help="Don't sync to ClickUp")
    
    # Add task with ClickUp sync
    task_parser = subparsers.add_parser("add-task", help="Add a task with ClickUp sync")
    task_parser.add_argument("project_id", help="Project ID")
    task_parser.add_argument("title", help="Task title")
    task_parser.add_argument("--description", help="Task description")
    task_parser.add_argument("--priority", choices=["critical", "high", "medium", "low"], default="medium")
    task_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    task_parser.add_argument("--hours", type=float, default=0.0, help="Estimated hours")
    task_parser.add_argument("--daily", action="store_true", help="Mark as daily task")
    task_parser.add_argument("--no-sync", action="store_true", help="Don't sync to ClickUp")
    
    # Complete task with ClickUp sync
    complete_parser = subparsers.add_parser("complete", help="Complete a task with ClickUp sync")
    complete_parser.add_argument("project_id", help="Project ID")
    complete_parser.add_argument("task_id", help="Task ID")
    complete_parser.add_argument("--no-sync", action="store_true", help="Don't sync to ClickUp")
    
    # Upload document
    upload_parser = subparsers.add_parser("upload", help="Upload document to ClickUp")
    upload_parser.add_argument("project_id", help="Project ID")
    upload_parser.add_argument("file_path", help="Path to file to upload")
    upload_parser.add_argument("--task-name", help="Task name for the upload")
    
    # Add comment
    comment_parser = subparsers.add_parser("comment", help="Add comment to ClickUp project")
    comment_parser.add_argument("project_id", help="Project ID")
    comment_parser.add_argument("comment", help="Comment text")
    comment_parser.add_argument("--task-name", help="Task name for the comment")
    
    # Sync existing project
    sync_parser = subparsers.add_parser("sync", help="Sync existing project to ClickUp")
    sync_parser.add_argument("project_id", help="Project ID to sync")
    
    # List projects
    list_parser = subparsers.add_parser("list", help="List projects")
    list_parser.add_argument("--status", choices=["planning", "active", "on_hold", "completed", "cancelled"])
    list_parser.add_argument("--priority", choices=["critical", "high", "medium", "low"])
    
    # Daily tasks
    daily_parser = subparsers.add_parser("daily", help="Show daily tasks")
    
    # Report
    report_parser = subparsers.add_parser("report", help="Generate integrated report")
    report_parser.add_argument("--save", help="Save report to file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ClickUpIntegratedManager(args.projects_dir, args.clickup_config)
    
    if args.command == "create":
        priority = Priority(args.priority)
        project_id = manager.create_project(
            name=args.name,
            description=args.description or "",
            priority=priority,
            owner=args.owner or "",
            budget=args.budget,
            revenue_potential=args.revenue,
            sync_to_clickup=not args.no_sync
        )
        print(f"Created project: {project_id}")
    
    elif args.command == "add-task":
        priority = Priority(args.priority)
        task_id = manager.add_task(
            project_id=args.project_id,
            title=args.title,
            description=args.description or "",
            priority=priority,
            due_date=args.due,
            estimated_hours=args.hours,
            daily_task=args.daily,
            sync_to_clickup=not args.no_sync
        )
        if task_id:
            print(f"Added task: {task_id}")
    
    elif args.command == "complete":
        if manager.complete_task(args.project_id, args.task_id, sync_to_clickup=not args.no_sync):
            print(f"Completed task: {args.task_id}")
        else:
            print(f"Task not found: {args.task_id}")
    
    elif args.command == "upload":
        if manager.upload_document(args.project_id, args.file_path, args.task_name):
            print(f"Document uploaded successfully")
        else:
            print(f"Failed to upload document")
    
    elif args.command == "comment":
        if manager.add_comment(args.project_id, args.comment, args.task_name):
            print(f"Comment added successfully")
        else:
            print(f"Failed to add comment")
    
    elif args.command == "sync":
        if manager.sync_project_to_clickup(args.project_id):
            print(f"Project {args.project_id} synced to ClickUp")
        else:
            print(f"Failed to sync project {args.project_id}")
    
    elif args.command == "list":
        status = ProjectStatus(args.status) if args.status else None
        priority = Priority(args.priority) if args.priority else None
        projects = manager.local_manager.list_projects(status=status, priority=priority)
        
        if not projects:
            print("No projects found.")
            return
        
        print(f"\nFound {len(projects)} projects:")
        for project in projects:
            status_emoji = {"planning": "📋", "active": "🚀", "on_hold": "⏸️", "completed": "✅", "cancelled": "❌"}.get(project.status.value, "❓")
            priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(project.priority.value, "⚪")
            clickup_status = "✅" if project.id in manager.project_mappings else "❌"
            print(f"{status_emoji} {priority_emoji} {clickup_status} {project.id}: {project.name}")
    
    elif args.command == "daily":
        daily_tasks = manager.local_manager.get_daily_tasks()
        if not daily_tasks:
            print("No daily tasks found.")
            return
        
        print(f"\nDaily Tasks ({len(daily_tasks)}):")
        for task in daily_tasks:
            priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
            print(f"{priority_emoji} {task['project_name']}: {task['title']}")
    
    elif args.command == "report":
        report = manager.generate_integrated_report()
        print(report)
        if args.save:
            manager.local_manager.save_report(args.save)

if __name__ == "__main__":
    main()
