#!/usr/bin/env python3
"""
Test script for ElevenLabs TTS functionality
"""

import os
import sys
import requests
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_elevenlabs_tts():
    """Test ElevenLabs TTS API directly"""
    
    # Get API key from environment or config
    api_key = os.getenv('ELEVENLABS_API_KEY', 'sk_9382e4b7a49fa13e8334898360f9e3bd75ee67cfb27492fc')
    voice_id = '21m00Tcm4TlvDq8ikWAM'
    
    if not api_key:
        print("❌ ElevenLabs API key not found")
        return False
    
    # Test text
    test_text = "Hello! This is a test of the ElevenLabs text-to-speech system. Your morning routine voice guide is working correctly."
    
    try:
        # ElevenLabs voice settings
        voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        payload = {
            "text": test_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": voice_settings
        }
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        print(f"🎤 Testing ElevenLabs TTS...")
        print(f"📝 Text: {test_text}")
        print(f"🔑 API Key: {api_key[:10]}...")
        print(f"🎵 Voice ID: {voice_id}")
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"✅ TTS Success!")
            print(f"📊 Audio size: {len(audio_data)} bytes")
            print(f"⏱️  Estimated duration: ~{len(test_text.split()) * 0.25:.1f} seconds")
            
            # Save test audio file
            with open('test_voice_output.mp3', 'wb') as f:
                f.write(audio_data)
            print(f"💾 Saved test audio as: test_voice_output.mp3")
            
            return True
        else:
            print(f"❌ TTS Failed!")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_scheduler_tts():
    """Test the scheduler TTS functionality"""
    try:
        from core.telegram_interface.scheduler import PersonalSystemScheduler
        from core.telegram_interface.config.config_manager import ConfigManager
        
        print("\n🧪 Testing Scheduler TTS Integration...")
        
        # Load config
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Create a mock bot for testing
        class MockBot:
            def __init__(self):
                self.application = None
        
        # Create scheduler instance
        scheduler = PersonalSystemScheduler(MockBot(), config)
        
        # Test TTS generation
        voice_text = "Your morning routine starts now. Wake up, drink water, and begin your day with intention."
        audio_data = scheduler._generate_speech(voice_text)
        
        if audio_data:
            print("✅ Scheduler TTS integration working!")
            print(f"📊 Generated audio: {len(audio_data)} bytes")
            
            # Save test file
            with open('test_scheduler_voice.mp3', 'wb') as f:
                f.write(audio_data)
            print("💾 Saved scheduler test audio as: test_scheduler_voice.mp3")
            return True
        else:
            print("❌ Scheduler TTS integration failed")
            return False
            
    except Exception as e:
        print(f"❌ Scheduler test error: {e}")
        return False

if __name__ == "__main__":
    print("🎤 ElevenLabs TTS Test Suite")
    print("=" * 40)
    
    # Test 1: Direct API test
    print("\n1️⃣ Testing ElevenLabs API directly...")
    api_success = test_elevenlabs_tts()
    
    # Test 2: Scheduler integration test
    print("\n2️⃣ Testing Scheduler TTS integration...")
    scheduler_success = test_scheduler_tts()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 40)
    print(f"🔗 ElevenLabs API: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"🤖 Scheduler Integration: {'✅ PASS' if scheduler_success else '❌ FAIL'}")
    
    if api_success and scheduler_success:
        print("\n🎉 All tests passed! Voice messages should work in your morning routine.")
    else:
        print("\n⚠️  Some tests failed. Check the configuration and API keys.")
