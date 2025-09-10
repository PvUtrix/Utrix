#!/usr/bin/env python3
"""
Tango.Vision Project Manager
Integrated project management system for startup projects with priorities, financial tracking, and daily tasks.
"""

import json
import argparse
import logging
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ProjectStatus(Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

@dataclass
class FinancialMetrics:
    """Financial tracking for projects"""
    budget: float = 0.0
    spent: float = 0.0
    revenue_potential: float = 0.0
    roi_estimate: float = 0.0
    break_even_date: Optional[str] = None
    
    @property
    def remaining_budget(self) -> float:
        return self.budget - self.spent
    
    @property
    def profit_potential(self) -> float:
        return self.revenue_potential - self.spent

@dataclass
class Task:
    """Individual task within a project"""
    id: str
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: str = ""
    due_date: Optional[str] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    created: str = ""
    completed: Optional[str] = None
    daily_task: bool = False
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if not self.created:
            self.created = datetime.now().isoformat()

@dataclass
class Project:
    """Project structure with all necessary components"""
    id: str
    name: str
    description: str = ""
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: Priority = Priority.MEDIUM
    start_date: str = ""
    target_completion: Optional[str] = None
    actual_completion: Optional[str] = None
    owner: str = ""
    team_members: List[str] = None
    financial: FinancialMetrics = None
    tasks: List[Task] = None
    tags: List[str] = None
    created: str = ""
    updated: str = ""
    
    def __post_init__(self):
        if self.team_members is None:
            self.team_members = []
        if self.financial is None:
            self.financial = FinancialMetrics()
        if self.tasks is None:
            self.tasks = []
        if self.tags is None:
            self.tags = []
        if not self.created:
            self.created = datetime.now().isoformat()
        if not self.start_date:
            self.start_date = datetime.now().isoformat()
        self.updated = datetime.now().isoformat()

class TangoVisionProjectManager:
    """Main project manager for Tango.Vision startup projects"""
    
    def __init__(self, projects_dir: str = None):
        """Initialize the project manager."""
        if projects_dir is None:
            # Default to Tango.Vision projects directory
            self.projects_dir = Path(__file__).parent
        else:
            self.projects_dir = Path(projects_dir)
        
        self.projects_file = self.projects_dir / "projects_data.json"
        self.daily_tasks_file = self.projects_dir / "daily_tasks.json"
        self.projects = self._load_projects()
    
    def _load_projects(self) -> Dict[str, Project]:
        """Load projects from file."""
        if self.projects_file.exists():
            try:
                with open(self.projects_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    projects = {}
                    for project_id, project_data in data.items():
                        # Convert dict back to Project object
                        project_data['financial'] = FinancialMetrics(**project_data['financial'])
                        project_data['tasks'] = [Task(**task) for task in project_data['tasks']]
                        project_data['priority'] = Priority(project_data['priority'])
                        project_data['status'] = ProjectStatus(project_data['status'])
                        projects[project_id] = Project(**project_data)
                    return projects
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading projects: {e}")
                return {}
        return {}
    
    def _save_projects(self) -> None:
        """Save projects to file."""
        self.projects_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Convert Project objects to dict for JSON serialization
            data = {}
            for project_id, project in self.projects.items():
                project_dict = asdict(project)
                # Convert enums to strings
                project_dict['priority'] = project.priority.value if hasattr(project.priority, 'value') else str(project.priority)
                project_dict['status'] = project.status.value if hasattr(project.status, 'value') else str(project.status)
                project_dict['financial'] = asdict(project.financial)
                for i, task in enumerate(project.tasks):
                    project_dict['tasks'][i] = asdict(task)
                    project_dict['tasks'][i]['priority'] = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)
                    project_dict['tasks'][i]['status'] = task.status.value if hasattr(task.status, 'value') else str(task.status)
                data[project_id] = project_dict
            
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Error saving projects: {e}")
    
    def create_project(self, name: str, description: str = "", priority: Priority = Priority.MEDIUM,
                      owner: str = "", budget: float = 0.0, revenue_potential: float = 0.0) -> str:
        """Create a new project."""
        project_id = f"proj_{len(self.projects) + 1:03d}_{name.lower().replace(' ', '_')}"
        
        financial = FinancialMetrics(
            budget=budget,
            revenue_potential=revenue_potential
        )
        
        project = Project(
            id=project_id,
            name=name,
            description=description,
            priority=priority,
            owner=owner,
            financial=financial
        )
        
        self.projects[project_id] = project
        self._save_projects()
        
        logger.info(f"Created project: {project_id} - {name}")
        return project_id
    
    def add_task(self, project_id: str, title: str, description: str = "", 
                priority: Priority = Priority.MEDIUM, due_date: Optional[str] = None,
                estimated_hours: float = 0.0, daily_task: bool = False) -> str:
        """Add a task to a project."""
        if project_id not in self.projects:
            logger.error(f"Project not found: {project_id}")
            return ""
        
        project = self.projects[project_id]
        task_id = f"task_{len(project.tasks) + 1:03d}"
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            estimated_hours=estimated_hours,
            daily_task=daily_task
        )
        
        project.tasks.append(task)
        project.updated = datetime.now().isoformat()
        self._save_projects()
        
        logger.info(f"Added task: {task_id} - {title} to project {project_id}")
        return task_id
    
    def complete_task(self, project_id: str, task_id: str) -> bool:
        """Mark a task as completed."""
        if project_id not in self.projects:
            logger.error(f"Project not found: {project_id}")
            return False
        
        project = self.projects[project_id]
        for task in project.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed = datetime.now().isoformat()
                project.updated = datetime.now().isoformat()
                self._save_projects()
                logger.info(f"Completed task: {task_id} - {task.title}")
                return True
        
        logger.warning(f"Task not found: {task_id}")
        return False
    
    def get_daily_tasks(self) -> List[Dict]:
        """Get all daily tasks across all projects."""
        daily_tasks = []
        for project in self.projects.values():
            for task in project.tasks:
                if task.daily_task and task.status != TaskStatus.COMPLETED:
                    # Handle both enum and string priority values
                    priority_value = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)
                    status_value = task.status.value if hasattr(task.status, 'value') else str(task.status)
                    
                    daily_tasks.append({
                        'project_id': project.id,
                        'project_name': project.name,
                        'task_id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'priority': priority_value,
                        'status': status_value,
                        'due_date': task.due_date
                    })
        return daily_tasks
    
    def get_project_summary(self, project_id: str = None) -> Dict:
        """Get summary of project(s)."""
        if project_id:
            if project_id not in self.projects:
                return {}
            projects = [self.projects[project_id]]
        else:
            projects = list(self.projects.values())
        
        summary = {
            'total_projects': len(projects),
            'active_projects': len([p for p in projects if (p.status == ProjectStatus.ACTIVE or (hasattr(p.status, 'value') and p.status.value == 'active') or str(p.status) == 'active')]),
            'total_tasks': sum(len(p.tasks) for p in projects),
            'completed_tasks': sum(len([t for t in p.tasks if (t.status == TaskStatus.COMPLETED or (hasattr(t.status, 'value') and t.status.value == 'completed') or str(t.status) == 'completed')]) for p in projects),
            'daily_tasks': sum(len([t for t in p.tasks if t.daily_task and not (t.status == TaskStatus.COMPLETED or (hasattr(t.status, 'value') and t.status.value == 'completed') or str(t.status) == 'completed')]) for p in projects),
            'total_budget': sum(p.financial.budget for p in projects),
            'total_spent': sum(p.financial.spent for p in projects),
            'total_revenue_potential': sum(p.financial.revenue_potential for p in projects)
        }
        
        if summary['total_tasks'] > 0:
            summary['completion_rate'] = (summary['completed_tasks'] / summary['total_tasks']) * 100
        else:
            summary['completion_rate'] = 0
        
        return summary
    
    def list_projects(self, status: Optional[ProjectStatus] = None, 
                     priority: Optional[Priority] = None) -> List[Project]:
        """List projects with optional filtering."""
        filtered_projects = list(self.projects.values())
        
        if status:
            filtered_projects = [p for p in filtered_projects if p.status == status]
        
        if priority:
            filtered_projects = [p for p in filtered_projects if p.priority == priority]
        
        return filtered_projects
    
    def update_financial(self, project_id: str, spent: float = None, 
                        revenue_potential: float = None) -> bool:
        """Update financial metrics for a project."""
        if project_id not in self.projects:
            logger.error(f"Project not found: {project_id}")
            return False
        
        project = self.projects[project_id]
        
        if spent is not None:
            project.financial.spent = spent
        
        if revenue_potential is not None:
            project.financial.revenue_potential = revenue_potential
        
        project.updated = datetime.now().isoformat()
        self._save_projects()
        
        logger.info(f"Updated financial metrics for project: {project_id}")
        return True
    
    def generate_report(self) -> str:
        """Generate a comprehensive project report."""
        summary = self.get_project_summary()
        daily_tasks = self.get_daily_tasks()
        
        report = f"""# Tango.Vision Project Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Projects**: {summary['total_projects']}
- **Active Projects**: {summary['active_projects']}
- **Total Tasks**: {summary['total_tasks']}
- **Completed Tasks**: {summary['completed_tasks']}
- **Completion Rate**: {summary['completion_rate']:.1f}%
- **Daily Tasks**: {summary['daily_tasks']}

## Financial Overview
- **Total Budget**: ${summary['total_budget']:,.2f}
- **Total Spent**: ${summary['total_spent']:,.2f}
- **Remaining Budget**: ${summary['total_budget'] - summary['total_spent']:,.2f}
- **Revenue Potential**: ${summary['total_revenue_potential']:,.2f}
- **Profit Potential**: ${summary['total_revenue_potential'] - summary['total_spent']:,.2f}

## Daily Tasks ({len(daily_tasks)})
"""
        
        if daily_tasks:
            for task in daily_tasks:
                priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
                report += f"- {priority_emoji} **{task['project_name']}**: {task['title']}\n"
        else:
            report += "No daily tasks found.\n"
        
        report += "\n## Projects\n"
        for project in self.projects.values():
            completed_tasks = len([t for t in project.tasks if t.status == TaskStatus.COMPLETED])
            total_tasks = len(project.tasks)
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            status_emoji = {"planning": "📋", "active": "🚀", "on_hold": "⏸️", "completed": "✅", "cancelled": "❌"}.get(project.status.value, "❓")
            priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(project.priority.value, "⚪")
            
            report += f"""
### {status_emoji} {priority_emoji} {project.name}
- **Status**: {project.status.value.title()}
- **Priority**: {project.priority.value.title()}
- **Tasks**: {completed_tasks}/{total_tasks} ({completion_rate:.1f}%)
- **Budget**: ${project.financial.budget:,.2f}
- **Spent**: ${project.financial.spent:,.2f}
- **Revenue Potential**: ${project.financial.revenue_potential:,.2f}
- **Profit Potential**: ${project.financial.profit_potential:,.2f}
"""
        
        return report
    
    def save_report(self, filename: str = None) -> str:
        """Save the report to a file."""
        if filename is None:
            filename = f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_path = self.projects_dir / filename
        report = self.generate_report()
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Report saved to: {report_path}")
            return str(report_path)
        except IOError as e:
            logger.error(f"Error saving report: {e}")
            return ""

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Tango.Vision Project Manager")
    parser.add_argument("--projects-dir", help="Projects directory path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create project
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--description", help="Project description")
    create_parser.add_argument("--priority", choices=["critical", "high", "medium", "low"], default="medium")
    create_parser.add_argument("--owner", help="Project owner")
    create_parser.add_argument("--budget", type=float, default=0.0, help="Project budget")
    create_parser.add_argument("--revenue", type=float, default=0.0, help="Revenue potential")
    
    # Add task
    task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    task_parser.add_argument("project_id", help="Project ID")
    task_parser.add_argument("title", help="Task title")
    task_parser.add_argument("--description", help="Task description")
    task_parser.add_argument("--priority", choices=["critical", "high", "medium", "low"], default="medium")
    task_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    task_parser.add_argument("--hours", type=float, default=0.0, help="Estimated hours")
    task_parser.add_argument("--daily", action="store_true", help="Mark as daily task")
    
    # Complete task
    complete_parser = subparsers.add_parser("complete", help="Complete a task")
    complete_parser.add_argument("project_id", help="Project ID")
    complete_parser.add_argument("task_id", help="Task ID")
    
    # List projects
    list_parser = subparsers.add_parser("list", help="List projects")
    list_parser.add_argument("--status", choices=["planning", "active", "on_hold", "completed", "cancelled"])
    list_parser.add_argument("--priority", choices=["critical", "high", "medium", "low"])
    
    # Daily tasks
    daily_parser = subparsers.add_parser("daily", help="Show daily tasks")
    
    # Report
    report_parser = subparsers.add_parser("report", help="Generate project report")
    report_parser.add_argument("--save", help="Save report to file")
    
    # Update financial
    financial_parser = subparsers.add_parser("financial", help="Update financial metrics")
    financial_parser.add_argument("project_id", help="Project ID")
    financial_parser.add_argument("--spent", type=float, help="Amount spent")
    financial_parser.add_argument("--revenue", type=float, help="Revenue potential")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = TangoVisionProjectManager(args.projects_dir)
    
    if args.command == "create":
        priority = Priority(args.priority)
        project_id = manager.create_project(
            name=args.name,
            description=args.description or "",
            priority=priority,
            owner=args.owner or "",
            budget=args.budget,
            revenue_potential=args.revenue
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
            daily_task=args.daily
        )
        if task_id:
            print(f"Added task: {task_id}")
    
    elif args.command == "complete":
        if manager.complete_task(args.project_id, args.task_id):
            print(f"Completed task: {args.task_id}")
        else:
            print(f"Task not found: {args.task_id}")
    
    elif args.command == "list":
        status = ProjectStatus(args.status) if args.status else None
        priority = Priority(args.priority) if args.priority else None
        projects = manager.list_projects(status=status, priority=priority)
        
        if not projects:
            print("No projects found.")
            return
        
        print(f"\nFound {len(projects)} projects:")
        for project in projects:
            status_emoji = {"planning": "📋", "active": "🚀", "on_hold": "⏸️", "completed": "✅", "cancelled": "❌"}.get(project.status.value, "❓")
            priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(project.priority.value, "⚪")
            print(f"{status_emoji} {priority_emoji} {project.id}: {project.name}")
    
    elif args.command == "daily":
        daily_tasks = manager.get_daily_tasks()
        if not daily_tasks:
            print("No daily tasks found.")
            return
        
        print(f"\nDaily Tasks ({len(daily_tasks)}):")
        for task in daily_tasks:
            priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
            print(f"{priority_emoji} {task['project_name']}: {task['title']}")
    
    elif args.command == "report":
        report = manager.generate_report()
        print(report)
        if args.save:
            manager.save_report(args.save)
    
    elif args.command == "financial":
        if manager.update_financial(args.project_id, args.spent, args.revenue):
            print(f"Updated financial metrics for project: {args.project_id}")
        else:
            print(f"Project not found: {args.project_id}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
