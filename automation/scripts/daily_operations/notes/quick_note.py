#!/usr/bin/env python3
"""
Quick Note - Rapid note capture and management
Part of the Personal System automation suite.
"""

import json
import os
import sys
import re
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the automation directory to the path
sys.path.append(str(Path(__file__).parent.parent))

class QuickNote:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "outputs"
        self.notes_file = self.data_dir / "quick_notes.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists with proper structure."""
        if not self.notes_file.exists():
            self.notes_file.parent.mkdir(exist_ok=True)
            with open(self.notes_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load notes data from file."""
        try:
            with open(self.notes_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict[str, Any]]):
        """Save notes data to file."""
        with open(self.notes_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_note_id(self, data: List[Dict[str, Any]]) -> str:
        """Generate a unique note ID."""
        existing_ids = [note.get('id', '') for note in data]
        counter = 1
        while f"note_{counter:04d}" in existing_ids:
            counter += 1
        return f"note_{counter:04d}"
    
    def _auto_categorize(self, content: str) -> str:
        """Auto-categorize note based on content."""
        content_lower = content.lower()
        
        # Health-related keywords
        health_keywords = ['health', 'exercise', 'workout', 'sleep', 'diet', 'meditation', 'stress', 'energy', 'mood']
        if any(keyword in content_lower for keyword in health_keywords):
            return 'health'
        
        # Learning-related keywords
        learning_keywords = ['learn', 'study', 'course', 'book', 'reading', 'skill', 'knowledge', 'education']
        if any(keyword in content_lower for keyword in learning_keywords):
            return 'learning'
        
        # Work-related keywords
        work_keywords = ['work', 'job', 'career', 'project', 'meeting', 'deadline', 'task', 'business']
        if any(keyword in content_lower for keyword in work_keywords):
            return 'work'
        
        # Personal-related keywords
        personal_keywords = ['family', 'friend', 'relationship', 'personal', 'life', 'goal', 'dream']
        if any(keyword in content_lower for keyword in personal_keywords):
            return 'personal'
        
        # Idea-related keywords
        idea_keywords = ['idea', 'think', 'thought', 'concept', 'innovation', 'creative', 'inspiration']
        if any(keyword in content_lower for keyword in idea_keywords):
            return 'idea'
        
        # Task-related keywords
        task_keywords = ['todo', 'task', 'reminder', 'do', 'need to', 'should', 'must']
        if any(keyword in content_lower for keyword in task_keywords):
            return 'task'
        
        return 'general'
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content."""
        # Look for hashtags
        hashtags = re.findall(r'#(\w+)', content)
        
        # Look for common patterns
        tags = []
        
        # Time-related tags
        if re.search(r'\b(today|tomorrow|yesterday|this week|next week)\b', content.lower()):
            tags.append('time-sensitive')
        
        # Priority tags
        if re.search(r'\b(urgent|important|priority|asap)\b', content.lower()):
            tags.append('priority')
        
        # Action tags
        if re.search(r'\b(action|follow-up|call|email|meeting)\b', content.lower()):
            tags.append('action-required')
        
        # Combine hashtags and extracted tags
        all_tags = list(set(hashtags + tags))
        return all_tags[:5]  # Limit to 5 tags
    
    def capture_note(self, content: str, category: str = "", tags: List[str] = None, 
                    priority: str = "medium") -> Dict[str, Any]:
        """Capture a quick note."""
        data = self._load_data()
        
        note_id = self._generate_note_id(data)
        
        # Auto-categorize if not provided
        if not category:
            category = self._auto_categorize(content)
        
        # Extract tags if not provided
        if not tags:
            tags = self._extract_tags(content)
        
        note = {
            'id': note_id,
            'content': content,
            'category': category,
            'tags': tags,
            'priority': priority.lower(),
            'created_date': date.today().isoformat(),
            'created_timestamp': datetime.now().isoformat(),
            'updated_timestamp': datetime.now().isoformat(),
            'status': 'active'
        }
        
        data.append(note)
        self._save_data(data)
        
        return {
            'success': True,
            'message': f"Note captured: {content[:50]}{'...' if len(content) > 50 else ''}",
            'note': note
        }
    
    def get_note(self, note_id: str) -> Dict[str, Any]:
        """Get a specific note."""
        data = self._load_data()
        
        for note in data:
            if note['id'] == note_id:
                return {
                    'success': True,
                    'message': f"Note found: {note['content'][:50]}{'...' if len(note['content']) > 50 else ''}",
                    'note': note
                }
        
        return {
            'success': False,
            'message': f"Note {note_id} not found"
        }
    
    def update_note(self, note_id: str, content: str = "", category: str = "", 
                   tags: List[str] = None, priority: str = "") -> Dict[str, Any]:
        """Update a note."""
        data = self._load_data()
        
        for note in data:
            if note['id'] == note_id:
                if content:
                    note['content'] = content
                if category:
                    note['category'] = category
                if tags:
                    note['tags'] = tags
                if priority:
                    note['priority'] = priority.lower()
                
                note['updated_timestamp'] = datetime.now().isoformat()
                self._save_data(data)
                
                return {
                    'success': True,
                    'message': f"Note updated: {note['content'][:50]}{'...' if len(note['content']) > 50 else ''}",
                    'note': note
                }
        
        return {
            'success': False,
            'message': f"Note {note_id} not found"
        }
    
    def delete_note(self, note_id: str) -> Dict[str, Any]:
        """Delete a note."""
        data = self._load_data()
        
        for i, note in enumerate(data):
            if note['id'] == note_id:
                deleted_note = data.pop(i)
                self._save_data(data)
                
                return {
                    'success': True,
                    'message': f"Note deleted: {deleted_note['content'][:50]}{'...' if len(deleted_note['content']) > 50 else ''}",
                    'note': deleted_note
                }
        
        return {
            'success': False,
            'message': f"Note {note_id} not found"
        }
    
    def list_notes(self, category: str = "all", priority: str = "all", 
                  tags: List[str] = None, limit: int = 20) -> Dict[str, Any]:
        """List notes with optional filters."""
        data = self._load_data()
        
        # Apply filters
        filtered_notes = []
        for note in data:
            if note['status'] != 'active':
                continue
            
            # Category filter
            if category != "all" and note['category'] != category:
                continue
            
            # Priority filter
            if priority != "all" and note['priority'] != priority:
                continue
            
            # Tags filter
            if tags:
                if not any(tag in note['tags'] for tag in tags):
                    continue
            
            filtered_notes.append(note)
        
        # Sort by creation date (newest first)
        filtered_notes.sort(key=lambda x: x['created_timestamp'], reverse=True)
        
        # Apply limit
        if limit > 0:
            filtered_notes = filtered_notes[:limit]
        
        # Generate summary
        summary = []
        if filtered_notes:
            summary.append(f"📝 Total notes: {len(filtered_notes)}")
            
            # Category breakdown
            categories = {}
            for note in filtered_notes:
                cat = note['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in categories.items():
                summary.append(f"📂 {cat.title()}: {count}")
        else:
            summary.append("📝 No notes found")
        
        return {
            'success': True,
            'message': f"Notes list ({len(filtered_notes)} found)",
            'notes': filtered_notes,
            'summary': summary,
            'filters': {
                'category': category,
                'priority': priority,
                'tags': tags,
                'limit': limit
            }
        }
    
    def search_notes(self, query: str, category: str = "all") -> Dict[str, Any]:
        """Search notes by content."""
        data = self._load_data()
        
        query_lower = query.lower()
        matching_notes = []
        
        for note in data:
            if note['status'] != 'active':
                continue
            
            # Category filter
            if category != "all" and note['category'] != category:
                continue
            
            # Search in content, tags, and category
            if (query_lower in note['content'].lower() or
                query_lower in ' '.join(note['tags']).lower() or
                query_lower in note['category'].lower()):
                matching_notes.append(note)
        
        # Sort by relevance (exact matches first, then partial matches)
        matching_notes.sort(key=lambda x: (
            query_lower in x['content'].lower(),
            x['created_timestamp']
        ), reverse=True)
        
        return {
            'success': True,
            'message': f"Search results for '{query}' ({len(matching_notes)} found)",
            'query': query,
            'notes': matching_notes,
            'count': len(matching_notes)
        }
    
    def get_today_notes(self) -> Dict[str, Any]:
        """Get today's notes."""
        data = self._load_data()
        today = date.today().isoformat()
        
        today_notes = [note for note in data 
                      if note.get('created_date') == today and note['status'] == 'active']
        
        # Sort by creation time
        today_notes.sort(key=lambda x: x['created_timestamp'], reverse=True)
        
        summary = []
        if today_notes:
            summary.append(f"📝 Notes today: {len(today_notes)}")
            
            # Category breakdown
            categories = {}
            for note in today_notes:
                cat = note['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in categories.items():
                summary.append(f"📂 {cat.title()}: {count}")
        else:
            summary.append("📝 No notes captured today")
        
        return {
            'success': True,
            'message': f"Today's notes ({len(today_notes)} found)",
            'date': today,
            'notes': today_notes,
            'summary': summary
        }
    
    def get_note_stats(self) -> Dict[str, Any]:
        """Get note statistics."""
        data = self._load_data()
        
        if not data:
            return {
                'success': True,
                'message': "No notes found",
                'stats': {
                    'total': 0,
                    'active': 0,
                    'categories': {},
                    'tags': {}
                }
            }
        
        total = len(data)
        active = sum(1 for note in data if note['status'] == 'active')
        
        # Category breakdown
        categories = {}
        for note in data:
            if note['status'] == 'active':
                cat = note['category']
                categories[cat] = categories.get(cat, 0) + 1
        
        # Tag breakdown
        tags = {}
        for note in data:
            if note['status'] == 'active':
                for tag in note['tags']:
                    tags[tag] = tags.get(tag, 0) + 1
        
        # Recent activity (last 7 days)
        recent_count = 0
        week_ago = (date.today() - timedelta(days=7)).isoformat()
        for note in data:
            if note.get('created_date', '') >= week_ago:
                recent_count += 1
        
        summary = []
        summary.append(f"📝 Total notes: {total}")
        summary.append(f"📋 Active notes: {active}")
        summary.append(f"📅 Notes this week: {recent_count}")
        
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1])
            summary.append(f"📂 Top category: {top_category[0]} ({top_category[1]})")
        
        return {
            'success': True,
            'message': "Note statistics",
            'stats': {
                'total': total,
                'active': active,
                'categories': categories,
                'tags': tags,
                'recent_count': recent_count
            },
            'summary': summary
        }

def main():
    """Main entry point."""
    note = QuickNote()
    
    if len(sys.argv) < 2:
        print("Usage: python quick_note.py <action> [args...]")
        print("Actions:")
        print("  capture <content> [category] [tags] [priority] - Capture a quick note")
        print("  get <note_id> - Get a specific note")
        print("  update <note_id> <content> [category] [tags] [priority] - Update a note")
        print("  delete <note_id> - Delete a note")
        print("  list [category] [priority] [limit] - List notes")
        print("  search <query> [category] - Search notes")
        print("  today - Get today's notes")
        print("  stats - Get note statistics")
        return
    
    action = sys.argv[1]
    
    if action == "capture":
        if len(sys.argv) < 3:
            print("Usage: python quick_note.py capture <content> [category] [tags] [priority]")
            return
        
        content = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else ""
        tags = sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] else []
        priority = sys.argv[5] if len(sys.argv) > 5 else "medium"
        
        result = note.capture_note(content, category, tags, priority)
        print(json.dumps(result, indent=2))
    
    elif action == "get":
        if len(sys.argv) < 3:
            print("Usage: python quick_note.py get <note_id>")
            return
        
        note_id = sys.argv[2]
        result = note.get_note(note_id)
        print(json.dumps(result, indent=2))
    
    elif action == "update":
        if len(sys.argv) < 4:
            print("Usage: python quick_note.py update <note_id> <content> [category] [tags] [priority]")
            return
        
        note_id = sys.argv[2]
        content = sys.argv[3]
        category = sys.argv[4] if len(sys.argv) > 4 else ""
        tags = sys.argv[5].split(',') if len(sys.argv) > 5 and sys.argv[5] else []
        priority = sys.argv[6] if len(sys.argv) > 6 else ""
        
        result = note.update_note(note_id, content, category, tags, priority)
        print(json.dumps(result, indent=2))
    
    elif action == "delete":
        if len(sys.argv) < 3:
            print("Usage: python quick_note.py delete <note_id>")
            return
        
        note_id = sys.argv[2]
        result = note.delete_note(note_id)
        print(json.dumps(result, indent=2))
    
    elif action == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else "all"
        priority = sys.argv[3] if len(sys.argv) > 3 else "all"
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        
        result = note.list_notes(category, priority, limit=limit)
        print(json.dumps(result, indent=2))
    
    elif action == "search":
        if len(sys.argv) < 3:
            print("Usage: python quick_note.py search <query> [category]")
            return
        
        query = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "all"
        
        result = note.search_notes(query, category)
        print(json.dumps(result, indent=2))
    
    elif action == "today":
        result = note.get_today_notes()
        print(json.dumps(result, indent=2))
    
    elif action == "stats":
        result = note.get_note_stats()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
