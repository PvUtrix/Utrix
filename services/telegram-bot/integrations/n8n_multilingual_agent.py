"""
n8n Multilingual AI Agent Integration
Handles complex multilingual intent detection using existing n8n instance via API
Now uses the n8n framework for better maintainability and reusability
"""

import asyncio
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
        
        # Test connection on initialization
        asyncio.create_task(self._test_connection())
    
    async def _test_connection(self):
        """Test connection to n8n instance."""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.n8n_base_url}/api/v1/active")
                if response.status_code == 200:
                    self.logger.info("✅ Connected to n8n instance successfully")
                else:
                    self.logger.warning(f"⚠️ n8n connection test returned status {response.status_code}")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not connect to n8n: {e}")
    
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
            
            # Send to n8n workflow
            response = await self._send_to_n8n(payload)
            
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
    
    async def _send_to_n8n(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send request to n8n workflow."""
        try:
            headers = {"Content-Type": "application/json"}
            
            # Add authentication if available
            if self.n8n_api_key:
                headers["Authorization"] = f"Bearer {self.n8n_api_key}"
            elif self.n8n_username and self.n8n_password:
                # Basic auth
                import base64
                credentials = base64.b64encode(f"{self.n8n_username}:{self.n8n_password}".encode()).decode()
                headers["Authorization"] = f"Basic {credentials}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.n8n_webhook_url,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    self.logger.warning(f"n8n returned status {response.status_code}: {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            self.logger.warning("n8n request timed out")
            return None
        except Exception as e:
            self.logger.error(f"Error sending to n8n: {e}")
            return None
    
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
        from .ai_assistant import AIAssistant
        
        # Use existing AI assistant as fallback
        ai_assistant = AIAssistant(self.config)
        
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
    
    async def create_workflow(self) -> bool:
        """Create the multilingual intent detection workflow in n8n."""
        try:
            workflow_data = {
                "name": "Multilingual Intent Detection",
                "nodes": [
                    {
                        "parameters": {
                            "httpMethod": "POST",
                            "path": "multilingual-intent",
                            "responseMode": "responseNode",
                            "options": {}
                        },
                        "id": "webhook-trigger",
                        "name": "Webhook Trigger",
                        "type": "n8n-nodes-base.webhook",
                        "typeVersion": 1,
                        "position": [240, 300]
                    },
                    {
                        "parameters": {
                            "jsCode": "// Extract data from webhook\nconst text = $input.first().json.text;\nconst user_id = $input.first().json.user_id;\nconst context = $input.first().json.context;\nconst language_hint = $input.first().json.language_hint;\n\n// Prepare data for AI processing\nreturn {\n  text: text,\n  user_id: user_id,\n  context: context,\n  language_hint: language_hint,\n  timestamp: new Date().toISOString()\n};"
                        },
                        "id": "data-extractor",
                        "name": "Extract Data",
                        "type": "n8n-nodes-base.code",
                        "typeVersion": 2,
                        "position": [460, 300]
                    },
                    {
                        "parameters": {
                            "model": "gpt-4o",
                            "options": {
                                "temperature": 0.3,
                                "maxTokens": 1000
                            },
                            "messages": {
                                "values": [
                                    {
                                        "role": "system",
                                        "content": "You are a multilingual personal assistant that understands user intent in multiple languages. Analyze the user's message and determine their intent.\n\nSupported intents:\n- tasks: Questions about tasks, projects, what to work on today\n- health: Health tracking, fitness, wellness questions\n- learning: Learning progress, courses, education\n- shadow_work: Shadow work, archetypes, personal development\n- journal: Journal entries, patterns, insights\n- goals: Goals, progress, achievements\n- values: Core values, life direction\n- help: General help, what can you do\n- unknown: Unclear or unrecognized intent\n\nRespond with a JSON object containing:\n- intent: The detected intent\n- confidence: Confidence score (0-1)\n- language: Detected language (en, ru, etc.)\n- response: A helpful response in the user's language\n- action: Any specific action to take\n- reasoning: Brief explanation of the intent detection"
                                    },
                                    {
                                        "role": "user",
                                        "content": "User message: \"{{ $json.text }}\"\nUser context: {{ JSON.stringify($json.context) }}\nLanguage hint: {{ $json.language_hint }}\n\nDetect the intent and provide a helpful response in the user's language."
                                    }
                                ]
                            }
                        },
                        "id": "ai-intent-detection",
                        "name": "AI Intent Detection",
                        "type": "n8n-nodes-base.openAi",
                        "typeVersion": 1,
                        "position": [680, 300]
                    },
                    {
                        "parameters": {
                            "jsCode": "// Parse AI response and structure the output\nconst aiResponse = $input.first().json.choices[0].message.content;\n\nlet parsedResponse;\ntry {\n  // Try to parse as JSON first\n  parsedResponse = JSON.parse(aiResponse);\n} catch (e) {\n  // If not JSON, create a structured response\n  parsedResponse = {\n    intent: \"unknown\",\n    confidence: 0.5,\n    language: \"en\",\n    response: aiResponse,\n    action: {},\n    reasoning: \"Could not parse AI response as JSON\"\n  };\n}\n\n// Add metadata\nparsedResponse.metadata = {\n  processed_at: new Date().toISOString(),\n  user_id: $('Extract Data').first().json.user_id,\n  original_text: $('Extract Data').first().json.text\n};\n\nreturn parsedResponse;"
                        },
                        "id": "response-processor",
                        "name": "Process Response",
                        "type": "n8n-nodes-base.code",
                        "typeVersion": 2,
                        "position": [900, 300]
                    },
                    {
                        "parameters": {
                            "respondWith": "json",
                            "responseBody": "={{ $json }}"
                        },
                        "id": "webhook-response",
                        "name": "Webhook Response",
                        "type": "n8n-nodes-base.respondToWebhook",
                        "typeVersion": 1,
                        "position": [1120, 300]
                    }
                ],
                "connections": {
                    "Webhook Trigger": {
                        "main": [
                            [
                                {
                                    "node": "Extract Data",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    },
                    "Extract Data": {
                        "main": [
                            [
                                {
                                    "node": "AI Intent Detection",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    },
                    "AI Intent Detection": {
                        "main": [
                            [
                                {
                                    "node": "Process Response",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    },
                    "Process Response": {
                        "main": [
                            [
                                {
                                    "node": "Webhook Response",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    }
                },
                "active": True,
                "settings": {
                    "executionOrder": "v1"
                }
            }
            
            headers = {"Content-Type": "application/json"}
            if self.n8n_api_key:
                headers["Authorization"] = f"Bearer {self.n8n_api_key}"
            elif self.n8n_username and self.n8n_password:
                import base64
                credentials = base64.b64encode(f"{self.n8n_username}:{self.n8n_password}".encode()).decode()
                headers["Authorization"] = f"Basic {credentials}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.n8n_api_url}/workflows",
                    json=workflow_data,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    self.logger.info("✅ Successfully created multilingual intent detection workflow in n8n")
                    return True
                else:
                    self.logger.error(f"Failed to create workflow: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error creating n8n workflow: {e}")
            return False
