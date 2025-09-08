#!/usr/bin/env python3
"""
Team Automation Script
Automates team management processes for the startup
"""

import yaml
import json
from datetime import datetime
from pathlib import Path

class TeamAutomation:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.team_dir = Path("automation/team")
        self.team_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_communication(self):
        """Set up automated team communication"""
        print("Setting up team communication...")
        
        # Create communication configuration
        comm_config = {
            "daily_standup": {
                "enabled": True,
                "time": "09:00",
                "questions": [
                    "What did you accomplish yesterday?",
                    "What are you working on today?",
                    "Any blockers or challenges?",
                    "How can the team help?"
                ],
                "automation": {
                    "reminder": True,
                    "summary_generation": True,
                    "follow_up": True
                }
            },
            "team_coordination": {
                "enabled": True,
                "channels": ["slack", "teams", "email"],
                "automation": {
                    "task_assignment": True,
                    "progress_tracking": True,
                    "meeting_scheduling": True
                }
            }
        }
        
        # Save configuration
        with open(self.team_dir / "communication-config.json", 'w') as f:
            json.dump(comm_config, f, indent=2)
        
        print("Team communication configured")
    
    def setup_performance_management(self):
        """Set up automated performance management"""
        print("Setting up performance management...")
        
        # Create performance management configuration
        perf_config = {
            "goal_setting": {
                "enabled": True,
                "frequency": "quarterly",
                "automation": {
                    "goal_tracking": True,
                    "progress_monitoring": True,
                    "reminder_notifications": True
                }
            },
            "performance_reviews": {
                "enabled": True,
                "frequency": "quarterly",
                "automation": {
                    "review_scheduling": True,
                    "feedback_collection": True,
                    "report_generation": True
                }
            },
            "recognition": {
                "enabled": True,
                "automation": {
                    "achievement_tracking": True,
                    "recognition_notifications": True,
                    "reward_management": True
                }
            }
        }
        
        # Save configuration
        with open(self.team_dir / "performance-config.json", 'w') as f:
            json.dump(perf_config, f, indent=2)
        
        print("Performance management configured")
    
    def setup_task_management(self):
        """Set up automated task management"""
        print("Setting up task management...")
        
        # Create task management configuration
        task_config = {
            "task_assignment": {
                "enabled": True,
                "rules": [
                    "skill_based_assignment",
                    "workload_balancing",
                    "availability_checking",
                    "deadline_consideration"
                ]
            },
            "progress_tracking": {
                "enabled": True,
                "automation": {
                    "status_updates": True,
                    "milestone_tracking": True,
                    "deadline_monitoring": True
                }
            },
            "workload_balancing": {
                "enabled": True,
                "algorithms": [
                    "capacity_planning",
                    "skill_matching",
                    "priority_balancing",
                    "deadline_optimization"
                ]
            }
        }
        
        # Save configuration
        with open(self.team_dir / "task-management-config.json", 'w') as f:
            json.dump(task_config, f, indent=2)
        
        print("Task management configured")
    
    def run_automation(self):
        """Run team automation setup"""
        print("Setting up team automation...")
        
        self.setup_communication()
        self.setup_performance_management()
        self.setup_task_management()
        
        print("Team automation setup completed!")

def main():
    """Main function"""
    automation = TeamAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main()
