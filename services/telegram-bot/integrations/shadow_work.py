"""
Shadow work integration for the Personal System Telegram Bot.
Connects to the user's shadow work system and provides prompts and logging.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from utils.logger import get_logger


class ShadowWorkIntegration:
    """Integration with the user's shadow work system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = get_logger(__name__)
        self.config = config or {}
        
        # Shadow work prompts from the user's system
        self.prompts = [
            "What am I most afraid to admit about myself?",
            "When do I feel most ashamed or embarrassed?",
            "What do I judge others for that I also do?",
            "What am I avoiding by staying busy?",
            "What would I do if I wasn't afraid?",
            "When do I prioritize systems over people?",
            "Where am I trying to control outcomes too much?",
            "What am I avoiding by focusing on building?",
            "What am I running from?",
            "Where do I avoid deep commitment?",
            "What would I lose if I stayed in one place?",
            "When do I lose myself in others' needs?",
            "Where am I being inauthentic to maintain connections?",
            "What am I afraid of in solitude?",
            "When do I suppress difficult emotions?",
            "Where am I avoiding asking for help?",
            "What am I afraid to feel?",
            "When do I judge others for not meeting my standards?",
            "Where am I being hypocritical?",
            "What am I afraid to admit about my own motivations?",
            "What emotion am I trying to avoid feeling today?",
            "What conversation am I dreading?",
            "What part of myself am I hiding today?",
            "Where did I see my shadow pattern today?",
            "What would it look like to integrate this shadow aspect?",
            "How can I practice self-compassion for this realization?",
            "What is this shadow aspect trying to protect me from?",
            "How can I honor this part of myself?",
            "What would integration look like in practice?",
            "How can I bring more light to this shadow area?"
        ]
        
        # Daily check-in prompts
        self.daily_prompts = [
            "What am I avoiding today?",
            "What emotion am I trying to avoid feeling?",
            "What conversation am I dreading?",
            "What part of myself am I hiding today?",
            "What resistance am I feeling?",
            "What am I afraid to admit to myself?",
            "What am I trying to control that I can't?",
            "What am I running from today?",
            "What am I afraid to feel?",
            "What am I avoiding by staying busy?"
        ]
    
    def get_daily_checkin_prompt(self) -> str:
        """Get a daily check-in prompt based on the current date."""
        # Use date to ensure consistent prompt for the day
        today = datetime.now().strftime("%Y-%m-%d")
        day_number = int(today.split('-')[2])
        return self.daily_prompts[day_number % len(self.daily_prompts)]
    
    def get_random_prompt(self) -> str:
        """Get a random shadow work prompt."""
        return random.choice(self.prompts)
    
    def log_insight(self, insight: str, user_id: int) -> bool:
        """Log a shadow work insight."""
        try:
            # Create shadow work log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "insight": insight,
                "type": "shadow_work_insight"
            }
            
            # Save to shadow work log file
            # Use absolute path from the telegram bot directory
            current_dir = Path(__file__).parent.parent
            log_file = current_dir / "data" / "storage" / "shadow_work_log.json"
            
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing logs
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Add new log entry
            logs.append(log_entry)
            
            # Save updated logs
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Shadow work insight logged for user {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging shadow work insight: {e}")
            return False
    
    def get_recent_insights(self, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent shadow work insights for a user."""
        try:
            # Use absolute path from the telegram bot directory
            current_dir = Path(__file__).parent.parent
            log_file = current_dir / "data" / "storage" / "shadow_work_log.json"
            
            if not log_file.exists():
                return []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Filter by user and sort by timestamp
            user_logs = [log for log in logs if log.get('user_id') == user_id]
            user_logs.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return user_logs[:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting recent insights: {e}")
            return []
    
    def get_insight_stats(self, user_id: int) -> Dict[str, Any]:
        """Get shadow work statistics for a user."""
        try:
            # Use absolute path from the telegram bot directory
            current_dir = Path(__file__).parent.parent
            log_file = current_dir / "data" / "storage" / "shadow_work_log.json"
            
            if not log_file.exists():
                return {
                    "total_insights": 0,
                    "this_week": 0,
                    "this_month": 0,
                    "last_insight": None
                }
            
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Filter by user
            user_logs = [log for log in logs if log.get('user_id') == user_id]
            
            if not user_logs:
                return {
                    "total_insights": 0,
                    "this_week": 0,
                    "this_month": 0,
                    "last_insight": None
                }
            
            # Calculate statistics
            now = datetime.now()
            week_ago = now.replace(day=now.day - 7)
            month_ago = now.replace(month=now.month - 1) if now.month > 1 else now.replace(year=now.year - 1, month=12)
            
            this_week = sum(1 for log in user_logs 
                          if datetime.fromisoformat(log['timestamp']) >= week_ago)
            this_month = sum(1 for log in user_logs 
                           if datetime.fromisoformat(log['timestamp']) >= month_ago)
            
            # Get last insight
            user_logs.sort(key=lambda x: x['timestamp'], reverse=True)
            last_insight = user_logs[0]['timestamp'] if user_logs else None
            
            return {
                "total_insights": len(user_logs),
                "this_week": this_week,
                "this_month": this_month,
                "last_insight": last_insight
            }
            
        except Exception as e:
            self.logger.error(f"Error getting insight stats: {e}")
            return {
                "total_insights": 0,
                "this_week": 0,
                "this_month": 0,
                "last_insight": None
            }
