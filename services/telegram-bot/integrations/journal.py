"""
Journal integration for the Personal System Telegram Bot.
Handles journal entries, ideas, and task management.
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from utils.logger import get_logger


class JournalIntegration:
    """Integration with the user's journal system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = get_logger(__name__)
        self.config = config or {}
        self.journal_path = Path(config.get('paths', {}).get('journal', '../../../knowledge/journal/'))
        self.notes_path = Path(config.get('paths', {}).get('notes', '../../../knowledge/notes/'))
    
    def create_entry(self, content: str, user_id: int) -> bool:
        """Create a journal entry."""
        try:
            # Create journal entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "type": "journal_entry",
                "content": content,
                "tags": self._extract_tags(content),
                "mood": self._extract_mood(content),
                "word_count": len(content.split())
            }
            
            # Save to journal log
            self._save_log_entry("journal_entries.json", entry)
            
            # Also save to daily journal file
            self._save_to_daily_journal(content)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating journal entry: {e}")
            return False
    
    def save_idea(self, idea: str, user_id: int) -> bool:
        """Save an idea."""
        try:
            # Create idea entry
            idea_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "type": "idea",
                "content": idea,
                "tags": self._extract_tags(idea),
                "category": self._categorize_idea(idea),
                "priority": self._extract_priority(idea)
            }
            
            # Save to ideas log
            self._save_log_entry("ideas.json", idea_entry)
            
            # Also save to ideas file
            self._save_to_ideas_file(idea)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving idea: {e}")
            return False
    
    def add_task(self, task: str, user_id: int) -> bool:
        """Add a task."""
        try:
            # Parse task details
            task_details = self._parse_task(task)
            
            # Create task entry
            task_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "type": "task",
                "content": task,
                "title": task_details.get('title', task),
                "priority": task_details.get('priority', 'medium'),
                "category": task_details.get('category', 'general'),
                "due_date": task_details.get('due_date'),
                "status": "pending",
                "tags": self._extract_tags(task)
            }
            
            # Save to tasks log
            self._save_log_entry("tasks.json", task_entry)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding task: {e}")
            return False
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract tags from text."""
        tags = []
        words = text.split()
        
        for word in words:
            if word.startswith('#') and len(word) > 1:
                tags.append(word[1:].lower())
        
        return tags
    
    def _extract_mood(self, text: str) -> Optional[str]:
        """Extract mood from text."""
        mood_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing'],
            'sad': ['sad', 'depressed', 'down', 'blue', 'miserable'],
            'angry': ['angry', 'frustrated', 'mad', 'irritated', 'annoyed'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense'],
            'calm': ['calm', 'peaceful', 'relaxed', 'content', 'serene'],
            'energetic': ['energetic', 'motivated', 'pumped', 'enthusiastic'],
            'tired': ['tired', 'exhausted', 'drained', 'fatigued', 'weary']
        }
        
        text_lower = text.lower()
        for mood, keywords in mood_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return mood
        
        return None
    
    def _categorize_idea(self, idea: str) -> str:
        """Categorize an idea."""
        idea_lower = idea.lower()
        
        categories = {
            'business': ['business', 'startup', 'company', 'entrepreneur', 'profit', 'market'],
            'creative': ['creative', 'art', 'design', 'write', 'paint', 'music', 'film'],
            'technology': ['app', 'software', 'tech', 'programming', 'code', 'ai', 'ml'],
            'health': ['health', 'fitness', 'exercise', 'diet', 'wellness', 'meditation'],
            'learning': ['learn', 'study', 'course', 'education', 'skill', 'knowledge'],
            'personal': ['personal', 'relationship', 'family', 'friend', 'love'],
            'productivity': ['productivity', 'efficiency', 'organization', 'system', 'workflow']
        }
        
        for category, keywords in categories.items():
            if any(keyword in idea_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _extract_priority(self, text: str) -> str:
        """Extract priority from text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['urgent', 'asap', 'critical', 'high priority']):
            return 'high'
        elif any(word in text_lower for word in ['low priority', 'someday', 'maybe']):
            return 'low'
        else:
            return 'medium'
    
    def _parse_task(self, task: str) -> Dict[str, Any]:
        """Parse task details from string."""
        task_details = {
            'title': task,
            'priority': 'medium',
            'category': 'general',
            'due_date': None
        }
        
        # Extract priority
        priority_match = re.search(r'\((high|medium|low)\)', task.lower())
        if priority_match:
            task_details['priority'] = priority_match.group(1)
        
        # Extract due date
        due_match = re.search(r'\(due:\s*([^)]+)\)', task.lower())
        if due_match:
            due_text = due_match.group(1)
            task_details['due_date'] = self._parse_due_date(due_text)
        
        # Extract category
        category_match = re.search(r'\(([^)]+)\)', task.lower())
        if category_match:
            category = category_match.group(1)
            if category not in ['high', 'medium', 'low'] and 'due:' not in category:
                task_details['category'] = category
        
        # Clean title
        title = re.sub(r'\([^)]*\)', '', task).strip()
        task_details['title'] = title
        
        return task_details
    
    def _parse_due_date(self, due_text: str) -> Optional[str]:
        """Parse due date from text."""
        due_text = due_text.lower()
        
        if 'tomorrow' in due_text:
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.strftime('%Y-%m-%d')
        elif 'next week' in due_text:
            next_week = datetime.now() + timedelta(days=7)
            return next_week.strftime('%Y-%m-%d')
        elif 'next month' in due_text:
            # Simple next month calculation
            current_month = datetime.now().month
            current_year = datetime.now().year
            if current_month == 12:
                next_month = datetime(current_year + 1, 1, 1)
            else:
                next_month = datetime(current_year, current_month + 1, 1)
            return next_month.strftime('%Y-%m-%d')
        
        return None
    
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
    
    def _save_to_daily_journal(self, content: str):
        """Save to daily journal file."""
        try:
            today = datetime.now()
            year_dir = self.journal_path / str(today.year)
            month_dir = year_dir / f"{today.month:02d}"
            
            month_dir.mkdir(parents=True, exist_ok=True)
            
            journal_file = month_dir / f"{today.strftime('%Y-%m-%d')}.md"
            
            # Create or append to journal file
            with open(journal_file, 'a', encoding='utf-8') as f:
                f.write(f"\n## {today.strftime('%H:%M')}\n\n{content}\n\n")
                
        except Exception as e:
            self.logger.error(f"Error saving to daily journal: {e}")
    
    def _save_to_ideas_file(self, idea: str):
        """Save to ideas file."""
        try:
            ideas_file = self.notes_path / "quick" / "ideas.md"
            ideas_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create or append to ideas file
            with open(ideas_file, 'a', encoding='utf-8') as f:
                f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{idea}\n\n")
                
        except Exception as e:
            self.logger.error(f"Error saving to ideas file: {e}")
    
    def get_recent_entries(self, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent journal entries for a user."""
        try:
            log_file = Path("data/storage") / "journal_entries.json"
            
            if not log_file.exists():
                return []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            # Filter by user and sort by timestamp
            user_entries = [entry for entry in entries if entry.get('user_id') == user_id]
            user_entries.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return user_entries[:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting recent entries: {e}")
            return []
    
    def get_ideas(self, user_id: int, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get ideas for a user, optionally filtered by category."""
        try:
            log_file = Path("data/storage") / "ideas.json"
            
            if not log_file.exists():
                return []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                ideas = json.load(f)
            
            # Filter by user
            user_ideas = [idea for idea in ideas if idea.get('user_id') == user_id]
            
            # Filter by category if specified
            if category:
                user_ideas = [idea for idea in user_ideas if idea.get('category') == category]
            
            # Sort by timestamp
            user_ideas.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return user_ideas
            
        except Exception as e:
            self.logger.error(f"Error getting ideas: {e}")
            return []
    
    def get_tasks(self, user_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks for a user, optionally filtered by status."""
        try:
            log_file = Path("data/storage") / "tasks.json"
            
            if not log_file.exists():
                return []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            
            # Filter by user
            user_tasks = [task for task in tasks if task.get('user_id') == user_id]
            
            # Filter by status if specified
            if status:
                user_tasks = [task for task in user_tasks if task.get('status') == status]
            
            # Sort by priority and timestamp
            user_tasks.sort(key=lambda x: (x.get('priority', 'medium'), x['timestamp']), reverse=True)
            
            return user_tasks
            
        except Exception as e:
            self.logger.error(f"Error getting tasks: {e}")
            return []
