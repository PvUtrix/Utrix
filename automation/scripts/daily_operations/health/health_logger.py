#!/usr/bin/env python3
"""
Health Logger - Track and manage health metrics
Part of the Personal System automation suite.
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class HealthLogger:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.data_file = self.data_dir / "health_data.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load health data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict[str, Any]]):
        """Save health data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_today_entry(self, data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Get today's health entry."""
        today = date.today().isoformat()
        for entry in data:
            if entry.get('date') == today:
                return entry
        return None
    
    def log_metric(self, metric_type: str, value: Any, notes: str = "") -> Dict[str, Any]:
        """Log a health metric for today."""
        data = self._load_data()
        today = date.today().isoformat()
        
        # Get or create today's entry
        today_entry = self._get_today_entry(data)
        if not today_entry:
            today_entry = {
                'date': today,
                'timestamp': datetime.now().isoformat(),
                'metrics': {},
                'notes': []
            }
            data.append(today_entry)
        
        # Add the metric
        today_entry['metrics'][metric_type] = {
            'value': value,
            'timestamp': datetime.now().isoformat(),
            'notes': notes
        }
        
        # Add note if provided
        if notes:
            today_entry['notes'].append({
                'timestamp': datetime.now().isoformat(),
                'note': notes
            })
        
        self._save_data(data)
        
        return {
            'success': True,
            'message': f"Logged {metric_type}: {value}",
            'date': today,
            'metric': metric_type,
            'value': value
        }
    
    def get_today_stats(self) -> Dict[str, Any]:
        """Get today's health statistics."""
        data = self._load_data()
        today_entry = self._get_today_entry(data)
        
        if not today_entry:
            return {
                'success': True,
                'message': "No health data logged today",
                'date': date.today().isoformat(),
                'metrics': {},
                'summary': "Start logging your health metrics!"
            }
        
        metrics = today_entry.get('metrics', {})
        
        # Calculate summary
        summary = []
        if 'steps' in metrics:
            steps = metrics['steps']['value']
            if steps >= 10000:
                summary.append(f"🎯 Great job! {steps:,} steps today")
            elif steps >= 5000:
                summary.append(f"👍 Good progress: {steps:,} steps")
            else:
                summary.append(f"💪 Keep moving: {steps:,} steps")
        
        if 'sleep' in metrics:
            sleep = metrics['sleep']['value']
            if sleep >= 8:
                summary.append(f"😴 Excellent sleep: {sleep} hours")
            elif sleep >= 7:
                summary.append(f"😊 Good sleep: {sleep} hours")
            else:
                summary.append(f"😴 Consider more rest: {sleep} hours")
        
        if 'water' in metrics:
            water = metrics['water']['value']
            if water >= 8:
                summary.append(f"💧 Well hydrated: {water} glasses")
            elif water >= 5:
                summary.append(f"💧 Good hydration: {water} glasses")
            else:
                summary.append(f"💧 Stay hydrated: {water} glasses")
        
        if 'mood' in metrics:
            mood = metrics['mood']['value']
            mood_emojis = {
                'excellent': '😄', 'great': '😊', 'good': '🙂',
                'okay': '😐', 'poor': '😔', 'terrible': '😢'
            }
            emoji = mood_emojis.get(mood.lower(), '😐')
            summary.append(f"{emoji} Mood: {mood.title()}")
        
        return {
            'success': True,
            'message': "Today's health summary",
            'date': today_entry['date'],
            'metrics': metrics,
            'summary': summary,
            'notes': today_entry.get('notes', [])
        }
    
    def get_weekly_stats(self) -> Dict[str, Any]:
        """Get weekly health statistics."""
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
                'message': "No health data for the past week",
                'period': '7 days',
                'summary': "Start logging your health metrics!"
            }
        
        # Calculate averages
        metrics_sum = {}
        metrics_count = {}
        
        for entry in weekly_data:
            for metric_type, metric_data in entry.get('metrics', {}).items():
                if metric_type in ['steps', 'sleep', 'water']:
                    value = float(metric_data['value'])
                    metrics_sum[metric_type] = metrics_sum.get(metric_type, 0) + value
                    metrics_count[metric_type] = metrics_count.get(metric_type, 0) + 1
        
        averages = {}
        for metric_type in metrics_sum:
            averages[metric_type] = round(metrics_sum[metric_type] / metrics_count[metric_type], 1)
        
        # Generate summary
        summary = []
        if 'steps' in averages:
            avg_steps = averages['steps']
            summary.append(f"📊 Average steps: {avg_steps:,.0f}/day")
        
        if 'sleep' in averages:
            avg_sleep = averages['sleep']
            summary.append(f"😴 Average sleep: {avg_sleep}h/night")
        
        if 'water' in averages:
            avg_water = averages['water']
            summary.append(f"💧 Average water: {avg_water} glasses/day")
        
        return {
            'success': True,
            'message': "Weekly health summary",
            'period': '7 days',
            'averages': averages,
            'summary': summary,
            'days_logged': len(weekly_data)
        }
    
    def list_metrics(self) -> Dict[str, Any]:
        """List all available metric types."""
        return {
            'success': True,
            'message': "Available health metrics",
            'metrics': {
                'steps': 'Number of steps taken',
                'sleep': 'Hours of sleep',
                'water': 'Glasses of water consumed',
                'mood': 'Mood rating (excellent/great/good/okay/poor/terrible)',
                'workout': 'Type of workout performed',
                'weight': 'Body weight',
                'calories': 'Calories consumed',
                'meditation': 'Minutes of meditation',
                'stress': 'Stress level (1-10)',
                'energy': 'Energy level (1-10)'
            }
        }

def main():
    """Main entry point."""
    logger = HealthLogger()
    
    if len(sys.argv) < 2:
        print("Usage: python health_logger.py <action> [args...]")
        print("Actions:")
        print("  log <metric_type> <value> [notes] - Log a health metric")
        print("  today - Get today's health stats")
        print("  weekly - Get weekly health stats")
        print("  list - List available metrics")
        return
    
    action = sys.argv[1]
    
    if action == "log":
        if len(sys.argv) < 4:
            print("Usage: python health_logger.py log <metric_type> <value> [notes]")
            return
        
        metric_type = sys.argv[2]
        value = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        
        # Convert numeric values
        if metric_type in ['steps', 'sleep', 'water', 'weight', 'calories', 'meditation', 'stress', 'energy']:
            try:
                value = float(value)
            except ValueError:
                print(f"Error: {metric_type} requires a numeric value")
                return
        
        result = logger.log_metric(metric_type, value, notes)
        print(json.dumps(result, indent=2))
    
    elif action == "today":
        result = logger.get_today_stats()
        print(json.dumps(result, indent=2))
    
    elif action == "weekly":
        result = logger.get_weekly_stats()
        print(json.dumps(result, indent=2))
    
    elif action == "list":
        result = logger.list_metrics()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
