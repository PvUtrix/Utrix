#!/usr/bin/env python3
"""
Interactive Morning Routine for Telegram Bot
Generates and formats personalized morning routines
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

class InteractiveMorningRoutine:
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
    
    def _get_today_health_data(self) -> Dict[str, Any]:
        """Get today's health data."""
        health_data = self._load_data(self.health_file)
        today = date.today().isoformat()
        
        # Look for today's health data
        for entry in health_data:
            if isinstance(entry, dict) and entry.get('date') == today:
                return entry.get('metrics', {})
        return {}
    
    def _get_recent_shadow_work(self) -> Optional[str]:
        """Get recent shadow work prompt."""
        shadow_data = self._load_data(self.shadow_work_file)
        if not shadow_data:
            return None
        
        # Get the most recent entry
        recent_entry = shadow_data[-1] if shadow_data else None
        if isinstance(recent_entry, dict):
            return recent_entry.get('prompt')
        return None
    
    def _get_weather_mood(self) -> str:
        """Get weather-based mood."""
        weather_options = [
            "☀️ Bright and sunny morning",
            "🌤️ Partly cloudy with gentle breeze",
            "🌧️ Cozy rainy morning",
            "❄️ Cool and crisp morning",
            "🌅 Peaceful dawn breaking",
            "🌊 Fresh morning air"
        ]
        return random.choice(weather_options)
    
    def _get_daily_quote(self) -> str:
        """Get an inspirational daily quote."""
        quotes = [
            "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart. - Roy T. Bennett",
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Your limitation—it's only your imagination.",
            "Great things never come from comfort zones.",
            "Dream it. Wish it. Do it.",
            "Success doesn't just find you. You have to go out and get it.",
            "The harder you work for something, the greater you'll feel when you achieve it.",
            "Dream bigger. Do bigger.",
            "Don't stop when you're tired. Stop when you're done.",
            "Wake up with determination. Go to bed with satisfaction."
        ]
        return random.choice(quotes)
    
    def _get_daily_intentions(self) -> List[str]:
        """Get daily intentions."""
        intentions = [
            "Show kindness to yourself and others",
            "Take breaks and stay hydrated",
            "Move your body in a way that feels good",
            "Focus on one important task at a time",
            "Practice gratitude throughout the day",
            "Listen to your body's needs",
            "Connect with someone you care about",
            "Learn something new or interesting",
            "Take time for reflection and mindfulness",
            "Celebrate small wins and progress"
        ]
        return random.sample(intentions, 3)
    
    def generate_routine(self) -> str:
        """Generate a formatted morning routine for Telegram."""
        today = date.today()
        weekday = today.strftime("%A")
        weather = self._get_weather_mood()
        quote = self._get_daily_quote()
        health_data = self._get_today_health_data()
        shadow_prompt = self._get_recent_shadow_work()
        intentions = self._get_daily_intentions()
        
        # Build the routine message
        routine = f"🌅 **Good Morning! Happy {weekday}!**\n\n"
        
        # Weather and quote
        routine += f"{weather}\n\n"
        routine += f"💭 *\"{quote}\"*\n\n"
        
        # Health check-in
        routine += "💪 **Health Check-in**\n"
        if health_data:
            routine += "Great! You've already logged some health data today:\n"
            for metric, data in health_data.items():
                if isinstance(data, dict):
                    routine += f"• {metric.title()}: {data.get('value', 'N/A')}\n"
        else:
            routine += "No health data logged yet today. Consider logging:\n"
            routine += "• Steps taken\n• Hours of sleep\n• Water intake\n• Mood rating\n• Any workouts\n"
        routine += "\n"
        
        # Shadow work reflection
        routine += "🕯️ **Shadow Work Reflection**\n"
        if shadow_prompt:
            routine += f"Today's reflection prompt:\n*\"{shadow_prompt}\"*\n\n"
            routine += "Take 5 minutes to reflect on this prompt. Be gentle with yourself.\n\n"
        else:
            routine += "No recent shadow work prompts found. Consider starting your shadow work journey.\n\n"
        
        # Daily intentions
        routine += "🎯 **Daily Intentions**\n"
        for i, intention in enumerate(intentions, 1):
            routine += f"{i}. {intention}\n"
        routine += "\n"
        
        # Quick actions
        routine += "⚡ **Quick Actions**\n"
        routine += "• Log your morning health metrics\n"
        routine += "• Set your top 3 priorities for today\n"
        routine += "• Take a moment to breathe and center yourself\n"
        routine += "• Review your daily intentions\n\n"
        
        # Footer
        routine += f"---\n"
        routine += f"*Generated at {datetime.now().strftime('%H:%M')} | Have a wonderful day!*"
        
        return routine
    
    def get_routine_help(self) -> str:
        """Get help information about morning routines."""
        return """🌅 **Morning Routine Help**

**What is a Morning Routine?**
A personalized daily routine that helps you start your day with intention, reflection, and purpose.

**What's Included:**
• Daily greeting and weather mood
• Inspirational quote
• Health check-in and suggestions
• Shadow work reflection prompt
• Daily intentions and goals
• Quick action suggestions

**Benefits:**
• Sets a positive tone for the day
• Encourages self-reflection
• Promotes healthy habits
• Provides structure and focus
• Builds mindfulness practices

**How to Use:**
• Run this script each morning
• Follow the reflection prompts
• Log your health metrics
• Set your daily intentions
• Take the suggested quick actions

**Tips:**
• Take your time with reflections
• Be honest with yourself
• Adjust intentions based on your energy
• Use this as a foundation, not a rigid schedule"""

def main():
    """Main entry point for interactive morning routine generation."""
    routine_generator = InteractiveMorningRoutine()
    
    if len(sys.argv) < 2:
        # Generate and show the routine
        routine = routine_generator.generate_routine()
        print(routine)
        return
    
    action = sys.argv[1]
    
    if action == "generate":
        routine = routine_generator.generate_routine()
        print(routine)
    
    elif action == "help":
        print(routine_generator.get_routine_help())
    
    else:
        print(f"❌ Unknown action: {action}")
        print("Available actions: generate, help")

if __name__ == "__main__":
    main()
