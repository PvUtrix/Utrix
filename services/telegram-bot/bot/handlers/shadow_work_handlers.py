"""
Shadow work command handlers for the Personal System Telegram Bot.
Handles shadow work check-ins, logging, and prompts.
"""

import logging
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command
from integrations.shadow_work import ShadowWorkIntegration


async def shadow_checkin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shadow_checkin command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/shadow_checkin")
    
    # Get shadow work integration
    shadow_work = ShadowWorkIntegration()
    
    # Get today's check-in prompt
    prompt = shadow_work.get_daily_checkin_prompt()
    
    checkin_message = f"""
🌙 **Daily Shadow Work Check-in**

**Today's Prompt:**
{prompt}

**Instructions:**
1. Take a moment to reflect on this question
2. Notice any resistance, fear, or discomfort
3. Write down one shadow aspect you want to explore today
4. Set intention to notice this pattern throughout the day

**Quick Response:**
Reply to this message with your reflection, or use:
• `/shadow_log` to log a detailed insight
• `/shadow_prompt` for another prompt

Remember: Your shadow is not your enemy. It's a part of you that needs to be seen, heard, and integrated. 💜
    """
    
    await update.message.reply_text(checkin_message, parse_mode='Markdown')


async def shadow_log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shadow_log command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/shadow_log")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/shadow_log', '').strip()
    
    if not args:
        # Ask for the insight
        await update.message.reply_text(
            "🌙 **Shadow Work Logging**\n\n"
            "Please share your shadow work insight or observation.\n\n"
            "Examples:\n"
            "• I noticed I was avoiding that difficult conversation\n"
            "• I felt defensive when someone criticized my work\n"
            "• I'm trying to control outcomes too much again\n\n"
            "Reply with your insight, or use:\n"
            "• `/shadow_log [your insight]` - Log directly\n"
            "• `/shadow_prompt` - Get a prompt to reflect on",
            parse_mode='Markdown'
        )
        return
    
    # Log the shadow work insight
    shadow_work = ShadowWorkIntegration()
    success = shadow_work.log_insight(args, user_id)
    
    if success:
        response = f"""
✅ **Shadow Work Insight Logged**

**Your Insight:**
"{args}"

**What to do next:**
• Notice this pattern throughout the day
• Practice self-compassion
• Consider how this shadow aspect serves you
• Look for opportunities to integrate it

**Integration Question:**
What would it look like to embrace this part of yourself with love and understanding?

Keep exploring! 🌙✨
        """
    else:
        response = "❌ Sorry, there was an error logging your insight. Please try again."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def shadow_prompt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shadow_prompt command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/shadow_prompt")
    
    # Get shadow work integration
    shadow_work = ShadowWorkIntegration()
    
    # Get a random prompt
    prompt = shadow_work.get_random_prompt()
    
    prompt_message = f"""
🌙 **Shadow Work Prompt**

**Reflection Question:**
{prompt}

**How to use this prompt:**
1. Sit with this question for a few moments
2. Notice what comes up - thoughts, feelings, resistance
3. Write down your honest response
4. Don't judge what emerges - just observe

**Quick Actions:**
• Reply with your reflection
• `/shadow_log [your response]` - Log your insight
• `/shadow_prompt` - Get another prompt

**Remember:** Shadow work is about bringing light to the parts of yourself that you've hidden away. Be gentle with yourself. 💜
    """
    
    await update.message.reply_text(prompt_message, parse_mode='Markdown')
