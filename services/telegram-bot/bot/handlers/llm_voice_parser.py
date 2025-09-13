"""
LLM-based Voice Command Parser for Personal System Telegram Bot
Handles complex voice commands using AI to parse intent, extract actions, and parameters
"""

import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMVoiceParser:
    """LLM-powered voice command parser for complex intent detection and action extraction."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize model manager
        from .llm_model_manager import LLMModelManager
        self.model_manager = LLMModelManager(config)
        
        # Keep fallback parsing for when LLM is not available
        self.fallback_available = True
    
    async def parse_voice_command(self, transcription: str, language: str = 'en') -> Dict[str, Any]:
        """
        Parse voice command using LLM to extract intent, actions, and parameters.
        
        Args:
            transcription: The transcribed voice text
            language: Detected language (en, ru, etc.)
            
        Returns:
            Dict containing parsed intent, actions, and parameters
        """
        try:
            # Try LLM-based parsing first
            llm_result = await self.model_manager.parse_voice_intent(transcription, language)
            
            if llm_result.get('confidence', 0) > 0.7:
                self.logger.info(f"LLM parsing successful: {llm_result['primary_action']} (confidence: {llm_result['confidence']})")
                return llm_result
            else:
                self.logger.info(f"LLM parsing low confidence ({llm_result.get('confidence', 0)}), trying fallback")
                if self.fallback_available:
                    return await self._parse_with_fallback(transcription, language)
                else:
                    return llm_result
                    
        except Exception as e:
            self.logger.error(f"Error parsing voice command: {e}")
            if self.fallback_available:
                return await self._parse_with_fallback(transcription, language)
            else:
                return self._create_error_response(f"Error parsing command: {str(e)}")
    
    async def _parse_with_llm(self, transcription: str, language: str) -> Dict[str, Any]:
        """Parse voice command using OpenAI GPT."""
        try:
            # Create the system prompt for intent parsing
            system_prompt = self._create_system_prompt(language)
            
            # Create the user prompt with the transcription
            user_prompt = f"""Voice Command: "{transcription}"

Please analyze this voice command and extract:
1. The primary intent (what the user wants to do)
2. All actions mentioned (add, delete, update, etc.)
3. Any parameters or details
4. The final action to take

Respond with a JSON object containing the parsed information."""

            # Make the API call
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Using mini for cost efficiency
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent parsing
                max_tokens=500
            )
            
            # Parse the response
            response_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    # Try to find JSON object in the response
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    json_text = response_text[json_start:json_end]
                
                parsed_result = json.loads(json_text)
                
                # Validate and enhance the result
                return self._validate_and_enhance_result(parsed_result, transcription, language)
                
            except json.JSONDecodeError as e:
                self.logger.warning(f"Failed to parse JSON from LLM response: {e}")
                return await self._parse_with_fallback(transcription, language)
                
        except Exception as e:
            self.logger.error(f"Error in LLM parsing: {e}")
            return await self._parse_with_fallback(transcription, language)
    
    def _create_system_prompt(self, language: str) -> str:
        """Create system prompt for LLM-based voice command parsing."""
        
        if language == 'ru':
            return """Ты - эксперт по анализу голосовых команд для персонального ассистента. Твоя задача - точно определить намерения пользователя и извлечь все действия из голосовых команд.

Поддерживаемые действия:
- add_task: Добавить задачу
- delete_task: Удалить задачу  
- update_task: Обновить задачу
- list_tasks: Показать задачи
- add_note: Добавить заметку
- log_health: Записать данные о здоровье
- log_learning: Записать данные об обучении
- unknown: Неизвестное действие

ВАЖНО: Если в команде есть несколько действий (например, "удалить задачу, добавить задачу"), определи ПОСЛЕДНЕЕ действие как основное.

Отвечай ТОЛЬКО в формате JSON:
{
    "intent": "основное_намерение",
    "primary_action": "основное_действие",
    "all_actions": ["все_действия"],
    "parameters": {
        "task_title": "название_задачи",
        "task_id": "id_задачи_для_удаления",
        "priority": "приоритет",
        "category": "категория"
    },
    "confidence": 0.95,
    "reasoning": "краткое_объяснение_анализа"
}"""
        else:
            return """You are an expert at analyzing voice commands for a personal assistant. Your task is to accurately determine user intent and extract all actions from voice commands.

Supported actions:
- add_task: Add a new task
- delete_task: Delete an existing task
- update_task: Update an existing task
- list_tasks: Show current tasks
- add_note: Add a quick note
- log_health: Log health data
- log_learning: Log learning activity
- unknown: Unknown or unclear action

IMPORTANT: If the command contains multiple actions (e.g., "delete the task, add the task"), identify the LAST action as the primary one.

Respond ONLY in JSON format:
{
    "intent": "primary_intent",
    "primary_action": "primary_action",
    "all_actions": ["all_actions_found"],
    "parameters": {
        "task_title": "extracted_task_title",
        "task_id": "task_id_for_deletion",
        "priority": "priority_level",
        "category": "task_category"
    },
    "confidence": 0.95,
    "reasoning": "brief_explanation_of_analysis"
}"""
    
    async def _parse_with_fallback(self, transcription: str, language: str) -> Dict[str, Any]:
        """Fallback parsing using keyword matching when LLM is not available."""
        text_lower = transcription.lower()
        
        # Define action keywords for different languages
        if language == 'ru':
            action_keywords = {
                'add_task': ['добавить задачу', 'создать задачу', 'новая задача', 'добавь задачу', 'надо добавить'],
                'delete_task': ['удалить задачу', 'удали задачу', 'убрать задачу', 'отменить задачу'],
                'list_tasks': ['показать задачи', 'какие задачи', 'мои задачи', 'список задач'],
                'add_note': ['заметка', 'запомни', 'идея', 'мысль'],
                'log_health': ['шаги', 'вес', 'сон', 'настроение', 'энергия', 'вода', 'упражнения'],
                'log_learning': ['изучил', 'учил', 'курс', 'книга', 'статья', 'видео', 'урок']
            }
        else:
            action_keywords = {
                'add_task': ['add task', 'create task', 'new task', 'add a task', 'add the task'],
                'delete_task': ['delete task', 'remove task', 'cancel task', 'delete the task'],
                'list_tasks': ['show tasks', 'what tasks', 'my tasks', 'list tasks'],
                'add_note': ['note', 'remember', 'idea', 'thought'],
                'log_health': ['steps', 'weight', 'sleep', 'mood', 'energy', 'water', 'exercise'],
                'log_learning': ['learned', 'studied', 'course', 'book', 'article', 'video', 'tutorial']
            }
        
        # Find all actions mentioned with their positions
        found_actions = []
        for action, keywords in action_keywords.items():
            for keyword in keywords:
                # Find all occurrences of this keyword
                start = 0
                while True:
                    position = text_lower.find(keyword, start)
                    if position == -1:
                        break
                    found_actions.append((action, position, keyword))
                    start = position + 1
        
        # Sort by position to find the order of actions
        found_actions.sort(key=lambda x: x[1])
        
        # Extract just the actions in order
        actions_in_order = [action for action, _, _ in found_actions]
        
        # Determine primary action (last one mentioned)
        primary_action = actions_in_order[-1] if actions_in_order else 'unknown'
        
        # Extract parameters based on action
        parameters = self._extract_parameters_fallback(transcription, primary_action, language)
        
        return {
            "intent": primary_action,
            "primary_action": primary_action,
            "all_actions": actions_in_order,
            "parameters": parameters,
            "confidence": 0.7 if actions_in_order else 0.3,
            "reasoning": f"Fallback parsing found actions in order: {actions_in_order} (all matches: {found_actions})",
            "method": "fallback"
        }
    
    def _extract_parameters_fallback(self, transcription: str, action: str, language: str) -> Dict[str, Any]:
        """Extract parameters using fallback methods."""
        parameters = {}
        
        if action in ['add_task', 'update_task']:
            # Extract task title using the existing logic
            task_title = self._extract_task_title_fallback(transcription, language)
            if task_title:
                parameters['task_title'] = task_title
                parameters['priority'] = 'medium'
                parameters['category'] = 'voice_command'
        
        elif action == 'delete_task':
            # Try to extract task ID or title for deletion
            # This is a simplified approach - in a real system you'd need more sophisticated matching
            parameters['task_identifier'] = transcription
        
        return parameters
    
    def _extract_task_title_fallback(self, transcription: str, language: str) -> Optional[str]:
        """Extract task title using fallback methods."""
        if language == 'ru':
            prefixes = [
                'надо добавить задачу,',
                'надо добавить задачу ',
                'добавить задачу,',
                'добавить задачу ',
                'создать задачу,',
                'создать задачу ',
                'добавь задачу ',
                'надо добавить,',
                'надо добавить ',
                'добавить,',
                'добавить ',
                'создать,',
                'создать '
            ]
        else:
            prefixes = [
                'add task,',
                'add task ',
                'create task,',
                'create task ',
                'new task,',
                'new task ',
                'add a task,',
                'add a task ',
                'add the task,',
                'add the task '
            ]
        
        text_lower = transcription.lower()
        best_match = ""
        best_length = 0
        
        for prefix in prefixes:
            if text_lower.startswith(prefix) and len(prefix) > best_length:
                best_match = prefix
                best_length = len(prefix)
        
        if best_match:
            task_title = transcription[len(best_match):].strip()
        else:
            # For complex commands, try to find the last "add task" pattern
            if language == 'en':
                # Look for patterns like "add the task to [something]"
                import re
                add_task_patterns = [
                    r'add the task to (.+)',
                    r'add task to (.+)',
                    r'add a task to (.+)',
                    r'create task to (.+)',
                    r'new task to (.+)'
                ]
                
                for pattern in add_task_patterns:
                    match = re.search(pattern, text_lower)
                    if match:
                        task_title = match.group(1).strip()
                        break
                else:
                    # Fallback: try to find comma and take everything after it
                    if ',' in transcription:
                        parts = transcription.split(',', 1)
                        if len(parts) > 1:
                            task_title = parts[1].strip()
                        else:
                            task_title = transcription
                    else:
                        task_title = transcription
            else:
                # Fallback: try to find comma and take everything after it
                if ',' in transcription:
                    parts = transcription.split(',', 1)
                    if len(parts) > 1:
                        task_title = parts[1].strip()
                    else:
                        task_title = transcription
                else:
                    task_title = transcription
        
        # Clean up the task title
        task_title = task_title.strip('.,!?')
        return task_title if task_title else None
    
    def _validate_and_enhance_result(self, parsed_result: Dict[str, Any], transcription: str, language: str) -> Dict[str, Any]:
        """Validate and enhance the LLM parsing result."""
        
        # Ensure required fields exist
        if 'intent' not in parsed_result:
            parsed_result['intent'] = 'unknown'
        if 'primary_action' not in parsed_result:
            parsed_result['primary_action'] = parsed_result.get('intent', 'unknown')
        if 'all_actions' not in parsed_result:
            parsed_result['all_actions'] = [parsed_result.get('primary_action', 'unknown')]
        if 'parameters' not in parsed_result:
            parsed_result['parameters'] = {}
        if 'confidence' not in parsed_result:
            parsed_result['confidence'] = 0.8
        if 'reasoning' not in parsed_result:
            parsed_result['reasoning'] = "LLM-based parsing"
        
        # Add method indicator
        parsed_result['method'] = 'llm'
        
        # Enhance parameters if needed
        if parsed_result['primary_action'] in ['add_task', 'update_task']:
            if 'task_title' not in parsed_result['parameters']:
                # Try to extract task title using fallback method
                task_title = self._extract_task_title_fallback(transcription, language)
                if task_title:
                    parsed_result['parameters']['task_title'] = task_title
                    parsed_result['parameters']['priority'] = 'medium'
                    parsed_result['parameters']['category'] = 'voice_command'
        
        return parsed_result
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response for failed parsing."""
        return {
            "intent": "unknown",
            "primary_action": "unknown",
            "all_actions": [],
            "parameters": {},
            "confidence": 0.0,
            "reasoning": error_message,
            "method": "error"
        }
