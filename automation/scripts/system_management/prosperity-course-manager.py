#!/usr/bin/env python3
"""
Prosperity Course Manager
Manages the 5-day prosperity mindset course progress and tracking
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

class ProsperityCourseManager:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent.parent / "domains" / "learning" / "prosperity-course-config.json"
        self.journal_path = Path(__file__).parent.parent.parent / "core" / "knowledge" / "journal" / datetime.now().strftime('%Y')

    def load_config(self):
        """Load course configuration"""
        if not self.config_path.exists():
            print("❌ Prosperity course configuration not found!")
            return None

        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_config(self, config):
        """Save course configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def get_current_day(self):
        """Get current day of the course"""
        config = self.load_config()
        if not config:
            return None

        start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
        current_date = datetime.now()
        days_into_course = (current_date - start_date).days + 1

        if days_into_course < 1 or days_into_course > config['duration_days']:
            return None

        return days_into_course

    def update_progress(self, day, completed=False, notes=""):
        """Update progress for a specific day"""
        config = self.load_config()
        if not config:
            return False

        config['current_day'] = day
        if completed:
            config['last_completed_day'] = day
            config['completion_notes'] = notes

        self.save_config(config)
        print(f"✅ Updated progress for Day {day}")
        return True

    def show_status(self):
        """Show current course status"""
        config = self.load_config()
        if not config:
            print("❌ Course configuration not found")
            return

        current_day = self.get_current_day()
        status = config.get('status', 'unknown')

        print(f"🎯 Prosperity Mindset Course Status")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Course: {config.get('course_name', 'Unknown')}")
        print(f"Status: {status}")
        print(f"Start Date: {config.get('start_date', 'Unknown')}")
        print(f"Duration: {config.get('duration_days', 0)} days")

        if current_day:
            print(f"Current Day: {current_day}/{config.get('duration_days', 0)}")
            if current_day <= 5:
                day_names = [
                    "Mindset Audit",
                    "Gratitude & Opportunity",
                    "Value Exchange Principle",
                    "Personal Prosperity Vision",
                    "Environment Curation"
                ]
                print(f"Today's Focus: {day_names[current_day-1]}")
        else:
            print("Current Day: Course completed or not started")

        print(f"Voice Reminders: {'✅ Enabled' if config.get('voice_enabled') else '❌ Disabled'}")

    def pause_course(self):
        """Pause the course"""
        config = self.load_config()
        if config:
            config['status'] = 'paused'
            self.save_config(config)
            print("⏸️ Course paused")

    def resume_course(self):
        """Resume the course"""
        config = self.load_config()
        if config:
            config['status'] = 'active'
            self.save_config(config)
            print("▶️ Course resumed")

    def reset_course(self, new_start_date=None):
        """Reset the course with optional new start date"""
        config = self.load_config()
        if config:
            if new_start_date:
                config['start_date'] = new_start_date
            config['current_day'] = 1
            config['status'] = 'active'
            if 'last_completed_day' in config:
                del config['last_completed_day']
            self.save_config(config)
            print(f"🔄 Course reset to Day 1 (Start: {config['start_date']})")

    def create_daily_journal_template(self, day):
        """Create a journal template for the specified day"""
        journal_dir = self.journal_path
        journal_dir.mkdir(parents=True, exist_ok=True)

        journal_file = journal_dir / f"prosperity-course-day-{day}.md"

        templates = {
            1: """# Prosperity Course - Day 1: Money Story Audit

## Money Memories
- First memory involving money: ____________________
- What I learned from parents about money: ____________________

## Current Beliefs
- Money is... ____________________
- Rich people are... ____________________
- To make a lot of money, you have to... ____________________
- I can't afford... ____________________

## Emotional Inventory
When I think about having a lot of money, I feel:
- Fear: ____________________
- Anxiety: ____________________
- Excitement: ____________________
- Other: ____________________

## Key Insights
Limiting beliefs identified: ____________________
Emotional patterns noticed: ____________________
New awareness gained: ____________________

## Reflections
How do these beliefs serve me? ____________________
What would change if I challenged them? ____________________""",

            2: """# Prosperity Course - Day 2: Gratitude & Opportunity

## Morning Gratitude Log (5 items)
1. ____________________ (Why I'm grateful: ____________________)
2. ____________________ (Why I'm grateful: ____________________)
3. ____________________ (Why I'm grateful: ____________________)
4. ____________________ (Why I'm grateful: ____________________)
5. ____________________ (Why I'm grateful: ____________________)

## Evening Opportunity Spotter (3 challenges)
1. Challenge: ____________________
   Opportunity: ____________________
   Action to take: ____________________

2. Challenge: ____________________
   Opportunity: ____________________
   Action to take: ____________________

3. Challenge: ____________________
   Opportunity: ____________________
   Action to take: ____________________

## Real-time Practice
Times I caught scarcity thinking today: _____
Times I reframed to opportunity: _____
Most challenging reframe: ____________________

## Daily Reflection
How did focusing on gratitude change my day? ____________________
What opportunities did I notice that I might have missed before? ____________________""",

            3: """# Prosperity Course - Day 3: Value Exchange Principle

## Value Creation Plan
Skill/Talent I will offer: ____________________
Person I will help: ____________________
How I will provide value: ____________________
Expected outcome: ____________________

## Value Creation Log
Date/Time: ____________________
Action taken: ____________________
Person's response: ____________________
How it felt: ____________________

## Multiples Thinking
How could this same value help:
- 10 people: ____________________
- 100 people: ____________________
- My community: ____________________

## Daily Reflection
What surprised me about giving without expectation? ____________________
How did this change my view of wealth creation? ____________________""",

            4: """# Prosperity Course - Day 4: Personal Prosperity Vision

## Perfect Average Tuesday (5 Years From Now)

### Morning Routine
Wake-up time: ____________________
How I feel upon waking: ____________________
First activity: ____________________
Gratitude practice: ____________________

### Work & Contribution
What I work on: ____________________
Who I help: ____________________
How I feel about my work: ____________________
Income sources: ____________________

### Health & Well-being
Exercise: ____________________
Nutrition: ____________________
Rest & recovery: ____________________
Energy level: ____________________

### Relationships & Community
Family time: ____________________
Friends/social: ____________________
Community contribution: ____________________
Quality of connections: ____________________

### Finances & Freedom
Monthly income: ____________________
Financial peace level: ____________________
How money feels: ____________________
Abundance indicators: ____________________

### Evening Wind-down
Evening routine: ____________________
Reflection practice: ____________________
Sleep quality: ____________________
Gratitude for the day: ____________________

## Vision Triggers Created
Phone wallpaper: [ ] Created
Computer background: [ ] Created
Vision board item: [ ] Created
Daily affirmation: ____________________

## Act As If Implementation
One element I'm implementing today: ____________________
How it feels: ____________________

## Vision Reflection
What excites me most about this vision? ____________________
What feels most realistic/achievable? ____________________
What belief shifts will this require? ____________________""",

            5: """# Prosperity Course - Day 5: Environment Curation

## Digital Environment Audit

### Accounts to Unfollow (Scarcity Focus)
1. ____________________ (Why: ____________________)
2. ____________________ (Why: ____________________)
3. ____________________ (Why: ____________________)
4. ____________________ (Why: ____________________)
5. ____________________ (Why: ____________________)

### Accounts to Follow (Abundance Focus)
1. ____________________ (Why: ____________________)
2. ____________________ (Why: ____________________)
3. ____________________ (Why: ____________________)
4. ____________________ (Why: ____________________)
5. ____________________ (Why: ____________________)

## Conversation Curation

### Positive Connection Plan
Person to contact: ____________________
Relationship context: ____________________
Scheduled date/time: ____________________
Topics to discuss: ____________________
Expected outcome: ____________________

## Prosperity Language Practice

### Scarcity Phrases Caught (24-hour challenge)
1. ____________________ → Reframed to: ____________________
2. ____________________ → Reframed to: ____________________
3. ____________________ → Reframed to: ____________________

## Habit Integration

### Habit Stacking Plan
Existing habit: ____________________
New prosperity habit: ____________________
Combined routine: ____________________
Implementation start: ____________________

## Environment Changes Made
Physical space: ____________________
Digital space: ____________________
Social circle: ____________________
Daily routine: ____________________

## Course Completion Reflection

### What I Learned
Most important insight: ____________________
Surprising discovery: ____________________
Practice I'll continue: ____________________

### Next Steps
Short-term goal (1 month): ____________________
Medium-term goal (6 months): ____________________
Long-term vision alignment: ____________________

### Gratitude for the Course
What I'm grateful for: ____________________
How this will impact my life: ____________________

## Course Status: ✅ COMPLETED
Completion Date: ____________________
Next Review Date: ____________________ (30 days from now)"""
        }

        if day in templates:
            with open(journal_file, 'w') as f:
                f.write(templates[day])
            print(f"📝 Created journal template: {journal_file}")
            return True

        return False

def main():
    manager = ProsperityCourseManager()

    if len(sys.argv) < 2:
        print("Usage: python prosperity-course-manager.py <command>")
        print("Commands:")
        print("  status          - Show course status")
        print("  pause           - Pause the course")
        print("  resume          - Resume the course")
        print("  reset [date]    - Reset course (optional: new start date YYYY-MM-DD)")
        print("  journal <day>   - Create journal template for specific day")
        print("  update <day>    - Mark day as completed")
        return

    command = sys.argv[1]

    if command == 'status':
        manager.show_status()

    elif command == 'pause':
        manager.pause_course()

    elif command == 'resume':
        manager.resume_course()

    elif command == 'reset':
        new_date = sys.argv[2] if len(sys.argv) > 2 else None
        manager.reset_course(new_date)

    elif command == 'journal':
        if len(sys.argv) < 3:
            print("❌ Please specify day number (1-5)")
            return
        try:
            day = int(sys.argv[2])
            if 1 <= day <= 5:
                manager.create_daily_journal_template(day)
            else:
                print("❌ Day must be between 1-5")
        except ValueError:
            print("❌ Invalid day number")

    elif command == 'update':
        if len(sys.argv) < 3:
            print("❌ Please specify day number")
            return
        try:
            day = int(sys.argv[2])
            notes = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            manager.update_progress(day, completed=True, notes=notes)
        except ValueError:
            print("❌ Invalid day number")

    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
