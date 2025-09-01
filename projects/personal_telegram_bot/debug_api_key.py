#!/usr/bin/env python3
"""
Debug OpenAI API Key Configuration
Tests the decryption and retrieval process.
"""

import sys
from pathlib import Path

# Add config directory to path
sys.path.append(str(Path(__file__).parent / "config"))

try:
    from secure_config import SecureConfigManager
    from config_manager import ConfigManager
    
    print("🔍 Debugging OpenAI API Key Configuration...")
    
    # Load config
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    print(f"📝 Config loaded: {bool(config)}")
    print(f"🔑 OpenAI section exists: {'openai' in config}")
    
    if 'openai' in config:
        openai_config = config['openai']
        print(f"📋 OpenAI config keys: {list(openai_config.keys())}")
        print(f"🔐 API key exists: {'api_key' in openai_config}")
        
        if 'api_key' in openai_config:
            encrypted_key = openai_config['api_key']
            print(f"🔐 Encrypted key length: {len(encrypted_key)}")
            print(f"🔐 Encrypted key preview: {encrypted_key[:50]}...")
            
            # Test secure config
            secure_config = SecureConfigManager()
            print(f"🔐 Secure config initialized: {bool(secure_config)}")
            
            # Try to decrypt
            try:
                decrypted_key = secure_config.decrypt_value(encrypted_key)
                print(f"🔓 Decrypted key length: {len(decrypted_key)}")
                print(f"🔓 Decrypted key preview: {decrypted_key[:20]}...")
                print(f"🔓 Key starts with 'sk-': {decrypted_key.startswith('sk-')}")
                
                if decrypted_key.startswith('sk-'):
                    print("✅ API key decryption successful!")
                else:
                    print("❌ API key format invalid after decryption")
                    
            except Exception as e:
                print(f"❌ Decryption failed: {e}")
                
    # Test the get_openai_config method
    print("\n🧪 Testing get_openai_config method...")
    try:
        openai_config = secure_config.get_openai_config(config)
        print(f"📋 Retrieved config keys: {list(openai_config.keys())}")
        
        if 'api_key' in openai_config:
            api_key = openai_config['api_key']
            print(f"🔑 Retrieved API key length: {len(api_key)}")
            print(f"🔑 Retrieved API key valid: {api_key.startswith('sk-')}")
        else:
            print("❌ No API key in retrieved config")
            
    except Exception as e:
        print(f"❌ get_openai_config failed: {e}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n�� Debug complete!")
