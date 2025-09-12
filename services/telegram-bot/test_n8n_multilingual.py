#!/usr/bin/env python3
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
        print(f"\nTest {i}: {test_case['language']} - '{test_case['text']}'")
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
