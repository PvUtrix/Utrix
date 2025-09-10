#!/usr/bin/env python3
"""
Simplified Voice Generator Lambda Function
Generates voice content using ElevenLabs API
"""

import json
import os
from datetime import datetime
import requests

def lambda_handler(event, context):
    """
    Generate voice content from text using ElevenLabs
    """
    try:
        # Get environment variables
        elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        elevenlabs_voice_id = os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # Default text to convert to speech
        text_to_speak = event.get('text', """
        Hello! This is your daily voice summary. 
        Your personal system is running smoothly. 
        All functions are operational and within free tier limits.
        Have a great day!
        """)
        
        result = {
            'date': datetime.utcnow().strftime('%Y-%m-%d'),
            'timestamp': datetime.utcnow().isoformat(),
            'text': text_to_speak,
            'voice_id': elevenlabs_voice_id,
            'status': 'success'
        }
        
        # Generate voice if ElevenLabs is configured
        if elevenlabs_key:
            try:
                # ElevenLabs API call
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{elevenlabs_voice_id}"
                headers = {
                    'Accept': 'audio/mpeg',
                    'Content-Type': 'application/json',
                    'xi-api-key': elevenlabs_key
                }
                data = {
                    'text': text_to_speak,
                    'model_id': 'eleven_monolingual_v1',
                    'voice_settings': {
                        'stability': 0.5,
                        'similarity_boost': 0.75
                    }
                }
                
                response = requests.post(url, json=data, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    # Save audio file (in real implementation, you'd save to S3)
                    audio_data = response.content
                    result['audio_generated'] = True
                    result['audio_size_bytes'] = len(audio_data)
                    
                    # Send to Telegram if configured
                    if telegram_token and telegram_chat_id:
                        # Send the actual audio file to Telegram
                        telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendVoice"
                        
                        # Prepare the audio file for upload
                        files = {
                            'voice': ('voice_message.mp3', audio_data, 'audio/mpeg')
                        }
                        
                        data = {
                            'chat_id': telegram_chat_id,
                            'caption': f"🎤 Voice message: {text_to_speak[:100]}..."
                        }
                        
                        try:
                            tg_response = requests.post(telegram_url, files=files, data=data, timeout=30)
                            result['telegram_sent'] = tg_response.status_code == 200
                            if tg_response.status_code != 200:
                                result['telegram_error'] = tg_response.text
                        except Exception as e:
                            result['telegram_error'] = str(e)
                            result['telegram_sent'] = False
                    
                else:
                    result['audio_generated'] = False
                    result['elevenlabs_error'] = f"API returned status {response.status_code}"
                    
            except Exception as e:
                result['audio_generated'] = False
                result['elevenlabs_error'] = str(e)
        else:
            result['audio_generated'] = False
            result['elevenlabs_error'] = 'ElevenLabs API key not configured'
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Voice generation failed',
                'timestamp': datetime.utcnow().isoformat()
            })
        }
