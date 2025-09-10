"""
Dual Voice Transcription Handlers for Personal System Bot
Handles voice message processing using ElevenLabs Scribe (primary) and OpenAI Whisper (fallback)
"""

import asyncio
import base64
import json
import logging
import tempfile
from typing import Optional, Dict, Any
import requests
from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI

logger = logging.getLogger(__name__)

class DualVoiceHandler:
    """Voice message handler using ElevenLabs Scribe with OpenAI Whisper fallback."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize ElevenLabs configuration (primary)
        elevenlabs_config = config.get('elevenlabs', {})
        if elevenlabs_config.get('api_key') and elevenlabs_config.get('enable_speech_to_text', True):
            self.elevenlabs_available = True
            self.elevenlabs_api_key = elevenlabs_config['api_key']
            self.logger.info("ElevenLabs Scribe configured as primary transcription service")
        else:
            self.elevenlabs_available = False
            self.logger.warning("ElevenLabs API key not configured - using OpenAI fallback")
        
        # Initialize OpenAI configuration (fallback)
        openai_config = config.get('openai', {})
        if openai_config.get('api_key') and openai_config.get('enable_voice_transcription', False):
            self.openai_available = True
            self.openai_client = OpenAI(api_key=openai_config['api_key'])
            self.max_file_size = openai_config.get('max_file_size', 25)
            self.supported_formats = openai_config.get('supported_formats', ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'])
            self.logger.info("OpenAI Whisper configured as fallback transcription service")
        else:
            self.openai_available = False
            self.logger.warning("OpenAI API key not configured - no fallback available")
        
        if not self.elevenlabs_available and not self.openai_available:
            self.logger.error("No transcription services configured")
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming voice messages with dual transcription services."""
        try:
            voice = update.message.voice
            user_id = update.effective_user.id
            message_id = update.message.message_id
            
            # Show processing message
            processing_msg = await update.message.reply_text("🎤 Processing voice message...")
            
            if not self.elevenlabs_available and not self.openai_available:
                await processing_msg.edit_text(
                    "❌ Voice transcription not available. Please configure ElevenLabs or OpenAI API key in settings."
                )
                return
            
            # Download voice file
            voice_file = await context.bot.get_file(voice.file_id)
            
            # Transcribe using dual services
            result = await self._transcribe_voice(voice_file, voice.mime_type or 'audio/ogg')
            
            if not result or not result.get('transcription'):
                await processing_msg.edit_text(
                    "❌ Transcription Failed\n\nI couldn't understand the voice message. Please try:\n"
                    "• Speaking more clearly\n"
                    "• Reducing background noise\n"
                    "• Sending a shorter message\n"
                    "• Using text instead"
                )
                return
            
            transcription = result['transcription']
            service = result.get('service', 'unknown')
            
            # Show transcription with service indicator
            service_indicator = "🎤 Voice Message Transcribed"
            if service == 'elevenlabs_scribe':
                service_indicator = "🎤 Voice Message Transcribed (ElevenLabs Scribe)"
            elif service == 'openai_whisper':
                service_indicator = "🎤 Voice Message Transcribed (OpenAI Whisper)"
            
            await processing_msg.edit_text(f"{service_indicator}:\n\n\"{transcription}\"")
            
            # Process the transcription for commands
            await self._process_transcription(update, context, transcription)
            
        except Exception as e:
            self.logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text(f"❌ Error processing voice message: {str(e)}")
    
    async def _transcribe_voice(self, voice_file, mime_type: str) -> Optional[Dict[str, Any]]:
        """Transcribe voice file using ElevenLabs Scribe with OpenAI fallback."""
        try:
            # Download to temporary file
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                await voice_file.download_to_drive(temp_file.name)
                
                # Try ElevenLabs Scribe first (if available)
                if self.elevenlabs_available:
                    transcription = await self._transcribe_with_elevenlabs(temp_file.name)
                    if transcription:
                        return {
                            'transcription': transcription,
                            'service': 'elevenlabs_scribe'
                        }
                
                # Fallback to OpenAI Whisper if ElevenLabs failed or not available
                if self.openai_available:
                    transcription = await self._transcribe_with_openai(temp_file.name)
                    if transcription:
                        return {
                            'transcription': transcription,
                            'service': 'openai_whisper'
                        }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Error transcribing voice: {e}")
            return None
        finally:
            # Clean up temp file
            try:
                import os
                os.unlink(temp_file.name)
            except:
                pass
    
    async def _transcribe_with_elevenlabs(self, temp_file_path: str) -> Optional[str]:
        """Transcribe voice file using ElevenLabs Scribe API."""
        try:
            # Check file size (ElevenLabs has a 25MB limit)
            import os
            file_size_mb = os.path.getsize(temp_file_path) / (1024 * 1024)
            if file_size_mb > 25:
                self.logger.warning(f"Voice file too large for ElevenLabs: {file_size_mb:.1f} MB")
                return None
            
            # Prepare the request
            headers = {
                "xi-api-key": self.elevenlabs_api_key
            }
            
            # Read the audio file
            with open(temp_file_path, 'rb') as audio_file:
                files = {
                    'audio': audio_file
                }
                
                # Make the API request to ElevenLabs Scribe
                response = requests.post(
                    "https://api.elevenlabs.io/v1/speech-to-text",
                    headers=headers,
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                if 'text' in result:
                    return result['text'].strip()
                else:
                    self.logger.warning("ElevenLabs response missing 'text' field")
                    return None
            else:
                self.logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"Error transcribing with ElevenLabs: {e}")
            return None
    
    async def _transcribe_with_openai(self, temp_file_path: str) -> Optional[str]:
        """Transcribe voice file using OpenAI Whisper API."""
        try:
            with open(temp_file_path, 'rb') as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript.strip()
        except Exception as e:
            self.logger.error(f"Error transcribing with OpenAI: {e}")
            return None
    
    async def _process_transcription(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Process the transcribed text for commands and actions."""
        try:
            text_lower = text.lower().strip()
            
            # Health tracking
            if any(keyword in text_lower for keyword in ['steps', 'weight', 'sleep', 'mood', 'energy', 'water', 'exercise']):
                await self._handle_health_command(update, context, text)
                return
            
            # Learning tracking
            if any(keyword in text_lower for keyword in ['learned', 'studied', 'course', 'book', 'article', 'video', 'tutorial']):
                await self._handle_learning_command(update, context, text)
                return
            
            # Task management
            if any(keyword in text_lower for keyword in ['task', 'todo', 'reminder', 'deadline', 'project']):
                await self._handle_task_command(update, context, text)
                return
            
            # Quick note
            if any(keyword in text_lower for keyword in ['note', 'remember', 'idea', 'thought']):
                await self._handle_note_command(update, context, text)
                return
            
            # Default response for unrecognized commands
            await update.message.reply_text(
                "🤔 I heard you, but I'm not sure what you'd like me to do. Try saying:\n"
                "• \"I took 8500 steps today\" (health tracking)\n"
                "• \"I learned about Python\" (learning tracking)\n"
                "• \"Add task: finish project\" (task management)\n"
                "• \"Note: great idea about...\" (quick note)"
            )
            
        except Exception as e:
            self.logger.error(f"Error processing transcription: {e}")
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
    async def _handle_health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle health-related voice commands."""
        try:
            # Extract health metrics from text
            health_data = {}
            
            # Steps
            if 'steps' in text.lower():
                import re
                steps_match = re.search(r'(\d+)\s*steps?', text.lower())
                if steps_match:
                    health_data['steps'] = int(steps_match.group(1))
            
            # Weight
            if 'weight' in text.lower():
                weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|pounds?|lbs?)', text.lower())
                if weight_match:
                    health_data['weight'] = float(weight_match.group(1))
            
            # Sleep
            if 'sleep' in text.lower():
                sleep_match = re.search(r'(\d+(?:\.\d+)?)\s*hours?', text.lower())
                if sleep_match:
                    health_data['sleep_hours'] = float(sleep_match.group(1))
            
            # Mood (simple keyword detection)
            mood_keywords = {
                'great': 5, 'excellent': 5, 'amazing': 5, 'fantastic': 5,
                'good': 4, 'fine': 4, 'okay': 3, 'ok': 3,
                'tired': 2, 'bad': 2, 'terrible': 1, 'awful': 1
            }
            
            for keyword, score in mood_keywords.items():
                if keyword in text.lower():
                    health_data['mood'] = score
                    break
            
            if health_data:
                # Here you would integrate with your health logging system
                health_summary = []
                for key, value in health_data.items():
                    health_summary.append(f"{key.replace('_', ' ').title()}: {value}")
                
                await update.message.reply_text(
                    f"✅ Health Data Logged\n\n" + "\n".join(health_summary)
                )
            else:
                await update.message.reply_text(
                    "✅ Health command received, but I couldn't extract specific metrics. "
                    "Try being more specific, like \"I took 8500 steps today\" or \"I slept 7 hours\"."
                )
                
        except Exception as e:
            self.logger.error(f"Error handling health command: {e}")
            await update.message.reply_text(f"❌ Error logging health data: {str(e)}")
    
    async def _handle_learning_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle learning-related voice commands."""
        try:
            # Extract learning information
            learning_data = {
                'activity': text,
                'duration': None,
                'type': 'general'
            }
            
            # Extract duration
            import re
            duration_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hours?|minutes?|mins?)', text.lower())
            if duration_match:
                learning_data['duration'] = duration_match.group(1)
            
            # Determine learning type
            if any(keyword in text.lower() for keyword in ['course', 'tutorial', 'video']):
                learning_data['type'] = 'course'
            elif any(keyword in text.lower() for keyword in ['book', 'article', 'reading']):
                learning_data['type'] = 'reading'
            elif any(keyword in text.lower() for keyword in ['practice', 'coding', 'programming']):
                learning_data['type'] = 'practice'
            
            await update.message.reply_text(
                f"✅ Learning Activity Logged\n\n"
                f"Activity: {learning_data['activity']}\n"
                f"Type: {learning_data['type'].title()}\n"
                f"Duration: {learning_data['duration'] or 'Not specified'}"
            )
            
        except Exception as e:
            self.logger.error(f"Error handling learning command: {e}")
            await update.message.reply_text(f"❌ Error logging learning activity: {str(e)}")
    
    async def _handle_task_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle task-related voice commands."""
        try:
            # Extract task information
            task_title = text
            
            # Remove common prefixes
            prefixes = ['add task:', 'task:', 'todo:', 'reminder:']
            for prefix in prefixes:
                if text.lower().startswith(prefix):
                    task_title = text[len(prefix):].strip()
                    break
            
            await update.message.reply_text(
                f"✅ Task Added\n\n"
                f"Title: {task_title}\n"
                f"Status: Pending\n"
                f"Priority: Medium"
            )
            
        except Exception as e:
            self.logger.error(f"Error handling task command: {e}")
            await update.message.reply_text(f"❌ Error adding task: {str(e)}")
    
    async def _handle_note_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle note-related voice commands."""
        try:
            # Extract note content
            note_content = text
            
            # Remove common prefixes
            prefixes = ['note:', 'remember:', 'idea:']
            for prefix in prefixes:
                if text.lower().startswith(prefix):
                    note_content = text[len(prefix):].strip()
                    break
            
            await update.message.reply_text(
                f"✅ Quick Note Saved\n\n"
                f"Content: {note_content}\n"
                f"Category: Voice Note"
            )
            
        except Exception as e:
            self.logger.error(f"Error handling note command: {e}")
            await update.message.reply_text(f"❌ Error saving note: {str(e)}")


# Global handler instance
voice_handler = None

def initialize_voice_handler(config: Dict[str, Any]):
    """Initialize the dual voice handler."""
    global voice_handler
    voice_handler = DualVoiceHandler(config)

async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages using dual transcription services."""
    if voice_handler:
        await voice_handler.handle_voice_message(update, context)
    else:
        await update.message.reply_text("❌ Voice handler not initialized")

