#!/usr/bin/env python3
"""
Project Creation Script for Tango.Vision
Interactive script to create new projects with proper structure and integration.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))
from project_manager import TangoVisionProjectManager, Priority, ProjectStatus

def get_user_input(prompt: str, default: str = "", required: bool = True) -> str:
    """Get user input with optional default value."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        value = input(full_prompt).strip()
        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("This field is required. Please enter a value.")

def get_choice(prompt: str, choices: List[str], default: str = "") -> str:
    """Get user choice from a list of options."""
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, 1):
        marker = " (default)" if choice == default else ""
        print(f"{i}. {choice}{marker}")
    
    while True:
        try:
            choice_input = input(f"Enter choice (1-{len(choices)}): ").strip()
            if not choice_input and default:
                return default
            
            choice_num = int(choice_input)
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print("Please enter a valid number")

def get_priority() -> Priority:
    """Get project priority from user."""
    priorities = ["critical", "high", "medium", "low"]
    choice = get_choice("Select project priority:", priorities, "medium")
    return Priority(choice)

def get_financial_info() -> Dict:
    """Get financial information from user."""
    print("\n=== Financial Information ===")
    
    budget = 0.0
    try:
        budget_input = get_user_input("Project budget ($)", "0", False)
        budget = float(budget_input) if budget_input else 0.0
    except ValueError:
        print("Invalid budget amount, using 0")
    
    revenue_potential = 0.0
    try:
        revenue_input = get_user_input("Revenue potential ($)", "0", False)
        revenue_potential = float(revenue_input) if revenue_input else 0.0
    except ValueError:
        print("Invalid revenue amount, using 0")
    
    return {
        "budget": budget,
        "revenue_potential": revenue_potential
    }

def get_initial_tasks() -> List[Dict]:
    """Get initial tasks from user."""
    print("\n=== Initial Tasks ===")
    tasks = []
    
    add_tasks = get_user_input("Add initial tasks? (y/n)", "y", False).lower() == 'y'
    
    if add_tasks:
        while True:
            print(f"\nTask {len(tasks) + 1}:")
            title = get_user_input("Task title", "", False)
            if not title:
                break
            
            description = get_user_input("Task description", "", False)
            priority = get_choice("Task priority:", ["critical", "high", "medium", "low"], "medium")
            
            daily_task = get_user_input("Is this a daily task? (y/n)", "n", False).lower() == 'y'
            
            estimated_hours = 0.0
            try:
                hours_input = get_user_input("Estimated hours", "0", False)
                estimated_hours = float(hours_input) if hours_input else 0.0
            except ValueError:
                print("Invalid hours, using 0")
            
            due_date = get_user_input("Due date (YYYY-MM-DD)", "", False)
            
            task = {
                "title": title,
                "description": description,
                "priority": priority,
                "daily_task": daily_task,
                "estimated_hours": estimated_hours,
                "due_date": due_date if due_date else None
            }
            
            tasks.append(task)
            
            add_more = get_user_input("Add another task? (y/n)", "n", False).lower() == 'y'
            if not add_more:
                break
    
    return tasks

def create_project_directory(project_id: str, project_name: str) -> Path:
    """Create project directory structure."""
    project_dir = Path(__file__).parent / project_id
    project_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    subdirs = [
        "docs",
        "tasks",
        "financial",
        "reports",
        "assets"
    ]
    
    for subdir in subdirs:
        (project_dir / subdir).mkdir(exist_ok=True)
    
    # Create README.md
    readme_content = f"""# {project_name}

## Project Overview
- **ID**: {project_id}
- **Created**: {datetime.now().strftime('%Y-%m-%d')}
- **Status**: Planning

## Directory Structure
- `docs/` - Project documentation
- `tasks/` - Task-related files
- `financial/` - Financial tracking and reports
- `reports/` - Progress and status reports
- `assets/` - Project assets and resources

## Quick Start
1. Review project details in the project manager
2. Check daily tasks: `python project_manager.py daily`
3. Update progress regularly
4. Generate reports: `python project_manager.py report`

## Integration
This project integrates with the Tango.Vision project management system and your personal automation workflows.
"""
    
    with open(project_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    return project_dir

def create_project_config(project_id: str, project_data: Dict) -> None:
    """Create project configuration file."""
    config_file = Path(__file__).parent / project_id / "project_config.yaml"
    
    config = {
        "project": {
            "id": project_id,
            "name": project_data["name"],
            "description": project_data["description"],
            "priority": project_data["priority"],
            "owner": project_data["owner"],
            "created": datetime.now().isoformat()
        },
        "integration": {
            "personal_system": True,
            "daily_workflows": True,
            "automation": True
        },
        "settings": {
            "auto_sync": True,
            "daily_reminders": True,
            "weekly_reports": True
        }
    }
    
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

def main():
    """Main project creation workflow."""
    print("=== Tango.Vision Project Creator ===\n")
    
    # Initialize project manager
    manager = TangoVisionProjectManager()
    
    # Get basic project information
    print("=== Project Information ===")
    name = get_user_input("Project name")
    description = get_user_input("Project description", "", False)
    priority = get_priority()
    owner = get_user_input("Project owner", "", False)
    
    # Get financial information
    financial = get_financial_info()
    
    # Create the project
    print(f"\nCreating project: {name}")
    project_id = manager.create_project(
        name=name,
        description=description,
        priority=priority,
        owner=owner,
        budget=financial["budget"],
        revenue_potential=financial["revenue_potential"]
    )
    
    # Create project directory structure
    project_dir = create_project_directory(project_id, name)
    print(f"Created project directory: {project_dir}")
    
    # Create project configuration
    create_project_config(project_id, {
        "name": name,
        "description": description,
        "priority": priority.value,
        "owner": owner
    })
    
    # Add initial tasks
    initial_tasks = get_initial_tasks()
    for task_data in initial_tasks:
        task_id = manager.add_task(
            project_id=project_id,
            title=task_data["title"],
            description=task_data["description"],
            priority=Priority(task_data["priority"]),
            due_date=task_data["due_date"],
            estimated_hours=task_data["estimated_hours"],
            daily_task=task_data["daily_task"]
        )
        print(f"Added task: {task_id} - {task_data['title']}")
    
    # Generate initial report
    print(f"\n=== Project Created Successfully ===")
    print(f"Project ID: {project_id}")
    print(f"Project Name: {name}")
    print(f"Priority: {priority.value}")
    print(f"Budget: ${financial['budget']:,.2f}")
    print(f"Revenue Potential: ${financial['revenue_potential']:,.2f}")
    print(f"Initial Tasks: {len(initial_tasks)}")
    
    # Show next steps
    print(f"\n=== Next Steps ===")
    print(f"1. View project: python project_manager.py list")
    print(f"2. Check daily tasks: python project_manager.py daily")
    print(f"3. Generate report: python project_manager.py report")
    print(f"4. Add more tasks: python project_manager.py add-task {project_id} 'Task Title'")
    print(f"5. Update financials: python project_manager.py financial {project_id} --spent 1000")
    
    # Save initial report
    report_file = manager.save_report(f"{project_id}_initial_report.md")
    if report_file:
        print(f"6. Initial report saved: {report_file}")

if __name__ == "__main__":
    main()
