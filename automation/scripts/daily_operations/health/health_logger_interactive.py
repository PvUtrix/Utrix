#!/usr/bin/env python3
"""
Interactive Health Logger for Telegram Bot
Provides a simple interface for logging health metrics
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class InteractiveHealthLogger:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.data_file = self.data_dir / "health_data.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump({}, f)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load health data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save health data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def log_health_metric(self, metric_type: str, value: str, notes: str = "") -> str:
        """Log a health metric for today."""
        today = date.today().isoformat()
        data = self._load_data()
        
        if today not in data:
            data[today] = {
                "date": today,
                "metrics": {},
                "notes": []
            }
        
        # Store the metric
        data[today]["metrics"][metric_type] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "notes": notes
        }
        
        # Add to notes if provided
        if notes:
            data[today]["notes"].append(f"{metric_type}: {notes}")
        
        self._save_data(data)
        
        return f"✅ Logged {metric_type}: {value}" + (f" (Notes: {notes})" if notes else "")
    
    def get_today_stats(self) -> str:
        """Get today's health statistics."""
        today = date.today().isoformat()
        data = self._load_data()
        
        if today not in data:
            return "📊 **Today's Health Stats**\n\nNo health data logged today.\n\n**Available Metrics:**\n- steps: Number of steps\n- sleep: Hours of sleep\n- water: Glasses of water\n- weight: Weight in kg/lbs\n- mood: Mood (1-10)\n- workout: Workout type\n- stress: Stress level (1-10)\n- energy: Energy level (1-10)"
        
        today_data = data[today]
        metrics = today_data.get("metrics", {})
        
        if not metrics:
            return "📊 **Today's Health Stats**\n\nNo metrics logged today."
        
        stats = "📊 **Today's Health Stats**\n\n"
        for metric, data in metrics.items():
            stats += f"• **{metric.title()}**: {data['value']}\n"
        
        return stats
    
    def get_available_metrics(self) -> str:
        """Get list of available health metrics."""
        return """📋 **Available Health Metrics:**

**Physical Health:**
• steps - Number of steps taken
• sleep - Hours of sleep
• water - Glasses of water consumed
• weight - Weight in kg or lbs
• workout - Type of workout/exercise

**Mental Health:**
• mood - Mood level (1-10)
• stress - Stress level (1-10)
• energy - Energy level (1-10)

**Example Usage:**
• Log steps: 8500
• Log sleep: 7.5
• Log water: 8
• Log mood: 8
• Log workout: cardio"""

def main():
    """Main entry point for interactive health logging."""
    logger = InteractiveHealthLogger()
    
    if len(sys.argv) < 2:
        # Show available metrics and today's stats
        print("📋 **Health Logger - Quick Start**\n")
        print(logger.get_available_metrics())
        print("\n" + "="*50 + "\n")
        print(logger.get_today_stats())
        return
    
    action = sys.argv[1]
    
    if action == "log":
        if len(sys.argv) < 4:
            print("❌ **Usage:** python health_logger_interactive.py log <metric_type> <value> [notes]")
            print("\n" + logger.get_available_metrics())
            return
        
        metric_type = sys.argv[2]
        value = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        
        result = logger.log_health_metric(metric_type, value, notes)
        print(result)
        print("\n" + logger.get_today_stats())
    
    elif action == "today":
        print(logger.get_today_stats())
    
    elif action == "metrics":
        print(logger.get_available_metrics())
    
    else:
        print(f"❌ Unknown action: {action}")
        print("Available actions: log, today, metrics")

if __name__ == "__main__":
    main()
