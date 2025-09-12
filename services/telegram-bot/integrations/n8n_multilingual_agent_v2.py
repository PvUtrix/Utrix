"""
n8n Multilingual AI Agent Integration (v2)
Simplified version using the n8n framework
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from utils.logger import get_logger

# Import the n8n framework
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "automation" / "integrations"))
from n8n_framework import N8nIntegration


class N8nMultilingualAgent:
    """n8n-powered multilingual AI agent for intent detection and response generation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(__name__)
        
        # Initialize n8n integration using the framework
        n8n_config = config.get('n8n', {})
        self.integration = N8nIntegration(n8n_config)
        
        # Fallback to local processing if n8n is not available
        self.fallback_enabled = n8n_config.get('fallback_enabled', True)
        
        # User context cache
        self.user_context_cache = {}
    
    async def process_message(self, text: str, user_id: int, message_type: str = "text") -> Dict[str, Any]:
        """
        Process a message through the n8n multilingual agent.
        
        Args:
            text: The message text (transcribed or typed)
            user_id: User ID for context
            message_type: "text" or "voice"
            
        Returns:
            Dict containing intent, confidence, response, and metadata
        """
        try:
            # Get user context
            user_context = await self._get_user_context(user_id)
            
            # Prepare payload for n8n
            payload = {
                "text": text,
                "user_id": user_id,
                "message_type": message_type,
                "timestamp": datetime.now().isoformat(),
                "context": user_context,
                "language_hint": self._detect_language_hint(text)
            }
            
            # Send to n8n workflow using the framework
            response = await self.integration.call_webhook("multilingual-intent", payload)
            
            if response:
                return self._process_n8n_response(response)
            else:
                # Fallback to local processing
                return await self._fallback_processing(text, user_id, message_type)
                
        except Exception as e:
            self.logger.error(f"Error processing message with n8n: {e}")
            if self.fallback_enabled:
                return await self._fallback_processing(text, user_id, message_type)
            else:
                return self._create_error_response(str(e))
    
    def _detect_language_hint(self, text: str) -> str:
        """Simple language detection based on character patterns."""
        # Check for Cyrillic characters (Russian, Ukrainian, etc.)
        if any('\u0400' <= char <= '\u04FF' for char in text):
            return "ru"
        
        # Check for common Russian words
        russian_words = ['что', 'какие', 'сегодня', 'задачи', 'проекты', 'здоровье', 'обучение', 'теневая', 'архетипы']
        if any(word in text.lower() for word in russian_words):
            return "ru"
        
        # Check for common English words
        english_words = ['what', 'how', 'when', 'where', 'why', 'today', 'tasks', 'projects', 'health', 'learning']
        if any(word in text.lower() for word in english_words):
            return "en"
        
        return "auto"
    
    async def _get_user_context(self, user_id: int) -> Dict[str, Any]:
        """Get user context for better intent detection."""
        if user_id in self.user_context_cache:
            return self.user_context_cache[user_id]
        
        # Load user's personal system data
        context = {
            "user_id": user_id,
            "preferred_language": "en",  # Default
            "recent_activities": [],
            "current_projects": [],
            "shadow_work_progress": {},
            "health_metrics": {},
            "learning_progress": {}
        }
        
        try:
            # Load from user's data files
            base_path = Path(self.config.get('paths', {}).get('base_path', '../../../'))
            
            # Load recent activities
            tasks_file = base_path / "automation/outputs/tasks.json"
            if tasks_file.exists():
                import json
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                    context["current_projects"] = tasks_data.get('active_tasks', [])[:5]
            
            # Load shadow work data
            shadow_file = base_path / "automation/outputs/shadow_work_data.json"
            if shadow_file.exists():
                with open(shadow_file, 'r', encoding='utf-8') as f:
                    shadow_data = json.load(f)
                    context["shadow_work_progress"] = shadow_data.get('progress', {})
            
            # Load health data
            health_file = base_path / "automation/outputs/health_data.json"
            if health_file.exists():
                with open(health_file, 'r', encoding='utf-8') as f:
                    health_data = json.load(f)
                    context["health_metrics"] = health_data.get('metrics', {})
            
        except Exception as e:
            self.logger.warning(f"Could not load user context: {e}")
        
        # Cache the context
        self.user_context_cache[user_id] = context
        return context
    
    def _process_n8n_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process the response from n8n workflow."""
        return {
            "intent": response.get("intent", "unknown"),
            "confidence": response.get("confidence", 0.5),
            "response_text": response.get("response", ""),
            "action": response.get("action", {}),
            "language": response.get("language", "en"),
            "metadata": response.get("metadata", {}),
            "source": "n8n"
        }
    
    async def _fallback_processing(self, text: str, user_id: int, message_type: str) -> Dict[str, Any]:
        """Fallback processing when n8n is not available."""
        try:
            from .ai_assistant import AIAssistant
            
            # Use existing AI assistant as fallback
            ai_assistant = AIAssistant(self.config)
        except Exception as e:
            self.logger.error(f"Failed to import AI assistant: {e}")
            return self._create_error_response("Fallback processing failed")
        
        # Simple multilingual pattern matching
        text_lower = text.lower()
        
        # Russian patterns
        russian_patterns = {
            "tasks": ["задачи", "что делать", "сегодня", "проекты", "работать", "приоритеты"],
            "health": ["здоровье", "фитнес", "спорт", "тренировка", "шаги", "сон"],
            "learning": ["обучение", "изучение", "курс", "книга", "учеба", "знания"],
            "shadow_work": ["теневая работа", "архетипы", "саморазвитие", "тень", "архетип"],
            "journal": ["журнал", "запись", "дневник", "размышления", "заметки"],
            "goals": ["цели", "достижения", "прогресс", "результаты"],
            "values": ["ценности", "принципы", "жизнь", "направление"]
        }
        
        # English patterns (existing)
        english_patterns = {
            "tasks": ["project", "work on", "priority", "today", "list my projects", "task", "todo"],
            "health": ["health", "fitness", "wellness", "exercise", "workout", "steps", "sleep"],
            "learning": ["learn", "study", "education", "course", "book", "knowledge"],
            "shadow_work": ["shadow", "archetype", "archetypes", "personal growth", "development"],
            "journal": ["journal", "pattern", "insight", "entry", "reflection"],
            "goals": ["goal", "progress", "achievement", "results"],
            "values": ["value", "values", "core values", "principles", "direction"]
        }
        
        # Detect language and match patterns
        detected_language = self._detect_language_hint(text)
        
        if detected_language == "ru":
            patterns = russian_patterns
        else:
            patterns = english_patterns
        
        # Find matching intent
        matched_intent = "unknown"
        confidence = 0.0
        
        for intent, keywords in patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    matched_intent = intent
                    confidence = 0.8
                    break
            if matched_intent != "unknown":
                break
        
        # Get response from AI assistant
        response_text = await ai_assistant.get_response(text, user_id)
        
        return {
            "intent": matched_intent,
            "confidence": confidence,
            "response_text": response_text,
            "action": {},
            "language": detected_language,
            "metadata": {"fallback": True},
            "source": "fallback"
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "intent": "error",
            "confidence": 1.0,
            "response_text": f"Sorry, I encountered an error: {error_message}",
            "action": {},
            "language": "en",
            "metadata": {"error": True},
            "source": "error"
        }
    
    async def setup_workflow(self) -> bool:
        """Setup the multilingual intent detection workflow using the framework."""
        try:
            return await self.integration.setup_multilingual_intent()
        except Exception as e:
            self.logger.error(f"Error setting up workflow: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test connection to n8n."""
        return await self.integration.test_connection()
