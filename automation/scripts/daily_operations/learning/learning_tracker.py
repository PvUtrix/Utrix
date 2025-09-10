#!/usr/bin/env python3
"""
Learning Tracker - Track and manage learning activities
Part of the Personal System automation suite.
"""

import json
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class LearningTracker:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.data_file = self.data_dir / "learning_data.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load learning data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict[str, Any]]):
        """Save learning data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_today_entry(self, data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Get today's learning entry."""
        today = date.today().isoformat()
        for entry in data:
            if entry.get('date') == today:
                return entry
        return None
    
    def log_activity(self, activity_type: str, duration: float, description: str = "", 
                    course: str = "", skill: str = "", notes: str = "") -> Dict[str, Any]:
        """Log a learning activity for today."""
        data = self._load_data()
        today = date.today().isoformat()
        
        # Get or create today's entry
        today_entry = self._get_today_entry(data)
        if not today_entry:
            today_entry = {
                'date': today,
                'timestamp': datetime.now().isoformat(),
                'activities': [],
                'total_time': 0,
                'notes': []
            }
            data.append(today_entry)
        
        # Create activity entry
        activity = {
            'type': activity_type,
            'duration': duration,
            'description': description,
            'course': course,
            'skill': skill,
            'timestamp': datetime.now().isoformat(),
            'notes': notes
        }
        
        today_entry['activities'].append(activity)
        today_entry['total_time'] += duration
        
        # Add note if provided
        if notes:
            today_entry['notes'].append({
                'timestamp': datetime.now().isoformat(),
                'note': notes
            })
        
        self._save_data(data)
        
        return {
            'success': True,
            'message': f"Logged {activity_type}: {duration} minutes",
            'date': today,
            'activity': activity,
            'total_time_today': today_entry['total_time']
        }
    
    def get_today_stats(self) -> Dict[str, Any]:
        """Get today's learning statistics."""
        data = self._load_data()
        today_entry = self._get_today_entry(data)
        
        if not today_entry:
            return {
                'success': True,
                'message': "No learning activities logged today",
                'date': date.today().isoformat(),
                'total_time': 0,
                'activities': [],
                'summary': "Start your learning journey today!"
            }
        
        activities = today_entry.get('activities', [])
        total_time = today_entry.get('total_time', 0)
        
        # Calculate summary
        summary = []
        if total_time > 0:
            hours = total_time / 60
            if hours >= 2:
                summary.append(f"🎓 Excellent learning day: {hours:.1f} hours")
            elif hours >= 1:
                summary.append(f"📚 Good learning progress: {hours:.1f} hours")
            else:
                summary.append(f"📖 Learning time: {total_time} minutes")
        
        # Group by activity type
        activity_types = {}
        for activity in activities:
            activity_type = activity['type']
            if activity_type not in activity_types:
                activity_types[activity_type] = {'count': 0, 'total_time': 0}
            activity_types[activity_type]['count'] += 1
            activity_types[activity_type]['total_time'] += activity['duration']
        
        # Add activity type summaries
        for activity_type, stats in activity_types.items():
            count = stats['count']
            time = stats['total_time']
            summary.append(f"📝 {activity_type.title()}: {count} sessions, {time} min")
        
        return {
            'success': True,
            'message': "Today's learning summary",
            'date': today_entry['date'],
            'total_time': total_time,
            'activities': activities,
            'activity_types': activity_types,
            'summary': summary,
            'notes': today_entry.get('notes', [])
        }
    
    def get_weekly_stats(self) -> Dict[str, Any]:
        """Get weekly learning statistics."""
        data = self._load_data()
        today = date.today()
        
        # Get last 7 days
        weekly_data = []
        for i in range(7):
            check_date = (today - timedelta(days=i)).isoformat()
            for entry in data:
                if entry.get('date') == check_date:
                    weekly_data.append(entry)
                    break
        
        if not weekly_data:
            return {
                'success': True,
                'message': "No learning data for the past week",
                'period': '7 days',
                'summary': "Start logging your learning activities!"
            }
        
        # Calculate totals
        total_time = sum(entry.get('total_time', 0) for entry in weekly_data)
        total_activities = sum(len(entry.get('activities', [])) for entry in weekly_data)
        
        # Group by activity type
        activity_types = {}
        for entry in weekly_data:
            for activity in entry.get('activities', []):
                activity_type = activity['type']
                if activity_type not in activity_types:
                    activity_types[activity_type] = {'count': 0, 'total_time': 0}
                activity_types[activity_type]['count'] += 1
                activity_types[activity_type]['total_time'] += activity['duration']
        
        # Generate summary
        summary = []
        if total_time > 0:
            avg_daily = total_time / len(weekly_data)
            summary.append(f"📊 Weekly total: {total_time/60:.1f} hours")
            summary.append(f"📈 Daily average: {avg_daily:.0f} minutes")
        
        summary.append(f"📚 Total activities: {total_activities}")
        
        for activity_type, stats in activity_types.items():
            count = stats['count']
            time = stats['total_time']
            summary.append(f"📝 {activity_type.title()}: {count} sessions, {time/60:.1f}h")
        
        return {
            'success': True,
            'message': "Weekly learning summary",
            'period': '7 days',
            'total_time': total_time,
            'total_activities': total_activities,
            'activity_types': activity_types,
            'summary': summary,
            'days_logged': len(weekly_data)
        }
    
    def get_course_progress(self, course_name: str = "") -> Dict[str, Any]:
        """Get progress for a specific course or all courses."""
        data = self._load_data()
        
        if course_name:
            # Get progress for specific course
            course_activities = []
            for entry in data:
                for activity in entry.get('activities', []):
                    if activity.get('course', '').lower() == course_name.lower():
                        course_activities.append({
                            'date': entry['date'],
                            'activity': activity
                        })
            
            if not course_activities:
                return {
                    'success': True,
                    'message': f"No activities found for course: {course_name}",
                    'course': course_name
                }
            
            total_time = sum(activity['activity']['duration'] for activity in course_activities)
            total_sessions = len(course_activities)
            
            return {
                'success': True,
                'message': f"Progress for {course_name}",
                'course': course_name,
                'total_time': total_time,
                'total_sessions': total_sessions,
                'activities': course_activities
            }
        else:
            # Get progress for all courses
            courses = {}
            for entry in data:
                for activity in entry.get('activities', []):
                    course = activity.get('course', 'General Learning')
                    if course not in courses:
                        courses[course] = {'total_time': 0, 'sessions': 0, 'last_activity': None}
                    
                    courses[course]['total_time'] += activity['duration']
                    courses[course]['sessions'] += 1
                    courses[course]['last_activity'] = entry['date']
            
            return {
                'success': True,
                'message': "All courses progress",
                'courses': courses
            }
    
    def list_activity_types(self) -> Dict[str, Any]:
        """List all available activity types."""
        return {
            'success': True,
            'message': "Available learning activity types",
            'activity_types': {
                'reading': 'Reading books, articles, documentation',
                'video': 'Watching educational videos, tutorials',
                'course': 'Taking online courses, classes',
                'practice': 'Hands-on practice, coding, exercises',
                'research': 'Research, investigation, analysis',
                'writing': 'Writing notes, documentation, essays',
                'discussion': 'Group discussions, forums, Q&A',
                'project': 'Working on projects, assignments',
                'review': 'Reviewing, studying, revision',
                'experiment': 'Experimentation, testing, exploration'
            }
        }

def main():
    """Main entry point."""
    tracker = LearningTracker()
    
    if len(sys.argv) < 2:
        print("Usage: python learning_tracker.py <action> [args...]")
        print("Actions:")
        print("  log <type> <duration> [description] [course] [skill] [notes] - Log learning activity")
        print("  today - Get today's learning stats")
        print("  weekly - Get weekly learning stats")
        print("  course [course_name] - Get course progress")
        print("  list - List available activity types")
        return
    
    action = sys.argv[1]
    
    if action == "log":
        if len(sys.argv) < 4:
            print("Usage: python learning_tracker.py log <type> <duration> [description] [course] [skill] [notes]")
            return
        
        activity_type = sys.argv[2]
        try:
            duration = float(sys.argv[3])
        except ValueError:
            print("Error: duration must be a number (minutes)")
            return
        
        description = sys.argv[4] if len(sys.argv) > 4 else ""
        course = sys.argv[5] if len(sys.argv) > 5 else ""
        skill = sys.argv[6] if len(sys.argv) > 6 else ""
        notes = sys.argv[7] if len(sys.argv) > 7 else ""
        
        result = tracker.log_activity(activity_type, duration, description, course, skill, notes)
        print(json.dumps(result, indent=2))
    
    elif action == "today":
        result = tracker.get_today_stats()
        print(json.dumps(result, indent=2))
    
    elif action == "weekly":
        result = tracker.get_weekly_stats()
        print(json.dumps(result, indent=2))
    
    elif action == "course":
        course_name = sys.argv[2] if len(sys.argv) > 2 else ""
        result = tracker.get_course_progress(course_name)
        print(json.dumps(result, indent=2))
    
    elif action == "list":
        result = tracker.list_activity_types()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
