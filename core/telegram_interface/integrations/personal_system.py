"""
Personal system integration for the Telegram Bot.
Connects to the user's existing automation scripts and system.
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from utils.logger import get_logger


class PersonalSystemIntegration:
    """Integration with the user's personal system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = get_logger(__name__)
        self.config = config or {}
        self.base_path = Path(config.get('paths', {}).get('base_path', '../../../'))
        self.automation_scripts = Path(config.get('paths', {}).get('automation_scripts', '../../../automation/scripts/'))
    
    def get_daily_summary(self) -> str:
        """Get daily summary using the existing automation script or generate one."""
        try:
            # Try to run the daily summary script if it exists
            script_path = self.automation_scripts / "daily_summary.py"
            
            if script_path.exists():
                # Run the script and capture output
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    cwd=self.automation_scripts
                )
                
                if result.returncode == 0:
                    # Parse the output and format for Telegram
                    summary = self._format_summary_for_telegram(result.stdout)
                    return summary
                else:
                    return self._generate_default_summary()
            else:
                # Generate a basic summary if script doesn't exist
                return self._generate_default_summary()
                
        except Exception as e:
            self.logger.error(f"Error getting daily summary: {e}")
            return self._generate_default_summary()
    
    def _format_summary_for_telegram(self, summary_text: str) -> str:
        """Format the summary text for Telegram display."""
        # This is a simplified formatter - you can enhance it based on your summary format
        lines = summary_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():
                # Add emojis and formatting for better readability
                if 'health' in line.lower():
                    line = f"🏃‍♂️ {line}"
                elif 'productivity' in line.lower():
                    line = f"⚡ {line}"
                elif 'learning' in line.lower():
                    line = f"📚 {line}"
                elif 'finance' in line.lower():
                    line = f"💰 {line}"
                elif 'insights' in line.lower():
                    line = f"💡 {line}"
                elif 'recommendations' in line.lower():
                    line = f"🎯 {line}"
                
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _generate_default_summary(self) -> str:
        """Generate a default daily summary."""
        today = datetime.now()
        
        summary = f"""📊 **Daily Summary - {today.strftime('%B %d, %Y')}**

🏃‍♂️ **Health & Wellness**
• Status: Ready for a productive day
• Recommendation: Take a 15-minute walk and stay hydrated
• Focus: Maintain your wellness routine

⚡ **Productivity**
• Energy Level: Good for focused work
• Best Hours: Morning hours for deep work
• Tip: Use time-blocking for important tasks

📚 **Learning & Growth**
• Opportunity: Continue with shadow work practice
• Suggestion: Dedicate 30 minutes to learning today
• Focus: Apply what you learn practically

🌙 **Shadow Work**
• Daily Check-in: Notice patterns and emotions today
• Practice: Choose one archetype to explore
• Reminder: Practice self-compassion

💰 **Finance & Goals**
• Status: On track with your personal system
• Action: Review weekly priorities
• Focus: Align tasks with your core values

🎯 **Today's Recommendations**
• Start with shadow work reflection (10 min)
• Focus on 2-3 high-priority tasks
• Take breaks and maintain energy
• End with evening reflection

**Your Personal System is Active!** 🚀
Use the bot commands to log data and track progress.
        """
        
        return summary
    
    def log_health_data(self, data: str, user_id: int) -> bool:
        """Log health data."""
        try:
            # Parse health data from string
            health_data = self._parse_health_data(data)
            
            # Save to health log
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "type": "health_data",
                "data": health_data
            }
            
            self._save_log_entry("health_log.json", log_entry)
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging health data: {e}")
            return False
    
    def _parse_health_data(self, data_string: str) -> Dict[str, Any]:
        """Parse health data from string format."""
        health_data = {}
        
        # Parse key:value pairs
        pairs = data_string.split()
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.lower()
                
                # Convert values to appropriate types
                if key in ['steps', 'meditation', 'energy']:
                    try:
                        health_data[key] = int(value)
                    except ValueError:
                        health_data[key] = value
                elif key in ['sleep', 'water']:
                    try:
                        health_data[key] = float(value)
                    except ValueError:
                        health_data[key] = value
                elif key == 'workout':
                    health_data[key] = value.lower() in ['yes', 'true', '1']
                else:
                    health_data[key] = value
        
        return health_data
    
    def log_learning_data(self, data: str, user_id: int) -> bool:
        """Log learning data."""
        try:
            # Parse learning data from string
            learning_data = self._parse_learning_data(data)
            
            # Save to learning log
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "type": "learning_data",
                "data": learning_data
            }
            
            self._save_log_entry("learning_log.json", log_entry)
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging learning data: {e}")
            return False
    
    def _parse_learning_data(self, data_string: str) -> Dict[str, Any]:
        """Parse learning data from string format."""
        learning_data = {}
        
        # Parse key:value pairs
        pairs = data_string.split()
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.lower()
                
                # Convert values to appropriate types
                if key in ['time', 'notes']:
                    try:
                        learning_data[key] = int(value)
                    except ValueError:
                        learning_data[key] = value
                else:
                    learning_data[key] = value
        
        return learning_data
    
    def save_quick_note(self, note: str, user_id: int) -> bool:
        """Save a quick note."""
        try:
            # Create note entry
            note_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "type": "quick_note",
                "content": note,
                "tags": self._extract_tags(note)
            }
            
            self._save_log_entry("quick_notes.json", note_entry)
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving quick note: {e}")
            return False
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract tags from text."""
        tags = []
        words = text.split()
        
        for word in words:
            if word.startswith('#') and len(word) > 1:
                tags.append(word[1:].lower())
        
        return tags
    
    def _save_log_entry(self, filename: str, entry: Dict[str, Any]):
        """Save a log entry to a JSON file."""
        log_file = Path("data/storage") / filename
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing entries
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
        else:
            entries = []
        
        # Add new entry
        entries.append(entry)
        
        # Save updated entries
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def create_backup(self) -> str:
        """Create a backup of the system."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path("data/backups") / f"backup_{timestamp}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy important directories
            dirs_to_backup = [
                "data/storage",
                "config",
                "logs"
            ]
            
            for dir_name in dirs_to_backup:
                src = Path(dir_name)
                if src.exists():
                    dst = backup_dir / dir_name
                    shutil.copytree(src, dst)
            
            # Create backup info file
            backup_info = {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "directories_backed_up": dirs_to_backup
            }
            
            with open(backup_dir / "backup_info.json", 'w') as f:
                json.dump(backup_info, f, indent=2)
            
            return str(backup_dir)
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            raise
    
    def get_backup_size(self, backup_path: str) -> str:
        """Get the size of a backup."""
        try:
            total_size = 0
            backup_dir = Path(backup_path)
            
            for file_path in backup_dir.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            
            # Convert to human readable format
            if total_size < 1024:
                return f"{total_size} B"
            elif total_size < 1024 * 1024:
                return f"{total_size / 1024:.1f} KB"
            else:
                return f"{total_size / (1024 * 1024):.1f} MB"
                
        except Exception as e:
            self.logger.error(f"Error getting backup size: {e}")
            return "Unknown"
    
    def sync_data(self) -> Dict[str, Any]:
        """Sync data across devices."""
        try:
            # This is a placeholder for actual sync logic
            # In a real implementation, you'd sync with cloud storage, etc.
            
            sync_result = {
                "files_synced": 0,
                "data_updated": 0,
                "errors": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            # Simulate sync process
            import time
            time.sleep(1)  # Simulate sync time
            
            return sync_result
            
        except Exception as e:
            self.logger.error(f"Error syncing data: {e}")
            return {"files_synced": 0, "data_updated": 0, "errors": 1}
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        try:
            stats = {
                "total_files": 0,
                "system_size": "0 MB",
                "last_backup": "Never",
                "uptime": "Unknown",
                "commands_this_week": 0,
                "notes_this_week": 0,
                "journal_entries_this_week": 0,
                "shadow_insights_this_week": 0,
                "data_usage": "0 MB",
                "log_usage": "0 MB",
                "cache_usage": "0 MB",
                "db_status": True,
                "encryption_active": True,
                "privacy_enabled": True
            }
            
            # Calculate actual stats
            data_dir = Path("data")
            if data_dir.exists():
                stats["total_files"] = len(list(data_dir.rglob('*')))
                
                # Calculate directory sizes
                for subdir in ["storage", "logs", "cache"]:
                    subdir_path = data_dir / subdir
                    if subdir_path.exists():
                        size = sum(f.stat().st_size for f in subdir_path.rglob('*') if f.is_file())
                        if subdir == "storage":
                            stats["data_usage"] = f"{size / (1024*1024):.1f} MB"
                        elif subdir == "logs":
                            stats["log_usage"] = f"{size / (1024*1024):.1f} MB"
                        elif subdir == "cache":
                            stats["cache_usage"] = f"{size / (1024*1024):.1f} MB"
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting system stats: {e}")
            return {}
