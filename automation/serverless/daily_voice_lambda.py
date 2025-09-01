#!/usr/bin/env python3
"""
Daily Voice Message Lambda Function
Generates and sends personalized daily voice messages via Telegram
"""

import json
import os
import base64
from datetime import datetime
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError
import requests
import logging

# Import our custom modules
from voice_content_generator import VoiceContentGenerator
from elevenlabs_tts import ElevenLabsTTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DailyVoiceBot:
    def __init__(self):
        self.content_generator = VoiceContentGenerator()
        self.tts = ElevenLabsTTS()

        # Telegram configuration
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.telegram_api_url = f"https://api.telegram.org/bot{self.telegram_token}"

        # AWS S3 for temporary storage (if needed)
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv('VOICE_BUCKET_NAME', 'daily-voice-messages')

    def generate_and_send_voice_message(self) -> Dict[str, Any]:
        """Main function to generate and send daily voice message"""
        logger.info("🎤 Starting daily voice message generation")

        try:
            # Step 1: Generate personalized content
            logger.info("📝 Generating personalized content...")
            text_content = self.content_generator.generate_daily_voice_content()

            if not text_content:
                return {
                    'success': False,
                    'error': 'Failed to generate content'
                }

            # Step 2: Validate content length for ElevenLabs free tier
            if not self.tts.validate_text_length(text_content):
                # Truncate if too long
                words = text_content.split()
                text_content = " ".join(words[:400]) + "."
                logger.warning("⚠️ Content truncated for free tier limits")

            # Step 3: Generate speech
            logger.info("🎵 Generating speech with ElevenLabs...")
            audio_data = self.tts.generate_speech(text_content)

            if not audio_data:
                return {
                    'success': False,
                    'error': 'Failed to generate speech'
                }

            # Step 4: Send via Telegram
            logger.info("📤 Sending voice message via Telegram...")
            result = self.send_voice_message(audio_data, text_content)

            if result['success']:
                # Step 5: Log success and save to database
                self._log_voice_message(text_content, len(audio_data))
                logger.info("✅ Daily voice message sent successfully!")
                return {
                    'success': True,
                    'message': 'Voice message sent successfully',
                    'word_count': len(text_content.split()),
                    'audio_size': len(audio_data),
                    'estimated_cost': self.tts.estimate_cost(text_content)
                }
            else:
                logger.error(f"❌ Failed to send voice message: {result.get('error')}")
                return {
                    'success': False,
                    'error': result.get('error')
                }

        except Exception as e:
            logger.error(f"❌ Error in voice message generation: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def send_voice_message(self, audio_data: bytes, caption: str = None) -> Dict[str, Any]:
        """Send voice message via Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            return {'success': False, 'error': 'Telegram credentials not configured'}

        try:
            # Prepare the voice message
            files = {
                'voice': ('daily_message.mp3', audio_data, 'audio/mpeg')
            }

            data = {
                'chat_id': self.telegram_chat_id,
                'duration': min(180, len(audio_data) // 16000),  # Rough duration estimate
                'caption': caption[:1024] if caption else None  # Telegram caption limit
            }

            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}

            response = requests.post(
                f"{self.telegram_api_url}/sendVoice",
                data=data,
                files=files,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info(f"✅ Voice message sent, message ID: {result['result']['message_id']}")
                    return {'success': True}
                else:
                    return {'success': False, 'error': result.get('description', 'Unknown error')}
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}: {response.text}'
                }

        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Request timed out'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _log_voice_message(self, content: str, audio_size: int):
        """Log voice message details to database"""
        try:
            # Save to core database for recent messages
            core_db = self.content_generator.core_db

            log_entry = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'content_preview': content[:200] + "..." if len(content) > 200 else content,
                'word_count': len(content.split()),
                'audio_size_bytes': audio_size,
                'elevenlabs_cost': self.tts.estimate_cost(content),
                'sent_at': datetime.now().isoformat(),
                'status': 'sent'
            }

            core_db.table('voice_messages').insert(log_entry).execute()
            logger.info("📊 Voice message logged to database")

        except Exception as e:
            logger.warning(f"Could not log voice message: {e}")

    def get_voice_history(self, days: int = 7) -> Dict[str, Any]:
        """Get voice message history"""
        try:
            core_db = self.content_generator.core_db

            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

            response = core_db.table('voice_messages') \
                .select('*') \
                .gte('date', start_date) \
                .order('sent_at', desc=True) \
                .execute()

            return {
                'success': True,
                'messages': response.data,
                'count': len(response.data)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def lambda_handler(event, context):
    """AWS Lambda handler for daily voice messages"""
    bot = DailyVoiceBot()

    action = event.get('action', 'send_daily')

    if action == 'send_daily':
        result = bot.generate_and_send_voice_message()
        return {
            'statusCode': 200 if result['success'] else 500,
            'body': json.dumps(result)
        }

    elif action == 'history':
        days = event.get('days', 7)
        history = bot.get_voice_history(days)
        return {
            'statusCode': 200 if history['success'] else 500,
            'body': json.dumps(history)
        }

    elif action == 'preview':
        # Generate content without sending
        try:
            content = bot.content_generator.generate_daily_voice_content()
            word_count = len(content.split())
            estimated_duration = word_count * 0.25  # Rough estimate in seconds
            cost = bot.tts.estimate_cost(content)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'content': content,
                    'word_count': word_count,
                    'estimated_duration_seconds': estimated_duration,
                    'estimated_cost': cost,
                    'will_fit_3min_limit': estimated_duration <= 180
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    return {'statusCode': 400, 'body': 'Invalid action'}

if __name__ == "__main__":
    # Local testing
    import sys

    bot = DailyVoiceBot()

    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == 'preview':
            print("🎤 Generating preview of today's voice message...")

            # Test content generation
            content = bot.content_generator.generate_daily_voice_content()
            print(f"\nContent Preview:\n{content[:300]}...")

            word_count = len(content.split())
            duration = word_count * 0.25
            cost = bot.tts.estimate_cost(content)

            print("
📊 Stats:"            print(f"  Words: {word_count}")
            print(f"  Duration: {duration:.1f} seconds")
            print(f"  Cost: ${cost:.6f}")
            print(f"  Under 3min: {'✅' if duration <= 180 else '❌'}")

        elif action == 'history':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            history = bot.get_voice_history(days)
            if history['success']:
                print(f"📚 Voice message history (last {days} days):")
                for msg in history['messages'][:5]:  # Show last 5
                    print(f"  {msg['date']}: {msg['word_count']} words, ${msg['elevenlabs_cost']:.6f}")
            else:
                print(f"❌ Error getting history: {history.get('error')}")

        else:
            print("Usage: python3 daily_voice_lambda.py [preview|history [days]]")

    else:
        print("🎤 Daily Voice Message Bot")
        print("Usage: python3 daily_voice_lambda.py [preview|history [days]]")
        print("\nExample: python3 daily_voice_lambda.py preview")
