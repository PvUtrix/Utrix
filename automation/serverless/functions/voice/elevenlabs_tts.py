#!/usr/bin/env python3
"""
ElevenLabs Text-to-Speech Integration
High-quality voice generation for daily messages
"""

import os
import requests
import json
import base64
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElevenLabsTTS:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')  # Default: Rachel
        self.base_url = "https://api.elevenlabs.io/v1"

        # ElevenLabs voice settings for optimal quality
        self.voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }

        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

    def generate_speech(self, text: str, model_id: str = "eleven_monolingual_v1") -> Optional[bytes]:
        """
        Generate speech from text using ElevenLabs
        Returns audio data as bytes
        """
        if not self.api_key:
            logger.error("ElevenLabs API key not found")
            return None

        # Prepare the request payload
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": self.voice_settings
        }

        url = f"{self.base_url}/text-to-speech/{self.voice_id}"

        try:
            logger.info(f"🎵 Generating speech for {len(text)} characters")

            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=60  # ElevenLabs can take time for longer texts
            )

            if response.status_code == 200:
                audio_data = response.content
                logger.info(f"✅ Generated audio: {len(audio_data)} bytes")
                return audio_data
            else:
                logger.error(f"ElevenLabs API error: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return None

        except requests.exceptions.Timeout:
            logger.error("ElevenLabs request timed out")
            return None
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None

    def generate_speech_stream(self, text: str, model_id: str = "eleven_monolingual_v1"):
        """
        Generate speech with streaming for better Lambda performance
        Returns response object for streaming
        """
        if not self.api_key:
            logger.error("ElevenLabs API key not found")
            return None

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": self.voice_settings
        }

        url = f"{self.base_url}/text-to-speech/{self.voice_id}/stream"

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                stream=True,
                timeout=60
            )

            if response.status_code == 200:
                return response
            else:
                logger.error(f"ElevenLabs streaming error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error in streaming speech generation: {e}")
            return None

    def get_voices(self) -> Optional[Dict[str, Any]]:
        """Get available voices from ElevenLabs"""
        if not self.api_key:
            return None

        try:
            response = requests.get(
                f"{self.base_url}/voices",
                headers={"xi-api-key": self.api_key}
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting voices: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return None

    def estimate_cost(self, text: str) -> float:
        """
        Estimate cost for text generation
        ElevenLabs charges per character
        """
        # Rough estimate: ~$0.00015 per character (varies by plan)
        character_count = len(text)
        estimated_cost = character_count * 0.00015
        return round(estimated_cost, 6)

    def validate_text_length(self, text: str, max_chars: int = 10000) -> bool:
        """
        Validate text length for ElevenLabs limits
        Free tier has character limits
        """
        if len(text) > max_chars:
            logger.warning(f"Text too long: {len(text)} chars (max: {max_chars})")
            return False
        return True

def lambda_handler(event, context):
    """AWS Lambda handler for ElevenLabs TTS"""
    tts = ElevenLabsTTS()

    action = event.get('action')

    if action == 'generate':
        text = event.get('text', '')
        if not text:
            return {'statusCode': 400, 'body': 'No text provided'}

        # Validate text length
        if not tts.validate_text_length(text):
            return {'statusCode': 400, 'body': 'Text too long for free tier'}

        # Generate speech
        audio_data = tts.generate_speech(text)

        if audio_data:
            # Return as base64 for Lambda
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'audio_data': audio_b64,
                    'content_type': 'audio/mpeg',
                    'size_bytes': len(audio_data),
                    'estimated_cost': tts.estimate_cost(text)
                })
            }
        else:
            return {'statusCode': 500, 'body': 'Speech generation failed'}

    elif action == 'voices':
        voices = tts.get_voices()
        if voices:
            return {'statusCode': 200, 'body': json.dumps(voices)}
        else:
            return {'statusCode': 500, 'body': 'Could not fetch voices'}

    elif action == 'estimate':
        text = event.get('text', '')
        cost = tts.estimate_cost(text)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'character_count': len(text),
                'estimated_cost_usd': cost
            })
        }

    return {'statusCode': 400, 'body': 'Invalid action'}

if __name__ == "__main__":
    # Local testing
    import sys

    if len(sys.argv) > 1:
        action = sys.argv[1]

        tts = ElevenLabsTTS()

        if action == 'voices':
            voices = tts.get_voices()
            if voices:
                print("Available voices:")
                for voice in voices.get('voices', []):
                    print(f"  {voice['voice_id']}: {voice['name']}")
            else:
                print("Could not fetch voices")

        elif action == 'test':
            test_text = "Hello! This is a test of ElevenLabs text-to-speech."
            print(f"Testing with text: {test_text}")

            audio_data = tts.generate_speech(test_text)
            if audio_data:
                print(f"✅ Generated audio: {len(audio_data)} bytes")
                print(f"💰 Estimated cost: ${tts.estimate_cost(test_text)}")

                # Save to file for testing
                with open('test_output.mp3', 'wb') as f:
                    f.write(audio_data)
                print("💾 Saved to test_output.mp3")
            else:
                print("❌ Speech generation failed")

        else:
            print("Usage: python3 elevenlabs_tts.py [voices|test]")
    else:
        print("ElevenLabs TTS Integration")
        print("Usage: python3 elevenlabs_tts.py [voices|test]")
