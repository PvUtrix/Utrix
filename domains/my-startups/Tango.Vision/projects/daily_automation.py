#!/usr/bin/env python3
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
