#!/usr/bin/env python3
"""
Morning Routine - Generate personalized morning routine
Part of the Personal System automation suite.
"""

import json
import os
import sys
import random
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class MorningRoutine:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.routine_file = self.data_dir / "morning_routines.json"
        self.health_file = self.data_dir / "health_data.json"
        self.tasks_file = self.data_dir / "tasks.json"
        self.shadow_work_file = self.data_dir / "shadow_work_data.json"
        self._ensure_data_files()
    
    def _ensure_data_files(self):
        """Ensure data files exist with proper structure."""
        if not self.routine_file.exists():
            self.routine_file.parent.mkdir(exist_ok=True)
            with open(self.routine_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict[str, Any]], file_path: Path):
        """Save data to file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_today_health_data(self) -> Dict[str, Any]:
        """Get today's health data."""
        health_data = self._load_data(self.health_file)
        today = date.today().isoformat()
        
        for entry in health_data:
            if entry.get('date') == today:
                return entry.get('metrics', {})
        return {}
    
    def _get_today_tasks(self) -> List[Dict[str, Any]]:
        """Get today's tasks."""
        tasks_data = self._load_data(self.tasks_file)
        today = date.today().isoformat()
        
        today_tasks = []
        for task in tasks_data:
            if (task['status'] == 'pending' and 
                task.get('due_date') == today):
                today_tasks.append(task)
        
        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        today_tasks.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        
        return today_tasks
    
    def _get_recent_shadow_work(self) -> List[Dict[str, Any]]:
        """Get recent shadow work insights."""
        shadow_data = self._load_data(self.shadow_work_file)
        
        # Get last 3 days of shadow work
        recent_insights = []
        for i in range(3):
            check_date = (date.today() - timedelta(days=i)).isoformat()
            for entry in shadow_data:
                if isinstance(entry, dict) and entry.get('date') == check_date:
                    recent_insights.extend(entry.get('insights', []))
        
        return recent_insights[-5:]  # Last 5 insights
    
    def _get_weather_context(self) -> str:
        """Get weather context (placeholder for future integration)."""
        # This could be integrated with a weather API in the future
        weather_options = [
            "☀️ Beautiful sunny day ahead",
            "🌤️ Partly cloudy, perfect for productivity",
            "🌧️ Rainy day - great for focused indoor work",
            "❄️ Cool and crisp morning",
            "🌅 Clear skies and fresh air"
        ]
        return random.choice(weather_options)
    
    def _get_motivational_quote(self) -> str:
        """Get a motivational quote."""
        quotes = [
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart. - Roy T. Bennett",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The way to get started is to quit talking and begin doing. - Walt Disney"
        ]
        return random.choice(quotes)
    
    def _get_shadow_work_prompt(self) -> str:
        """Get a shadow work reflection prompt."""
        prompts = [
            "What emotion am I avoiding today?",
            "What pattern in my behavior do I want to change?",
            "What would my shadow self want me to acknowledge?",
            "What am I afraid to face about myself?",
            "What old belief is no longer serving me?",
            "What part of myself am I rejecting?",
            "What would I do if I wasn't afraid?",
            "What am I hiding from others and why?"
        ]
        return random.choice(prompts)
    
    def generate_routine(self, include_health: bool = True, include_tasks: bool = True, 
                        include_shadow_work: bool = True) -> Dict[str, Any]:
        """Generate a personalized morning routine."""
        today = date.today()
        weekday = today.strftime('%A')
        
        # Get context data
        health_data = self._get_today_health_data() if include_health else {}
        today_tasks = self._get_today_tasks() if include_tasks else []
        shadow_insights = self._get_recent_shadow_work() if include_shadow_work else []
        
        # Generate routine components
        routine = {
            'date': today.isoformat(),
            'weekday': weekday,
            'timestamp': datetime.now().isoformat(),
            'weather': self._get_weather_context(),
            'quote': self._get_motivational_quote(),
            'sections': []
        }
        
        # Morning Greeting
        greeting = f"🌅 Good morning! Happy {weekday}!"
        routine['sections'].append({
            'title': 'Morning Greeting',
            'content': greeting,
            'type': 'greeting'
        })
        
        # Weather & Motivation
        routine['sections'].append({
            'title': 'Today\'s Context',
            'content': f"{routine['weather']}\n\n💭 \"{routine['quote']}\"",
            'type': 'context'
        })
        
        # Health Check-in
        if include_health:
            health_section = self._generate_health_section(health_data)
            if health_section:
                routine['sections'].append(health_section)
        
        # Today's Priorities
        if include_tasks and today_tasks:
            tasks_section = self._generate_tasks_section(today_tasks)
            routine['sections'].append(tasks_section)
        
        # Shadow Work Reflection
        if include_shadow_work:
            shadow_section = self._generate_shadow_work_section(shadow_insights)
            routine['sections'].append(shadow_section)
        
        # Daily Intentions
        intentions_section = self._generate_intentions_section()
        routine['sections'].append(intentions_section)
        
        # Save routine
        self._save_routine(routine)
        
        return {
            'success': True,
            'message': f"Morning routine generated for {weekday}",
            'routine': routine
        }
    
    def _generate_health_section(self, health_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate health check-in section."""
        if not health_data:
            return {
                'title': 'Health Check-in',
                'content': "💪 No health data logged yet today. Consider logging:\n• Steps taken\n• Hours of sleep\n• Water intake\n• Mood rating\n• Any workouts",
                'type': 'health',
                'suggestions': ['Log your morning health metrics', 'Set health goals for today']
            }
        
        content = "💪 Health Check-in:\n"
        suggestions = []
        
        if 'sleep' in health_data:
            sleep_hours = health_data['sleep']['value']
            if sleep_hours >= 8:
                content += f"😴 Great sleep: {sleep_hours} hours\n"
            elif sleep_hours >= 7:
                content += f"😊 Good sleep: {sleep_hours} hours\n"
            else:
                content += f"😴 Consider more rest: {sleep_hours} hours\n"
                suggestions.append("Prioritize sleep tonight")
        
        if 'mood' in health_data:
            mood = health_data['mood']['value']
            mood_emojis = {
                'excellent': '😄', 'great': '😊', 'good': '🙂',
                'okay': '😐', 'poor': '😔', 'terrible': '😢'
            }
            emoji = mood_emojis.get(mood.lower(), '😐')
            content += f"{emoji} Mood: {mood.title()}\n"
        
        if 'steps' not in health_data:
            suggestions.append("Log your steps today")
        if 'water' not in health_data:
            suggestions.append("Track your water intake")
        
        return {
            'title': 'Health Check-in',
            'content': content,
            'type': 'health',
            'suggestions': suggestions
        }
    
    def _generate_tasks_section(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate today's tasks section."""
        content = "📋 Today's Priorities:\n"
        
        high_priority = [task for task in tasks if task['priority'] == 'high']
        medium_priority = [task for task in tasks if task['priority'] == 'medium']
        low_priority = [task for task in tasks if task['priority'] == 'low']
        
        if high_priority:
            content += "\n🔴 High Priority:\n"
            for task in high_priority[:3]:  # Limit to top 3
                content += f"• {task['title']}\n"
        
        if medium_priority:
            content += "\n🟡 Medium Priority:\n"
            for task in medium_priority[:3]:  # Limit to top 3
                content += f"• {task['title']}\n"
        
        if low_priority:
            content += "\n🟢 Low Priority:\n"
            for task in low_priority[:2]:  # Limit to top 2
                content += f"• {task['title']}\n"
        
        suggestions = []
        if len(tasks) > 8:
            suggestions.append("Consider breaking down large tasks")
        if high_priority:
            suggestions.append("Focus on high-priority tasks first")
        
        return {
            'title': 'Today\'s Priorities',
            'content': content,
            'type': 'tasks',
            'suggestions': suggestions,
            'task_count': len(tasks)
        }
    
    def _generate_shadow_work_section(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate shadow work reflection section."""
        content = "🧠 Shadow Work Reflection:\n"
        
        if insights:
            content += "\nRecent insights to reflect on:\n"
            for insight in insights[-2:]:  # Last 2 insights
                content += f"• {insight.get('insight', 'No insight text')}\n"
        
        prompt = self._get_shadow_work_prompt()
        content += f"\n💭 Today's reflection prompt:\n\"{prompt}\""
        
        suggestions = [
            "Take 5 minutes to reflect on the prompt",
            "Journal about any patterns you notice",
            "Be gentle with yourself during reflection"
        ]
        
        return {
            'title': 'Shadow Work Reflection',
            'content': content,
            'type': 'shadow_work',
            'suggestions': suggestions,
            'prompt': prompt
        }
    
    def _generate_intentions_section(self) -> Dict[str, Any]:
        """Generate daily intentions section."""
        intentions = [
            "Practice gratitude for at least 3 things",
            "Take breaks and stay hydrated",
            "Be present in each moment",
            "Show kindness to yourself and others",
            "Learn something new today",
            "Move your body in a way that feels good",
            "Connect with someone you care about"
        ]
        
        # Select 3 random intentions
        selected_intentions = random.sample(intentions, 3)
        
        content = "🎯 Daily Intentions:\n"
        for i, intention in enumerate(selected_intentions, 1):
            content += f"{i}. {intention}\n"
        
        return {
            'title': 'Daily Intentions',
            'content': content,
            'type': 'intentions',
            'intentions': selected_intentions
        }
    
    def _save_routine(self, routine: Dict[str, Any]):
        """Save routine to file."""
        routines = self._load_data(self.routine_file)
        routines.append(routine)
        self._save_data(routines, self.routine_file)
    
    def get_recent_routines(self, days: int = 7) -> Dict[str, Any]:
        """Get recent morning routines."""
        routines = self._load_data(self.routine_file)
        
        # Get routines from last N days
        cutoff_date = (date.today() - timedelta(days=days)).isoformat()
        recent_routines = [r for r in routines if r.get('date', '') >= cutoff_date]
        
        return {
            'success': True,
            'message': f"Recent routines ({len(recent_routines)} found)",
            'routines': recent_routines,
            'period': f"{days} days"
        }

def main():
    """Main entry point."""
    routine = MorningRoutine()
    
    if len(sys.argv) < 2:
        print("Usage: python morning_routine.py <action> [args...]")
        print("Actions:")
        print("  generate [--no-health] [--no-tasks] [--no-shadow] - Generate morning routine")
        print("  recent [days] - Get recent routines")
        return
    
    action = sys.argv[1]
    
    if action == "generate":
        include_health = "--no-health" not in sys.argv
        include_tasks = "--no-tasks" not in sys.argv
        include_shadow_work = "--no-shadow" not in sys.argv
        
        result = routine.generate_routine(include_health, include_tasks, include_shadow_work)
        print(json.dumps(result, indent=2))
    
    elif action == "recent":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        result = routine.get_recent_routines(days)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
