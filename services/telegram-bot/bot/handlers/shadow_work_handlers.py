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
        response = f"""
❌ **Error Logging Insight**

There was an error saving your shadow work insight. Please try again.

**Your Insight:**
"{args}"

**Troubleshooting:**
• Check your internet connection
• Try again in a few moments
• Contact support if the issue persists

Keep exploring! 🌙✨
        """
    
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


async def shadow_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shadow_report command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/shadow_report")
    
    # Get shadow work integration
    shadow_work = ShadowWorkIntegration()
    
    # Get user's shadow work statistics
    stats = shadow_work.get_insight_stats(user_id)
    recent_insights = shadow_work.get_recent_insights(user_id, 5)
    
    # Format the report
    report_message = f"""
📊 **Shadow Work Progress Report**

**Your Statistics:**
• Total Insights: {stats['total_insights']}
• This Week: {stats['this_week']}
• This Month: {stats['this_month']}
• Last Insight: {stats['last_insight'][:10] if stats['last_insight'] else 'None'}

**Recent Insights:**
"""
    
    if recent_insights:
        for i, insight in enumerate(recent_insights, 1):
            date = insight['timestamp'][:10]
            content = insight['insight'][:100] + "..." if len(insight['insight']) > 100 else insight['insight']
            report_message += f"{i}. *{date}*: {content}\n\n"
    else:
        report_message += "No insights logged yet. Start your shadow work journey! 🌙\n\n"
    
    report_message += """
**Next Steps:**
• Continue daily check-ins
• Log insights as they arise
• Practice self-compassion
• Embrace your shadow with love

**Quick Actions:**
• `/shadow_checkin` - Daily check-in
• `/shadow_log` - Log new insight
• `/shadow_prompt` - Get reflection prompt

Remember: Every insight is progress! 💜✨
    """
    
    await update.message.reply_text(report_message, parse_mode='Markdown')


async def shadow_reminders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shadow_reminders command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/shadow_reminders")
    
    reminders_message = """
🔔 **Shadow Work Reminders**

**Daily Practices:**
• Morning check-in with your shadow
• Notice resistance throughout the day
• Log insights as they arise
• Evening reflection on patterns

**Weekly Practices:**
• Review your shadow work progress
• Identify recurring patterns
• Set intentions for integration
• Practice self-compassion

**Monthly Practices:**
• Deep dive into one shadow aspect
• Celebrate your growth
• Adjust your approach
• Plan next month's focus

**Quick Reminders:**
• Your shadow is not your enemy
• Every insight is valuable
• Progress, not perfection
• Self-compassion is key

**Set Your Own Reminders:**
• Use your phone's reminder app
• Set daily shadow work time
• Create accountability partners
• Track your consistency

**Remember:** Shadow work is a journey, not a destination. Be patient and kind with yourself. 🌙💜
    """
    
    await update.message.reply_text(reminders_message, parse_mode='Markdown')


async def shadow_focus_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shadow_focus command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/shadow_focus")
    
    # Check if there's text after the command
    command_text = update.message.text
    args = command_text.replace('/shadow_focus', '').strip()
    
    if not args:
        # Ask for the shadow aspect to focus on
        focus_message = """
🎭 **Set Shadow Work Focus**

What shadow aspect would you like to focus on this week?

**Common Shadow Aspects:**
• Perfectionism
• People-pleasing
• Control issues
• Avoidance patterns
• Self-criticism
• Fear of vulnerability
• Need for approval
• Anger or resentment

**How to use:**
• `/shadow_focus [aspect]` - Set your focus
• Example: `/shadow_focus perfectionism`
• Example: `/shadow_focus people-pleasing`

**Focus Benefits:**
• Deeper self-awareness
• Targeted growth
• Pattern recognition
• Integration practice

**Quick Actions:**
• `/shadow_prompt` - Get reflection prompt
• `/shadow_log` - Log insights about this aspect
• `/shadow_report` - See your progress

What shadow aspect calls to you today? 🌙
        """
        
        await update.message.reply_text(focus_message, parse_mode='Markdown')
        return
    
    # Set the focus
    focus_message = f"""
🎭 **Shadow Focus Set**

**Your Focus:** {args}

**This Week's Practice:**
• Notice when this aspect shows up
• Observe without judgment
• Log insights as they arise
• Practice self-compassion
• Look for integration opportunities

**Reflection Questions:**
• How does this aspect serve me?
• What is it trying to protect me from?
• How can I honor this part of myself?
• What would integration look like?

**Daily Check-ins:**
• Morning: Set intention to notice this aspect
• Evening: Reflect on what you observed
• Log insights: Use `/shadow_log [your insight]`

**Remember:** This is about awareness and integration, not elimination. Be gentle with yourself. 💜

**Quick Actions:**
• `/shadow_prompt` - Get reflection prompt
• `/shadow_log` - Log insights about this aspect
• `/shadow_report` - Track your progress
    """
    
    await update.message.reply_text(focus_message, parse_mode='Markdown')
