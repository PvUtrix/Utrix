#!/usr/bin/env python3
"""
Test OpenAI Configuration
Verifies that OpenAI API key is properly configured and accessible.
"""

import sys
from pathlib import Path

# Add config directory to path
sys.path.append(str(Path(__file__).parent / "config"))

try:
    from secure_config import SecureConfigManager
    from config_manager import ConfigManager
    
    print("🔧 Testing OpenAI Configuration...")
    
    # Load config
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    # Test secure config
    secure_config = SecureConfigManager()
    
    # Check OpenAI config
    openai_config = secure_config.get_openai_config(config)
    
    if not openai_config:
        print("❌ OpenAI configuration not found in config.yaml")
        print("💡 Add OpenAI section to your config.yaml file")
        sys.exit(1)
    
    api_key = openai_config.get('api_key', '')
    if not api_key:
        print("❌ OpenAI API key not configured")
        print("💡 Use: /admin set_openai_key YOUR_API_KEY in Telegram bot")
        sys.exit(1)
    
    # Validate config
    is_valid, message = secure_config.validate_openai_config(config)
    
    if is_valid:
        print("✅ OpenAI configuration is valid!")
        print(f"📝 Model: {openai_config.get('model', 'whisper-1')}")
        print(f"📁 Max file size: {openai_config.get('max_file_size', 25)} MB")
        print(f"🎵 Supported formats: {', '.join(openai_config.get('supported_formats', []))}")
        print(f"🎤 Voice transcription: {'Enabled' if openai_config.get('enable_voice_transcription') else 'Disabled'}")
        
        # Test API key format (basic validation)
        if api_key.startswith('sk-') and len(api_key) > 20:
            print("✅ API key format looks valid")
        else:
            print("⚠️  API key format may be invalid")
            
    else:
        print(f"❌ OpenAI configuration validation failed: {message}")
        sys.exit(1)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all dependencies are installed")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n🎉 OpenAI configuration test completed successfully!")
print("🚀 Your bot is ready for voice message transcription!")
