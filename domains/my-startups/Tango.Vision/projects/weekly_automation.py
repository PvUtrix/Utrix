#!/usr/bin/env python3
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
    print(f"\nProject Summary:")
    print(f"- Total Projects: {summary['total_projects']}")
    print(f"- Active Projects: {summary['active_projects']}")
    print(f"- Completion Rate: {summary['completion_rate']:.1f}%")
    print(f"- Total Budget: ${summary['total_budget']:,.2f}")
    print(f"- Total Spent: ${summary['total_spent']:,.2f}")
    
    print("Weekly automation completed successfully")

if __name__ == "__main__":
    main()
