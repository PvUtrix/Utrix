"""
Simple Multilingual AI Agent
A working version that handles multilingual intent detection with fallback
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from utils.logger import get_logger


class SimpleMultilingualAgent:
    """Simple multilingual AI agent for intent detection and response generation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(__name__)
        self.fallback_enabled = config.get('n8n', {}).get('fallback_enabled', True)
        
    async def process_message(self, text: str, user_id: int, message_type: str = "text") -> Dict[str, Any]:
        """Process a message and return intent detection results."""
        try:
            # Simple multilingual pattern matching
            result = await self._simple_intent_detection(text, user_id, message_type)
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return self._create_error_response("Processing failed")
    
    async def _simple_intent_detection(self, text: str, user_id: int, message_type: str) -> Dict[str, Any]:
        """Simple multilingual intent detection using pattern matching."""
        text_lower = text.lower()
        
        # Russian patterns
        russian_patterns = {
            'tasks': ['задачи', 'задач', 'задачу', 'работа', 'дела', 'сегодня', 'что делать', 'приоритет', 'подготовить', 'презентацию', 'презентация', 'встрече', 'встреча', 'встречи', 'проект', 'проекты', 'планировать', 'планирование'],
            'health': ['здоровье', 'здоровья', 'фитнес', 'тренировка', 'спорт', 'вес', 'диета', 'шаги', 'сон', 'настроение', 'энергия', 'вода', 'упражнения'],
            'learning': ['учёба', 'обучение', 'курс', 'курсы', 'изучение', 'знания', 'прогресс', 'изучил', 'изучал', 'книга', 'статья', 'видео', 'урок'],
            'shadow_work': ['тень', 'архетип', 'архетипы', 'теневая работа', 'саморазвитие', 'теневая', 'работа'],
            'journal': ['журнал', 'дневник', 'запись', 'записи', 'размышления', 'паттерны', 'заметка', 'заметки', 'идея', 'мысли'],
            'goals': ['цели', 'цель', 'достижения', 'прогресс', 'планы', 'мечты', 'результаты'],
            'values': ['ценности', 'принципы', 'жизнь', 'направление', 'смысл', 'направления'],
            'help': ['помощь', 'помоги', 'что умеешь', 'возможности', 'команды', 'что делать']
        }
        
        # English patterns
        english_patterns = {
            'tasks': ['tasks', 'work', 'project', 'priority', 'today', 'what to do', 'list'],
            'health': ['health', 'fitness', 'workout', 'sport', 'weight', 'diet', 'wellness'],
            'learning': ['learning', 'course', 'courses', 'study', 'knowledge', 'progress', 'education'],
            'shadow_work': ['shadow', 'archetype', 'archetypes', 'shadow work', 'personal development'],
            'journal': ['journal', 'diary', 'entry', 'entries', 'reflection', 'patterns', 'insights'],
            'goals': ['goals', 'goal', 'achievements', 'progress', 'plans', 'dreams'],
            'values': ['values', 'principles', 'life', 'direction', 'meaning', 'purpose'],
            'help': ['help', 'assist', 'what can you do', 'capabilities', 'commands']
        }
        
        # Detect language and intent
        detected_language = self._detect_language(text)
        patterns = russian_patterns if detected_language == 'ru' else english_patterns
        
        # Find matching intent
        intent = 'unknown'
        confidence = 0.0
        matched_patterns = []
        
        for intent_name, pattern_list in patterns.items():
            for pattern in pattern_list:
                if pattern in text_lower:
                    matched_patterns.append(pattern)
                    confidence = min(0.9, confidence + 0.2)  # Increase confidence for each match
                    if intent == 'unknown':
                        intent = intent_name
        
        # Generate response
        response_text = self._generate_response(intent, detected_language, text)
        
        return {
            "intent": intent,
            "confidence": confidence,
            "response_text": response_text,
            "language": detected_language,
            "matched_patterns": matched_patterns,
            "source": "simple_pattern_matching",
            "metadata": {
                "user_id": user_id,
                "message_type": message_type,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection based on character analysis."""
        # Count Cyrillic characters
        cyrillic_count = sum(1 for char in text if '\u0400' <= char <= '\u04FF')
        # Count Latin characters
        latin_count = sum(1 for char in text if char.isalpha() and ord(char) < 128)
        
        if cyrillic_count > latin_count:
            return 'ru'
        else:
            return 'en'
    
    def _generate_response(self, intent: str, language: str, original_text: str) -> str:
        """Generate appropriate response based on intent and language."""
        responses = {
            'ru': {
                'tasks': "Отличный вопрос! Я могу помочь вам с задачами и проектами. Вот что я рекомендую:\n\n• Проверьте ваши активные проекты\n• Определите приоритеты на сегодня\n• Составьте план действий\n\nХотите, чтобы я проанализировал ваши текущие задачи?",
                'health': "Здоровье - это важно! Я могу помочь с:\n\n• Отслеживанием прогресса в фитнесе\n• Анализом привычек\n• Рекомендациями по здоровому образу жизни\n\nЧто именно вас интересует в плане здоровья?",
                'learning': "Обучение - ключ к росту! Я могу помочь с:\n\n• Отслеживанием прогресса в курсах\n• Рекомендациями по обучению\n• Анализом ваших знаний\n\nНад чем вы сейчас работаете?",
                'shadow_work': "Теневая работа - глубокая тема! Я могу помочь с:\n\n• Анализом архетипов\n• Выявлением паттернов\n• Работой с теневыми аспектами\n\nЧто вас интересует в саморазвитии?",
                'journal': "Журнал - отличный инструмент для рефлексии! Я могу помочь с:\n\n• Анализом записей\n• Выявлением паттернов\n• Генерацией инсайтов\n\nХотите поделиться своими размышлениями?",
                'goals': "Цели дают направление! Я могу помочь с:\n\n• Отслеживанием прогресса\n• Анализом достижений\n• Планированием следующих шагов\n\nКакие у вас цели?",
                'values': "Ценности - основа жизни! Я могу помочь с:\n\n• Определением ваших ценностей\n• Анализом соответствия жизни ценностям\n• Поиском смысла и направления\n\nЧто для вас важно?",
                'help': "Я ваш персональный помощник! Я могу помочь с:\n\n• Задачами и проектами\n• Здоровьем и фитнесом\n• Обучением и развитием\n• Теневой работой\n• Журналом и рефлексией\n• Целями и достижениями\n• Ценностями и смыслом\n\nПросто спросите меня о чем угодно!",
                'unknown': "Интересный вопрос! Я могу помочь с различными аспектами вашей жизни. Попробуйте спросить о задачах, здоровье, обучении или других темах."
            },
            'en': {
                'tasks': "Great question! I can help you with tasks and projects. Here's what I recommend:\n\n• Check your active projects\n• Identify today's priorities\n• Create an action plan\n\nWould you like me to analyze your current tasks?",
                'health': "Health is important! I can help with:\n\n• Fitness progress tracking\n• Habit analysis\n• Healthy lifestyle recommendations\n\nWhat specifically interests you about health?",
                'learning': "Learning is key to growth! I can help with:\n\n• Course progress tracking\n• Learning recommendations\n• Knowledge analysis\n\nWhat are you working on?",
                'shadow_work': "Shadow work is a deep topic! I can help with:\n\n• Archetype analysis\n• Pattern recognition\n• Working with shadow aspects\n\nWhat interests you about personal development?",
                'journal': "Journaling is a great reflection tool! I can help with:\n\n• Entry analysis\n• Pattern recognition\n• Insight generation\n\nWould you like to share your thoughts?",
                'goals': "Goals provide direction! I can help with:\n\n• Progress tracking\n• Achievement analysis\n• Next step planning\n\nWhat are your goals?",
                'values': "Values are the foundation of life! I can help with:\n\n• Identifying your values\n• Analyzing life-value alignment\n• Finding meaning and direction\n\nWhat's important to you?",
                'help': "I'm your personal assistant! I can help with:\n\n• Tasks and projects\n• Health and fitness\n• Learning and development\n• Shadow work\n• Journaling and reflection\n• Goals and achievements\n• Values and meaning\n\nJust ask me anything!",
                'unknown': "Interesting question! I can help with various aspects of your life. Try asking about tasks, health, learning, or other topics."
            }
        }
        
        return responses.get(language, responses['en']).get(intent, responses['en']['unknown'])
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "intent": "error",
            "confidence": 0.0,
            "response_text": f"I'm sorry, I encountered an error: {error_message}",
            "language": "en",
            "source": "error",
            "metadata": {"error": error_message}
        }
