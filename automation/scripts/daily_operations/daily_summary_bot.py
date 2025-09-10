#!/usr/bin/env python3
# Daily Summary Generator for Telegram Bot
# Non-interactive version that generates summary without user input
# 
# IMPORTANT: This script follows the "No Fake Data" policy.
# All metrics must come from real sources or manual input.

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class DailySummaryBotGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.today = datetime.now()
        self.summary_data = {
            "date": self.today.strftime("%Y-%m-%d"),
            "sections": {},
            "reflections": {}
        }
    
    def collect_health_data(self) -> Dict[str, Any]:
        """Collect health metrics for the day from existing data files."""
        try:
            # Check for existing health data
            health_file = self.base_path / "automation" / "outputs" / "health_data.json"
            if health_file.exists():
                with open(health_file, 'r') as f:
                    health_data = json.load(f)
                    # Get today's data
                    today_str = self.today.strftime("%Y-%m-%d")
                    if today_str in health_data:
                        return health_data[today_str]
            
            # Check for health logs in the system
            health_logs_dir = self.base_path / "automation" / "outputs" / "health_logs"
            if health_logs_dir.exists():
                today_file = health_logs_dir / f"health_{self.today.strftime('%Y%m%d')}.json"
                if today_file.exists():
                    with open(today_file, 'r') as f:
                        return json.load(f)
            
            return None
        except Exception as e:
            print(f"Error collecting health data: {e}")
            return None
    
    def collect_learning_data(self) -> Dict[str, Any]:
        """Collect learning progress from existing data files."""
        try:
            # Check for learning data
            learning_file = self.base_path / "automation" / "outputs" / "learning_data.json"
            if learning_file.exists():
                with open(learning_file, 'r') as f:
                    learning_data = json.load(f)
                    today_str = self.today.strftime("%Y-%m-%d")
                    if today_str in learning_data:
                        return learning_data[today_str]
            
            return None
        except Exception as e:
            print(f"Error collecting learning data: {e}")
            return None
    
    def collect_task_data(self) -> Dict[str, Any]:
        """Collect task completion data."""
        try:
            # Check for task data
            task_file = self.base_path / "automation" / "outputs" / "tasks.json"
            if task_file.exists():
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                    # Get today's tasks
                    today_str = self.today.strftime("%Y-%m-%d")
                    today_tasks = [task for task in task_data.get('tasks', []) 
                                 if task.get('date') == today_str]
                    if today_tasks:
                        return {
                            "total_tasks": len(today_tasks),
                            "completed_tasks": len([t for t in today_tasks if t.get('completed', False)]),
                            "tasks": today_tasks
                        }
            
            return None
        except Exception as e:
            print(f"Error collecting task data: {e}")
            return None
    
    def collect_shadow_work_data(self) -> Dict[str, Any]:
        """Collect shadow work data."""
        try:
            # Check for shadow work data
            shadow_file = self.base_path / "automation" / "outputs" / "shadow_work_data.json"
            if shadow_file.exists():
                with open(shadow_file, 'r') as f:
                    shadow_data = json.load(f)
                    today_str = self.today.strftime("%Y-%m-%d")
                    today_entries = [entry for entry in shadow_data.get('entries', []) 
                                   if entry.get('date') == today_str]
                    if today_entries:
                        return {
                            "entries_count": len(today_entries),
                            "entries": today_entries
                        }
            
            return None
        except Exception as e:
            print(f"Error collecting shadow work data: {e}")
            return None
    
    def create_summary(self) -> str:
        """Create the complete daily summary."""
        # Collect all data
        self.summary_data["sections"]["health"] = self.collect_health_data()
        self.summary_data["sections"]["learning"] = self.collect_learning_data()
        self.summary_data["sections"]["tasks"] = self.collect_task_data()
        self.summary_data["sections"]["shadow_work"] = self.collect_shadow_work_data()
        
        # Check if we have any real data
        has_real_data = any(
            data is not None for data in self.summary_data['sections'].values()
        )
        
        # Create summary header (Telegram-friendly format)
        summary_parts = [f"Daily Summary - {self.today.strftime('%B %d, %Y')}\n"]
        
        if not has_real_data:
            summary_parts.extend([
                "No Data Available",
                "",
                "No tracked data found for today. Start logging to see your daily summary!",
                "",
                "Quick Actions:",
                "- Use /log_health to track health metrics",
                "- Use /log_learning to track learning progress", 
                "- Use /add_task to add tasks",
                "- Use /quick_note to capture thoughts",
                "",
                "Reflection Prompts:",
                "- What was your biggest win today?",
                "- What challenged you the most?",
                "- What are you grateful for?",
                "- What will you do differently tomorrow?"
            ])
        else:
            # Format available data
            if self.summary_data['sections']['health']:
                health_data = self.summary_data['sections']['health']
                summary_parts.extend([
                    "Health & Wellness",
                    f"- Steps: {health_data.get('steps', 'Not tracked')}",
                    f"- Sleep: {health_data.get('sleep', 'Not tracked')} hours",
                    f"- Water: {health_data.get('water', 'Not tracked')} glasses",
                    f"- Mood: {health_data.get('mood', 'Not tracked')}",
                    ""
                ])
            
            if self.summary_data['sections']['learning']:
                learning_data = self.summary_data['sections']['learning']
                summary_parts.extend([
                    "Learning & Growth",
                    f"- Study Time: {learning_data.get('study_time', 'Not tracked')} minutes",
                    f"- Topics: {', '.join(learning_data.get('topics', [])) if learning_data.get('topics') else 'Not tracked'}",
                    f"- Progress: {learning_data.get('progress', 'Not tracked')}",
                    ""
                ])
            
            if self.summary_data['sections']['tasks']:
                task_data = self.summary_data['sections']['tasks']
                completed = task_data.get('completed_tasks', 0)
                total = task_data.get('total_tasks', 0)
                summary_parts.extend([
                    "Tasks & Productivity",
                    f"- Completed: {completed}/{total} tasks",
                    f"- Completion Rate: {(completed/total*100):.1f}%" if total > 0 else "- Completion Rate: 0%",
                    ""
                ])
            
            if self.summary_data['sections']['shadow_work']:
                shadow_data = self.summary_data['sections']['shadow_work']
                summary_parts.extend([
                    "Shadow Work",
                    f"- Entries: {shadow_data.get('entries_count', 0)} insights captured",
                    ""
                ])
            
            summary_parts.extend([
                "Reflection Prompts:",
                "- What was your biggest win today?",
                "- What challenged you the most?", 
                "- What are you grateful for?",
                "- What will you do differently tomorrow?"
            ])
        
        summary_parts.extend([
            "",
            f"---",
            f"Generated at {datetime.now().strftime('%H:%M')} | Next summary in 24 hours"
        ])
        
        return "\n".join(summary_parts)
    
    def save_summary(self, summary: str):
        """Save the summary to file."""
        try:
            # Create output directory
            output_dir = self.base_path / "automation" / "outputs" / "daily_summaries"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save markdown file
            filename = f"summary_{self.today.strftime('%Y%m%d')}.md"
            filepath = output_dir / filename
            filepath.write_text(summary, encoding='utf-8')
            
            # Save JSON data
            json_filename = f"data_{self.today.strftime('%Y%m%d')}.json"
            json_filepath = output_dir / json_filename
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(self.summary_data, f, indent=2, default=str, ensure_ascii=False)
            
            print(f"✅ Summary saved to {filepath}")
            print(f"📊 Data saved to {json_filepath}")
        except Exception as e:
            print(f"Error saving summary: {e}")

def main():
    """Main function for bot execution."""
    try:
        generator = DailySummaryBotGenerator()
        summary = generator.create_summary()
        
        # Save the summary
        generator.save_summary(summary)
        
        # Print the summary (this will be captured by the bot)
        print(summary)
        
    except Exception as e:
        error_msg = f"Error generating daily summary: {e}"
        print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
