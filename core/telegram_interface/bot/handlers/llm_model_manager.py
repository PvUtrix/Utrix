"""
LLM Model Manager for Personal System Telegram Bot
Manages different LLM models for different use cases with cost optimization
"""

import json
import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)

class ModelUseCase(Enum):
    """Different use cases for LLM models."""
    VOICE_INTENT_PARSING = "voice_intent_parsing"
    VOICE_RESPONSE_GENERATION = "voice_response_generation"
    TEXT_INTENT_PARSING = "text_intent_parsing"
    TEXT_RESPONSE_GENERATION = "text_response_generation"
    SHADOW_WORK_ANALYSIS = "shadow_work_analysis"
    TASK_ANALYSIS = "task_analysis"
    HEALTH_ANALYSIS = "health_analysis"
    LEARNING_ANALYSIS = "learning_analysis"
    GENERAL_CHAT = "general_chat"

class LLMModelManager:
    """Manages different LLM models for different use cases with cost optimization."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client if available
        self.openai_available = False
        try:
            from openai import OpenAI
            openai_config = config.get('openai', {})
            if openai_config.get('api_key'):
                self.openai_client = OpenAI(api_key=openai_config['api_key'])
                self.openai_available = True
                self.logger.info("OpenAI client initialized for model management")
            else:
                self.logger.warning("OpenAI API key not configured - using fallback methods")
        except ImportError:
            self.logger.warning("OpenAI library not available - using fallback methods")
        
        # Load model configurations
        from ...config.model_config_loader import ModelConfigLoader
        self.config_loader = ModelConfigLoader()
        self.model_configs = self._load_model_configs()
    
    def _load_model_configs(self) -> Dict[ModelUseCase, Dict[str, Any]]:
        """Load model configurations for different use cases."""
        
        # Load configuration from file
        config_data = self.config_loader.load_config()
        llm_models_config = config_data.get('llm_models', {})
        
        # Convert to ModelUseCase enum keys
        model_configs = {}
        for use_case in ModelUseCase:
            use_case_str = use_case.value
            if use_case_str in llm_models_config:
                model_configs[use_case] = llm_models_config[use_case_str]
                self.logger.info(f"Loaded model config for {use_case_str}: {llm_models_config[use_case_str]['model']}")
            else:
                # Use default if not configured
                model_configs[use_case] = self._get_default_config_for_use_case(use_case)
                self.logger.warning(f"Using default config for {use_case_str}")
        
        return model_configs
    
    def _get_default_config_for_use_case(self, use_case: ModelUseCase) -> Dict[str, Any]:
        """Get default configuration for a use case."""
        defaults = {
            ModelUseCase.VOICE_INTENT_PARSING: {
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 500,
                "description": "Fast, cheap model for parsing voice command intents",
                "cost_tier": "low"
            },
            ModelUseCase.VOICE_RESPONSE_GENERATION: {
                "model": "gpt-4o-mini", 
                "temperature": 0.3,
                "max_tokens": 300,
                "description": "Quick responses for voice commands",
                "cost_tier": "low"
            },
            ModelUseCase.TEXT_INTENT_PARSING: {
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 400,
                "description": "Parse text message intents",
                "cost_tier": "low"
            },
            ModelUseCase.TEXT_RESPONSE_GENERATION: {
                "model": "gpt-4o",
                "temperature": 0.7,
                "max_tokens": 800,
                "description": "High-quality responses for text messages",
                "cost_tier": "medium"
            },
            ModelUseCase.SHADOW_WORK_ANALYSIS: {
                "model": "gpt-4o",
                "temperature": 0.5,
                "max_tokens": 1200,
                "description": "Deep analysis of shadow work patterns",
                "cost_tier": "high"
            },
            ModelUseCase.TASK_ANALYSIS: {
                "model": "gpt-4o-mini",
                "temperature": 0.2,
                "max_tokens": 600,
                "description": "Analyze task patterns and priorities",
                "cost_tier": "low"
            },
            ModelUseCase.HEALTH_ANALYSIS: {
                "model": "gpt-4o-mini",
                "temperature": 0.3,
                "max_tokens": 500,
                "description": "Analyze health data and patterns",
                "cost_tier": "low"
            },
            ModelUseCase.LEARNING_ANALYSIS: {
                "model": "gpt-4o-mini",
                "temperature": 0.3,
                "max_tokens": 500,
                "description": "Analyze learning progress and recommendations",
                "cost_tier": "low"
            },
            ModelUseCase.GENERAL_CHAT: {
                "model": "gpt-4o",
                "temperature": 0.8,
                "max_tokens": 1000,
                "description": "General conversational AI",
                "cost_tier": "medium"
            }
        }
        
        return defaults.get(use_case, {
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "max_tokens": 500,
            "description": "Default fallback model",
            "cost_tier": "low"
        })
    
    def get_model_config(self, use_case: ModelUseCase) -> Dict[str, Any]:
        """Get model configuration for a specific use case."""
        return self.model_configs.get(use_case, {
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "max_tokens": 500,
            "description": "Default fallback model",
            "cost_tier": "low"
        })
    
    async def generate_response(self, 
                              use_case: ModelUseCase, 
                              messages: List[Dict[str, str]], 
                              **kwargs) -> Optional[str]:
        """Generate a response using the appropriate model for the use case."""
        
        if not self.openai_available:
            self.logger.warning("OpenAI not available, cannot generate LLM response")
            return None
        
        try:
            # Get model configuration for this use case
            model_config = self.get_model_config(use_case)
            
            # Merge with any additional parameters
            request_params = {
                "model": model_config["model"],
                "messages": messages,
                "temperature": model_config["temperature"],
                "max_tokens": model_config["max_tokens"]
            }
            
            # Override with any provided kwargs
            request_params.update(kwargs)
            
            self.logger.info(f"Generating response for {use_case.value} using {model_config['model']}")
            
            # Make the API call
            response = self.openai_client.chat.completions.create(**request_params)
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating response for {use_case.value}: {e}")
            return None
    
    async def parse_voice_intent(self, transcription: str, language: str = 'en') -> Dict[str, Any]:
        """Parse voice command intent using the appropriate model."""
        
        if not self.openai_available:
            self.logger.warning("OpenAI not available, using fallback parsing")
            return await self._fallback_voice_parsing(transcription, language)
        
        try:
            # Create the system prompt for intent parsing
            system_prompt = self._create_intent_parsing_prompt(language)
            
            # Create the user prompt with the transcription
            user_prompt = f"""Voice Command: "{transcription}"

Please analyze this voice command and extract:
1. The primary intent (what the user wants to do)
2. All actions mentioned (add, delete, update, etc.)
3. Any parameters or details
4. The final action to take

Respond with a JSON object containing the parsed information."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Use the voice intent parsing model
            response_text = await self.generate_response(
                ModelUseCase.VOICE_INTENT_PARSING,
                messages
            )
            
            if not response_text:
                return await self._fallback_voice_parsing(transcription, language)
            
            # Parse the JSON response
            parsed_result = self._parse_json_response(response_text)
            
            if parsed_result:
                return self._validate_and_enhance_intent_result(parsed_result, transcription, language)
            else:
                return await self._fallback_voice_parsing(transcription, language)
                
        except Exception as e:
            self.logger.error(f"Error in LLM voice intent parsing: {e}")
            return await self._fallback_voice_parsing(transcription, language)
    
    def _create_intent_parsing_prompt(self, language: str) -> str:
        """Create system prompt for intent parsing."""
        
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
    
    def _parse_json_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse JSON from LLM response."""
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
            
            return json.loads(json_text)
            
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse JSON from LLM response: {e}")
            return None
    
    def _validate_and_enhance_intent_result(self, parsed_result: Dict[str, Any], transcription: str, language: str) -> Dict[str, Any]:
        """Validate and enhance the intent parsing result."""
        
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
        
        return parsed_result
    
    async def _fallback_voice_parsing(self, transcription: str, language: str) -> Dict[str, Any]:
        """Fallback voice parsing when LLM is not available."""
        # This would use the existing fallback logic from LLMVoiceParser
        # For now, return a basic structure
        return {
            "intent": "unknown",
            "primary_action": "unknown",
            "all_actions": [],
            "parameters": {},
            "confidence": 0.3,
            "reasoning": "Fallback parsing - LLM not available",
            "method": "fallback"
        }
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        if not self.openai_available:
            return []
        
        # This would ideally fetch from OpenAI API, but for now return common models
        return [
            "gpt-4o",
            "gpt-4o-mini", 
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
    
    def get_cost_estimate(self, use_case: ModelUseCase, input_tokens: int, output_tokens: int) -> Dict[str, Any]:
        """Get cost estimate for a specific use case."""
        model_config = self.get_model_config(use_case)
        model = model_config["model"]
        
        # Rough cost estimates (as of 2024)
        cost_per_1k_tokens = {
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
        }
        
        if model in cost_per_1k_tokens:
            input_cost = (input_tokens / 1000) * cost_per_1k_tokens[model]["input"]
            output_cost = (output_tokens / 1000) * cost_per_1k_tokens[model]["output"]
            total_cost = input_cost + output_cost
            
            return {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "input_cost": input_cost,
                "output_cost": output_cost,
                "total_cost": total_cost,
                "cost_tier": model_config.get("cost_tier", "unknown")
            }
        
        return {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": 0.0,
            "cost_tier": model_config.get("cost_tier", "unknown")
        }
    
    def update_model_config(self, use_case: ModelUseCase, new_config: Dict[str, Any]) -> bool:
        """Update model configuration for a specific use case."""
        try:
            if use_case in self.model_configs:
                self.model_configs[use_case].update(new_config)
                self.logger.info(f"Updated model config for {use_case.value}: {new_config}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error updating model config for {use_case.value}: {e}")
            return False
