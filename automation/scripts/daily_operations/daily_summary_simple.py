#!/usr/bin/env python3
# Ultra-simple daily summary for Telegram bot
# No special characters, no formatting, just plain text

from datetime import datetime

def main():
    today = datetime.now().strftime('%B %d, %Y')
    
    summary = f"""Daily Summary - {today}

No Data Available

No tracked data found for today. Start logging to see your daily summary!

Quick Actions:
- Use /log_health to track health metrics
- Use /log_learning to track learning progress
- Use /add_task to add tasks
- Use /quick_note to capture thoughts

Reflection Prompts:
- What was your biggest win today?
- What challenged you the most?
- What are you grateful for?
- What will you do differently tomorrow?

---
Generated at {datetime.now().strftime('%H:%M')} | Next summary in 24 hours"""
    
    print(summary)

if __name__ == "__main__":
    main()
