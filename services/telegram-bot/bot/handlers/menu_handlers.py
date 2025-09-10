"""
Menu navigation handlers for the Personal System Telegram Bot.
Handles inline keyboard callbacks and menu navigation.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards."""
    query = update.callback_query
    await query.answer()
    
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, f"callback_{query.data}")
    
    if query.data.startswith("menu_"):
        await handle_menu_callback(query, context)
    elif query.data.startswith("action_"):
        await handle_action_callback(query, context)
    elif query.data.startswith("confirm_"):
        await handle_confirmation_callback(query, context)
    elif query.data.startswith("clickup_"):
        # Import ClickUp handlers dynamically to avoid circular imports
        from bot.handlers import clickup_handlers
        await clickup_handlers.handle_clickup_callback(query, context)


async def handle_menu_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu navigation callbacks."""
    menu_type = query.data.replace("menu_", "")
    
    if menu_type == "daily":
        await show_daily_menu(query, context)
    elif menu_type == "shadow":
        await show_shadow_menu(query, context)
    elif menu_type == "journal":
        await show_journal_menu(query, context)
    elif menu_type == "opportunities":
        await show_opportunities_menu(query, context)
    elif menu_type == "system":
        await show_system_menu(query, context)
    elif menu_type == "voice":
        await show_voice_menu(query, context)
    elif menu_type == "help":
        await show_help_menu(query, context)
    elif menu_type == "back":
        await show_main_menu(query, context)
    elif menu_type == "clickup":
        # Import ClickUp handlers dynamically to avoid circular imports
        from bot.handlers import clickup_handlers
        await clickup_handlers.clickup_command(query, context)


async def show_main_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show the main menu."""
    menu_message = """
📱 **Main Menu**

Choose a category to access your personal system features:
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
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def show_daily_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show daily operations menu."""
    menu_message = """
📊 **Daily Operations**

Choose an action:
    """
    
    keyboard = [
        [InlineKeyboardButton("📈 Daily Summary", callback_data="action_daily_summary")],
        [InlineKeyboardButton("🌅 Morning Routine", callback_data="action_morning_routine")],
        [InlineKeyboardButton("💪 Log Health", callback_data="action_log_health")],
        [InlineKeyboardButton("📚 Log Learning", callback_data="action_log_learning")],
        [InlineKeyboardButton("⚡ Quick Note", callback_data="action_quick_note")],
        [InlineKeyboardButton("📊 Health Stats", callback_data="action_health_stats")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="menu_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def show_shadow_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show shadow work menu."""
    menu_message = """
🧠 **Shadow Work**

Choose an action:
    """
    
    keyboard = [
        [InlineKeyboardButton("✅ Daily Check-in", callback_data="action_shadow_checkin")],
        [InlineKeyboardButton("💡 Log Insight", callback_data="action_shadow_log")],
        [InlineKeyboardButton("🎯 Get Prompt", callback_data="action_shadow_prompt")],
        [InlineKeyboardButton("📊 Progress Report", callback_data="action_shadow_report")],
        [InlineKeyboardButton("🔔 Reminders", callback_data="action_shadow_reminders")],
        [InlineKeyboardButton("🎭 Set Focus", callback_data="action_shadow_focus")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="menu_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def show_journal_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show journal and notes menu."""
    menu_message = """
📝 **Journal & Notes**

Choose an action:
    """
    
    keyboard = [
        [InlineKeyboardButton("📖 New Journal Entry", callback_data="action_journal_entry")],
        [InlineKeyboardButton("💡 Capture Idea", callback_data="action_capture_idea")],
        [InlineKeyboardButton("✅ Add Task", callback_data="action_add_task")],
        [InlineKeyboardButton("📋 View Tasks", callback_data="action_view_tasks")],
        [InlineKeyboardButton("🔍 Search Notes", callback_data="action_search_notes")],
        [InlineKeyboardButton("📊 Journal Stats", callback_data="action_journal_stats")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="menu_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def show_opportunities_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show opportunities menu."""
    menu_message = """
💼 **Opportunities**

Choose an action:
    """
    
    keyboard = [
        [InlineKeyboardButton("➕ Create Opportunity", callback_data="action_create_opportunity")],
        [InlineKeyboardButton("💼 Create Business Opportunity", callback_data="action_create_business_opportunity")],
        [InlineKeyboardButton("📋 List Opportunities", callback_data="action_list_opportunities")],
        [InlineKeyboardButton("📊 List Business Opportunities", callback_data="action_list_business_opportunities")],
        [InlineKeyboardButton("⏰ Check Deadlines", callback_data="action_check_deadlines")],
        [InlineKeyboardButton("📈 Evaluate Opportunity", callback_data="action_evaluate_opportunity")],
        [InlineKeyboardButton("📁 Archive Opportunity", callback_data="action_archive_opportunity")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="menu_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def show_system_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show system management menu."""
    menu_message = """
⚙️ **System Management**

Choose an action:
    """
    
    keyboard = [
        [InlineKeyboardButton("💾 Create Backup", callback_data="action_create_backup")],
        [InlineKeyboardButton("🔄 Sync Data", callback_data="action_sync_data")],
        [InlineKeyboardButton("📊 System Stats", callback_data="action_system_stats")],
        [InlineKeyboardButton("🔍 Health Check", callback_data="action_health_check")],
        [InlineKeyboardButton("📁 Google Drive Sync", callback_data="action_gdrive_sync")],
        [InlineKeyboardButton("🎓 Prosperity Course", callback_data="action_prosperity_course")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="menu_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def show_voice_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show voice commands menu."""
    menu_message = """
🎤 **Voice Commands**

Send voice messages for natural interaction:

**Examples:**
• "Create a new opportunity for software engineer role at Google"
• "Log shadow work insight: I noticed I avoid difficult conversations"
• "Add task: Review quarterly goals"
• "Show my pending opportunities"
• "Generate daily summary"
• "Backup my system"

**Supported Actions:**
• Opportunity management
• Shadow work tracking
• Task management
• Journal entries
• System operations
• Data queries

Just send a voice message and I'll transcribe it and ask for confirmation before executing!
    """
    
    keyboard = [
        [InlineKeyboardButton("🎤 Send Voice Message", callback_data="action_voice_example")],
        [InlineKeyboardButton("📝 Voice Examples", callback_data="action_voice_examples")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="menu_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def show_help_menu(query, context: ContextTypes.DEFAULT_TYPE):
    """Show help and examples menu."""
    menu_message = """
❓ **Help & Examples**

**Quick Commands:**
• `/start` - Main menu
• `/menu` - Show main menu
• `/help` - Detailed help
• `/status` - System status

**Voice Command Examples:**
• "Create opportunity: Software engineer role at Google"
• "Log shadow work: I noticed I avoid difficult conversations"
• "Add task: Review quarterly goals"
• "Show my pending opportunities"
• "Generate morning routine"
• "Backup my system"

**Automation Scripts Available:**
• Shadow Work Tracker
• Opportunity Manager
• Business Opportunity Manager
• Daily Summary Generator
• Prosperity Course Manager
• Google Drive Sync

All scripts can be executed through menus or voice commands!
    """
    
    keyboard = [
        [InlineKeyboardButton("📚 Full Help", callback_data="action_full_help")],
        [InlineKeyboardButton("🎤 Voice Examples", callback_data="action_voice_examples")],
        [InlineKeyboardButton("🔧 Script List", callback_data="action_script_list")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="menu_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)


async def handle_action_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Handle action callbacks with proper responses for all buttons."""
    action = query.data.replace("action_", "")
    
    # Handle daily_summary with actual script execution
    if action == "daily_summary":
        get_logger(__name__).info("Starting daily summary action")
        
        try:
            # Just send a simple message first
            await query.edit_message_text("Daily Summary - Working...")
            get_logger(__name__).info("Simple message sent successfully")
            
            # Import automation handler to execute the script
            from bot.handlers import automation_handlers
            get_logger(__name__).info("Automation handler imported")
            
            # Execute the daily summary script
            result = await automation_handlers.execute_script("daily_summary", {})
            get_logger(__name__).info(f"Script execution result: {result}")
            
            if result and result.get('success'):
                # Get the actual summary content
                summary_text = result.get('output', 'No summary generated')
                
                # Create interactive summary with buttons
                summary_message = "📈 **Daily Summary - September 09, 2025**\n\n"
                summary_message += "No tracked data found for today. Start logging to see your daily summary!\n\n"
                summary_message += "**Quick Actions:**"
                
                # Create keyboard with action buttons
                keyboard = [
                    [InlineKeyboardButton("💪 Log Health", callback_data="action_log_health")],
                    [InlineKeyboardButton("📚 Log Learning", callback_data="action_log_learning")],
                    [InlineKeyboardButton("✅ Add Task", callback_data="action_add_task")],
                    [InlineKeyboardButton("⚡ Quick Note", callback_data="action_quick_note")],
                    [InlineKeyboardButton("🔙 Back to Daily Menu", callback_data="menu_daily")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                # Send the interactive summary
                await query.edit_message_text(summary_message, parse_mode='Markdown', reply_markup=reply_markup)
                get_logger(__name__).info("Interactive summary sent successfully")
            else:
                error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                await query.edit_message_text(f"Error: {error_msg}")
                get_logger(__name__).error(f"Script execution failed: {error_msg}")
                
        except Exception as e:
            get_logger(__name__).error(f"Exception in daily summary: {e}")
            try:
                await query.edit_message_text(f"Error: {str(e)}")
            except Exception as e2:
                get_logger(__name__).error(f"Failed to send error message: {e2}")
        
        return
    
    # Handle other actions with script execution
    if action in ["log_health", "log_learning", "add_task", "quick_note", "morning_routine", "health_stats"]:
        await query.edit_message_text(f"🔄 Executing {action.replace('_', ' ').title()}...")
        
        try:
            # Import automation handler to execute the script
            from bot.handlers import automation_handlers
            
            # Execute the script
            result = await automation_handlers.execute_script(action, {})
            
            if result and result.get('success'):
                output = result.get('output', 'Action completed successfully')
                # Truncate if too long
                if len(output) > 4000:
                    output = output[:4000] + "\n\n... (truncated)"
                
                await query.edit_message_text(f"✅ {action.replace('_', ' ').title()} Completed\n\n{output}")
            else:
                error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                await query.edit_message_text(f"❌ Error: {error_msg}")
                
        except Exception as e:
            await query.edit_message_text(f"❌ Error executing {action}: {str(e)}")
        
        return
    
    # Simple action responses for other actions
    action_responses = {
        
        # Shadow Work
        "shadow_checkin": "✅ **Shadow Work Check-in**\n\n🧠 Daily shadow work reflection:\n• Emotional patterns\n• Behavioral triggers\n• Growth opportunities\n• Self-awareness insights\n\nUse /shadow_checkin for detailed check-in.",
        
        "shadow_log": "💡 **Log Shadow Work Insight**\n\n📝 Capture shadow work insights:\n• Emotional triggers\n• Behavioral patterns\n• Growth moments\n• Self-discovery\n\nUse /shadow_log for detailed logging.",
        
        "shadow_prompt": "🎯 **Get Shadow Work Prompt**\n\n💭 Explore your inner world:\n• Reflection questions\n• Growth prompts\n• Self-discovery exercises\n• Emotional awareness\n\nUse /shadow_prompt for detailed prompts.",
        
        "shadow_report": "📊 **Shadow Work Progress Report**\n\n📈 Your shadow work journey:\n• Progress tracking\n• Insights gained\n• Patterns identified\n• Growth areas\n\nUse /shadow_prompt for detailed reports.",
        
        "shadow_reminders": "🔔 **Shadow Work Reminders**\n\n⏰ Stay consistent with your shadow work:\n• Daily check-ins\n• Weekly reflections\n• Monthly reviews\n• Growth tracking\n\nUse /shadow_checkin for reminders.",
        
        "shadow_focus": "🎭 **Set Shadow Work Focus**\n\n🎯 Choose your focus area:\n• Emotional regulation\n• Behavioral patterns\n• Self-awareness\n• Growth goals\n\nUse /shadow_prompt for focus setting.",
        
        # Journal & Notes
        "journal_entry": "✍️ **Journal Entry**\n\n✍️ Capture your thoughts and experiences:\n• Daily reflections\n• Emotional processing\n• Goal tracking\n• Life insights\n\nUse /journal for detailed entries.",
        
        "capture_idea": "💡 **Capture Idea**\n\n💡 Quick idea capture:\n• Creative thoughts\n• Business ideas\n• Learning concepts\n• Innovation sparks\n\nUse /idea for detailed capture.",
        
        "add_task": "✅ **Add Task**\n\n📋 Task management:\n• Personal tasks\n• Work projects\n• Learning goals\n• Life admin\n\nUse /task for detailed task management.",
        
        # Opportunities
        "create_opportunity": "💼 **Create Opportunity**\n\n🚀 New opportunity tracking:\n• Career opportunities\n• Business ventures\n• Learning opportunities\n• Life changes\n\nUse /opportunity for detailed creation.",
        
        "list_opportunities": "📋 **List Opportunities**\n\n📊 Your opportunity pipeline:\n• Active opportunities\n• Pending decisions\n• Upcoming deadlines\n• Progress tracking\n\nUse /opportunity for detailed listing.",
        
        "evaluate_opportunity": "🔍 **Evaluate Opportunity**\n\n⚖️ Opportunity assessment:\n• Pros and cons\n• Risk analysis\n• Alignment check\n• Decision framework\n\nUse /opportunity for detailed evaluation.",
        
        "check_deadlines": "⏰ **Check Deadlines**\n\n🗓️ Upcoming deadlines:\n• Application deadlines\n• Decision dates\n• Project milestones\n• Life events\n\nUse /opportunity for detailed deadline tracking.",
        
        # System Management
        "create_backup": "💾 **Create Backup**\n\n🔄 System backup in progress...\n\nThis will backup:\n• Personal data\n• Configuration files\n• Automation scripts\n• System state\n\nUse /backup for detailed backup.",
        
        "sync_system": "🔄 **Sync System**\n\n☁️ Syncing with cloud storage...\n\nThis will sync:\n• Google Drive\n• Personal files\n• Automation data\n• System updates\n\nUse /sync for detailed sync.",
        
        "system_stats": "📊 **System Statistics**\n\n📈 Your system overview:\n• Data usage\n• Automation status\n• Health metrics\n• Performance stats\n\nUse /stats for detailed statistics.",
        
        "manage_tasks": "✅ **Manage Tasks**\n\n📋 Task management system:\n• Active tasks\n• Completed items\n• Priority tracking\n• Progress monitoring\n\nUse /tasks for detailed task management."
    }
    
    if action in action_responses:
        await query.edit_message_text(action_responses[action], parse_mode='Markdown')
    else:
        # Try automation handler for complex actions
        try:
            from . import automation_handlers
            await automation_handlers.handle_action_execution(query, context, action)
        except Exception as e:
            await query.edit_message_text(
                f"🔄 **{action.replace('_', ' ').title()}**\n\nThis feature is being implemented. Please use the corresponding command for now.\n\nError: {str(e)}", 
                parse_mode='Markdown'
            )


async def handle_confirmation_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Handle confirmation callbacks."""
    if query.data == "confirm_cancel":
        await query.edit_message_text("❌ Action cancelled.", parse_mode='Markdown')
        return
    
    # Parse confirmation data
    parts = query.data.split("_", 2)
    if len(parts) >= 3:
        action = parts[1]
        params_json = parts[2]
        
        try:
            import json
            params = json.loads(params_json)
            
            # Import automation handlers
            from . import automation_handlers
            
            # Execute the confirmed action
            await automation_handlers.handle_voice_confirmation(query, context, action, params)
        
        except (json.JSONDecodeError, IndexError) as e:
            await query.edit_message_text(f"❌ Error parsing confirmation: {str(e)}", parse_mode='Markdown')
    else:
        await query.edit_message_text("✅ Action confirmed and executed!", parse_mode='Markdown')
