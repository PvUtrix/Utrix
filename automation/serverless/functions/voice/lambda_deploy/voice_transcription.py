"""
Voice Transcription Serverless Function
Handles voice message transcription using OpenAI Whisper API
"""

import json
import os
import tempfile
import base64
from typing import Dict, Any, Optional
import logging
from openai import OpenAI

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
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
        # Initialize OpenAI client
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': 'OpenAI API key not configured'
                })
            }
        
        client = OpenAI(api_key=openai_api_key)
        
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
            # Transcribe using OpenAI Whisper
            with open(temp_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            # Return successful transcription
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'transcription': transcript.strip(),
                    'user_id': user_id,
                    'message_id': message_id,
                    'service': 'openai_whisper'
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


def vercel_handler(request):
    """
    Vercel serverless function handler for voice transcription.
    """
    try:
        # Initialize OpenAI client
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': 'OpenAI API key not configured'
                })
            }
        
        client = OpenAI(api_key=openai_api_key)
        
        # Parse request
        if request.method != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({
                    'success': False,
                    'error': 'Method not allowed'
                })
            }
        
        body = request.get_json()
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
            # Transcribe using OpenAI Whisper
            with open(temp_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            # Return successful transcription
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'transcription': transcript.strip(),
                    'user_id': user_id,
                    'message_id': message_id,
                    'service': 'openai_whisper'
                })
            }
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': f'Transcription failed: {str(e)}'
                })
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            })
        }
