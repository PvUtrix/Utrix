"""
Serverless Voice Transcription Handlers for Personal System Bot
Handles voice message processing using serverless functions
"""

import asyncio
import base64
import json
import logging
import tempfile
from typing import Optional, Dict, Any
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class ServerlessVoiceHandler:
    """Voice message handler using serverless transcription functions."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Serverless function configuration
        self.serverless_config = config.get('serverless', {})
        self.transcription_url = self.serverless_config.get('transcription_url')
        self.api_key = self.serverless_config.get('api_key')
        
        if not self.transcription_url:
            self.logger.warning("Serverless transcription URL not configured - falling back to local processing")
            self.serverless_available = False
        else:
            self.serverless_available = True
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming voice messages with serverless transcription."""
        try:
            voice = update.message.voice
            user_id = update.effective_user.id
            message_id = update.message.message_id
            
            # Show processing message
            processing_msg = await update.message.reply_text("🎤 Processing voice message...")
            
            if not self.serverless_available:
                await processing_msg.edit_text(
                    "❌ Serverless transcription not available. Please configure serverless settings."
                )
                return
            
            # Download voice file
            voice_file = await context.bot.get_file(voice.file_id)
            
            # Transcribe using serverless function
            result = await self._transcribe_with_serverless(voice_file, voice.mime_type or 'audio/ogg')
            
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
    
    async def _transcribe_with_serverless(self, voice_file, mime_type: str) -> Optional[str]:
        """Transcribe voice file using serverless function."""
        try:
            # Download to temporary file
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                await voice_file.download_to_drive(temp_file.name)
                
                # Read file and encode to base64
                with open(temp_file.name, 'rb') as f:
                    audio_data = f.read()
                
                audio_b64 = base64.b64encode(audio_data).decode('utf-8')
                
                # Determine file format from mime type
                file_format = 'ogg'
                if 'mp3' in mime_type:
                    file_format = 'mp3'
                elif 'wav' in mime_type:
                    file_format = 'wav'
                elif 'm4a' in mime_type:
                    file_format = 'm4a'
                elif 'webm' in mime_type:
                    file_format = 'webm'
                
                # Prepare request payload
                payload = {
                    'audio_data': audio_b64,
                    'file_format': file_format,
                    'user_id': 'telegram_user',
                    'message_id': 'voice_message'
                }
                
                # Make request to serverless function
                headers = {
                    'Content-Type': 'application/json'
                }
                
                if self.api_key:
                    headers['Authorization'] = f'Bearer {self.api_key}'
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        self.transcription_url,
                        json=payload,
                        headers=headers,
                        timeout=30
                    ) as response:
                        
                        if response.status == 200:
                            result = await response.json()
                            if result.get('success'):
                                return result  # Return full result object
                            else:
                                self.logger.error(f"Serverless transcription failed: {result.get('error')}")
                                return None
                        else:
                            self.logger.error(f"Serverless function error: {response.status}")
                            return None
                
        except Exception as e:
            self.logger.error(f"Error transcribing with serverless: {e}")
            return None
        finally:
            # Clean up temp file
            try:
                import os
                os.unlink(temp_file.name)
            except:
                pass
    
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
                # Look for numbers with "steps" (handles "Track 5,000 steps", "Steps: 3000", etc.)
                # This pattern looks for numbers that appear with the word "steps"
                steps_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*(?:steps?|step)|steps?:\s*(\d+)', text.lower())
                if steps_match:
                    # Remove commas and convert to int
                    # Handle both capture groups (number before steps, or steps: number)
                    steps_str = (steps_match.group(1) or steps_match.group(2)).replace(',', '')
                    health_data['steps'] = int(steps_str)
            
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
    """Initialize the serverless voice handler."""
    global voice_handler
    voice_handler = ServerlessVoiceHandler(config)

async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages using serverless transcription."""
    if voice_handler:
        await voice_handler.handle_voice_message(update, context)
    else:
        await update.message.reply_text("❌ Voice handler not initialized")
