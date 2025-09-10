"""
Automation script integration handlers for the Personal System Telegram Bot.
Handles execution of automation scripts and integration with the personal system.
"""

import logging
import subprocess
import json
import os
from typing import Dict, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command


class AutomationScriptExecutor:
    """Execute automation scripts from the personal system."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(__name__)
        self.scripts_path = config.get('paths', {}).get('automation_scripts', '../../../automation/scripts/')
        
        # Map actions to script commands
        self.script_mappings = {
            # Daily Operations - Health
            "log_health": {
                "script": "daily_operations/health/health_logger_interactive.py",
                "args": [],
                "description": "Log health metrics"
            },
            "health_stats": {
                "script": "daily_operations/health/health_logger_interactive.py",
                "args": ["today"],
                "description": "Get today's health statistics"
            },
            
            # Daily Operations - Learning
            "log_learning": {
                "script": "daily_operations/learning/learning_tracker_interactive.py",
                "args": [],
                "description": "Log learning activity"
            },
            
            # Daily Operations - Tasks
            "add_task": {
                "script": "daily_operations/tasks/task_manager_interactive.py",
                "args": [],
                "description": "Add a new task"
            },
            "view_tasks": {
                "script": "daily_operations/tasks/task_manager_interactive.py",
                "args": ["list"],
                "description": "View tasks"
            },
            
            # Daily Operations - Morning Routine
            "morning_routine": {
                "script": "daily_operations/routines/morning_routine_interactive.py",
                "args": [],
                "description": "Generate morning routine"
            },
            
            # Daily Operations - Quick Notes
            "quick_note": {
                "script": "daily_operations/notes/quick_note_interactive.py",
                "args": [],
                "description": "Capture a quick note"
            },
            
            # Daily Operations - Daily Summary
            "daily_summary": {
                "script": "daily_operations/daily_summary_simple.py",
                "args": [],
                "description": "Generate daily summary"
            },
            
            # Shadow Work Tracker
            "shadow_checkin": {
                "script": "shadow_work/shadow_work_tracker.py",
                "args": ["--action", "checkin"],
                "description": "Daily shadow work check-in"
            },
            "shadow_log": {
                "script": "shadow_work/shadow_work_tracker.py", 
                "args": ["--action", "insight"],
                "description": "Log shadow work insight"
            },
            "shadow_prompt": {
                "script": "shadow_work/shadow_work_tracker.py",
                "args": ["--action", "explore"],
                "description": "Get shadow work prompt"
            },
            "shadow_report": {
                "script": "shadow_work/shadow_work_tracker.py",
                "args": ["--action", "report"],
                "description": "Generate shadow work report"
            },
            "shadow_reminders": {
                "script": "shadow_work/shadow_work_tracker.py",
                "args": ["--action", "reminders"],
                "description": "Get shadow work reminders"
            },
            "shadow_focus": {
                "script": "shadow_work/shadow_work_tracker.py",
                "args": ["--action", "focus"],
                "description": "Set shadow work focus"
            },
            
            # Opportunity Manager
            "create_opportunity": {
                "script": "opportunities/opportunity_manager.py",
                "args": ["create"],
                "description": "Create new opportunity"
            },
            "list_opportunities": {
                "script": "opportunities/opportunity_manager.py",
                "args": ["list"],
                "description": "List all opportunities"
            },
            "evaluate_opportunity": {
                "script": "opportunities/opportunity_manager.py",
                "args": ["evaluate"],
                "description": "Evaluate opportunity"
            },
            "check_deadlines": {
                "script": "opportunities/opportunity_manager.py",
                "args": ["deadlines"],
                "description": "Check upcoming deadlines"
            },
            "archive_opportunity": {
                "script": "opportunities/opportunity_manager.py",
                "args": ["archive"],
                "description": "Archive opportunity"
            },
            
            # Business Opportunity Manager
            "create_business_opportunity": {
                "script": "opportunities/business_opportunity_manager.py",
                "args": ["create"],
                "description": "Create new business opportunity"
            },
            "list_business_opportunities": {
                "script": "opportunities/business_opportunity_manager.py",
                "args": ["list"],
                "description": "List all business opportunities"
            },
            
            # Prosperity Course
            "prosperity_course": {
                "script": "system_management/prosperity-course-manager.py",
                "args": ["status"],
                "description": "Check prosperity course status"
            },
            
            # System Management
            "create_backup": {
                "script": "system_management/create_backup.py",
                "args": [],
                "description": "Create system backup"
            },
            "gdrive_sync": {
                "script": "system_management/google_drive_sync.py",
                "args": ["--sync"],
                "description": "Sync with Google Drive"
            }
        }
    
    async def execute_action(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute automation script for given action."""
        if action not in self.script_mappings:
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "output": ""
            }
        
        script_config = self.script_mappings[action]
        script_path = os.path.join(self.scripts_path, script_config["script"])
        
        if not os.path.exists(script_path):
            return {
                "success": False,
                "error": f"Script not found: {script_path}",
                "output": ""
            }
        
        try:
            # Build command with absolute path
            abs_script_path = os.path.abspath(script_path)
            cmd = ["python3", abs_script_path] + script_config["args"]
            
            # Add parameters if provided
            if params:
                cmd = self._add_parameters(cmd, action, params)
            
            self.logger.info(f"Executing command: {' '.join(cmd)}")
            
            # Execute script from the telegram_interface directory
            telegram_interface_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=telegram_interface_dir,
                timeout=60  # 60 second timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Script execution timed out",
                "output": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}",
                "output": ""
            }
    
    def _add_parameters(self, cmd: list, action: str, params: Dict[str, Any]) -> list:
        """Add parameters to command based on action type."""
        if action == "log_health" and "metric" in params and "value" in params:
            # Health logging: metric type and value
            cmd.extend([params["metric"], params["value"]])
            if "notes" in params:
                cmd.append(params["notes"])
        
        elif action == "log_learning" and "activity" in params and "duration" in params:
            # Learning logging: activity type and duration
            cmd.extend([params["activity"], params["duration"]])
            if "description" in params:
                cmd.append(params["description"])
            if "course" in params:
                cmd.append(params["course"])
            if "skill" in params:
                cmd.append(params["skill"])
            if "notes" in params:
                cmd.append(params["notes"])
        
        elif action == "add_task" and "title" in params:
            # Task creation: title and optional fields
            cmd.append(params["title"])
            if "description" in params:
                cmd.append(params["description"])
            if "priority" in params:
                cmd.append(params["priority"])
            if "due_date" in params:
                cmd.append(params["due_date"])
            if "category" in params:
                cmd.append(params["category"])
        
        elif action == "quick_note" and "content" in params:
            # Quick note: content and optional fields
            cmd.append(params["content"])
            if "category" in params:
                cmd.append(params["category"])
            if "tags" in params:
                cmd.append(",".join(params["tags"]))
            if "priority" in params:
                cmd.append(params["priority"])
        
        elif action == "create_opportunity" and "description" in params:
            # Extract name, type, and source from description
            description = params["description"]
            parts = description.split(" at ", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                source = parts[1].strip()
                cmd.extend([name, "Job", source])
            else:
                cmd.extend([description, "General", "Voice Command"])
        
        elif action == "create_business_opportunity" and "description" in params:
            description = params["description"]
            cmd.extend([description, "Business", "Voice Command"])
        
        elif action == "shadow_log" and "insight" in params:
            cmd.extend(["--insight", params["insight"]])
        
        elif action == "shadow_focus" and "shadow_aspect" in params:
            cmd.extend(["--shadow-aspect", params["shadow_aspect"]])
        
        elif action == "evaluate_opportunity" and "opportunity_id" in params:
            cmd.extend([params["opportunity_id"]])
        
        elif action == "archive_opportunity" and "opportunity_id" in params:
            cmd.extend([params["opportunity_id"], "Completed"])
        
        return cmd
    
    def get_available_actions(self) -> Dict[str, str]:
        """Get list of available actions and their descriptions."""
        return {action: config["description"] for action, config in self.script_mappings.items()}


class AutomationHandler:
    """Handle automation script execution through Telegram interface."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(__name__)
        self.executor = AutomationScriptExecutor(config)
    
    async def handle_action_execution(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                    action: str, params: Dict[str, Any] = None):
        """Handle execution of automation actions."""
        user_id = context.user_data.get('user_id')
        username = context.user_data.get('username', 'unknown')
        
        log_command(self.logger, user_id, username, f"execute_{action}")
        
        # Show processing message
        processing_msg = await update.callback_query.edit_message_text(
            f"🔄 Executing: {action}\n\nPlease wait...",
            parse_mode='Markdown'
        )
        
        try:
            # Execute the action
            result = await self.executor.execute_action(action, params)
            
            if result["success"]:
                # Success message
                success_text = f"✅ **Action Completed Successfully**\n\n"
                success_text += f"**Action:** {action}\n\n"
                
                if result["output"]:
                    # Truncate long output
                    output = result["output"]
                    if len(output) > 1000:
                        output = output[:1000] + "\n\n... (truncated)"
                    success_text += f"**Output:**\n```\n{output}\n```"
                
                await processing_msg.edit_text(success_text, parse_mode='Markdown')
            
            else:
                # Error message
                error_text = f"❌ **Action Failed**\n\n"
                error_text += f"**Action:** {action}\n"
                error_text += f"**Error:** {result['error']}\n\n"
                
                if result["output"]:
                    error_text += f"**Output:**\n```\n{result['output']}\n```"
                
                await processing_msg.edit_text(error_text, parse_mode='Markdown')
        
        except Exception as e:
            self.logger.error(f"Error executing action {action}: {e}")
            await processing_msg.edit_text(
                f"❌ **Unexpected Error**\n\nError executing {action}: {str(e)}",
                parse_mode='Markdown'
            )
    
    async def handle_voice_confirmation(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                      action: str, params: Dict[str, Any]):
        """Handle confirmation of voice commands."""
        user_id = context.user_data.get('user_id')
        username = context.user_data.get('username', 'unknown')
        
        log_command(self.logger, user_id, username, f"confirm_voice_{action}")
        
        # Show processing message
        processing_msg = await update.callback_query.edit_message_text(
            f"🔄 Executing voice command: {action}\n\nPlease wait...",
            parse_mode='Markdown'
        )
        
        try:
            # Execute the action
            result = await self.executor.execute_action(action, params)
            
            if result["success"]:
                # Success message
                success_text = f"✅ **Voice Command Executed**\n\n"
                success_text += f"**Action:** {action}\n\n"
                
                if params:
                    success_text += "**Parameters:**\n"
                    for key, value in params.items():
                        success_text += f"• {key.title()}: {value}\n"
                    success_text += "\n"
                
                if result["output"]:
                    # Truncate long output
                    output = result["output"]
                    if len(output) > 1000:
                        output = output[:1000] + "\n\n... (truncated)"
                    success_text += f"**Result:**\n```\n{output}\n```"
                
                await processing_msg.edit_text(success_text, parse_mode='Markdown')
            
            else:
                # Error message
                error_text = f"❌ **Voice Command Failed**\n\n"
                error_text += f"**Action:** {action}\n"
                error_text += f"**Error:** {result['error']}\n\n"
                
                if result["output"]:
                    error_text += f"**Output:**\n```\n{result['output']}\n```"
                
                await processing_msg.edit_text(error_text, parse_mode='Markdown')
        
        except Exception as e:
            self.logger.error(f"Error executing voice command {action}: {e}")
            await processing_msg.edit_text(
                f"❌ **Unexpected Error**\n\nError executing voice command {action}: {str(e)}",
                parse_mode='Markdown'
            )
    
    async def show_script_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show status of available automation scripts."""
        user_id = context.user_data.get('user_id')
        username = context.user_data.get('username', 'unknown')
        
        log_command(self.logger, user_id, username, "script_status")
        
        available_actions = self.executor.get_available_actions()
        
        status_text = "🔧 **Available Automation Scripts**\n\n"
        
        # Group by category
        categories = {
            "Daily Operations": [action for action in available_actions.keys() if action in [
                "daily_summary", "morning_routine", "log_health", "health_stats", 
                "log_learning", "add_task", "view_tasks", "quick_note"
            ]],
            "Shadow Work": [action for action in available_actions.keys() if action.startswith("shadow_")],
            "Opportunities": [action for action in available_actions.keys() if "opportunity" in action],
            "System Management": ["create_backup", "gdrive_sync", "prosperity_course"]
        }
        
        for category, actions in categories.items():
            if actions:
                status_text += f"**{category}:**\n"
                for action in actions:
                    if action in available_actions:
                        status_text += f"• {available_actions[action]}\n"
                status_text += "\n"
        
        await update.message.reply_text(status_text, parse_mode='Markdown')


# Global automation handler instance
automation_handler = None

def initialize_automation_handler(config: Dict[str, Any]):
    """Initialize the automation handler with config."""
    global automation_handler
    automation_handler = AutomationHandler(config)


async def handle_action_execution(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                action: str, params: Dict[str, Any] = None):
    """Handle execution of automation actions."""
    if automation_handler:
        await automation_handler.handle_action_execution(update, context, action, params)
    else:
        await update.callback_query.edit_message_text(
            "❌ Automation handler not initialized. Please restart the bot.",
            parse_mode='Markdown'
        )


async def execute_script(action: str, params: dict = None) -> Dict[str, Any]:
    """Execute a script directly and return the result."""
    if automation_handler:
        return await automation_handler.executor.execute_action(action, params or {})
    else:
        return {
            "success": False,
            "error": "Automation handler not initialized",
            "output": ""
        }


async def handle_voice_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                  action: str, params: Dict[str, Any]):
    """Handle confirmation of voice commands."""
    if automation_handler:
        await automation_handler.handle_voice_confirmation(update, context, action, params)
    else:
        await update.callback_query.edit_message_text(
            "❌ Automation handler not initialized. Please restart the bot.",
            parse_mode='Markdown'
        )


async def show_script_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show status of available automation scripts."""
    if automation_handler:
        await automation_handler.show_script_status(update, context)
    else:
        await update.message.reply_text(
            "❌ Automation handler not initialized. Please restart the bot.",
            parse_mode='Markdown'
        )
