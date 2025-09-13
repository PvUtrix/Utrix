"""
Model Configuration Loader for Personal System Telegram Bot
Loads and manages LLM model configurations
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ModelConfigLoader:
    """Loads and manages LLM model configurations."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.logger = logging.getLogger(__name__)
        self._config_cache = None
    
    def _get_default_config_path(self) -> str:
        """Get the default path to the model configuration file."""
        current_dir = Path(__file__).parent
        return str(current_dir / "llm_models.yaml")
    
    def load_config(self) -> Dict[str, Any]:
        """Load model configuration from YAML file."""
        if self._config_cache is not None:
            return self._config_cache
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                self._config_cache = config
                self.logger.info(f"Loaded model configuration from {self.config_path}")
                return config
        except FileNotFoundError:
            self.logger.warning(f"Model config file not found: {self.config_path}")
            return self._get_default_config()
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing model config YAML: {e}")
            return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading model config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration when file is not available."""
        return {
            "llm_models": {
                "voice_intent_parsing": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "max_tokens": 500,
                    "description": "Fast, cheap model for parsing voice command intents",
                    "cost_tier": "low"
                },
                "voice_response_generation": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.3,
                    "max_tokens": 300,
                    "description": "Quick responses for voice commands",
                    "cost_tier": "low"
                },
                "text_intent_parsing": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "max_tokens": 400,
                    "description": "Parse text message intents",
                    "cost_tier": "low"
                },
                "text_response_generation": {
                    "model": "gpt-4o",
                    "temperature": 0.7,
                    "max_tokens": 800,
                    "description": "High-quality responses for text messages",
                    "cost_tier": "medium"
                },
                "shadow_work_analysis": {
                    "model": "gpt-4o",
                    "temperature": 0.5,
                    "max_tokens": 1200,
                    "description": "Deep analysis of shadow work patterns",
                    "cost_tier": "high"
                },
                "task_analysis": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.2,
                    "max_tokens": 600,
                    "description": "Analyze task patterns and priorities",
                    "cost_tier": "low"
                },
                "health_analysis": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.3,
                    "max_tokens": 500,
                    "description": "Analyze health data and patterns",
                    "cost_tier": "low"
                },
                "learning_analysis": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.3,
                    "max_tokens": 500,
                    "description": "Analyze learning progress and recommendations",
                    "cost_tier": "low"
                },
                "general_chat": {
                    "model": "gpt-4o",
                    "temperature": 0.8,
                    "max_tokens": 1000,
                    "description": "General conversational AI",
                    "cost_tier": "medium"
                }
            }
        }
    
    def get_model_config(self, use_case: str) -> Dict[str, Any]:
        """Get model configuration for a specific use case."""
        config = self.load_config()
        return config.get("llm_models", {}).get(use_case, {})
    
    def get_strategy_config(self, strategy: str) -> Dict[str, str]:
        """Get model strategy configuration."""
        config = self.load_config()
        return config.get("model_strategies", {}).get(strategy, {})
    
    def get_cost_limits(self) -> Dict[str, Any]:
        """Get cost management configuration."""
        config = self.load_config()
        return config.get("cost_management", {})
    
    def get_fallback_models(self, primary_model: str) -> list:
        """Get fallback models for a primary model."""
        config = self.load_config()
        fallbacks = config.get("model_fallbacks", {})
        return fallbacks.get(primary_model, [])
    
    def reload_config(self) -> Dict[str, Any]:
        """Reload configuration from file."""
        self._config_cache = None
        return self.load_config()
    
    def validate_config(self) -> bool:
        """Validate the loaded configuration."""
        try:
            config = self.load_config()
            
            # Check required sections
            required_sections = ["llm_models"]
            for section in required_sections:
                if section not in config:
                    self.logger.error(f"Missing required section: {section}")
                    return False
            
            # Check required use cases
            required_use_cases = [
                "voice_intent_parsing",
                "voice_response_generation", 
                "text_intent_parsing",
                "text_response_generation",
                "general_chat"
            ]
            
            llm_models = config.get("llm_models", {})
            for use_case in required_use_cases:
                if use_case not in llm_models:
                    self.logger.error(f"Missing required use case: {use_case}")
                    return False
                
                use_case_config = llm_models[use_case]
                required_fields = ["model", "temperature", "max_tokens"]
                for field in required_fields:
                    if field not in use_case_config:
                        self.logger.error(f"Missing required field {field} in {use_case}")
                        return False
            
            self.logger.info("Model configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating configuration: {e}")
            return False
