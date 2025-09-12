#!/usr/bin/env python3
"""
Scheduler for Personal System Telegram Bot
Handles automated tasks like morning routine reminders.
"""

import asyncio
import logging
import tempfile
import os
from datetime import datetime, time
from typing import Dict, Any
import pytz
import requests

from bot.bot import PersonalSystemBot
from utils.logger import get_logger
from services.task_integration import get_top_3_tasks, format_tasks_for_morning_routine


class PersonalSystemScheduler:
    """Scheduler for automated bot tasks."""
    
    def __init__(self, bot: PersonalSystemBot, config: Dict[str, Any]):
        self.bot = bot
        self.config = config
        self.logger = get_logger(__name__)
        self.running = False
        
        # Get timezone from config or default to UTC
        timezone_str = config.get('timezone', 'UTC')
        self.timezone = pytz.timezone(timezone_str)
        
        # Morning routine time (6:00 AM)
        self.morning_routine_time = time(6, 0)
        
        # Get allowed users for notifications
        self.allowed_users = config['telegram'].get('allowed_users', [])
        
        # Initialize TTS if enabled
        self.tts_enabled = False
        self.elevenlabs_config = config.get('elevenlabs', {})
        if (self.elevenlabs_config.get('api_key') and 
            self.elevenlabs_config.get('enable_text_to_speech', False)):
            self.tts_enabled = True
            self.elevenlabs_api_key = self.elevenlabs_config['api_key']
            self.voice_id = self.elevenlabs_config.get('voice_id', '21m00Tcm4TlvDq8ikWAM')
            self.logger.info("ElevenLabs TTS enabled for voice messages")
        else:
            self.logger.warning("ElevenLabs TTS not configured - voice messages will be text-only")
    
    async def start(self):
        """Start the scheduler."""
        self.running = True
        self.logger.info("Scheduler started")
        
        try:
            while self.running:
                await self._check_scheduled_tasks()
                await asyncio.sleep(60)  # Check every minute
        except Exception as e:
            self.logger.error(f"Error in scheduler: {e}")
        finally:
            self.running = False
    
    async def stop(self):
        """Stop the scheduler."""
        self.running = False
        self.logger.info("Scheduler stopped")
    
    async def _check_scheduled_tasks(self):
        """Check and execute scheduled tasks."""
        current_time = datetime.now(self.timezone)
        current_time_only = current_time.time()
        
        # Check if it's time for morning routine (6:00 AM)
        if (current_time_only.hour == self.morning_routine_time.hour and 
            current_time_only.minute == self.morning_routine_time.minute):
            await self._send_morning_routine()
    
    async def _send_morning_routine(self):
        """Send morning routine to all allowed users."""
        self.logger.info("Sending morning routine to users")
        
        for user_id in self.allowed_users:
            try:
                # Send morning routine text message
                routine_text = self._get_morning_routine_text()
                
                await self.bot.application.bot.send_message(
                    chat_id=user_id,
                    text=routine_text,
                    parse_mode='Markdown'
                )
                
                # Send voice message if TTS is enabled
                if self.tts_enabled:
                    try:
                        voice_guide = self._get_voice_guide_text()
                        audio_data = self._generate_speech(voice_guide)
                        
                        if audio_data:
                            # Send as voice message
                            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                                temp_file.write(audio_data)
                                temp_file.flush()
                                
                                await self.bot.application.bot.send_voice(
                                    chat_id=user_id,
                                    voice=open(temp_file.name, 'rb'),
                                    caption="🎤 Your morning routine voice guide"
                                )
                                
                                # Clean up temp file
                                os.unlink(temp_file.name)
                                
                            self.logger.info(f"Voice message sent to user {user_id}")
                        else:
                            # Fallback to text if TTS fails
                            await self.bot.application.bot.send_message(
                                chat_id=user_id,
                                text=f"🎤 **Voice Guide Version:**\n\n{voice_guide}\n\n"
                                     "💡 **Tip:** Use your phone's text-to-speech feature to read this aloud!",
                                parse_mode='Markdown'
                            )
                            self.logger.warning(f"TTS failed for user {user_id}, sent text fallback")
                            
                    except Exception as tts_error:
                        self.logger.error(f"TTS error for user {user_id}: {tts_error}")
                        # Fallback to text
                        voice_guide = self._get_voice_guide_text()
                        await self.bot.application.bot.send_message(
                            chat_id=user_id,
                            text=f"🎤 **Voice Guide Version:**\n\n{voice_guide}\n\n"
                                 "💡 **Tip:** Use your phone's text-to-speech feature to read this aloud!",
                            parse_mode='Markdown'
                        )
                else:
                    # Send voice guide as text if TTS not enabled
                    voice_guide = self._get_voice_guide_text()
                    await self.bot.application.bot.send_message(
                        chat_id=user_id,
                        text=f"🎤 **Voice Guide Version:**\n\n{voice_guide}\n\n"
                             "💡 **Tip:** Use your phone's text-to-speech feature to read this aloud!",
                        parse_mode='Markdown'
                    )
                
                self.logger.info(f"Morning routine sent to user {user_id}")
                
            except Exception as e:
                self.logger.error(f"Error sending morning routine to user {user_id}: {e}")
    
    def _get_morning_routine_text(self):
        """Get the formatted morning routine text."""
        # Get top 3 tasks for today
        tasks_result = get_top_3_tasks()
        tasks_section = ""
        
        if tasks_result['success'] and tasks_result['tasks']:
            tasks_section = format_tasks_for_morning_routine(tasks_result['tasks'])
        else:
            tasks_section = "📝 **Your Top 3 Priority Tasks Today:**\n\nNo specific tasks found. Take this opportunity to plan your day or work on long-term goals!"
        
        return f"""
🌅 **Good morning! Here's your routine for today:**

{tasks_section}

---

**⏰ 6:00 AM - Wake Up**
• No snooze - feet on floor immediately
• Drink glass of water (on nightstand)
• 5 deep breaths with gratitude

**🌡️ 6:03 AM - Digestive Warm-Up**
• Prepare warm water (40-45°C) - 250ml
• Drink slowly, mindfully (5-7 minutes)
• Feel the gentle warmth activating digestion
• Express gratitude for body's natural processes

**🧘 6:10 AM - Mindfulness**
• 10-minute meditation (Headspace app)
• Set daily intention
• Visualize successful day

**💪 6:25 AM - Movement**
• 5-minute stretching routine
• 20 pushups
• 30 jumping jacks
• Cold shower (2 minutes)

**☕ 6:45 AM - Fuel**
• Prepare coffee/tea mindfully
• Healthy breakfast (protein + complex carbs)
• Vitamins and supplements

**📝 7:05 AM - Planning**
• Review calendar and priorities
• Focus on your top 3 tasks above
• Time block the day
• Check weather and news (5 min max)

**📚 7:25 AM - Learning**
• Read for 20 minutes
• Take 3 key notes
• Add to knowledge base
• Sync company presentations (5 min)

**🚀 7:50 AM - Start Work**
• Clean workspace
• Open required apps/tools
• Begin with your #1 priority task

**💡 Remember:**
• Prep clothes night before
• Phone on airplane mode until 7:30 AM
• No email until after your first priority task
• Track energy levels for pattern recognition

Ready to start your day? 🌟
        """
    
    def _get_voice_guide_text(self):
        """Get the voice guide version of the morning routine."""
        # Get top 3 tasks for today
        tasks_result = get_top_3_tasks()
        tasks_section = ""
        
        if tasks_result['success'] and tasks_result['tasks']:
            tasks_section = "Your top 3 priority tasks for today are:\n"
            for i, task in enumerate(tasks_result['tasks'], 1):
                priority_emoji = {
                    'high': 'high priority', 'urgent': 'urgent', 'critical': 'critical',
                    'medium': 'medium priority', 'low': 'low priority'
                }.get(task.get('priority', 'medium').lower(), 'medium priority')
                
                title = task.get('title', 'Untitled Task')
                tasks_section += f"Task {i}: {title} - {priority_emoji}.\n"
        else:
            tasks_section = "No specific tasks found for today. Take this opportunity to plan your day or work on long-term goals.\n"
        
        return f"""
Your morning routine starts now.

{tasks_section}

6:00 AM - Wake Up. No snooze, feet on floor immediately. Drink water, take 5 deep breaths with gratitude.

6:03 AM - Digestive Warm-Up. Prepare warm water 40-45 degrees Celsius, 250ml. Drink slowly and mindfully for 5-7 minutes. Feel the gentle warmth activating your digestion.

6:10 AM - Mindfulness. 10-minute meditation with Headspace app. Set your daily intention. Visualize your successful day.

6:25 AM - Movement. 5-minute stretching routine, 20 pushups, 30 jumping jacks, then a 2-minute cold shower.

6:45 AM - Fuel. Prepare coffee or tea mindfully. Healthy breakfast with protein and complex carbs. Take your vitamins and supplements.

7:05 AM - Planning. Review your calendar and priorities. Focus on your top 3 tasks mentioned above. Time block your day. Check weather and news for 5 minutes maximum.

7:25 AM - Learning. Read for 20 minutes. Take 3 key notes. Add to your knowledge base. Sync company presentations for 5 minutes.

7:50 AM - Start Work. Clean your workspace. Open required apps and tools. Begin with your first priority task.

Remember: Prep clothes the night before. Keep phone on airplane mode until 7:30 AM. No email until after your first priority task. Track your energy levels.

You've got this! Start your day with intention and purpose.
        """
    
    def _generate_speech(self, text: str) -> bytes:
        """Generate speech from text using ElevenLabs TTS."""
        if not self.tts_enabled:
            return None
            
        try:
            # ElevenLabs voice settings for optimal quality
            voice_settings = {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
            
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": voice_settings
            }
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            
            self.logger.info(f"Generating speech for {len(text)} characters")
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=60  # ElevenLabs can take time for longer texts
            )
            
            if response.status_code == 200:
                audio_data = response.content
                self.logger.info(f"Generated audio: {len(audio_data)} bytes")
                return audio_data
            else:
                self.logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error("ElevenLabs request timed out")
            return None
        except Exception as e:
            self.logger.error(f"Error generating speech: {e}")
            return None
    
    async def send_morning_routine_now(self, user_id: int):
        """Send morning routine immediately to a specific user."""
        try:
            from telegram import Update
            from telegram.ext import ContextTypes
            from bot.handlers.daily_handlers import morning_routine_command
            
            update = Update(0)
            context = ContextTypes.DEFAULT_TYPE()
            context.user_data = {'user_id': user_id, 'username': f'user_{user_id}'}
            
            await morning_routine_command(update, context)
            self.logger.info(f"Morning routine sent immediately to user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error sending immediate morning routine to user {user_id}: {e}")


async def run_scheduler(config: Dict[str, Any]):
    """Run the scheduler as a standalone process."""
    from bot.bot import PersonalSystemBot
    
    # Create bot instance
    bot = PersonalSystemBot(config)
    
    # Create and start scheduler
    scheduler = PersonalSystemScheduler(bot, config)
    
    try:
        await scheduler.start()
    except KeyboardInterrupt:
        await scheduler.stop()


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Add the project root to Python path
    project_root = Path(__file__).parent
    sys.path.append(str(project_root))
    
    from config.config_manager import ConfigManager
    from utils.logger import setup_logging
    
    # Setup logging
    setup_logging()
    
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    # Run scheduler
    asyncio.run(run_scheduler(config))
