"""
Journal and note handlers for the Personal System Telegram Bot.
Handles journal entries, ideas, and task management.
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command
from integrations.journal import JournalIntegration


async def journal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /journal command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/journal")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/journal', '').strip()
    
    if not args:
        # Ask for journal entry
        await update.message.reply_text(
            "📝 **Journal Entry**\n\n"
            "Create a journal entry to reflect on your day, thoughts, or experiences.\n\n"
            "**Usage:**\n"
            "• `/journal [your entry]` - Create entry directly\n"
            "• Reply with your journal entry\n\n"
            "**Journaling Prompts:**\n"
            "• What am I grateful for today?\n"
            "• What challenged me today?\n"
            "• What did I learn about myself?\n"
            "• How am I feeling right now?\n"
            "• What would I like to remember about today?",
            parse_mode='Markdown'
        )
        return
    
    # Save journal entry
    journal = JournalIntegration({})
    success = journal.create_entry(args, user_id)
    
    if success:
        response = f"""
✅ **Journal Entry Created**

**Your Entry:**
"{args}"

**What happens next:**
• Entry saved to your journal
• Will be included in your daily summary
• Can be reviewed during weekly/monthly reviews
• Helps track patterns and growth over time

Keep writing! 📖✨
        """
    else:
        response = "❌ Sorry, there was an error creating your journal entry. Please try again."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def idea_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /idea command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/idea")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/idea', '').strip()
    
    if not args:
        # Ask for the idea
        await update.message.reply_text(
            "💡 **Capture Idea**\n\n"
            "Capture a new idea, inspiration, or creative thought.\n\n"
            "**Usage:**\n"
            "• `/idea [your idea]` - Capture idea directly\n"
            "• Reply with your idea\n\n"
            "**Idea Categories:**\n"
            "• Business ideas\n"
            "• Creative projects\n"
            "• Personal improvements\n"
            "• Solutions to problems\n"
            "• Inspirations from others\n\n"
            "**Examples:**\n"
            "• `/idea Create an app for habit tracking`\n"
            "• `/idea Write a book about personal systems`\n"
            "• `/idea Start a weekly reflection practice`",
            parse_mode='Markdown'
        )
        return
    
    # Save the idea
    journal = JournalIntegration({})
    success = journal.save_idea(args, user_id)
    
    if success:
        response = f"""
💡 **Idea Captured**

**Your Idea:**
"{args}"

**What happens next:**
• Idea saved to your ideas collection
• Will be reviewed during weekly planning
• Can be developed into projects
• Helps track your creative thinking

Keep those ideas flowing! 🚀
        """
    else:
        response = "❌ Sorry, there was an error saving your idea. Please try again."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /task command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/task")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/task', '').strip()
    
    if not args:
        # Ask for the task
        await update.message.reply_text(
            "📋 **Add Task**\n\n"
            "Add a new task to your system.\n\n"
            "**Usage:**\n"
            "• `/task [task description]` - Add task directly\n"
            "• Reply with your task\n\n"
            "**Task Format:**\n"
            "• Simple: `/task Call mom`\n"
            "• With priority: `/task Review project proposal (high)`\n"
            "• With due date: `/task Submit report (due: tomorrow)`\n"
            "• With category: `/task Buy groceries (personal)`\n\n"
            "**Examples:**\n"
            "• `/task Follow up with client about proposal`\n"
            "• `/task Schedule dentist appointment (health)`\n"
            "• `/task Review weekly goals (planning)`",
            parse_mode='Markdown'
        )
        return
    
    # Save the task
    journal = JournalIntegration({})
    success = journal.add_task(args, user_id)
    
    if success:
        response = f"""
✅ **Task Added**

**Your Task:**
"{args}"

**What happens next:**
• Task added to your task list
• Will be included in your daily summary
• Can be reviewed during daily planning
• Helps track your productivity

Stay organized! 📝
        """
    else:
        response = "❌ Sorry, there was an error adding your task. Please try again."
    
    await update.message.reply_text(response, parse_mode='Markdown')
