#!/usr/bin/env python3
"""
Secure Configuration Manager
Handles sensitive configuration data like API keys securely.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
import base64

logger = logging.getLogger(__name__)


class SecureConfigManager:
    """Manages sensitive configuration data with encryption."""
    
    def __init__(self, config_dir: str = "./config", keys_dir: str = "./data/keys"):
        self.config_dir = Path(config_dir)
        self.keys_dir = Path(keys_dir)
        self.keys_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize encryption
        self._init_encryption()
    
    def _init_encryption(self):
        """Initialize encryption key for sensitive data."""
        key_file = self.keys_dir / "config.key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Generate new encryption key
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            
            logger.info("Generated new encryption key for secure config")
        
        self.cipher = Fernet(self.encryption_key)
    
    def encrypt_value(self, value: str) -> str:
        """Encrypt a sensitive value."""
        if not value:
            return ""
        return base64.b64encode(self.cipher.encrypt(value.encode())).decode()
    
    def decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt a sensitive value."""
        if not encrypted_value:
            return ""
        try:
            decoded = base64.b64decode(encrypted_value.encode())
            return self.cipher.decrypt(decoded).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt value: {e}")
            return ""
    
    def get_openai_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get OpenAI configuration with decrypted API key."""
        openai_config = config.get('openai', {})
        
        if not openai_config:
            return {}
        
        # Decrypt API key if it exists
        encrypted_key = openai_config.get('api_key', '')
        if encrypted_key:
            decrypted_key = self.decrypt_value(encrypted_key)
            openai_config['api_key'] = decrypted_key
        
        return openai_config
    
    def set_openai_api_key(self, api_key: str) -> bool:
        """Securely store OpenAI API key."""
        try:
            # Encrypt the API key
            encrypted_key = self.encrypt_value(api_key)
            
            # Update config file
            config_file = self.config_dir / "config.yaml"
            if not config_file.exists():
                logger.error("Config file not found")
                return False
            
            # Read current config
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update OpenAI API key
            if 'openai:' in content:
                # Replace existing API key
                import re
                pattern = r'(api_key:\s*)"[^"]*"'
                replacement = rf'\1"{encrypted_key}"'
                new_content = re.sub(pattern, replacement, content)
            else:
                # Add OpenAI section if it doesn't exist
                openai_section = f"""
# OpenAI Configuration
openai:
  api_key: "{encrypted_key}"  # Your OpenAI API key for Whisper transcription
  model: "whisper-1"  # Whisper model to use
  max_file_size: 25  # Maximum audio file size in MB
  supported_formats: ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
  enable_voice_transcription: true
"""
                new_content = content + openai_section
            
            # Write updated config
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            logger.info("OpenAI API key securely stored")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store OpenAI API key: {e}")
            return False
    
    def validate_openai_config(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """Validate OpenAI configuration."""
        openai_config = config.get('openai', {})
        
        if not openai_config:
            return False, "OpenAI configuration not found"
        
        api_key = openai_config.get('api_key', '')
        if not api_key:
            return False, "OpenAI API key not configured"
        
        # Check if voice transcription is enabled
        if not openai_config.get('enable_voice_transcription', False):
            return False, "Voice transcription is disabled"
        
        return True, "OpenAI configuration is valid"
    
    def get_supported_audio_formats(self, config: Dict[str, Any]) -> list[str]:
        """Get list of supported audio formats for voice messages."""
        openai_config = config.get('openai', {})
        return openai_config.get('supported_formats', ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"])
    
    def get_max_audio_file_size(self, config: Dict[str, Any]) -> int:
        """Get maximum audio file size in MB."""
        openai_config = config.get('openai', {})
        return openai_config.get('max_file_size', 25)
