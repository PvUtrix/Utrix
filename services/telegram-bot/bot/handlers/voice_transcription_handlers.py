"""
Enhanced Voice Transcription Handlers for Personal System Bot
Provides improved voice message processing with better integration to daily operations
"""

import logging
import os
import tempfile
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command

# Import OpenAI for voice transcription
try:
    import openai
except ImportError:
    openai = None

class VoiceTranscriptionHandler:
    """Enhanced voice message handler with better daily operations integration."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(__name__)
        
        # Initialize OpenAI if available
        openai_config = config.get('openai', {})
        if openai and openai_config.get('api_key'):
            openai.api_key = openai_config['api_key']
            self.openai_available = True
            self.model = openai_config.get('model', 'whisper-1')
            self.max_file_size = openai_config.get('max_file_size', 25)
        else:
            self.openai_available = False
            self.logger.warning("OpenAI not available - voice transcription disabled")
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming voice messages with enhanced processing."""
        user_id = context.user_data.get('user_id')
        username = context.user_data.get('username', 'unknown')
        
        log_command(self.logger, user_id, username, "voice_message")
        
        if not self.openai_available:
            await update.message.reply_text(
                "🎤 **Voice transcription is not available.**\n\n"
                "Please configure OpenAI API key in settings to enable voice commands.",
                parse_mode='Markdown'
            )
            return
        
        if not update.message.voice:
            return
        
        try:
            # Show processing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Download voice file
            voice_file = await context.bot.get_file(update.message.voice.file_id)
            
            # Transcribe voice message
            transcription = await self._transcribe_voice(voice_file)
            
            if not transcription:
                await update.message.reply_text(
                    "❌ **Transcription Failed**\n\n"
                    "I couldn't understand the voice message. Please try:\n"
                    "• Speaking more clearly\n"
                    "• Reducing background noise\n"
                    "• Sending a shorter message\n"
                    "• Using text instead",
                    parse_mode='Markdown'
                )
                return
            
            # Send transcription confirmation
            await update.message.reply_text(
                f"🎤 **Voice Message Transcribed:**\n\n"
                f"*\"{transcription}\"*\n\n"
                f"🔍 **Processing your request...**",
                parse_mode='Markdown'
            )
            
            # Process the transcribed text
            await self._process_transcribed_text(update, context, transcription)
            
        except Exception as e:
            self.logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text(
                "❌ **Error processing voice message**\n\n"
                "Something went wrong. Please try again or use text commands.",
                parse_mode='Markdown'
            )
    
    async def _transcribe_voice(self, voice_file) -> Optional[str]:
        """Transcribe voice file using OpenAI Whisper."""
        try:
            # Download to temporary file
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                await voice_file.download_to_drive(temp_file.name)
                
                # Check file size
                file_size_mb = os.path.getsize(temp_file.name) / (1024 * 1024)
                if file_size_mb > self.max_file_size:
                    os.unlink(temp_file.name)
                    self.logger.warning(f"Voice file too large: {file_size_mb:.1f} MB")
                    return None
                
                # Transcribe using OpenAI Whisper
                with open(temp_file.name, 'rb') as audio_file:
                    transcript = openai.Audio.transcribe(
                        model=self.model,
                        file=audio_file,
                        response_format="text"
                    )
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
                return transcript.strip() if transcript else None
        
        except Exception as e:
            self.logger.error(f"Error transcribing voice: {e}")
            return None
    
    async def _process_transcribed_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Process transcribed text and execute appropriate actions."""
        text_lower = text.lower()
        
        # Check for daily operations commands
        if any(keyword in text_lower for keyword in ['health', 'log health', 'health metrics']):
            await self._handle_health_command(update, context, text)
        elif any(keyword in text_lower for keyword in ['learning', 'log learning', 'study']):
            await self._handle_learning_command(update, context, text)
        elif any(keyword in text_lower for keyword in ['task', 'add task', 'todo']):
            await self._handle_task_command(update, context, text)
        elif any(keyword in text_lower for keyword in ['note', 'quick note', 'idea']):
            await self._handle_note_command(update, context, text)
        elif any(keyword in text_lower for keyword in ['morning routine', 'routine']):
            await self._handle_morning_routine_command(update, context, text)
        elif any(keyword in text_lower for keyword in ['daily summary', 'summary']):
            await self._handle_daily_summary_command(update, context, text)
        else:
            # General AI response
            await self._handle_general_command(update, context, text)
    
    async def _handle_health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle health-related voice commands."""
        # Extract health metrics from text
        metrics = []
        if 'steps' in text.lower():
            # Try to extract number
            import re
            steps_match = re.search(r'(\d+)\s*steps?', text.lower())
            if steps_match:
                metrics.append(f"steps {steps_match.group(1)}")
        
        if 'sleep' in text.lower():
            sleep_match = re.search(r'(\d+(?:\.\d+)?)\s*hours?\s*sleep', text.lower())
            if sleep_match:
                metrics.append(f"sleep {sleep_match.group(1)}")
        
        if 'water' in text.lower():
            water_match = re.search(r'(\d+)\s*glasses?\s*water', text.lower())
            if water_match:
                metrics.append(f"water {water_match.group(1)}")
        
        if 'mood' in text.lower():
            mood_match = re.search(r'mood\s*(\d+)', text.lower())
            if mood_match:
                metrics.append(f"mood {mood_match.group(1)}")
        
        if metrics:
            # Execute health logging
            from bot.handlers import automation_handlers
            for metric in metrics:
                result = await automation_handlers.execute_script('log_health', {'metric': metric})
                if result and result.get('success'):
                    await update.message.reply_text(
                        f"✅ **Health Metric Logged**\n\n{metric.title()}",
                        parse_mode='Markdown'
                    )
        else:
            # Show health logger help
            result = await automation_handlers.execute_script('log_health', {})
            if result and result.get('success'):
                await update.message.reply_text(
                    f"💪 **Health Logger**\n\n{result.get('output', '')}",
                    parse_mode='Markdown'
                )
    
    async def _handle_learning_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle learning-related voice commands."""
        # Extract learning activity from text
        activity_type = "reading"  # default
        duration = "30"  # default 30 minutes
        
        if 'course' in text.lower():
            activity_type = "course"
        elif 'practice' in text.lower():
            activity_type = "practice"
        elif 'project' in text.lower():
            activity_type = "project"
        elif 'research' in text.lower():
            activity_type = "research"
        
        # Try to extract duration
        import re
        duration_match = re.search(r'(\d+)\s*(?:minutes?|mins?|hours?|hrs?)', text.lower())
        if duration_match:
            duration = duration_match.group(1)
        
        # Execute learning logging
        from bot.handlers import automation_handlers
        result = await automation_handlers.execute_script('log_learning', {
            'type': activity_type,
            'duration': duration,
            'description': text
        })
        
        if result and result.get('success'):
            await update.message.reply_text(
                f"📚 **Learning Activity Logged**\n\n"
                f"Type: {activity_type.title()}\n"
                f"Duration: {duration} minutes\n"
                f"Description: {text}",
                parse_mode='Markdown'
            )
        else:
            # Show learning tracker help
            result = await automation_handlers.execute_script('log_learning', {})
            if result and result.get('success'):
                await update.message.reply_text(
                    f"📚 **Learning Tracker**\n\n{result.get('output', '')}",
                    parse_mode='Markdown'
                )
    
    async def _handle_task_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle task-related voice commands."""
        # Extract task details
        task_title = text
        priority = "medium"
        
        if 'urgent' in text.lower() or 'important' in text.lower():
            priority = "high"
        elif 'low' in text.lower():
            priority = "low"
        
        # Execute task creation
        from bot.handlers import automation_handlers
        result = await automation_handlers.execute_script('add_task', {
            'title': task_title,
            'priority': priority
        })
        
        if result and result.get('success'):
            await update.message.reply_text(
                f"✅ **Task Added**\n\n"
                f"Title: {task_title}\n"
                f"Priority: {priority.title()}",
                parse_mode='Markdown'
            )
        else:
            # Show task manager help
            result = await automation_handlers.execute_script('add_task', {})
            if result and result.get('success'):
                await update.message.reply_text(
                    f"📋 **Task Manager**\n\n{result.get('output', '')}",
                    parse_mode='Markdown'
                )
    
    async def _handle_note_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle note-related voice commands."""
        # Extract note details
        content = text
        category = "general"
        
        if 'idea' in text.lower():
            category = "idea"
        elif 'reminder' in text.lower():
            category = "reminder"
        elif 'task' in text.lower():
            category = "task"
        
        # Execute note capture
        from bot.handlers import automation_handlers
        result = await automation_handlers.execute_script('quick_note', {
            'content': content,
            'category': category
        })
        
        if result and result.get('success'):
            await update.message.reply_text(
                f"📝 **Note Captured**\n\n"
                f"Content: {content}\n"
                f"Category: {category.title()}",
                parse_mode='Markdown'
            )
        else:
            # Show quick note help
            result = await automation_handlers.execute_script('quick_note', {})
            if result and result.get('success'):
                await update.message.reply_text(
                    f"📝 **Quick Note**\n\n{result.get('output', '')}",
                    parse_mode='Markdown'
                )
    
    async def _handle_morning_routine_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle morning routine voice commands."""
        from bot.handlers import automation_handlers
        result = await automation_handlers.execute_script('morning_routine', {})
        
        if result and result.get('success'):
            await update.message.reply_text(
                f"🌅 **Morning Routine**\n\n{result.get('output', '')}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ **Error generating morning routine**\n\nPlease try again later.",
                parse_mode='Markdown'
            )
    
    async def _handle_daily_summary_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle daily summary voice commands."""
        from bot.handlers import automation_handlers
        result = await automation_handlers.execute_script('daily_summary', {})
        
        if result and result.get('success'):
            await update.message.reply_text(
                f"📊 **Daily Summary**\n\n{result.get('output', '')}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ **Error generating daily summary**\n\nPlease try again later.",
                parse_mode='Markdown'
            )
    
    async def _handle_general_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle general voice commands with AI response."""
        # Create interactive response with quick actions
        keyboard = [
            [InlineKeyboardButton("💪 Log Health", callback_data="action_log_health")],
            [InlineKeyboardButton("📚 Log Learning", callback_data="action_log_learning")],
            [InlineKeyboardButton("✅ Add Task", callback_data="action_add_task")],
            [InlineKeyboardButton("⚡ Quick Note", callback_data="action_quick_note")],
            [InlineKeyboardButton("🌅 Morning Routine", callback_data="action_morning_routine")],
            [InlineKeyboardButton("📊 Daily Summary", callback_data="action_daily_summary")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🎤 **Voice Message Received**\n\n"
            f"*\"{text}\"*\n\n"
            f"🤖 **AI Response:**\n"
            f"I understand you said: \"{text}\"\n\n"
            f"Here are some quick actions you can take:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

# Global voice handler instance
voice_handler = None

def initialize_voice_handler(config: Dict[str, Any]):
    """Initialize the voice handler with configuration."""
    global voice_handler
    voice_handler = VoiceTranscriptionHandler(config)

async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages."""
    if voice_handler:
        await voice_handler.handle_voice_message(update, context)
    else:
        await update.message.reply_text(
            "❌ **Voice handler not initialized**\n\n"
            "Please restart the bot to enable voice transcription.",
            parse_mode='Markdown'
        )
