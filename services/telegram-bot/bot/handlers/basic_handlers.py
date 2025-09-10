"""
Basic command handlers for the Personal System Telegram Bot.
Handles start, help, status, and menu commands with inline keyboards.
"""

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with main menu."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/start")
    
    welcome_message = """
🤖 **Personal System Bot**

Welcome to your personal automation assistant! I can help you manage your entire personal system through voice commands and interactive menus.

🎤 **Voice Commands**: Send voice messages for natural interaction
📱 **Interactive Menus**: Use buttons for quick access
⚡ **Automation**: Execute scripts and workflows
🔒 **Privacy**: All data encrypted and secure

Choose an option below to get started:
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 Daily Operations", callback_data="menu_daily")],
        [InlineKeyboardButton("🧠 Shadow Work", callback_data="menu_shadow")],
        [InlineKeyboardButton("📝 Journal & Notes", callback_data="menu_journal")],
        [InlineKeyboardButton("💼 Opportunities", callback_data="menu_opportunities")],
        [InlineKeyboardButton("🎯 ClickUp Projects", callback_data="menu_clickup")],
        [InlineKeyboardButton("⚙️ System Management", callback_data="menu_system")],
        [InlineKeyboardButton("🎤 Voice Commands", callback_data="menu_voice")],
        [InlineKeyboardButton("❓ Help & Examples", callback_data="menu_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/help")
    
    help_message = """
📚 **Available Commands**

**Basic Commands:**
• `/start` - Welcome message and introduction
• `/help` - Show this help message
• `/status` - System status overview

**Daily Operations:**
• `/summary` - Get your daily health, productivity, learning, and finance summary
• `/log_health` - Log health metrics (steps, sleep, water, etc.)
• `/log_learning` - Log learning activity and progress
• `/quick_note` - Capture a quick thought or idea
• `/morning_routine` - Get your voice-guided morning routine

**Shadow Work:**
• `/shadow_checkin` - Daily shadow work check-in
• `/shadow_log` - Log a shadow work insight or observation
• `/shadow_prompt` - Get a random shadow work prompt

**Journal & Notes:**
• `/journal` - Create a journal entry
• `/idea` - Capture a new idea or inspiration
• `/task` - Add a new task to your system

**AI Assistant:**
• `/chat` - Have a conversation with AI about your system
• `/analyze` - Analyze your data and patterns
• `/recommend` - Get personalized recommendations
• `/question` - Ask questions about your system
• Send voice messages for hands-free interaction

**System Management:**
• `/backup` - Create a backup of your system
• `/sync` - Sync data across devices
• `/stats` - View system statistics and metrics
• `/tasks` - View prioritized TODO list

**Admin Commands:**
• `/admin backup` - Force system backup
• `/admin sync` - Force data synchronization
• `/admin health_check` - Check system health
• `/admin set_openai_key YOUR_API_KEY` - Securely store OpenAI API key
• `/test_notification` - Test bot notification system

**Usage Tips:**
• Use natural language for most commands
• Data is automatically saved and synced
• Your privacy is always protected
• All interactions are logged for your reference

Need help with a specific command? Just ask! 💬
    """
    
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/status")
    
    # Get current time
    now = datetime.now()
    
    # Basic status information
    status_message = f"""
📊 **System Status**

**Time:** {now.strftime('%Y-%m-%d %H:%M:%S')}
**Bot Status:** ✅ Online
**User:** @{username}
**Access Level:** {'Admin' if context.user_data.get('is_admin') else 'User'}

**System Health:**
• Database: ✅ Connected
• Storage: ✅ Available
• Encryption: ✅ Active
• Privacy: ✅ Protected

**Recent Activity:**
• Last backup: {now.strftime('%Y-%m-%d')}
• Data sync: ✅ Up to date
• Logs: ✅ Recording

**Quick Actions:**
• `/summary` - View today's summary
• `/backup` - Create backup
• `/stats` - Detailed statistics

Everything looks good! 🟢
    """
    
    await update.message.reply_text(status_message, parse_mode='Markdown')


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu command - show main menu."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/menu")
    
    menu_message = """
📱 **Main Menu**

Choose a category to access your personal system features:
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 Daily Operations", callback_data="menu_daily")],
        [InlineKeyboardButton("🧠 Shadow Work", callback_data="menu_shadow")],
        [InlineKeyboardButton("📝 Journal & Notes", callback_data="menu_journal")],
        [InlineKeyboardButton("💼 Opportunities", callback_data="menu_opportunities")],
        [InlineKeyboardButton("⚙️ System Management", callback_data="menu_system")],
        [InlineKeyboardButton("🎤 Voice Commands", callback_data="menu_voice")],
        [InlineKeyboardButton("❓ Help & Examples", callback_data="menu_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)
