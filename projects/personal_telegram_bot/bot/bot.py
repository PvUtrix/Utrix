"""
Main bot class for the Personal System Telegram Bot.
Handles bot initialization, command routing, and core functionality.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from bot.handlers import (
    basic_handlers,
    daily_handlers,
    shadow_work_handlers,
    journal_handlers,
    system_handlers,
    ai_handlers,
    menu_handlers,
    voice_handlers,
    automation_handlers
)
from bot.middleware.auth_middleware import AuthMiddleware
from integrations.personal_system import PersonalSystemIntegration
from utils.logger import get_logger, log_command


class PersonalSystemBot:
    """Main bot class for personal system integration."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(__name__)
        self.application = None
        self.personal_system = PersonalSystemIntegration(config)
        
        # Bot settings
        self.bot_token = config['telegram']['bot_token']
        self.allowed_users = config['telegram'].get('allowed_users', [])
        self.admin_users = config['telegram'].get('admin_users', [])
        
        # Initialize bot
        self._setup_bot()
        
        # Initialize handlers
        self._initialize_handlers()
    
    def _setup_bot(self):
        """Setup the Telegram bot application."""
        self.application = Application.builder().token(self.bot_token).build()
        
        # Create middleware instance
        self.auth_middleware = AuthMiddleware(self.allowed_users, self.admin_users)
        
        # Register command handlers
        self._register_handlers()
        
        # Add error handler
        self.application.add_error_handler(self._error_handler)
    
    def _initialize_handlers(self):
        """Initialize handler instances with config."""
        # Initialize voice handler
        voice_handlers.initialize_voice_handler(self.config)
        
        # Initialize automation handler
        automation_handlers.initialize_automation_handler(self.config)
    
    def _register_handlers(self):
        """Register all command handlers."""
        
        # Basic commands
        self.application.add_handler(CommandHandler("start", self._with_auth(basic_handlers.start_command)))
        self.application.add_handler(CommandHandler("help", self._with_auth(basic_handlers.help_command)))
        self.application.add_handler(CommandHandler("status", self._with_auth(basic_handlers.status_command)))
        self.application.add_handler(CommandHandler("menu", self._with_auth(basic_handlers.menu_command)))
        
        # Daily operations
        self.application.add_handler(CommandHandler("summary", self._with_auth(daily_handlers.summary_command)))
        self.application.add_handler(CommandHandler("log_health", self._with_auth(daily_handlers.log_health_command)))
        self.application.add_handler(CommandHandler("log_learning", self._with_auth(daily_handlers.log_learning_command)))
        self.application.add_handler(CommandHandler("quick_note", self._with_auth(daily_handlers.quick_note_command)))
        self.application.add_handler(CommandHandler("morning_routine", self._with_auth(daily_handlers.morning_routine_command)))
        
        # Shadow work
        self.application.add_handler(CommandHandler("shadow_checkin", self._with_auth(shadow_work_handlers.shadow_checkin_command)))
        self.application.add_handler(CommandHandler("shadow_log", self._with_auth(shadow_work_handlers.shadow_log_command)))
        self.application.add_handler(CommandHandler("shadow_prompt", self._with_auth(shadow_work_handlers.shadow_prompt_command)))
        
        # Journal and notes
        self.application.add_handler(CommandHandler("journal", self._with_auth(journal_handlers.journal_command)))
        self.application.add_handler(CommandHandler("idea", self._with_auth(journal_handlers.idea_command)))
        self.application.add_handler(CommandHandler("task", self._with_auth(journal_handlers.task_command)))
        
        # System management
        self.application.add_handler(CommandHandler("backup", self._with_auth(system_handlers.backup_command)))
        self.application.add_handler(CommandHandler("sync", self._with_auth(system_handlers.sync_command)))
        self.application.add_handler(CommandHandler("stats", self._with_auth(system_handlers.stats_command)))
        self.application.add_handler(CommandHandler("tasks", self._with_auth(system_handlers.tasks_command)))
        
        # AI-powered commands
        self.application.add_handler(CommandHandler("chat", self._with_auth(ai_handlers.chat_command)))
        self.application.add_handler(CommandHandler("analyze", self._with_auth(ai_handlers.analyze_command)))
        self.application.add_handler(CommandHandler("recommend", self._with_auth(ai_handlers.recommend_command)))
        self.application.add_handler(CommandHandler("question", self._with_auth(ai_handlers.question_command)))
        
        # Voice message handler
        self.application.add_handler(MessageHandler(filters.VOICE, self._with_auth(voice_handlers.voice_message_handler)))
        
        # General text message handler (for conversational AI)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._with_auth(ai_handlers.text_message_handler)))
        
        # Callback query handler for inline keyboards
        from telegram.ext import CallbackQueryHandler
        self.application.add_handler(CallbackQueryHandler(self._with_auth(menu_handlers.handle_callback_query)))
        
        # Admin commands
        if self.admin_users:
            self.application.add_handler(CommandHandler("admin", self._with_auth(system_handlers.admin_command)))
            self.application.add_handler(CommandHandler("test_notification", self._with_auth(system_handlers.test_notification_command)))
    
    async def _error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors in the bot."""
        self.logger.error(f"Exception while handling an update: {context.error}")
        
        # Send error message to user if possible
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Sorry, something went wrong. Please try again later."
            )
    
    async def start(self):
        """Start the bot."""
        self.logger.info("Starting bot...")
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        self.logger.info("Bot started successfully!")
        
        # Send startup notification to admin users
        await self._send_startup_notification()
        
        # Keep the bot running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            self.logger.info("Stopping bot...")
            await self._send_shutdown_notification()
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the bot."""
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
        
        self.logger.info("Bot stopped.")
    
    async def _send_startup_notification(self):
        """Send startup notification to admin users."""
        if not self.admin_users:
            return
        
        startup_message = """
🤖 **Personal System Bot Started**

✅ Bot is now online and ready to use!

**Available Features:**
🎤 Voice Commands - Send voice messages for natural interaction
📱 Interactive Menus - Use /start for button navigation
⚡ Automation Scripts - Access all your automation tools
🔒 Privacy Protected - All data encrypted and secure

**Quick Start:**
• Send /start for the main menu
• Send voice messages for commands
• Use buttons for quick access

**Voice Examples:**
• "Create opportunity for software engineer role"
• "Log shadow work insight: [your insight]"
• "Generate daily summary"
• "Show my opportunities"

The bot is ready to help you manage your personal system! 🚀
        """
        
        for admin_id in self.admin_users:
            try:
                await self.application.bot.send_message(
                    chat_id=admin_id,
                    text=startup_message,
                    parse_mode='Markdown'
                )
                self.logger.info(f"Startup notification sent to admin {admin_id}")
            except Exception as e:
                self.logger.error(f"Failed to send startup notification to {admin_id}: {e}")
    
    async def _send_shutdown_notification(self):
        """Send shutdown notification to admin users."""
        if not self.admin_users:
            return
        
        shutdown_message = """
🤖 **Personal System Bot Shutting Down**

⚠️ Bot is going offline for maintenance or restart.

**Status:** Shutting down gracefully
**Time:** {timestamp}

The bot will be back online shortly! 🔄
        """.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for admin_id in self.admin_users:
            try:
                await self.application.bot.send_message(
                    chat_id=admin_id,
                    text=shutdown_message,
                    parse_mode='Markdown'
                )
                self.logger.info(f"Shutdown notification sent to admin {admin_id}")
            except Exception as e:
                self.logger.error(f"Failed to send shutdown notification to {admin_id}: {e}")
    
    def is_user_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to use the bot."""
        return not self.allowed_users or user_id in self.allowed_users
    
    def is_user_admin(self, user_id: int) -> bool:
        """Check if user is an admin."""
        return user_id in self.admin_users
    
    def _with_auth(self, handler_func):
        """Wrapper to add authentication to handlers."""
        async def wrapped_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Run authentication middleware
            await self.auth_middleware(update, context)
            # Call the original handler
            return await handler_func(update, context)
        return wrapped_handler
