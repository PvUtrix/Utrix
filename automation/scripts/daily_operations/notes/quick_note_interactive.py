#!/usr/bin/env python3
"""
Interactive Quick Note for Telegram Bot
Provides a simple interface for capturing quick notes
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class InteractiveQuickNote:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.data_file = self.data_dir / "quick_notes.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump({}, f)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load quick notes data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save quick notes data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def capture_note(self, content: str, category: str = "general", tags: str = "", priority: str = "medium") -> str:
        """Capture a quick note."""
        today = date.today().isoformat()
        data = self._load_data()
        
        if today not in data:
            data[today] = {
                "date": today,
                "notes": [],
                "count": 0
            }
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
        
        # Create note entry
        note = {
            "id": data[today]["count"] + 1,
            "content": content,
            "category": category,
            "tags": tag_list,
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        }
        
        data[today]["notes"].append(note)
        data[today]["count"] += 1
        
        self._save_data(data)
        
        # Format response
        response = f"📝 **Note Captured**\n\n"
        response += f"💭 **Content**: {content}\n"
        response += f"🏷️ **Category**: {category.title()}\n"
        if tag_list:
            response += f"🔖 **Tags**: {', '.join(tag_list)}\n"
        response += f"⚡ **Priority**: {priority.title()}\n"
        response += f"🆔 **ID**: {note['id']}"
        
        return response
    
    def get_today_notes(self) -> str:
        """Get today's quick notes."""
        today = date.today().isoformat()
        data = self._load_data()
        
        if today not in data:
            return "📝 **Today's Quick Notes**\n\nNo notes captured today.\n\n**Available Categories:**\n- general: General notes\n- idea: Ideas and thoughts\n- reminder: Reminders\n- task: Task-related notes\n- learning: Learning notes\n- personal: Personal notes"
        
        today_data = data[today]
        notes = today_data.get("notes", [])
        
        if not notes:
            return "📝 **Today's Quick Notes**\n\nNo notes captured today."
        
        # Sort by priority and timestamp
        priority_order = {"urgent": 4, "high": 3, "medium": 2, "low": 1}
        notes.sort(key=lambda x: (priority_order.get(x.get("priority", "medium"), 2), x.get("timestamp", "")), reverse=True)
        
        response = f"📝 **Today's Quick Notes** ({len(notes)} notes)\n\n"
        
        for note in notes:
            priority_emoji = {"urgent": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}.get(note.get("priority", "medium"), "🟡")
            category_emoji = {
                "general": "📝", "idea": "💡", "reminder": "⏰", 
                "task": "✅", "learning": "📚", "personal": "👤"
            }.get(note.get("category", "general"), "📝")
            
            response += f"{category_emoji} **{note['content']}** {priority_emoji}\n"
            response += f"   🏷️ {note['category'].title()}"
            if note.get("tags"):
                response += f" | 🔖 {', '.join(note['tags'])}"
            response += f" | 🆔 {note['id']}\n\n"
        
        return response
    
    def get_note_stats(self) -> str:
        """Get quick note statistics."""
        data = self._load_data()
        
        total_notes = 0
        category_counts = {}
        priority_counts = {"urgent": 0, "high": 0, "medium": 0, "low": 0}
        
        for date_str, day_data in data.items():
            notes = day_data.get("notes", [])
            total_notes += len(notes)
            
            for note in notes:
                category = note.get("category", "general")
                category_counts[category] = category_counts.get(category, 0) + 1
                
                priority = note.get("priority", "medium")
                priority_counts[priority] += 1
        
        if total_notes == 0:
            return "📊 **Quick Note Statistics**\n\nNo notes captured yet."
        
        response = f"📊 **Quick Note Statistics**\n\n"
        response += f"📝 **Total Notes**: {total_notes}\n\n"
        
        response += f"🏷️ **By Category:**\n"
        for category, count in sorted(category_counts.items()):
            response += f"• {category.title()}: {count}\n"
        
        response += f"\n⚡ **By Priority:**\n"
        response += f"🚨 Urgent: {priority_counts['urgent']}\n"
        response += f"🔴 High: {priority_counts['high']}\n"
        response += f"🟡 Medium: {priority_counts['medium']}\n"
        response += f"🟢 Low: {priority_counts['low']}"
        
        return response
    
    def get_help(self) -> str:
        """Get help information."""
        return """📝 **Quick Note Help**

**Capturing Notes:**
• python quick_note_interactive.py capture "Your note content" [category] [tags] [priority]

**Categories:**
• general - General notes (default)
• idea - Ideas and thoughts
• reminder - Reminders
• task - Task-related notes
• learning - Learning notes
• personal - Personal notes

**Priority Levels:**
• low - Low priority (green)
• medium - Medium priority (yellow, default)
• high - High priority (red)
• urgent - Urgent priority (red with alert)

**Tags:**
• Comma-separated list of tags
• Example: "work,important,meeting"

**Examples:**
• Simple note: "Remember to call mom"
• Categorized note: "Great idea for app" "idea" "mobile,startup"
• Priority note: "Fix critical bug" "task" "work,urgent" "urgent"

**Available Commands:**
• capture - Capture a new note
• today - Show today's notes
• stats - Show note statistics
• help - Show this help"""

def main():
    """Main entry point for interactive quick note capture."""
    note_taker = InteractiveQuickNote()
    
    if len(sys.argv) < 2:
        # Show help and current stats
        print("📝 **Quick Note - Quick Start**\n")
        print(note_taker.get_help())
        print("\n" + "="*50 + "\n")
        print(note_taker.get_today_notes())
        return
    
    action = sys.argv[1]
    
    if action == "capture":
        if len(sys.argv) < 3:
            print("❌ **Usage:** python quick_note_interactive.py capture <content> [category] [tags] [priority]")
            print("\n" + note_taker.get_help())
            return
        
        content = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "general"
        tags = sys.argv[4] if len(sys.argv) > 4 else ""
        priority = sys.argv[5] if len(sys.argv) > 5 else "medium"
        
        result = note_taker.capture_note(content, category, tags, priority)
        print(result)
        print("\n" + note_taker.get_today_notes())
    
    elif action == "today":
        print(note_taker.get_today_notes())
    
    elif action == "stats":
        print(note_taker.get_note_stats())
    
    elif action == "help":
        print(note_taker.get_help())
    
    else:
        print(f"❌ Unknown action: {action}")
        print("Available actions: capture, today, stats, help")

if __name__ == "__main__":
    main()
