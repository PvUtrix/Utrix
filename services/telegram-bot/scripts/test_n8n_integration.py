#!/usr/bin/env python3
"""
Test script for n8n Multilingual Integration
Tests the integration with your existing n8n instance
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.append(str(Path(__file__).parent.parent))

from integrations.n8n_multilingual_agent import N8nMultilingualAgent
from integrations.ai_assistant import AIAssistant
import yaml


async def test_n8n_integration():
    """Test the n8n integration with sample messages."""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print("🧪 Testing n8n Multilingual Integration")
    print("=" * 50)
    
    # Test cases
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
        },
        {
            "text": "What are my shadow archetypes?",
            "language": "English",
            "expected_intent": "shadow_work"
        },
        {
            "text": "Что я изучал сегодня?",
            "language": "Russian",
            "expected_intent": "learning"
        }
    ]
    
    # Initialize the n8n agent
    n8n_agent = N8nMultilingualAgent(config)
    
    print(f"🔗 n8n URL: {config['n8n']['base_url']}")
    print(f"📡 Webhook: {config['n8n']['base_url']}/webhook/{config['n8n']['webhook_path']}")
    print()
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['language']} - '{test_case['text']}'")
        print("-" * 40)
        
        try:
            result = await n8n_agent.process_message(
                text=test_case['text'],
                user_id=12345,
                message_type="text"
            )
            
            print(f"✅ Intent: {result['intent']}")
            print(f"📊 Confidence: {result['confidence']:.2f}")
            print(f"🌐 Language: {result['language']}")
            print(f"🔧 Source: {result['source']}")
            print(f"💬 Response: {result['response_text'][:100]}...")
            
            if result['intent'] == test_case['expected_intent']:
                print("✅ Intent detection correct!")
            else:
                print(f"⚠️ Expected '{test_case['expected_intent']}', got '{result['intent']}'")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    # Test fallback processing
    print("🔄 Testing fallback processing...")
    print("-" * 40)
    
    try:
        # Temporarily disable n8n to test fallback
        original_url = config['n8n']['base_url']
        config['n8n']['base_url'] = "http://nonexistent:5678"
        
        fallback_agent = N8nMultilingualAgent(config)
        result = await fallback_agent.process_message(
            text="What should I work on today?",
            user_id=12345,
            message_type="text"
        )
        
        print(f"✅ Fallback Intent: {result['intent']}")
        print(f"📊 Confidence: {result['confidence']:.2f}")
        print(f"🔧 Source: {result['source']}")
        print("✅ Fallback processing works!")
        
        # Restore original URL
        config['n8n']['base_url'] = original_url
        
    except Exception as e:
        print(f"❌ Fallback test error: {e}")
    
    print("\n🎉 Testing completed!")


async def test_ai_assistant_integration():
    """Test the AI assistant with n8n integration."""
    
    print("\n🤖 Testing AI Assistant with n8n Integration")
    print("=" * 50)
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    ai_assistant = AIAssistant(config)
    
    test_messages = [
        "Какие у меня задачи на сегодня?",
        "What are my shadow archetypes?",
        "Как дела с обучением?",
        "What should I work on today?"
    ]
    
    for message in test_messages:
        print(f"Testing: '{message}'")
        print("-" * 30)
        
        try:
            response = await ai_assistant.get_response(message, 12345)
            print(f"Response: {response[:200]}...")
            print("✅ Success!")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()


async def main():
    """Main test function."""
    await test_n8n_integration()
    await test_ai_assistant_integration()


if __name__ == "__main__":
    asyncio.run(main())
