"""
Daily operation handlers for the Personal System Telegram Bot.
Handles summary, health logging, learning logging, and quick notes.
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command
from integrations.personal_system import PersonalSystemIntegration


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /summary command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/summary")
    
    try:
        # Get personal system integration
        personal_system = PersonalSystemIntegration({})
        
        # Generate daily summary
        summary = personal_system.get_daily_summary()
    except Exception as e:
        get_logger(__name__).error(f"Error getting daily summary: {e}")
        summary = "📊 **Daily Summary**\n\nI'm still learning about your system. Try using some commands to log data first!\n\n• `/log_health` - Log health metrics\n• `/log_learning` - Log learning activity\n• `/quick_note` - Add a quick note\n• `/journal` - Create a journal entry"
    
    await update.message.reply_text(summary, parse_mode='Markdown')


async def log_health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /log_health command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/log_health")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/log_health', '').strip()
    
    if not args:
        # Ask for health metrics
        await update.message.reply_text(
            "🏃‍♂️ **Health Logging**\n\n"
            "Please log your health metrics. You can use:\n\n"
            "**Quick format:** `/log_health steps:8000 sleep:7.5 water:8 workout:yes`\n\n"
            "**Or reply with details:**\n"
            "• Steps taken today\n"
            "• Hours of sleep last night\n"
            "• Glasses of water consumed\n"
            "• Workout completed (yes/no)\n"
            "• Meditation minutes\n"
            "• Energy level (1-10)\n\n"
            "Example: `/log_health steps:8500 sleep:7.5 water:8 workout:yes meditation:15 energy:8`",
            parse_mode='Markdown'
        )
        return
    
    # Parse and log health data
    personal_system = PersonalSystemIntegration({})
    success = personal_system.log_health_data(args, user_id)
    
    if success:
        response = "✅ **Health data logged successfully!**\n\nYour health metrics have been recorded."
    else:
        response = "❌ Sorry, there was an error logging your health data. Please try again."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def log_learning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /log_learning command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/log_learning")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/log_learning', '').strip()
    
    if not args:
        # Ask for learning activity
        await update.message.reply_text(
            "📚 **Learning Logging**\n\n"
            "Please log your learning activity. You can use:\n\n"
            "**Quick format:** `/log_learning topic:Python time:30 notes:3`\n\n"
            "**Or reply with details:**\n"
            "• What topic/subject you studied\n"
            "• Time spent learning (minutes)\n"
            "• Number of notes created\n"
            "• Key insights or progress\n\n"
            "Example: `/log_learning topic:System Design time:45 notes:5 insights:Learned about microservices`",
            parse_mode='Markdown'
        )
        return
    
    # Parse and log learning data
    personal_system = PersonalSystemIntegration({})
    success = personal_system.log_learning_data(args, user_id)
    
    if success:
        response = "✅ **Learning activity logged successfully!**\n\nYour learning progress has been recorded."
    else:
        response = "❌ Sorry, there was an error logging your learning activity. Please try again."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def quick_note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quick_note command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/quick_note")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/quick_note', '').strip()
    
    if not args:
        # Ask for the note
        await update.message.reply_text(
            "💭 **Quick Note**\n\n"
            "Capture a quick thought, idea, or observation.\n\n"
            "**Usage:**\n"
            "• `/quick_note [your note]` - Add note directly\n"
            "• Reply with your note\n\n"
            "**Examples:**\n"
            "• `/quick_note Need to follow up with John about the project`\n"
            "• `/quick_note Idea: Create a habit tracking app`\n"
            "• `/quick_note Remember to call mom tomorrow`",
            parse_mode='Markdown'
        )
        return
    
    # Save the quick note
    personal_system = PersonalSystemIntegration({})
    success = personal_system.save_quick_note(args, user_id)
    
    if success:
        response = f"""
✅ **Quick Note Saved**

**Your Note:**
"{args}"

**What happens next:**
• Note saved to your knowledge base
• Will be included in your daily summary
• Can be reviewed during weekly planning
• Automatically categorized and tagged

Keep capturing those thoughts! 💡
        """
    else:
        response = "❌ Sorry, there was an error saving your note. Please try again."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def morning_routine_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /morning_routine command - voice-guided morning routine."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/morning_routine")
    
    # Get current time to personalize the routine
    from datetime import datetime
    current_time = datetime.now()
    current_hour = current_time.hour
    
    # Determine if it's actually morning
    if current_hour < 5 or current_hour > 11:
        time_context = "🌙 Good evening! Here's your morning routine for tomorrow:"
    elif current_hour < 12:
        time_context = "🌅 Good morning! Here's your routine for today:"
    else:
        time_context = "☀️ Good day! Here's your morning routine:"
    
    # Create the morning routine text
    routine_text = f"""
{time_context}

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
    
    # Send the routine as text first
    await update.message.reply_text(routine_text, parse_mode='Markdown')
    
    # Try to send as voice message if possible
    try:
        # For now, we'll send a text-to-speech message
        # In the future, this could be enhanced with actual TTS
        voice_note = f"""
{time_context}

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
        
        # Send as a text message that can be read aloud
        await update.message.reply_text(
            f"🎤 **Voice Guide Version:**\n\n{voice_note}\n\n"
            "💡 **Tip:** You can use your phone's text-to-speech feature to read this aloud, "
            "or ask me to send it as a voice message in the future!",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        get_logger(__name__).error(f"Error creating voice guide: {e}")
        await update.message.reply_text(
            "📝 **Text version sent successfully!**\n\n"
            "💡 **Pro tip:** You can use your phone's text-to-speech feature to have this read aloud to you each morning.",
            parse_mode='Markdown'
        )
