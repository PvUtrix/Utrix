#!/usr/bin/env python3
"""
Quick Setup Script for n8n Integration
Automates the initial setup tasks for the n8n integration framework
"""

import asyncio
import yaml
import sys
from pathlib import Path
import subprocess
import os


class N8nQuickSetup:
    """Quick setup for n8n integration"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.telegram_bot_dir = self.project_root / "services" / "telegram-bot"
        self.config_file = self.telegram_bot_dir / "config" / "config.yaml"
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        try:
            import httpx
            import yaml
            print("✅ Dependencies are installed")
            return True
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("Installing dependencies...")
            
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "httpx", "pyyaml"], check=True)
                print("✅ Dependencies installed successfully")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies")
                print("💡 Try running: python3 -m pip install httpx pyyaml")
                return False
    
    def update_config(self, n8n_url: str, n8n_api_key: str, openai_api_key: str):
        """Update configuration file with n8n details"""
        print("📝 Updating configuration...")
        
        if not self.config_file.exists():
            print(f"❌ Config file not found: {self.config_file}")
            return False
        
        # Load existing config
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Update n8n configuration
        if 'n8n' not in config:
            config['n8n'] = {}
        
        config['n8n'].update({
            'base_url': n8n_url,
            'api_key': n8n_api_key,
            'webhook_path': 'multilingual-intent',
            'timeout': 10,
            'fallback_enabled': True,
            'openai': {
                'api_key': openai_api_key,
                'model': 'gpt-4o',
                'temperature': 0.3,
                'max_tokens': 1000
            }
        })
        
        # Save updated config
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print("✅ Configuration updated")
        return True
    
    async def test_connection(self, n8n_url: str, api_key: str):
        """Test connection to n8n instance"""
        print("🔍 Testing n8n connection...")
        
        try:
            # Add the framework to path
            sys.path.append(str(self.project_root / "automation" / "integrations"))
            from n8n_framework import N8nClient
            
            client = N8nClient(n8n_url, api_key=api_key)
            success = await client.test_connection()
            
            if success:
                print("✅ n8n connection successful")
                return True
            else:
                print("❌ n8n connection failed")
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {e}")
            return False
    
    async def deploy_workflow(self, n8n_url: str, api_key: str):
        """Deploy the multilingual intent workflow"""
        print("🚀 Deploying multilingual intent workflow...")
        
        try:
            sys.path.append(str(self.project_root / "automation" / "integrations"))
            from n8n_framework import N8nIntegration
            
            integration = N8nIntegration({
                'base_url': n8n_url,
                'api_key': api_key
            })
            
            success = await integration.setup_multilingual_intent()
            
            if success:
                print("✅ Workflow deployed successfully")
                return True
            else:
                print("❌ Workflow deployment failed")
                return False
                
        except Exception as e:
            print(f"❌ Deployment error: {e}")
            return False
    
    async def test_multilingual_processing(self):
        """Test multilingual processing"""
        print("🧪 Testing multilingual processing...")
        
        try:
            # Change to telegram bot directory
            os.chdir(self.telegram_bot_dir)
            
            # Load config
            with open('config/config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            # Import and test
            sys.path.append(str(self.telegram_bot_dir))
            from integrations.n8n_multilingual_agent_v2 import N8nMultilingualAgent
            
            agent = N8nMultilingualAgent(config)
            
            # Test Russian message
            result = await agent.process_message(
                "Какие у меня задачи на сегодня?",
                12345,
                "voice"
            )
            
            print(f"✅ Test completed:")
            print(f"   Intent: {result['intent']}")
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"   Source: {result['source']}")
            print(f"   Response: {result['response_text'][:100]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False
    
    def create_test_script(self):
        """Create a test script for future use"""
        print("📝 Creating test script...")
        
        test_script = self.telegram_bot_dir / "test_n8n_multilingual.py"
        
        script_content = '''#!/usr/bin/env python3
"""
Test script for n8n multilingual integration
"""

import asyncio
import yaml
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from integrations.n8n_multilingual_agent_v2 import N8nMultilingualAgent

async def test_multilingual():
    """Test multilingual processing"""
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    agent = N8nMultilingualAgent(config)
    
    test_cases = [
        {
            "text": "Какие у меня задачи на сегодня?",
            "language": "Russian",
            "expected_intent": "tasks"
        },
        {
            "text": "What tasks do I have for today?",
            "language": "English",
            "expected_intent": "tasks"
        },
        {
            "text": "Как дела с моим здоровьем?",
            "language": "Russian",
            "expected_intent": "health"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\nTest {i}: {test_case['language']} - '{test_case['text']}'")
        print("-" * 40)
        
        result = await agent.process_message(
            test_case['text'],
            12345,
            "text"
        )
        
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Source: {result['source']}")
        print(f"Response: {result['response_text'][:100]}...")
        
        if result['intent'] == test_case['expected_intent']:
            print("✅ Intent detection correct!")
        else:
            print(f"⚠️ Expected '{test_case['expected_intent']}', got '{result['intent']}'")

if __name__ == "__main__":
    asyncio.run(test_multilingual())
'''
        
        with open(test_script, 'w') as f:
            f.write(script_content)
        
        # Make it executable
        test_script.chmod(0o755)
        
        print(f"✅ Test script created: {test_script}")
        return True
    
    async def run_setup(self):
        """Run the complete setup process"""
        print("🚀 n8n Integration Quick Setup")
        print("=" * 40)
        
        # Get user input
        print("Please provide your n8n instance details:")
        n8n_url = input("n8n URL (e.g., http://localhost:5678): ").strip()
        n8n_api_key = input("n8n API key (or press Enter to skip): ").strip() or None
        openai_api_key = input("OpenAI API key (or press Enter to configure later): ").strip() or None
        
        if not n8n_url:
            print("❌ n8n URL is required")
            return False
        
        if not openai_api_key:
            print("⚠️ OpenAI API key not provided - you'll need to configure it in the n8n workflow later")
            openai_api_key = "your_openai_api_key_here"
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            return False
        
        # Step 2: Update configuration
        if not self.update_config(n8n_url, n8n_api_key, openai_api_key):
            return False
        
        # Step 3: Test connection
        if not await self.test_connection(n8n_url, n8n_api_key):
            print("⚠️ Connection failed, but continuing with setup...")
        
        # Step 4: Deploy workflow
        if not await self.deploy_workflow(n8n_url, n8n_api_key):
            print("⚠️ Workflow deployment failed, but continuing...")
        
        # Step 5: Test multilingual processing
        if not await self.test_multilingual_processing():
            print("⚠️ Multilingual test failed, but setup is complete")
        
        # Step 6: Create test script
        self.create_test_script()
        
        print("\\n🎉 Setup completed!")
        print("\\nNext steps:")
        print("1. Configure OpenAI API key in your n8n workflow")
        print("2. Test with: python test_n8n_multilingual.py")
        print("3. Restart your Telegram bot")
        
        return True


async def main():
    """Main setup function"""
    setup = N8nQuickSetup()
    await setup.run_setup()


if __name__ == "__main__":
    asyncio.run(main())
