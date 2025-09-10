"""
Logging utilities for the Personal System Telegram Bot.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_file: str = "logs/bot.log"):
    """Setup logging configuration for the bot."""
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Set specific logger levels
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)


def log_command(logger: logging.Logger, user_id: int, username: str, command: str, args: str = ""):
    """Log a command execution."""
    logger.info(f"Command executed - User: {user_id} (@{username}), Command: {command}, Args: {args}")


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log an error with context."""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_privacy_event(logger: logging.Logger, event: str, user_id: int, details: str = ""):
    """Log privacy-related events."""
    logger.info(f"Privacy Event - {event} - User: {user_id} - {details}")


def log_system_event(logger: logging.Logger, event: str, details: str = ""):
    """Log system-level events."""
    logger.info(f"System Event - {event} - {details}")
