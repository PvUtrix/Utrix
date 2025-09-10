#!/usr/bin/env python3
"""
Scheduler for Personal System Telegram Bot
Handles automated tasks like morning routine reminders.
"""

import asyncio
import logging
from datetime import datetime, time
from typing import Dict, Any
import pytz

from bot.bot import PersonalSystemBot
from utils.logger import get_logger


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
                # Send morning routine directly using bot's application
                routine_text = self._get_morning_routine_text()
                
                await self.bot.application.bot.send_message(
                    chat_id=user_id,
                    text=routine_text,
                    parse_mode='Markdown'
                )
                
                # Send voice guide version
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
        return """
🌅 **Good morning! Here's your routine for today:**

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
• Choose 3 MITs (Most Important Tasks)
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
• Begin with MIT #1

**💡 Remember:**
• Prep clothes night before
• Phone on airplane mode until 7:30 AM
• No email until after MIT #1
• Track energy levels for pattern recognition

Ready to start your day? 🌟
        """
    
    def _get_voice_guide_text(self):
        """Get the voice guide version of the morning routine."""
        return """
Your morning routine starts now.

6:00 AM - Wake Up. No snooze, feet on floor immediately. Drink water, take 5 deep breaths with gratitude.

6:03 AM - Digestive Warm-Up. Prepare warm water 40-45 degrees Celsius, 250ml. Drink slowly and mindfully for 5-7 minutes. Feel the gentle warmth activating your digestion.

6:10 AM - Mindfulness. 10-minute meditation with Headspace app. Set your daily intention. Visualize your successful day.

6:25 AM - Movement. 5-minute stretching routine, 20 pushups, 30 jumping jacks, then a 2-minute cold shower.

6:45 AM - Fuel. Prepare coffee or tea mindfully. Healthy breakfast with protein and complex carbs. Take your vitamins and supplements.

7:05 AM - Planning. Review your calendar and priorities. Choose 3 Most Important Tasks. Time block your day. Check weather and news for 5 minutes maximum.

7:25 AM - Learning. Read for 20 minutes. Take 3 key notes. Add to your knowledge base. Sync company presentations for 5 minutes.

7:50 AM - Start Work. Clean your workspace. Open required apps and tools. Begin with your first Most Important Task.

Remember: Prep clothes the night before. Keep phone on airplane mode until 7:30 AM. No email until after your first MIT. Track your energy levels.

You've got this! Start your day with intention and purpose.
        """
    
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
