"""
Voice message handlers for the Personal System Telegram Bot.
Handles voice message transcription, action parsing, and confirmation.
"""

import logging
import os
import tempfile
import json
from typing import Dict, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command

# Import OpenAI for voice transcription
try:
    import openai
except ImportError:
    openai = None


class VoiceActionParser:
    """Parse voice commands into actionable items."""
    
    def __init__(self):
        self.action_patterns = {
            # Opportunity management
            "create_opportunity": [
                "create opportunity", "new opportunity", "add opportunity",
                "opportunity for", "job opportunity", "career opportunity"
            ],
            "create_business_opportunity": [
                "create business opportunity", "new business opportunity", 
                "business opportunity", "startup opportunity", "investment opportunity"
            ],
            "list_opportunities": [
                "show opportunities", "list opportunities", "my opportunities",
                "pending opportunities", "opportunities list"
            ],
            "evaluate_opportunity": [
                "evaluate opportunity", "score opportunity", "rate opportunity",
                "assess opportunity", "review opportunity"
            ],
            
            # Shadow work
            "shadow_checkin": [
                "shadow work checkin", "shadow checkin", "daily shadow work",
                "shadow work check-in", "shadow check-in"
            ],
            "shadow_log": [
                "log shadow work", "shadow work insight", "shadow insight",
                "shadow work observation", "shadow observation"
            ],
            "shadow_prompt": [
                "shadow work prompt", "shadow prompt", "shadow work question",
                "shadow work exercise"
            ],
            "shadow_report": [
                "shadow work report", "shadow progress", "shadow work progress",
                "shadow work summary"
            ],
            
            # Daily operations
            "daily_summary": [
                "daily summary", "today's summary", "generate summary",
                "show summary", "get summary"
            ],
            "morning_routine": [
                "morning routine", "daily routine", "morning guidance",
                "start my day", "morning plan"
            ],
            "log_health": [
                "log health", "health metrics", "health data", "health tracking",
                "record health", "health log"
            ],
            "log_learning": [
                "log learning", "learning activity", "learning progress",
                "record learning", "learning log"
            ],
            
            # Journal and tasks
            "journal_entry": [
                "journal entry", "new journal", "write journal", "journal",
                "daily journal", "journal note"
            ],
            "capture_idea": [
                "capture idea", "new idea", "save idea", "idea",
                "record idea", "note idea"
            ],
            "add_task": [
                "add task", "new task", "create task", "task",
                "add todo", "new todo"
            ],
            "view_tasks": [
                "show tasks", "list tasks", "my tasks", "tasks",
                "todo list", "pending tasks"
            ],
            
            # System management
            "create_backup": [
                "create backup", "backup system", "backup", "system backup",
                "backup data", "save backup"
            ],
            "sync_data": [
                "sync data", "synchronize", "sync", "data sync",
                "sync system", "update sync"
            ],
            "system_stats": [
                "system stats", "system statistics", "stats", "system status",
                "system health", "system info"
            ],
            "gdrive_sync": [
                "google drive sync", "gdrive sync", "drive sync",
                "sync google drive", "cloud sync"
            ],
            
            # Prosperity course
            "prosperity_course": [
                "prosperity course", "course status", "prosperity",
                "course progress", "prosperity progress"
            ]
        }
    
    def parse_voice_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse voice command text into actionable item."""
        text_lower = text.lower().strip()
        
        # Find matching action
        for action, patterns in self.action_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    # Extract parameters based on action type
                    params = self._extract_parameters(text, action, pattern)
                    return {
                        "action": action,
                        "original_text": text,
                        "parameters": params,
                        "confidence": self._calculate_confidence(text_lower, pattern)
                    }
        
        return None
    
    def _extract_parameters(self, text: str, action: str, pattern: str) -> Dict[str, Any]:
        """Extract parameters from voice command text."""
        params = {}
        
        if action in ["create_opportunity", "create_business_opportunity"]:
            # Extract opportunity description
            if "for" in text.lower():
                parts = text.lower().split("for", 1)
                if len(parts) > 1:
                    params["description"] = parts[1].strip()
            elif ":" in text:
                parts = text.split(":", 1)
                if len(parts) > 1:
                    params["description"] = parts[1].strip()
            else:
                # Try to extract after the pattern
                pattern_pos = text.lower().find(pattern)
                if pattern_pos != -1:
                    remaining = text[pattern_pos + len(pattern):].strip()
                    if remaining:
                        params["description"] = remaining
        
        elif action == "shadow_log":
            # Extract insight text
            if ":" in text:
                parts = text.split(":", 1)
                if len(parts) > 1:
                    params["insight"] = parts[1].strip()
            elif "insight" in text.lower():
                parts = text.lower().split("insight", 1)
                if len(parts) > 1:
                    params["insight"] = parts[1].strip()
        
        elif action == "add_task":
            # Extract task description
            if ":" in text:
                parts = text.split(":", 1)
                if len(parts) > 1:
                    params["task"] = parts[1].strip()
            elif "task" in text.lower():
                parts = text.lower().split("task", 1)
                if len(parts) > 1:
                    params["task"] = parts[1].strip()
        
        elif action == "capture_idea":
            # Extract idea text
            if ":" in text:
                parts = text.split(":", 1)
                if len(parts) > 1:
                    params["idea"] = parts[1].strip()
            elif "idea" in text.lower():
                parts = text.lower().split("idea", 1)
                if len(parts) > 1:
                    params["idea"] = parts[1].strip()
        
        return params
    
    def _calculate_confidence(self, text: str, pattern: str) -> float:
        """Calculate confidence score for the match."""
        # Simple confidence based on pattern length and exactness
        if pattern in text:
            return 0.9
        elif any(word in text for word in pattern.split()):
            return 0.7
        else:
            return 0.5


class VoiceMessageHandler:
    """Handle voice messages with transcription and action parsing."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(__name__)
        self.parser = VoiceActionParser()
        
        # Initialize OpenAI if available
        if openai and config.get('openai', {}).get('api_key'):
            openai.api_key = config['openai']['api_key']
            self.openai_available = True
        else:
            self.openai_available = False
            self.logger.warning("OpenAI not available - voice transcription disabled")
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming voice messages."""
        user_id = context.user_data.get('user_id')
        username = context.user_data.get('username', 'unknown')
        
        log_command(self.logger, user_id, username, "voice_message")
        
        if not self.openai_available:
            await update.message.reply_text(
                "🎤 Voice transcription is not available. Please configure OpenAI API key in settings.",
                parse_mode='Markdown'
            )
            return
        
        # Download voice file
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        
        try:
            # Transcribe voice message
            transcription = await self._transcribe_voice(voice_file)
            
            if not transcription:
                await update.message.reply_text(
                    "❌ Could not transcribe voice message. Please try again.",
                    parse_mode='Markdown'
                )
                return
            
            # Show transcription
            await update.message.reply_text(
                f"🎤 **Transcribed:** {transcription}",
                parse_mode='Markdown'
            )
            
            # Parse action
            action_item = self.parser.parse_voice_command(transcription)
            
            if action_item:
                await self._handle_parsed_action(update, context, action_item)
            else:
                await update.message.reply_text(
                    "❓ I didn't understand that command. Try saying something like:\n\n"
                    "• 'Create opportunity for software engineer role'\n"
                    "• 'Log shadow work insight: I avoid difficult conversations'\n"
                    "• 'Add task: Review quarterly goals'\n"
                    "• 'Show my opportunities'\n"
                    "• 'Generate daily summary'",
                    parse_mode='Markdown'
                )
        
        except Exception as e:
            self.logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text(
                "❌ Error processing voice message. Please try again.",
                parse_mode='Markdown'
            )
    
    async def _transcribe_voice(self, voice_file) -> Optional[str]:
        """Transcribe voice file using OpenAI Whisper."""
        try:
            # Download to temporary file
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                await voice_file.download_to_drive(temp_file.name)
                
                # Transcribe using OpenAI Whisper
                with open(temp_file.name, 'rb') as audio_file:
                    transcript = openai.Audio.transcribe(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
                return transcript.strip()
        
        except Exception as e:
            self.logger.error(f"Error transcribing voice: {e}")
            return None
    
    async def _handle_parsed_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action_item: Dict[str, Any]):
        """Handle parsed action with confirmation."""
        action = action_item["action"]
        params = action_item["parameters"]
        confidence = action_item["confidence"]
        
        # Create confirmation message
        confirmation_text = self._create_confirmation_text(action, params, confidence)
        
        # Create confirmation keyboard
        keyboard = [
            [
                InlineKeyboardButton("✅ Yes, Execute", callback_data=f"confirm_{action}_{json.dumps(params)}"),
                InlineKeyboardButton("❌ No, Cancel", callback_data="confirm_cancel")
            ],
            [InlineKeyboardButton("✏️ Edit", callback_data=f"edit_{action}_{json.dumps(params)}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            confirmation_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    def _create_confirmation_text(self, action: str, params: Dict[str, Any], confidence: float) -> str:
        """Create confirmation text for parsed action."""
        action_descriptions = {
            "create_opportunity": "Create new opportunity",
            "create_business_opportunity": "Create new business opportunity",
            "list_opportunities": "List all opportunities",
            "evaluate_opportunity": "Evaluate opportunity",
            "shadow_checkin": "Daily shadow work check-in",
            "shadow_log": "Log shadow work insight",
            "shadow_prompt": "Get shadow work prompt",
            "shadow_report": "Generate shadow work report",
            "daily_summary": "Generate daily summary",
            "morning_routine": "Get morning routine",
            "log_health": "Log health metrics",
            "log_learning": "Log learning activity",
            "journal_entry": "Create journal entry",
            "capture_idea": "Capture idea",
            "add_task": "Add new task",
            "view_tasks": "View tasks",
            "create_backup": "Create system backup",
            "sync_data": "Sync data",
            "system_stats": "Show system statistics",
            "gdrive_sync": "Sync with Google Drive",
            "prosperity_course": "Check prosperity course status"
        }
        
        action_desc = action_descriptions.get(action, action)
        confidence_emoji = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.6 else "🔴"
        
        text = f"🤖 **Action Confirmation**\n\n"
        text += f"**Action:** {action_desc}\n"
        text += f"**Confidence:** {confidence_emoji} {confidence:.0%}\n\n"
        
        if params:
            text += "**Parameters:**\n"
            for key, value in params.items():
                text += f"• {key.title()}: {value}\n"
            text += "\n"
        
        text += "Do you want me to execute this action?"
        
        return text


# Global voice handler instance
voice_handler = None

def initialize_voice_handler(config: Dict[str, Any]):
    """Initialize the voice handler with config."""
    global voice_handler
    voice_handler = VoiceMessageHandler(config)


async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages."""
    if voice_handler:
        await voice_handler.handle_voice_message(update, context)
    else:
        await update.message.reply_text(
            "❌ Voice handler not initialized. Please restart the bot.",
            parse_mode='Markdown'
        )
