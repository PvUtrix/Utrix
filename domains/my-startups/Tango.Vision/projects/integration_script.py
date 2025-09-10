#!/usr/bin/env python3
"""
Integration Script for Tango.Vision Projects
Sets up integration with the personal system and migrates existing projects.
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))
from project_manager import TangoVisionProjectManager, Priority, ProjectStatus

class IntegrationSetup:
    """Sets up integration between Tango.Vision projects and personal system"""
    
    def __init__(self):
        """Initialize the integration setup."""
        self.projects_dir = Path(__file__).parent
        self.personal_system_root = self.projects_dir.parent.parent.parent.parent.parent
        self.manager = TangoVisionProjectManager()
    
    def setup_directories(self) -> bool:
        """Set up necessary directories for integration."""
        try:
            # Create automation outputs directory if it doesn't exist
            automation_outputs = self.personal_system_root / "automation" / "outputs"
            automation_outputs.mkdir(parents=True, exist_ok=True)
            
            # Create daily summaries directory
            daily_summaries = automation_outputs / "daily_summaries"
            daily_summaries.mkdir(exist_ok=True)
            
            # Create project reports directory
            project_reports = self.projects_dir / "reports"
            project_reports.mkdir(exist_ok=True)
            
            print("✅ Directory structure set up successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up directories: {e}")
            return False
    
    def migrate_existing_project(self, project_path: str) -> bool:
        """Migrate an existing project to the new system."""
        project_path = Path(project_path)
        
        if not project_path.exists():
            print(f"❌ Project path not found: {project_path}")
            return False
        
        try:
            # Extract project name from path
            project_name = project_path.name
            
            # Read existing project structure
            readme_file = project_path / "README.md"
            project_description = ""
            if readme_file.exists():
                with open(readme_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract description from README
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('#'):
                            project_description = line.strip()
                            break
            
            # Create project in the new system
            project_id = self.manager.create_project(
                name=project_name,
                description=project_description or f"Migrated project: {project_name}",
                priority=Priority.MEDIUM,
                owner="System Migration"
            )
            
            # Create project directory structure
            new_project_dir = self.projects_dir / project_id
            new_project_dir.mkdir(exist_ok=True)
            
            # Copy existing files
            for item in project_path.iterdir():
                if item.is_file() and item.name != "README.md":
                    shutil.copy2(item, new_project_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, new_project_dir / item.name, dirs_exist_ok=True)
            
            # Create new README
            new_readme = new_project_dir / "README.md"
            with open(new_readme, 'w', encoding='utf-8') as f:
                f.write(f"""# {project_name}

## Project Overview
- **ID**: {project_id}
- **Migrated**: {datetime.now().strftime('%Y-%m-%d')}
- **Status**: Planning

## Original Structure
This project was migrated from the original structure. Original files have been preserved.

## Integration
This project now integrates with the Tango.Vision project management system.

## Quick Start
1. Review project details: `python project_manager.py list`
2. Add tasks: `python project_manager.py add-task {project_id} "Task Title"`
3. Track progress: `python project_manager.py report`
""")
            
            # Add initial tasks based on existing structure
            self._add_tasks_from_structure(project_id, project_path)
            
            print(f"✅ Successfully migrated project: {project_name} -> {project_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error migrating project: {e}")
            return False
    
    def _add_tasks_from_structure(self, project_id: str, original_path: Path) -> None:
        """Add tasks based on existing project structure."""
        # Look for common task indicators in the structure
        task_indicators = [
            "README.md", "checklist", "todo", "tasks", "plan", "steps"
        ]
        
        tasks_added = 0
        
        # Add tasks for each subdirectory
        for item in original_path.iterdir():
            if item.is_dir():
                # Create a task for each major phase/directory
                task_title = f"Complete {item.name.replace('_', ' ').title()}"
                task_description = f"Work on {item.name} phase of the project"
                
                self.manager.add_task(
                    project_id=project_id,
                    title=task_title,
                    description=task_description,
                    priority=Priority.MEDIUM,
                    estimated_hours=8.0
                )
                tasks_added += 1
        
        # Add a daily task for project review
        self.manager.add_task(
            project_id=project_id,
            title="Daily project review",
            description="Review project progress and update status",
            priority=Priority.MEDIUM,
            daily_task=True,
            estimated_hours=0.5
        )
        tasks_added += 1
        
        print(f"✅ Added {tasks_added} initial tasks to migrated project")
    
    def setup_automation_integration(self) -> bool:
        """Set up automation integration with personal system."""
        try:
            # Create a daily automation script
            daily_script = self.projects_dir / "daily_automation.py"
            with open(daily_script, 'w', encoding='utf-8') as f:
                f.write('''#!/usr/bin/env python3
"""
Daily Automation for Tango.Vision Projects
Run this script daily to sync project tasks with personal system.
"""

import sys
from pathlib import Path

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))
from daily_workflow import DailyWorkflowIntegration

def main():
    """Run daily automation tasks."""
    print("Running Tango.Vision daily automation...")
    
    integration = DailyWorkflowIntegration()
    
    # Generate daily summary
    summary_file = integration.save_daily_summary()
    if summary_file:
        print(f"Daily summary saved: {summary_file}")
    
    # Sync with personal tasks
    if integration.sync_with_personal_tasks():
        print("Synced with personal task manager")
    
    # Update daily workflow
    if integration.update_personal_daily_workflow():
        print("Updated personal daily workflow")
    
    print("Daily automation completed successfully")

if __name__ == "__main__":
    main()
''')
            
            # Make the script executable
            daily_script.chmod(0o755)
            
            # Create a weekly automation script
            weekly_script = self.projects_dir / "weekly_automation.py"
            with open(weekly_script, 'w', encoding='utf-8') as f:
                f.write('''#!/usr/bin/env python3
"""
Weekly Automation for Tango.Vision Projects
Run this script weekly to generate comprehensive reports.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))
from project_manager import TangoVisionProjectManager

def main():
    """Run weekly automation tasks."""
    print("Running Tango.Vision weekly automation...")
    
    manager = TangoVisionProjectManager()
    
    # Generate comprehensive report
    report_file = manager.save_report(f"weekly_report_{datetime.now().strftime('%Y%m%d')}.md")
    if report_file:
        print(f"Weekly report saved: {report_file}")
    
    # Show project summary
    summary = manager.get_project_summary()
    print(f"\\nProject Summary:")
    print(f"- Total Projects: {summary['total_projects']}")
    print(f"- Active Projects: {summary['active_projects']}")
    print(f"- Completion Rate: {summary['completion_rate']:.1f}%")
    print(f"- Total Budget: ${summary['total_budget']:,.2f}")
    print(f"- Total Spent: ${summary['total_spent']:,.2f}")
    
    print("Weekly automation completed successfully")

if __name__ == "__main__":
    main()
''')
            
            # Make the script executable
            weekly_script.chmod(0o755)
            
            print("✅ Automation integration scripts created")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up automation integration: {e}")
            return False
    
    def create_sample_project(self) -> bool:
        """Create a sample project to demonstrate the system."""
        try:
            # Create a sample project
            project_id = self.manager.create_project(
                name="Sample Project",
                description="A sample project to demonstrate the Tango.Vision project management system",
                priority=Priority.MEDIUM,
                owner="System",
                budget=5000.0,
                revenue_potential=15000.0
            )
            
            # Add sample tasks
            sample_tasks = [
                {
                    "title": "Project planning",
                    "description": "Define project scope, timeline, and resources",
                    "priority": Priority.HIGH,
                    "estimated_hours": 16.0
                },
                {
                    "title": "Daily standup",
                    "description": "Daily team sync and progress review",
                    "priority": Priority.MEDIUM,
                    "daily_task": True,
                    "estimated_hours": 0.5
                },
                {
                    "title": "Development phase",
                    "description": "Core development work",
                    "priority": Priority.HIGH,
                    "estimated_hours": 40.0
                },
                {
                    "title": "Testing and QA",
                    "description": "Quality assurance and testing",
                    "priority": Priority.MEDIUM,
                    "estimated_hours": 20.0
                },
                {
                    "title": "Documentation",
                    "description": "Create project documentation",
                    "priority": Priority.LOW,
                    "estimated_hours": 8.0
                }
            ]
            
            for task_data in sample_tasks:
                self.manager.add_task(
                    project_id=project_id,
                    title=task_data["title"],
                    description=task_data["description"],
                    priority=task_data["priority"],
                    estimated_hours=task_data["estimated_hours"],
                    daily_task=task_data.get("daily_task", False)
                )
            
            print(f"✅ Created sample project: {project_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating sample project: {e}")
            return False
    
    def run_full_setup(self) -> bool:
        """Run the complete integration setup."""
        print("🚀 Starting Tango.Vision Project Management Integration Setup")
        print("=" * 60)
        
        success = True
        
        # Step 1: Setup directories
        print("\n1. Setting up directory structure...")
        if not self.setup_directories():
            success = False
        
        # Step 2: Setup automation integration
        print("\n2. Setting up automation integration...")
        if not self.setup_automation_integration():
            success = False
        
        # Step 3: Migrate existing resstrPO project
        print("\n3. Migrating existing resstrPO project...")
        resstrpo_path = self.projects_dir / "resstrPO"
        if resstrpo_path.exists():
            if not self.migrate_existing_project(resstrpo_path):
                success = False
        else:
            print("ℹ️  No existing resstrPO project found to migrate")
        
        # Step 4: Create sample project
        print("\n4. Creating sample project...")
        if not self.create_sample_project():
            success = False
        
        # Step 5: Generate initial report
        print("\n5. Generating initial report...")
        try:
            report_file = self.manager.save_report("integration_setup_report.md")
            if report_file:
                print(f"✅ Initial report saved: {report_file}")
            else:
                success = False
        except Exception as e:
            print(f"❌ Error generating initial report: {e}")
            success = False
        
        # Summary
        print("\n" + "=" * 60)
        if success:
            print("🎉 Integration setup completed successfully!")
            print("\nNext steps:")
            print("1. Review projects: python project_manager.py list")
            print("2. View daily tasks: python project_manager.py daily")
            print("3. Generate report: python project_manager.py report")
            print("4. Run daily automation: python daily_automation.py")
        else:
            print("⚠️  Integration setup completed with some errors")
            print("Please review the error messages above and fix any issues")
        
        return success

def main():
    """Main entry point for integration setup."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tango.Vision Project Management Integration Setup")
    parser.add_argument("--migrate", help="Migrate existing project from path")
    parser.add_argument("--setup-all", action="store_true", help="Run full integration setup")
    
    args = parser.parse_args()
    
    integration = IntegrationSetup()
    
    if args.migrate:
        integration.migrate_existing_project(args.migrate)
    elif args.setup_all:
        integration.run_full_setup()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
