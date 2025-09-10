#!/usr/bin/env python3
"""
Personal System Telegram Bot
Main entry point for the Telegram bot interface to your personal system.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from bot.bot import PersonalSystemBot
from config.config_manager import ConfigManager
from utils.logger import setup_logging
from scheduler import PersonalSystemScheduler
from health_check import HealthCheckServer


async def main():
    """Main function to run the Telegram bot."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Personal System Telegram Bot...")
        
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Validate configuration
        if not config_manager.validate_config(config):
            logger.error("Invalid configuration. Please check your config.yaml file.")
            return
        
        # Create and start the bot
        bot = PersonalSystemBot(config)
        
        # Create scheduler
        scheduler = PersonalSystemScheduler(bot, config)
        
        # Create health check server
        health_port = int(os.getenv('HEALTH_CHECK_PORT', '8000'))
        health_check = HealthCheckServer(health_port)
        
        logger.info("Bot, scheduler, and health check initialized successfully. Starting...")
        
        # Start bot, scheduler, and health check concurrently
        await asyncio.gather(
            bot.start(),
            scheduler.start(),
            health_check.start()
        )
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise


if __name__ == "__main__":
    # Create necessary directories
    directories = [
        "data/storage",
        "data/cache", 
        "data/backups",
        "data/keys",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Run the bot
    asyncio.run(main())
