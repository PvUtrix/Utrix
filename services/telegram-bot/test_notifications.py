#!/usr/bin/env python3
"""
Test script to verify notification system works.
"""

import asyncio
import yaml
from bot.bot import PersonalSystemBot

async def test_notifications():
    """Test the notification system."""
    print("🧪 Testing notification system...")
    
    # Load config
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create bot instance
    bot = PersonalSystemBot(config)
    
    # Test startup notification
    print("📤 Testing startup notification...")
    await bot._send_startup_notification()
    
    # Test shutdown notification
    print("📤 Testing shutdown notification...")
    await bot._send_shutdown_notification()
    
    print("✅ Notification tests completed!")
    print("\n🚀 To test with the actual bot:")
    print("1. Run: python main.py")
    print("2. Send /test_notification to your bot")
    print("3. The bot will send you startup/shutdown messages automatically")

if __name__ == "__main__":
    asyncio.run(test_notifications())
