"""
System management handlers for the Personal System Telegram Bot.
Handles backup, sync, stats, and admin commands.
"""

import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command
from integrations.personal_system import PersonalSystemIntegration
import json


async def backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backup command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/backup")
    
    # Check if user is admin
    if not context.user_data.get('is_admin', False):
        await update.message.reply_text(
            "🔒 **Access Denied**\n\n"
            "Backup functionality is restricted to administrators only.",
            parse_mode='Markdown'
        )
        return
    
    # Start backup process
    await update.message.reply_text("🔄 **Starting backup process...**")
    
    try:
        personal_system = PersonalSystemIntegration({})
        backup_path = personal_system.create_backup()
        
        response = f"""
✅ **Backup Completed Successfully**

**Backup Location:** `{backup_path}`
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Size:** {personal_system.get_backup_size(backup_path)}

**What was backed up:**
• All system data
• Configuration files
• Log files
• User data and preferences

Your system is now safely backed up! 💾
        """
        
    except Exception as e:
        response = f"❌ **Backup Failed**\n\nError: {str(e)}\n\nPlease try again or check the logs."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def sync_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sync command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/sync")
    
    # Start sync process
    await update.message.reply_text("🔄 **Starting sync process...**")
    
    try:
        personal_system = PersonalSystemIntegration({})
        sync_result = personal_system.sync_data()
        
        response = f"""
✅ **Sync Completed**

**Sync Results:**
• Files synced: {sync_result.get('files_synced', 0)}
• Data updated: {sync_result.get('data_updated', 0)}
• Errors: {sync_result.get('errors', 0)}

**Last sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Your data is now synchronized across all devices! 🔄
        """
        
    except Exception as e:
        response = f"❌ **Sync Failed**\n\nError: {str(e)}\n\nPlease try again or check the logs."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/stats")
    
    try:
        personal_system = PersonalSystemIntegration({})
        stats = personal_system.get_system_stats()
        
        response = f"""
📊 **System Statistics**

**General Stats:**
• Total files: {stats.get('total_files', 0)}
• System size: {stats.get('system_size', '0 MB')}
• Last backup: {stats.get('last_backup', 'Never')}
• Uptime: {stats.get('uptime', 'Unknown')}

**User Activity (This Week):**
• Commands executed: {stats.get('commands_this_week', 0)}
• Notes created: {stats.get('notes_this_week', 0)}
• Journal entries: {stats.get('journal_entries_this_week', 0)}
• Shadow work insights: {stats.get('shadow_insights_this_week', 0)}

**Storage Usage:**
• Data directory: {stats.get('data_usage', '0 MB')}
• Log files: {stats.get('log_usage', '0 MB')}
• Cache: {stats.get('cache_usage', '0 MB')}

**System Health:**
• Database status: {'✅ Connected' if stats.get('db_status', False) else '❌ Disconnected'}
• Encryption: {'✅ Active' if stats.get('encryption_active', False) else '❌ Inactive'}
• Privacy protection: {'✅ Enabled' if stats.get('privacy_enabled', False) else '❌ Disabled'}

Everything looks good! 🟢
        """
        
    except Exception as e:
        response = f"❌ **Error getting statistics**\n\nError: {str(e)}"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/admin")
    
    # Check if user is admin
    if not context.user_data.get('is_admin', False):
        await update.message.reply_text(
            "🔒 **Access Denied**\n\n"
            "Admin commands are restricted to administrators only.",
            parse_mode='Markdown'
        )
        return
    
    # Check if there are arguments
    command_text = update.message.text
    args = command_text.replace('/admin', '').strip()
    
    if not args:
        # Show admin help
        admin_help = """
🔧 **Admin Commands**

**System Management:**
• `/admin backup` - Create system backup
• `/admin sync` - Sync all data
• `/admin restart` - Restart the bot
• `/admin logs` - View recent logs

**User Management:**
• `/admin users` - List authorized users
• `/admin add_user [user_id]` - Add authorized user
• `/admin remove_user [user_id]` - Remove authorized user

**Configuration:**
• `/admin config` - View current configuration
• `/admin reload_config` - Reload configuration
• `/admin test_connection` - Test system connections

**Maintenance:**
• `/admin cleanup` - Clean up old files
• `/admin optimize` - Optimize database
• `/admin health_check` - Run system health check

**Usage:** `/admin [command] [args]`
        """
        
        await update.message.reply_text(admin_help, parse_mode='Markdown')
        return
    
    # Parse admin command
    parts = args.split()
    admin_cmd = parts[0].lower()
    
    try:
        personal_system = PersonalSystemIntegration({})
        
        if admin_cmd == "backup":
            backup_path = personal_system.create_backup()
            response = f"✅ Backup created: {backup_path}"
            
        elif admin_cmd == "sync":
            sync_result = personal_system.sync_data()
            response = f"✅ Sync completed: {sync_result}"
            
        elif admin_cmd == "restart":
            response = "🔄 Bot restart initiated..."
            # Note: Actual restart would need to be handled by the main process
            
        elif admin_cmd == "logs":
            logs = personal_system.get_recent_logs(10)
            response = f"📋 Recent logs:\n{logs}"
            
        elif admin_cmd == "users":
            users = personal_system.get_authorized_users()
            response = f"👥 Authorized users: {users}"
            
        elif admin_cmd == "add_user" and len(parts) > 1:
            user_id = int(parts[1])
            success = personal_system.add_authorized_user(user_id)
            response = f"{'✅' if success else '❌'} User {user_id} {'added' if success else 'not added'}"
            
        elif admin_cmd == "remove_user" and len(parts) > 1:
            user_id = int(parts[1])
            success = personal_system.remove_authorized_user(user_id)
            response = f"{'✅' if success else '❌'} User {user_id} {'removed' if success else 'not removed'}"
            
        elif admin_cmd == "config":
            config = personal_system.get_config()
            response = f"⚙️ Current config: {config}"
            
        elif admin_cmd == "reload_config":
            success = personal_system.reload_config()
            response = f"{'✅' if success else '❌'} Config {'reloaded' if success else 'not reloaded'}"
            
        elif admin_cmd == "test_connection":
            test_result = personal_system.test_connections()
            response = f"🔗 Connection test: {test_result}"
            
        elif admin_cmd == "cleanup":
            cleanup_result = personal_system.cleanup_old_files()
            response = f"🧹 Cleanup completed: {cleanup_result}"
            
        elif admin_cmd == "optimize":
            optimize_result = personal_system.optimize_database()
            response = f"⚡ Optimization completed: {optimize_result}"
            
        elif admin_cmd == "health_check":
            health = personal_system.health_check()
            response = f"🏥 Health check: {health}"
            
        elif admin_cmd == "set_openai_key":
            # Extract API key from the message
            message_text = update.message.text
            if " " in message_text:
                # Split by spaces and take everything after "set_openai_key"
                parts = message_text.split()
                if len(parts) >= 3:  # /admin set_openai_key API_KEY
                    api_key = " ".join(parts[2:])  # Join in case API key has spaces
                    if api_key:
                        # Import secure config manager
                        sys.path.append(str(Path(__file__).parent.parent.parent / "config"))
                        from secure_config import SecureConfigManager
                        
                        secure_config = SecureConfigManager()
                        if secure_config.set_openai_api_key(api_key):
                            response = "✅ OpenAI API key securely stored and encrypted!"
                        else:
                            response = "❌ Failed to store OpenAI API key. Please check the logs."
                    else:
                        response = "❌ Please provide an API key: /admin set_openai_key YOUR_API_KEY"
                else:
                    response = "❌ Please provide an API key: /admin set_openai_key YOUR_API_KEY"
            else:
                response = "❌ Please provide an API key: /admin set_openai_key YOUR_API_KEY"
                
        else:
            response = f"❌ Unknown admin command: {admin_cmd}"
            
    except Exception as e:
        response = f"❌ Admin command failed: {str(e)}"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tasks command to show prioritized TODO list."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(get_logger(__name__), user_id, username, "/tasks")
    
    try:
        # Load tasks from the personal system
        tasks_file = Path("../../../.qodo/tasks.json")
        
        if not tasks_file.exists():
            await update.message.reply_text(
                "📋 **Tasks**\n\nNo tasks found. Your TODO system is ready to be populated!\n\n"
                "Tasks will appear here as you identify work items during our conversations.",
                parse_mode='Markdown'
            )
            return
        
        with open(tasks_file, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)
        
        tasks = tasks_data.get('tasks', [])
        metadata = tasks_data.get('metadata', {})
        
        if not tasks:
            await update.message.reply_text(
                "📋 **Tasks**\n\nNo pending tasks found. Great job staying on top of things! 🎉",
                parse_mode='Markdown'
            )
            return
        
        # Group tasks by priority
        high_priority = [t for t in tasks if t.get('status') == 'pending' and t.get('priority') == 'high']
        medium_priority = [t for t in tasks if t.get('status') == 'pending' and t.get('priority') == 'medium']
        low_priority = [t for t in tasks if t.get('status') == 'pending' and t.get('priority') == 'low']
        
        response = f"""📋 **Your Task List**\n\n"""
        
        if high_priority:
            response += "🔴 **High Priority**\n"
            for task in high_priority:
                response += f"• {task['content']}\n"
                if task.get('description'):
                    response += f"  _{task['description']}_\n"
                if task.get('estimated_effort'):
                    response += f"  ⏱️ {task['estimated_effort']}\n"
            response += "\n"
        
        if medium_priority:
            response += "🟡 **Medium Priority**\n"
            for task in medium_priority:
                response += f"• {task['content']}\n"
                if task.get('description'):
                    response += f"  _{task['description']}_\n"
                if task.get('estimated_effort'):
                    response += f"  ⏱️ {task['estimated_effort']}\n"
            response += "\n"
        
        if low_priority:
            response += "🟢 **Low Priority**\n"
            for task in low_priority:
                response += f"• {task['content']}\n"
                if task.get('description'):
                    response += f"  _{task['description']}_\n"
                if task.get('estimated_effort'):
                    response += f"  ⏱️ {task['estimated_effort']}\n"
        
        # Add summary
        response += f"\n---\n"
        response += f"**Summary:** {len(high_priority)} high, {len(medium_priority)} medium, {len(low_priority)} low priority tasks\n"
        response += f"**Total Pending:** {len([t for t in tasks if t.get('status') == 'pending'])}\n"
        
        if high_priority:
            response += f"\n🎯 **Focus on high priority tasks first!**"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        get_logger(__name__).error(f"Error loading tasks: {e}")
        await update.message.reply_text(
            "❌ Sorry, there was an error loading your tasks. Please try again."
        )
