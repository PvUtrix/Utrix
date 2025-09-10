#!/usr/bin/env python3
"""
Daily Workflow Integration for Tango.Vision Projects
Integrates project tasks with the personal system's daily workflows.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))
from project_manager import TangoVisionProjectManager, TaskStatus

class DailyWorkflowIntegration:
    """Integrates Tango.Vision projects with daily personal workflows"""
    
    def __init__(self, projects_dir: str = None):
        """Initialize the daily workflow integration."""
        self.manager = TangoVisionProjectManager(projects_dir)
        self.personal_system_root = Path(__file__).parent.parent.parent.parent.parent
        self.daily_workflow_file = self.personal_system_root / "core/workflows/daily.md"
        self.automation_outputs = self.personal_system_root / "automation/outputs"
    
    def get_today_tasks(self) -> List[Dict]:
        """Get tasks that should be worked on today."""
        today = datetime.now().date()
        today_tasks = []
        
        for project in self.manager.projects.values():
            for task in project.tasks:
                # Include daily tasks
                if task.daily_task and task.status != TaskStatus.COMPLETED:
                    today_tasks.append({
                        'project_id': project.id,
                        'project_name': project.name,
                        'task_id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'priority': task.priority.value,
                        'status': task.status.value,
                        'type': 'daily',
                        'estimated_hours': task.estimated_hours
                    })
                
                # Include tasks due today
                elif task.due_date:
                    try:
                        due_date = datetime.strptime(task.due_date, '%Y-%m-%d').date()
                        if due_date == today and task.status != TaskStatus.COMPLETED:
                            today_tasks.append({
                                'project_id': project.id,
                                'project_name': project.name,
                                'task_id': task.id,
                                'title': task.title,
                                'description': task.description,
                                'priority': task.priority.value,
                                'status': task.status.value,
                                'type': 'due_today',
                                'estimated_hours': task.estimated_hours
                            })
                    except ValueError:
                        continue
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        today_tasks.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return today_tasks
    
    def generate_daily_summary(self) -> str:
        """Generate a daily summary of project tasks."""
        today_tasks = self.get_today_tasks()
        project_summary = self.manager.get_project_summary()
        
        summary = f"""# Daily Project Summary - {datetime.now().strftime('%Y-%m-%d')}

## Today's Focus
- **Total Projects**: {project_summary['total_projects']}
- **Active Projects**: {project_summary['active_projects']}
- **Tasks for Today**: {len(today_tasks)}
- **Daily Tasks**: {project_summary['daily_tasks']}

## Today's Tasks ({len(today_tasks)})
"""
        
        if today_tasks:
            current_project = None
            for task in today_tasks:
                if task['project_name'] != current_project:
                    current_project = task['project_name']
                    summary += f"\n### {current_project}\n"
                
                priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
                type_emoji = {"daily": "🔄", "due_today": "📅"}.get(task['type'], "📋")
                hours_text = f" ({task['estimated_hours']}h)" if task['estimated_hours'] > 0 else ""
                
                summary += f"- {priority_emoji} {type_emoji} **{task['title']}**{hours_text}\n"
                if task['description']:
                    summary += f"  - {task['description']}\n"
        else:
            summary += "No specific tasks for today. Focus on general project work.\n"
        
        # Add financial overview
        summary += f"""
## Financial Overview
- **Total Budget**: ${project_summary['total_budget']:,.2f}
- **Total Spent**: ${project_summary['total_spent']:,.2f}
- **Remaining**: ${project_summary['total_budget'] - project_summary['total_spent']:,.2f}
- **Revenue Potential**: ${project_summary['total_revenue_potential']:,.2f}

## Quick Actions
- Complete task: `python project_manager.py complete <project_id> <task_id>`
- Add task: `python project_manager.py add-task <project_id> "Task Title"`
- View all projects: `python project_manager.py list`
- Generate report: `python project_manager.py report`
"""
        
        return summary
    
    def save_daily_summary(self) -> str:
        """Save daily summary to automation outputs."""
        summary = self.generate_daily_summary()
        
        # Ensure automation outputs directory exists
        self.automation_outputs.mkdir(parents=True, exist_ok=True)
        
        # Save to daily summaries directory
        daily_summaries_dir = self.automation_outputs / "daily_summaries"
        daily_summaries_dir.mkdir(exist_ok=True)
        
        filename = f"tango_vision_daily_{datetime.now().strftime('%Y%m%d')}.md"
        summary_file = daily_summaries_dir / filename
        
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            return str(summary_file)
        except IOError as e:
            print(f"Error saving daily summary: {e}")
            return ""
    
    def update_personal_daily_workflow(self) -> bool:
        """Update the personal daily workflow with project tasks."""
        if not self.daily_workflow_file.exists():
            print(f"Daily workflow file not found: {self.daily_workflow_file}")
            return False
        
        try:
            # Read current daily workflow
            with open(self.daily_workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if Tango.Vision section already exists
            if "## Tango.Vision Projects" in content:
                # Update existing section
                start_marker = "## Tango.Vision Projects"
                end_marker = "## "
                
                start_idx = content.find(start_marker)
                if start_idx != -1:
                    # Find the end of the Tango.Vision section
                    end_idx = content.find(end_marker, start_idx + len(start_marker))
                    if end_idx == -1:
                        end_idx = len(content)
                    
                    # Replace the section
                    new_section = self._generate_workflow_section()
                    content = content[:start_idx] + new_section + content[end_idx:]
            else:
                # Add new section at the end
                new_section = self._generate_workflow_section()
                content += f"\n{new_section}"
            
            # Write updated content
            with open(self.daily_workflow_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except IOError as e:
            print(f"Error updating daily workflow: {e}")
            return False
    
    def _generate_workflow_section(self) -> str:
        """Generate the Tango.Vision section for daily workflow."""
        today_tasks = self.get_today_tasks()
        daily_tasks = [t for t in today_tasks if t['type'] == 'daily']
        due_today = [t for t in today_tasks if t['type'] == 'due_today']
        
        section = """## Tango.Vision Projects

### Daily Tasks
"""
        
        if daily_tasks:
            for task in daily_tasks:
                priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
                section += f"- {priority_emoji} **{task['project_name']}**: {task['title']}\n"
        else:
            section += "- No daily tasks\n"
        
        if due_today:
            section += "\n### Due Today\n"
            for task in due_today:
                priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
                section += f"- {priority_emoji} **{task['project_name']}**: {task['title']}\n"
        
        section += """
### Quick Commands
- View daily tasks: `python project_manager.py daily`
- Complete task: `python project_manager.py complete <project_id> <task_id>`
- Generate report: `python project_manager.py report`

"""
        
        return section
    
    def sync_with_personal_tasks(self) -> bool:
        """Sync project tasks with the personal task manager."""
        try:
            # Get today's project tasks
            today_tasks = self.get_today_tasks()
            
            # Load personal tasks
            personal_tasks_file = self.automation_outputs / "tasks.json"
            if not personal_tasks_file.exists():
                print("Personal tasks file not found")
                return False
            
            with open(personal_tasks_file, 'r', encoding='utf-8') as f:
                personal_tasks = json.load(f)
            
            # Add project tasks to personal tasks if not already present
            added_count = 0
            for task in today_tasks:
                # Check if task already exists in personal tasks
                task_exists = any(
                    f"[{task['project_name']}]" in t.get('title', '') and 
                    task['title'] in t.get('title', '')
                    for t in personal_tasks
                )
                
                if not task_exists:
                    personal_task = {
                        "id": f"tangovision_{task['task_id']}",
                        "title": f"[{task['project_name']}] {task['title']}",
                        "priority": task['priority'],
                        "status": "pending",
                        "category": "tangovision",
                        "description": task['description'],
                        "created": datetime.now().isoformat(),
                        "due_date": None,
                        "completed": None
                    }
                    personal_tasks.append(personal_task)
                    added_count += 1
            
            # Save updated personal tasks
            if added_count > 0:
                with open(personal_tasks_file, 'w', encoding='utf-8') as f:
                    json.dump(personal_tasks, f, indent=2, ensure_ascii=False)
                print(f"Added {added_count} project tasks to personal task manager")
            
            return True
            
        except Exception as e:
            print(f"Error syncing with personal tasks: {e}")
            return False

def main():
    """Main entry point for daily workflow integration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tango.Vision Daily Workflow Integration")
    parser.add_argument("--projects-dir", help="Projects directory path")
    parser.add_argument("--action", choices=["summary", "sync", "update-workflow", "all"], 
                       default="all", help="Action to perform")
    
    args = parser.parse_args()
    
    integration = DailyWorkflowIntegration(args.projects_dir)
    
    if args.action in ["summary", "all"]:
        print("Generating daily summary...")
        summary_file = integration.save_daily_summary()
        if summary_file:
            print(f"Daily summary saved: {summary_file}")
        
        # Also print to console
        print("\n" + "="*50)
        print(integration.generate_daily_summary())
    
    if args.action in ["sync", "all"]:
        print("Syncing with personal task manager...")
        if integration.sync_with_personal_tasks():
            print("Sync completed successfully")
        else:
            print("Sync failed")
    
    if args.action in ["update-workflow", "all"]:
        print("Updating personal daily workflow...")
        if integration.update_personal_daily_workflow():
            print("Daily workflow updated successfully")
        else:
            print("Failed to update daily workflow")

if __name__ == "__main__":
    main()
