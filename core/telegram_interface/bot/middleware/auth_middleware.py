"""
Authentication middleware for the Personal System Telegram Bot.
Handles user access control and privacy protection.
"""

import logging
from typing import List, Optional
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_privacy_event


class AuthMiddleware:
    """Middleware for handling user authentication and access control."""
    
    def __init__(self, allowed_users: List[int], admin_users: List[int]):
        self.allowed_users = allowed_users
        self.admin_users = admin_users
        self.logger = get_logger(__name__)
    
    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process update through authentication middleware."""
        
        # Skip authentication for certain update types
        if not update.effective_user:
            return
        
        user_id = update.effective_user.id
        username = update.effective_user.username or "unknown"
        
        # Log the interaction
        if update.message and update.message.text:
            command = update.message.text.split()[0] if update.message.text else ""
            log_privacy_event(
                self.logger,
                "command_attempt",
                user_id,
                f"Command: {command}, User: @{username}"
            )
        
        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            await self._handle_unauthorized_access(update, user_id, username)
            return
        
        # Add user info to context for handlers
        context.user_data['user_id'] = user_id
        context.user_data['username'] = username
        context.user_data['is_admin'] = self._is_user_admin(user_id)
        
        # Continue processing
        return True
    
    def _is_user_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to use the bot."""
        # If no allowed users specified, allow all
        if not self.allowed_users:
            return True
        
        return user_id in self.allowed_users
    
    def _is_user_admin(self, user_id: int) -> bool:
        """Check if user is an admin."""
        return user_id in self.admin_users
    
    async def _handle_unauthorized_access(self, update: Update, user_id: int, username: str):
        """Handle unauthorized access attempts."""
        log_privacy_event(
            self.logger,
            "unauthorized_access",
            user_id,
            f"User @{username} attempted to access bot"
        )
        
        if update.message:
            await update.message.reply_text(
                "🔒 Access denied. You are not authorized to use this bot.\n\n"
                "If you believe this is an error, please contact the administrator."
            )
