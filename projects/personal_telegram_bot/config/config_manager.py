"""
Configuration manager for the Personal System Telegram Bot.
Handles loading, validating, and managing configuration settings.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}. "
                "Please copy config.yaml.sample to config.yaml and configure it."
            )
        
        with open(self.config_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)
        
        # Resolve relative paths
        self._resolve_paths()
        
        return self.config
    
    def _resolve_paths(self):
        """Resolve relative paths in configuration."""
        base_dir = self.config_path.parent.parent
        
        # Resolve personal system paths
        if 'paths' in self.config:
            for key, path in self.config['paths'].items():
                if isinstance(path, str) and path.startswith('../../../'):
                    resolved_path = base_dir / path
                    self.config['paths'][key] = str(resolved_path)
        
        # Resolve storage paths
        if 'storage' in self.config:
            for key, path in self.config['storage'].items():
                if isinstance(path, str) and path.startswith('./'):
                    resolved_path = base_dir / path
                    self.config['storage'][key] = str(resolved_path)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration settings."""
        required_sections = ['telegram', 'paths', 'storage', 'privacy', 'features']
        
        # Check required sections
        for section in required_sections:
            if section not in config:
                print(f"Missing required configuration section: {section}")
                return False
        
        # Validate Telegram settings
        telegram = config.get('telegram', {})
        if not telegram.get('bot_token') or telegram['bot_token'] == "YOUR_BOT_TOKEN_HERE":
            print("Please set your Telegram bot token in config.yaml")
            return False
        
        # Validate paths
        paths = config.get('paths', {})
        required_paths = ['base_path', 'automation_scripts', 'journal', 'notes']
        for path_key in required_paths:
            if path_key not in paths:
                print(f"Missing required path: {path_key}")
                return False
        
        # Check if personal system paths exist
        for path_key, path_value in paths.items():
            if path_key in ['base_path', 'automation_scripts', 'journal', 'notes']:
                if not Path(path_value).exists():
                    print(f"Warning: Path does not exist: {path_key} -> {path_value}")
        
        return True
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)."""
        if not self.config:
            self.load_config()
        
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (supports dot notation)."""
        if not self.config:
            self.load_config()
        
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def save_config(self):
        """Save current configuration to file."""
        if not self.config:
            return
        
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file, default_flow_style=False, indent=2)
    
    def reload_config(self) -> Dict[str, Any]:
        """Reload configuration from file."""
        self.config = None
        return self.load_config()
