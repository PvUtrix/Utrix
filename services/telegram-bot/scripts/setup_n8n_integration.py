#!/usr/bin/env python3
"""
Setup script for n8n Multilingual Integration
Configures and tests the connection to your existing n8n instance
"""

import asyncio
import httpx
import yaml
import json
from pathlib import Path
from typing import Dict, Any


class N8nSetup:
    def __init__(self, config_path: str = "config/n8n_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load n8n configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return {
                "n8n": {
                    "base_url": "http://localhost:5678",
                    "api_key": "",
                    "username": "",
                    "password": "",
                    "webhook_path": "multilingual-intent",
                    "timeout": 10,
                    "fallback_enabled": True
                }
            }
    
    def save_config(self):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        print(f"✅ Configuration saved to {self.config_path}")
    
    async def test_connection(self) -> bool:
        """Test connection to n8n instance."""
        print("🔍 Testing connection to n8n instance...")
        
        try:
            headers = {}
            if self.config["n8n"]["api_key"]:
                headers["Authorization"] = f"Bearer {self.config['n8n']['api_key']}"
            elif self.config["n8n"]["username"] and self.config["n8n"]["password"]:
                import base64
                credentials = base64.b64encode(
                    f"{self.config['n8n']['username']}:{self.config['n8n']['password']}".encode()
                ).decode()
                headers["Authorization"] = f"Basic {credentials}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.config['n8n']['base_url']}/api/v1/active",
                    headers=headers
                )
                
                if response.status_code == 200:
                    print("✅ Successfully connected to n8n instance")
                    return True
                else:
                    print(f"❌ Connection failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    async def create_workflow(self) -> bool:
        """Create the multilingual intent detection workflow."""
        print("🚀 Creating multilingual intent detection workflow...")
        
        workflow_data = {
            "name": "Multilingual Intent Detection",
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": self.config["n8n"]["webhook_path"],
                        "responseMode": "responseNode",
                        "options": {}
                    },
                    "id": "webhook-trigger",
                    "name": "Webhook Trigger",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [240, 300]
                },
                {
                    "parameters": {
                        "jsCode": "// Extract data from webhook\nconst text = $input.first().json.text;\nconst user_id = $input.first().json.user_id;\nconst context = $input.first().json.context;\nconst language_hint = $input.first().json.language_hint;\n\n// Prepare data for AI processing\nreturn {\n  text: text,\n  user_id: user_id,\n  context: context,\n  language_hint: language_hint,\n  timestamp: new Date().toISOString()\n};"
                    },
                    "id": "data-extractor",
                    "name": "Extract Data",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [460, 300]
                },
                {
                    "parameters": {
                        "model": self.config["n8n"].get("openai", {}).get("model", "gpt-4o"),
                        "options": {
                            "temperature": self.config["n8n"].get("openai", {}).get("temperature", 0.3),
                            "maxTokens": self.config["n8n"].get("openai", {}).get("max_tokens", 1000)
                        },
                        "messages": {
                            "values": [
                                {
                                    "role": "system",
                                    "content": "You are a multilingual personal assistant that understands user intent in multiple languages. Analyze the user's message and determine their intent.\n\nSupported intents:\n- tasks: Questions about tasks, projects, what to work on today\n- health: Health tracking, fitness, wellness questions\n- learning: Learning progress, courses, education\n- shadow_work: Shadow work, archetypes, personal development\n- journal: Journal entries, patterns, insights\n- goals: Goals, progress, achievements\n- values: Core values, life direction\n- help: General help, what can you do\n- unknown: Unclear or unrecognized intent\n\nRespond with a JSON object containing:\n- intent: The detected intent\n- confidence: Confidence score (0-1)\n- language: Detected language (en, ru, etc.)\n- response: A helpful response in the user's language\n- action: Any specific action to take\n- reasoning: Brief explanation of the intent detection"
                                },
                                {
                                    "role": "user",
                                    "content": "User message: \"{{ $json.text }}\"\nUser context: {{ JSON.stringify($json.context) }}\nLanguage hint: {{ $json.language_hint }}\n\nDetect the intent and provide a helpful response in the user's language."
                                }
                            ]
                        }
                    },
                    "id": "ai-intent-detection",
                    "name": "AI Intent Detection",
                    "type": "n8n-nodes-base.openAi",
                    "typeVersion": 1,
                    "position": [680, 300]
                },
                {
                    "parameters": {
                        "jsCode": "// Parse AI response and structure the output\nconst aiResponse = $input.first().json.choices[0].message.content;\n\nlet parsedResponse;\ntry {\n  // Try to parse as JSON first\n  parsedResponse = JSON.parse(aiResponse);\n} catch (e) {\n  // If not JSON, create a structured response\n  parsedResponse = {\n    intent: \"unknown\",\n    confidence: 0.5,\n    language: \"en\",\n    response: aiResponse,\n    action: {},\n    reasoning: \"Could not parse AI response as JSON\"\n  };\n}\n\n// Add metadata\nparsedResponse.metadata = {\n  processed_at: new Date().toISOString(),\n  user_id: $('Extract Data').first().json.user_id,\n  original_text: $('Extract Data').first().json.text\n};\n\nreturn parsedResponse;"
                    },
                    "id": "response-processor",
                    "name": "Process Response",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [900, 300]
                },
                {
                    "parameters": {
                        "respondWith": "json",
                        "responseBody": "={{ $json }}"
                    },
                    "id": "webhook-response",
                    "name": "Webhook Response",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "typeVersion": 1,
                    "position": [1120, 300]
                }
            ],
            "connections": {
                "Webhook Trigger": {
                    "main": [
                        [
                            {
                                "node": "Extract Data",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "Extract Data": {
                    "main": [
                        [
                            {
                                "node": "AI Intent Detection",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "AI Intent Detection": {
                    "main": [
                        [
                            {
                                "node": "Process Response",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "Process Response": {
                    "main": [
                        [
                            {
                                "node": "Webhook Response",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "active": True,
            "settings": {
                "executionOrder": "v1"
            }
        }
        
        try:
            headers = {"Content-Type": "application/json"}
            if self.config["n8n"]["api_key"]:
                headers["Authorization"] = f"Bearer {self.config['n8n']['api_key']}"
            elif self.config["n8n"]["username"] and self.config["n8n"]["password"]:
                import base64
                credentials = base64.b64encode(
                    f"{self.config['n8n']['username']}:{self.config['n8n']['password']}".encode()
                ).decode()
                headers["Authorization"] = f"Basic {credentials}"
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.config['n8n']['base_url']}/api/v1/workflows",
                    json=workflow_data,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    workflow_id = response.json().get("id")
                    print(f"✅ Successfully created workflow with ID: {workflow_id}")
                    print(f"🌐 Webhook URL: {self.config['n8n']['base_url']}/webhook/{self.config['n8n']['webhook_path']}")
                    return True
                else:
                    print(f"❌ Failed to create workflow: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error creating workflow: {e}")
            return False
    
    async def test_webhook(self) -> bool:
        """Test the webhook endpoint."""
        print("🧪 Testing webhook endpoint...")
        
        test_payload = {
            "text": "Какие у меня задачи на сегодня?",
            "user_id": 12345,
            "message_type": "voice",
            "timestamp": "2025-01-27T10:00:00Z",
            "context": {
                "user_id": 12345,
                "preferred_language": "ru",
                "current_projects": ["Test Project 1", "Test Project 2"]
            },
            "language_hint": "ru"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.config['n8n']['base_url']}/webhook/{self.config['n8n']['webhook_path']}",
                    json=test_payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Webhook test successful!")
                    print(f"📊 Response: {json.dumps(result, indent=2)}")
                    return True
                else:
                    print(f"❌ Webhook test failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Webhook test error: {e}")
            return False
    
    def interactive_setup(self):
        """Interactive setup for n8n configuration."""
        print("🚀 n8n Multilingual Integration Setup")
        print("=" * 50)
        
        # Get n8n URL
        current_url = self.config["n8n"]["base_url"]
        new_url = input(f"Enter your n8n instance URL [{current_url}]: ").strip()
        if new_url:
            self.config["n8n"]["base_url"] = new_url
        
        # Get authentication method
        print("\nAuthentication method:")
        print("1. API Key (recommended)")
        print("2. Username/Password")
        
        auth_choice = input("Choose authentication method [1]: ").strip() or "1"
        
        if auth_choice == "1":
            api_key = input("Enter your n8n API key: ").strip()
            if api_key:
                self.config["n8n"]["api_key"] = api_key
                self.config["n8n"]["username"] = ""
                self.config["n8n"]["password"] = ""
        else:
            username = input("Enter your n8n username: ").strip()
            password = input("Enter your n8n password: ").strip()
            if username and password:
                self.config["n8n"]["username"] = username
                self.config["n8n"]["password"] = password
                self.config["n8n"]["api_key"] = ""
        
        # Get OpenAI API key
        openai_key = input("Enter your OpenAI API key (for n8n workflow): ").strip()
        if openai_key:
            if "openai" not in self.config["n8n"]:
                self.config["n8n"]["openai"] = {}
            self.config["n8n"]["openai"]["api_key"] = openai_key
        
        # Save configuration
        self.save_config()
    
    async def run_setup(self):
        """Run the complete setup process."""
        print("🚀 Starting n8n Multilingual Integration Setup")
        print("=" * 60)
        
        # Interactive setup
        self.interactive_setup()
        
        # Test connection
        if not await self.test_connection():
            print("❌ Setup failed: Could not connect to n8n instance")
            return False
        
        # Create workflow
        if not await self.create_workflow():
            print("❌ Setup failed: Could not create workflow")
            return False
        
        # Test webhook
        if not await self.test_webhook():
            print("⚠️ Setup completed but webhook test failed")
            print("💡 You may need to configure OpenAI API key in n8n")
            return False
        
        print("\n🎉 Setup completed successfully!")
        print("✅ n8n integration is ready to use")
        print(f"🌐 Webhook URL: {self.config['n8n']['base_url']}/webhook/{self.config['n8n']['webhook_path']}")
        return True


async def main():
    """Main setup function."""
    setup = N8nSetup()
    await setup.run_setup()


if __name__ == "__main__":
    asyncio.run(main())
