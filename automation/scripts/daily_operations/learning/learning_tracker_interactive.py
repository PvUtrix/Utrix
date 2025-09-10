#!/usr/bin/env python3
"""
Interactive Learning Tracker for Telegram Bot
Provides a simple interface for tracking learning activities
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class InteractiveLearningTracker:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.data_file = self.data_dir / "learning_data.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump({}, f)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load learning data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save learning data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def log_learning_activity(self, activity_type: str, duration: str, description: str = "", course: str = "", skill: str = "", notes: str = "") -> str:
        """Log a learning activity for today."""
        today = date.today().isoformat()
        data = self._load_data()
        
        if today not in data:
            data[today] = {
                "date": today,
                "activities": [],
                "total_time": 0
            }
        
        # Parse duration (assume minutes if no unit specified)
        try:
            if duration.isdigit():
                duration_minutes = int(duration)
            elif duration.endswith('h'):
                duration_minutes = int(duration[:-1]) * 60
            elif duration.endswith('m'):
                duration_minutes = int(duration[:-1])
            else:
                duration_minutes = int(duration)
        except ValueError:
            duration_minutes = 0
        
        # Create activity entry
        activity = {
            "type": activity_type,
            "duration": duration_minutes,
            "description": description,
            "course": course,
            "skill": skill,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        data[today]["activities"].append(activity)
        data[today]["total_time"] += duration_minutes
        
        self._save_data(data)
        
        # Format response
        response = f"✅ Logged {activity_type}: {duration_minutes} minutes"
        if description:
            response += f"\n📝 Description: {description}"
        if course:
            response += f"\n🎓 Course: {course}"
        if skill:
            response += f"\n💡 Skill: {skill}"
        
        return response
    
    def get_today_stats(self) -> str:
        """Get today's learning statistics."""
        today = date.today().isoformat()
        data = self._load_data()
        
        if today not in data:
            return "📚 **Today's Learning Stats**\n\nNo learning activities logged today.\n\n**Available Activity Types:**\n- reading: Reading books/articles\n- course: Online courses\n- practice: Hands-on practice\n- research: Research and exploration\n- tutorial: Following tutorials\n- project: Working on projects"
        
        today_data = data[today]
        activities = today_data.get("activities", [])
        total_time = today_data.get("total_time", 0)
        
        if not activities:
            return "📚 **Today's Learning Stats**\n\nNo activities logged today."
        
        stats = f"📚 **Today's Learning Stats**\n\n"
        stats += f"⏱️ **Total Time**: {total_time} minutes ({total_time/60:.1f} hours)\n\n"
        stats += f"📋 **Activities** ({len(activities)}):\n"
        
        for activity in activities:
            stats += f"• **{activity['type'].title()}**: {activity['duration']} min"
            if activity.get('description'):
                stats += f" - {activity['description']}"
            stats += "\n"
        
        return stats
    
    def get_available_activities(self) -> str:
        """Get list of available learning activity types."""
        return """📋 **Available Learning Activity Types:**

**Study Activities:**
• reading - Reading books, articles, papers
• course - Online courses, tutorials, lectures
• practice - Hands-on practice, coding, exercises
• research - Research, exploration, investigation

**Project Activities:**
• tutorial - Following step-by-step tutorials
• project - Working on personal projects
• review - Reviewing and consolidating knowledge
• discussion - Discussions, forums, communities

**Example Usage:**
• Log reading: 30m "Python Programming"
• Log course: 45m "Machine Learning Basics"
• Log practice: 60m "Data Structures"
• Log project: 90m "Web App Development"

**Duration Formats:**
• 30 (minutes)
• 30m (minutes)
• 1h (hours)"""

def main():
    """Main entry point for interactive learning tracking."""
    tracker = InteractiveLearningTracker()
    
    if len(sys.argv) < 2:
        # Show available activities and today's stats
        print("📚 **Learning Tracker - Quick Start**\n")
        print(tracker.get_available_activities())
        print("\n" + "="*50 + "\n")
        print(tracker.get_today_stats())
        return
    
    action = sys.argv[1]
    
    if action == "log":
        if len(sys.argv) < 4:
            print("❌ **Usage:** python learning_tracker_interactive.py log <type> <duration> [description] [course] [skill] [notes]")
            print("\n" + tracker.get_available_activities())
            return
        
        activity_type = sys.argv[2]
        duration = sys.argv[3]
        description = sys.argv[4] if len(sys.argv) > 4 else ""
        course = sys.argv[5] if len(sys.argv) > 5 else ""
        skill = sys.argv[6] if len(sys.argv) > 6 else ""
        notes = sys.argv[7] if len(sys.argv) > 7 else ""
        
        result = tracker.log_learning_activity(activity_type, duration, description, course, skill, notes)
        print(result)
        print("\n" + tracker.get_today_stats())
    
    elif action == "today":
        print(tracker.get_today_stats())
    
    elif action == "activities":
        print(tracker.get_available_activities())
    
    else:
        print(f"❌ Unknown action: {action}")
        print("Available actions: log, today, activities")

if __name__ == "__main__":
    main()
