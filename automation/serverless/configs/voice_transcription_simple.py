#!/usr/bin/env python3
"""
Simple Voice Transcription Lambda Function
Handles voice message transcription using ElevenLabs Scribe (primary) and OpenAI Whisper (fallback)
"""

import json
import os
import tempfile
import base64
import logging
import requests

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def transcribe_with_elevenlabs(temp_file_path: str, api_key: str) -> str:
    """Transcribe audio using ElevenLabs Scribe API."""
    try:
        # Check file size (ElevenLabs has a 25MB limit)
        file_size_mb = os.path.getsize(temp_file_path) / (1024 * 1024)
        if file_size_mb > 25:
            logger.warning(f"Voice file too large for ElevenLabs: {file_size_mb:.1f} MB")
            return None
        
        # Prepare the request
        headers = {
            "xi-api-key": api_key
        }
        
        # Read the audio file
        with open(temp_file_path, 'rb') as audio_file:
            files = {
                'file': audio_file
            }
            
            data = {
                'model_id': 'scribe_v1'
            }
            
            # Make the API request to ElevenLabs Scribe
            response = requests.post(
                "https://api.elevenlabs.io/v1/speech-to-text",
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            if 'text' in result:
                return result['text'].strip()
            else:
                logger.warning("ElevenLabs response missing 'text' field")
                return None
        else:
            logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        logger.error(f"Error transcribing with ElevenLabs: {e}")
        return None

def transcribe_with_openai(temp_file_path: str, api_key: str) -> str:
    """Transcribe audio using OpenAI Whisper API."""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        with open(temp_file_path, 'rb') as audio_file:
            files = {
                'file': audio_file,
                'model': (None, 'whisper-1')
            }
            
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('text', '').strip()
        else:
            logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        logger.error(f"Error transcribing with OpenAI: {e}")
        return None

def lambda_handler(event, context):
    """
    AWS Lambda handler for voice transcription.
    
    Expected event structure:
    {
        "audio_data": "base64_encoded_audio_data",
        "file_format": "ogg|mp3|wav|m4a|webm",
        "user_id": "telegram_user_id",
        "message_id": "telegram_message_id"
    }
    """
    
    try:
        # Initialize API clients
        elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not elevenlabs_api_key and not openai_api_key:
            logger.error("Neither ELEVENLABS_API_KEY nor OPENAI_API_KEY found in environment variables")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': 'No transcription API keys configured'
                })
            }
        
        # Parse request
        body = json.loads(event.get('body', '{}'))
        audio_data_b64 = body.get('audio_data')
        file_format = body.get('file_format', 'ogg')
        user_id = body.get('user_id')
        message_id = body.get('message_id')
        
        if not audio_data_b64:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'success': False,
                    'error': 'No audio data provided'
                })
            }
        
        # Decode audio data
        try:
            audio_data = base64.b64decode(audio_data_b64)
        except Exception as e:
            logger.error(f"Failed to decode audio data: {e}")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'success': False,
                    'error': 'Invalid audio data format'
                })
            }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=f'.{file_format}', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            # Try ElevenLabs Scribe first (if available)
            transcript = None
            service_used = None
            
            if elevenlabs_api_key:
                transcript = transcribe_with_elevenlabs(temp_file_path, elevenlabs_api_key)
                if transcript:
                    service_used = 'elevenlabs_scribe'
            
            # Fallback to OpenAI Whisper if ElevenLabs failed or not available
            if not transcript and openai_api_key:
                transcript = transcribe_with_openai(temp_file_path, openai_api_key)
                if transcript:
                    service_used = 'openai_whisper'
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            if transcript:
                # Return successful transcription
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'success': True,
                        'transcription': transcript.strip(),
                        'user_id': user_id,
                        'message_id': message_id,
                        'service': service_used
                    })
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'success': False,
                        'error': 'Transcription failed with all available services'
                    })
                }
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            logger.error(f"Transcription failed: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': f'Transcription failed: {str(e)}'
                })
            }
    
    except Exception as e:
        logger.error(f"Lambda handler error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            })
        }

