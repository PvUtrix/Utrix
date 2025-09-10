"""
ClickUp Integration Handlers for the Personal System Telegram Bot.
Handles ClickUp project and task management through Telegram.
"""

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Add the Tango.Vision projects directory to the path
tango_vision_path = Path(__file__).parent.parent.parent.parent.parent / "domains" / "my-startups" / "Tango.Vision" / "projects"
sys.path.append(str(tango_vision_path))

from utils.logger import get_logger, log_command

try:
    from clickup_integrated_manager import ClickUpIntegratedManager
    CLICKUP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"ClickUp integration not available: {e}")
    CLICKUP_AVAILABLE = False

logger = get_logger(__name__)

class ClickUpHandler:
    """Handles ClickUp integration for the Telegram bot."""
    
    def __init__(self, config: Dict):
        """Initialize the ClickUp handler."""
        self.config = config
        self.manager = None
        
        if CLICKUP_AVAILABLE:
            try:
                # Initialize ClickUp manager
                clickup_config_path = tango_vision_path / "clickup_config.json"
                self.manager = ClickUpIntegratedManager(
                    projects_dir=str(tango_vision_path),
                    clickup_config_file=str(clickup_config_path)
                )
                logger.info("ClickUp integration initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ClickUp integration: {e}")
                self.manager = None
    
    def is_available(self) -> bool:
        """Check if ClickUp integration is available."""
        return CLICKUP_AVAILABLE and self.manager is not None and self.manager.clickup_enabled

async def clickup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clickup command with main ClickUp menu."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(logger, user_id, username, "/clickup")
    
    # Initialize ClickUp handler
    clickup_handler = ClickUpHandler(context.bot_data.get('config', {}))
    
    if not clickup_handler.is_available():
        await update.message.reply_text(
            "❌ ClickUp integration is not available.\n\n"
            "Please ensure:\n"
            "1. ClickUp is configured in Tango.Vision projects\n"
            "2. API credentials are set up\n"
            "3. Integration is properly installed"
        )
        return
    
    menu_message = """
🎯 **ClickUp Integration**

Manage your Tango.Vision projects directly through ClickUp!

Choose an option below:
    """
    
    keyboard = [
        [InlineKeyboardButton("📋 List Projects", callback_data="clickup_list_projects")],
        [InlineKeyboardButton("➕ Create Project", callback_data="clickup_create_project")],
        [InlineKeyboardButton("📝 Add Task", callback_data="clickup_add_task")],
        [InlineKeyboardButton("📊 Project Status", callback_data="clickup_project_status")],
        [InlineKeyboardButton("📄 Upload Document", callback_data="clickup_upload_doc")],
        [InlineKeyboardButton("💬 Add Comment", callback_data="clickup_add_comment")],
        [InlineKeyboardButton("🔄 Sync Project", callback_data="clickup_sync_project")],
        [InlineKeyboardButton("📈 Generate Report", callback_data="clickup_generate_report")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(menu_message, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_clickup_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Handle ClickUp callback queries."""
    data = query.data
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(logger, user_id, username, f"clickup_callback_{data}")
    
    # Initialize ClickUp handler
    clickup_handler = ClickUpHandler(context.bot_data.get('config', {}))
    
    if not clickup_handler.is_available():
        await query.answer("❌ ClickUp integration not available")
        return
    
    if data == "clickup_list_projects":
        await show_projects_list(query, context, clickup_handler)
    elif data == "clickup_create_project":
        await show_create_project_menu(query, context, clickup_handler)
    elif data == "clickup_add_task":
        await show_add_task_menu(query, context, clickup_handler)
    elif data == "clickup_project_status":
        await show_project_status_menu(query, context, clickup_handler)
    elif data == "clickup_upload_doc":
        await show_upload_document_menu(query, context, clickup_handler)
    elif data == "clickup_add_comment":
        await show_add_comment_menu(query, context, clickup_handler)
    elif data == "clickup_sync_project":
        await show_sync_project_menu(query, context, clickup_handler)
    elif data == "clickup_generate_report":
        await generate_clickup_report(query, context, clickup_handler)

async def show_projects_list(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Show list of projects."""
    try:
        projects = clickup_handler.manager.local_manager.list_projects()
        
        if not projects:
            await query.edit_message_text("📋 **No projects found**\n\nCreate your first project to get started!")
            return
        
        message = "📋 **Your Projects**\n\n"
        
        for project in projects:
            # Check ClickUp sync status
            sync_status = "✅" if project.id in clickup_handler.manager.project_mappings else "❌"
            
            # Get project stats
            completed_tasks = len([t for t in project.tasks if t.status.value == 'completed'])
            total_tasks = len(project.tasks)
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            message += f"{sync_status} **{project.name}**\n"
            message += f"   ID: `{project.id}`\n"
            message += f"   Status: {project.status.value.title()}\n"
            message += f"   Priority: {project.priority.value.title()}\n"
            message += f"   Tasks: {completed_tasks}/{total_tasks} ({completion_rate:.1f}%)\n"
            message += f"   Budget: ${project.financial.budget:,.2f}\n\n"
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error showing projects list: {e}")
        await query.edit_message_text(f"❌ Error loading projects: {str(e)}")

async def show_create_project_menu(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Show project creation menu."""
    message = """
➕ **Create New Project**

To create a new project, send a message in this format:

```
/project_create Project Name
Description of the project
Priority: high|medium|low
Budget: 10000
Revenue: 50000
```

**Example:**
```
/project_create My New App
A revolutionary mobile application
Priority: high
Budget: 25000
Revenue: 100000
```

Or use the quick create button below:
    """
    
    keyboard = [
        [InlineKeyboardButton("🚀 Quick Create (High Priority)", callback_data="clickup_quick_create_high")],
        [InlineKeyboardButton("📋 Quick Create (Medium Priority)", callback_data="clickup_quick_create_medium")],
        [InlineKeyboardButton("🔙 Back to ClickUp Menu", callback_data="clickup_back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def show_add_task_menu(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Show add task menu."""
    try:
        projects = clickup_handler.manager.local_manager.list_projects()
        
        if not projects:
            await query.edit_message_text("❌ **No projects found**\n\nCreate a project first before adding tasks.")
            return
        
        message = "📝 **Add Task to Project**\n\n"
        message += "To add a task, send a message in this format:\n\n"
        message += "```\n/task_add <project_id> Task Title\nDescription of the task\nPriority: high|medium|low\nDue: 2024-12-31\nHours: 8\nDaily: true|false\n```\n\n"
        message += "**Available Projects:**\n"
        
        keyboard = []
        for project in projects[:5]:  # Show first 5 projects
            message += f"• `{project.id}` - {project.name}\n"
            keyboard.append([InlineKeyboardButton(f"📝 Add to {project.name}", callback_data=f"clickup_add_task_{project.id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to ClickUp Menu", callback_data="clickup_back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error showing add task menu: {e}")
        await query.edit_message_text(f"❌ Error loading projects: {str(e)}")

async def show_project_status_menu(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Show project status menu."""
    try:
        projects = clickup_handler.manager.local_manager.list_projects()
        
        if not projects:
            await query.edit_message_text("❌ **No projects found**")
            return
        
        message = "📊 **Project Status**\n\n"
        
        keyboard = []
        for project in projects:
            # Get ClickUp status if available
            clickup_status = clickup_handler.manager.get_clickup_status(project.id)
            
            message += f"**{project.name}**\n"
            message += f"Local: {len(project.tasks)} tasks\n"
            
            if clickup_status:
                message += f"ClickUp: {clickup_status['total_tasks']} tasks ({clickup_status['completion_rate']:.1f}% complete)\n"
            else:
                message += "ClickUp: Not synced\n"
            
            message += "\n"
            
            keyboard.append([InlineKeyboardButton(f"📊 {project.name} Details", callback_data=f"clickup_status_{project.id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to ClickUp Menu", callback_data="clickup_back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error showing project status: {e}")
        await query.edit_message_text(f"❌ Error loading project status: {str(e)}")

async def show_upload_document_menu(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Show upload document menu."""
    message = """
📄 **Upload Document to ClickUp**

To upload a document, send a message in this format:

```
/upload_doc <project_id> /path/to/document.pdf
Task Name: Document Upload
```

**Note:** The file must be accessible from the server where the bot is running.

**Available Projects:**
    """
    
    try:
        projects = clickup_handler.manager.local_manager.list_projects()
        
        keyboard = []
        for project in projects[:5]:
            message += f"• `{project.id}` - {project.name}\n"
            keyboard.append([InlineKeyboardButton(f"📄 Upload to {project.name}", callback_data=f"clickup_upload_{project.id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to ClickUp Menu", callback_data="clickup_back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error showing upload menu: {e}")
        await query.edit_message_text(f"❌ Error loading projects: {str(e)}")

async def show_add_comment_menu(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Show add comment menu."""
    message = """
💬 **Add Comment to ClickUp Project**

To add a comment, send a message in this format:

```
/comment_add <project_id> Your comment text here
Task Name: Project Update
```

**Available Projects:**
    """
    
    try:
        projects = clickup_handler.manager.local_manager.list_projects()
        
        keyboard = []
        for project in projects[:5]:
            message += f"• `{project.id}` - {project.name}\n"
            keyboard.append([InlineKeyboardButton(f"💬 Comment on {project.name}", callback_data=f"clickup_comment_{project.id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to ClickUp Menu", callback_data="clickup_back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error showing comment menu: {e}")
        await query.edit_message_text(f"❌ Error loading projects: {str(e)}")

async def show_sync_project_menu(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Show sync project menu."""
    try:
        projects = clickup_handler.manager.local_manager.list_projects()
        
        if not projects:
            await query.edit_message_text("❌ **No projects found**")
            return
        
        message = "🔄 **Sync Projects to ClickUp**\n\n"
        
        keyboard = []
        for project in projects:
            sync_status = "✅ Synced" if project.id in clickup_handler.manager.project_mappings else "❌ Not Synced"
            message += f"**{project.name}** - {sync_status}\n"
            
            if project.id not in clickup_handler.manager.project_mappings:
                keyboard.append([InlineKeyboardButton(f"🔄 Sync {project.name}", callback_data=f"clickup_sync_{project.id}")])
        
        if not keyboard:
            message += "\n✅ All projects are synced!"
        
        keyboard.append([InlineKeyboardButton("🔙 Back to ClickUp Menu", callback_data="clickup_back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error showing sync menu: {e}")
        await query.edit_message_text(f"❌ Error loading projects: {str(e)}")

async def generate_clickup_report(query, context: ContextTypes.DEFAULT_TYPE, clickup_handler: ClickUpHandler):
    """Generate ClickUp report."""
    try:
        report = clickup_handler.manager.generate_integrated_report()
        
        # Truncate if too long for Telegram
        if len(report) > 4000:
            report = report[:4000] + "\n\n... (report truncated)"
        
        await query.edit_message_text(f"📈 **ClickUp Integration Report**\n\n```\n{report}\n```", parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        await query.edit_message_text(f"❌ Error generating report: {str(e)}")

# Command handlers for direct commands
async def project_create_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /project_create command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(logger, user_id, username, "/project_create")
    
    # Initialize ClickUp handler
    clickup_handler = ClickUpHandler(context.bot_data.get('config', {}))
    
    if not clickup_handler.is_available():
        await update.message.reply_text("❌ ClickUp integration not available")
        return
    
    # Parse command arguments
    args = context.args
    if len(args) < 1:
        await update.message.reply_text(
            "❌ Usage: /project_create <project_name>\n"
            "Example: /project_create My New App"
        )
        return
    
    project_name = " ".join(args)
    
    try:
        # Create project
        project_id = clickup_handler.manager.create_project(
            name=project_name,
            description=f"Project created via Telegram bot on {datetime.now().strftime('%Y-%m-%d')}",
            priority="medium",
            owner=username,
            sync_to_clickup=True
        )
        
        await update.message.reply_text(
            f"✅ **Project Created Successfully!**\n\n"
            f"**Name:** {project_name}\n"
            f"**ID:** `{project_id}`\n"
            f"**Status:** Synced to ClickUp\n\n"
            f"Use `/clickup` to manage your projects!",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        await update.message.reply_text(f"❌ Error creating project: {str(e)}")

async def task_add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /task_add command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(logger, user_id, username, "/task_add")
    
    # Initialize ClickUp handler
    clickup_handler = ClickUpHandler(context.bot_data.get('config', {}))
    
    if not clickup_handler.is_available():
        await update.message.reply_text("❌ ClickUp integration not available")
        return
    
    # Parse command arguments
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "❌ Usage: /task_add <project_id> <task_title>\n"
            "Example: /task_add proj_001_my_project Implement new feature"
        )
        return
    
    project_id = args[0]
    task_title = " ".join(args[1:])
    
    try:
        # Add task
        task_id = clickup_handler.manager.add_task(
            project_id=project_id,
            title=task_title,
            description=f"Task created via Telegram bot by {username}",
            priority="medium",
            sync_to_clickup=True
        )
        
        await update.message.reply_text(
            f"✅ **Task Added Successfully!**\n\n"
            f"**Title:** {task_title}\n"
            f"**ID:** `{task_id}`\n"
            f"**Project:** `{project_id}`\n"
            f"**Status:** Synced to ClickUp\n\n"
            f"Use `/clickup` to manage your tasks!",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error adding task: {e}")
        await update.message.reply_text(f"❌ Error adding task: {str(e)}")

async def upload_doc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /upload_doc command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(logger, user_id, username, "/upload_doc")
    
    # Initialize ClickUp handler
    clickup_handler = ClickUpHandler(context.bot_data.get('config', {}))
    
    if not clickup_handler.is_available():
        await update.message.reply_text("❌ ClickUp integration not available")
        return
    
    # Parse command arguments
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "❌ Usage: /upload_doc <project_id> <file_path>\n"
            "Example: /upload_doc proj_001_my_project /path/to/document.pdf"
        )
        return
    
    project_id = args[0]
    file_path = args[1]
    
    try:
        # Upload document
        success = clickup_handler.manager.upload_document(
            project_id=project_id,
            file_path=file_path,
            task_name=f"Document uploaded by {username}"
        )
        
        if success:
            await update.message.reply_text(
                f"✅ **Document Uploaded Successfully!**\n\n"
                f"**File:** {file_path}\n"
                f"**Project:** `{project_id}`\n"
                f"**Status:** Synced to ClickUp\n\n"
                f"Check your ClickUp workspace to see the uploaded document!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Failed to upload document")
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        await update.message.reply_text(f"❌ Error uploading document: {str(e)}")

async def comment_add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /comment_add command."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    log_command(logger, user_id, username, "/comment_add")
    
    # Initialize ClickUp handler
    clickup_handler = ClickUpHandler(context.bot_data.get('config', {}))
    
    if not clickup_handler.is_available():
        await update.message.reply_text("❌ ClickUp integration not available")
        return
    
    # Parse command arguments
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "❌ Usage: /comment_add <project_id> <comment_text>\n"
            "Example: /comment_add proj_001_my_project Important project update"
        )
        return
    
    project_id = args[0]
    comment_text = " ".join(args[1:])
    
    try:
        # Add comment
        success = clickup_handler.manager.add_comment(
            project_id=project_id,
            comment=comment_text,
            task_name=f"Comment from {username}"
        )
        
        if success:
            await update.message.reply_text(
                f"✅ **Comment Added Successfully!**\n\n"
                f"**Comment:** {comment_text}\n"
                f"**Project:** `{project_id}`\n"
                f"**Status:** Synced to ClickUp\n\n"
                f"Check your ClickUp workspace to see the comment!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Failed to add comment")
        
    except Exception as e:
        logger.error(f"Error adding comment: {e}")
        await update.message.reply_text(f"❌ Error adding comment: {str(e)}")
