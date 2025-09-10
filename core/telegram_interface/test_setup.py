#!/usr/bin/env python3
"""
Test script to verify Telegram bot setup and dependencies.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-telegram-bot: {e}")
        return False
    
    try:
        import openai
        print("✅ openai imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import openai: {e}")
        return False
    
    try:
        import yaml
        print("✅ pyyaml imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pyyaml: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        import cryptography
        print("✅ cryptography imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import cryptography: {e}")
        return False
    
    return True

def test_config():
    """Test if configuration file exists and is valid."""
    print("\n⚙️ Testing configuration...")
    
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        print("   Please copy config/config.yaml.sample to config/config.yaml")
        return False
    
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check required fields
        required_fields = ['telegram', 'paths', 'openai']
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required config field: {field}")
                return False
        
        # Check telegram bot token
        if not config['telegram'].get('bot_token') or config['telegram']['bot_token'] == "YOUR_BOT_TOKEN_HERE":
            print("❌ Telegram bot token not configured")
            print("   Please set your bot token in config/config.yaml")
            return False
        
        # Check OpenAI API key
        if not config['openai'].get('api_key'):
            print("❌ OpenAI API key not configured")
            print("   Please set your OpenAI API key in config/config.yaml")
            return False
        
        print("✅ Configuration file is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def test_directories():
    """Test if required directories exist."""
    print("\n📁 Testing directories...")
    
    required_dirs = [
        "data/storage",
        "data/cache", 
        "data/backups",
        "data/keys",
        "logs"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Directory missing: {dir_path}")
            all_exist = False
        else:
            print(f"✅ Directory exists: {dir_path}")
    
    if not all_exist:
        print("   Creating missing directories...")
        for dir_path in required_dirs:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Created: {dir_path}")
    
    return True

def test_automation_scripts():
    """Test if automation scripts are accessible."""
    print("\n🔧 Testing automation scripts...")
    
    scripts_path = "../../automation/scripts/"
    if not os.path.exists(scripts_path):
        print(f"❌ Automation scripts directory not found: {scripts_path}")
        return False
    
    required_scripts = [
        "shadow_work_tracker.py",
        "opportunity_manager.py", 
        "business_opportunity_manager.py",
        "daily_summary.py"
    ]
    
    all_exist = True
    for script in required_scripts:
        script_path = os.path.join(scripts_path, script)
        if not os.path.exists(script_path):
            print(f"❌ Script missing: {script}")
            all_exist = False
        else:
            print(f"✅ Script found: {script}")
    
    return all_exist

def main():
    """Run all tests."""
    print("🤖 Personal System Telegram Bot Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_directories,
        test_automation_scripts
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("\n🚀 Next steps:")
        print("1. Make sure your bot token and OpenAI API key are set in config/config.yaml")
        print("2. Run: python main.py")
        print("3. Send /start to your bot on Telegram")
    else:
        print("❌ Some tests failed. Please fix the issues above before running the bot.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
