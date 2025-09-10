#!/usr/bin/env python3
"""
Health Check Server for Personal System Telegram Bot
Provides health monitoring endpoint for Coolify deployment
"""

import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from typing import Dict, Any
import json
import psutil
from aiohttp import web, ClientSession
import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthCheckServer:
    """Health check server for monitoring bot status"""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.app = web.Application()
        self.setup_routes()
        self.start_time = datetime.now()
        self.bot_status = "unknown"
        self.last_check = None
        
    def setup_routes(self):
        """Setup HTTP routes for health checks"""
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/status', self.status_check)
        self.app.router.add_get('/metrics', self.metrics)
        self.app.router.add_get('/', self.root)
        
    async def health_check(self, request):
        """Basic health check endpoint"""
        try:
            # Check system resources
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Check if bot is running (basic check)
            bot_running = await self.check_bot_status()
            
            health_data = {
                "status": "healthy" if bot_running else "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "uptime": str(datetime.now() - self.start_time),
                "bot_status": self.bot_status,
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "disk_percent": disk.percent,
                    "memory_available": memory.available,
                    "disk_free": disk.free
                },
                "version": "1.0.0",
                "environment": os.getenv('ENVIRONMENT', 'production')
            }
            
            status_code = 200 if bot_running else 503
            return web.json_response(health_data, status=status_code)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            error_data = {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            return web.json_response(error_data, status=500)
    
    async def status_check(self, request):
        """Detailed status check endpoint"""
        try:
            status_data = {
                "timestamp": datetime.now().isoformat(),
                "uptime": str(datetime.now() - self.start_time),
                "bot_status": self.bot_status,
                "last_check": self.last_check.isoformat() if self.last_check else None,
                "environment": {
                    "python_version": sys.version,
                    "environment": os.getenv('ENVIRONMENT', 'production'),
                    "log_level": os.getenv('LOG_LEVEL', 'INFO')
                },
                "services": {
                    "health_server": "running",
                    "bot": self.bot_status,
                    "telegram_api": await self.check_telegram_api()
                }
            }
            
            return web.json_response(status_data)
            
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def metrics(self, request):
        """Metrics endpoint for monitoring"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            
            metrics_data = {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_total": memory.total,
                    "memory_available": memory.available,
                    "memory_percent": memory.percent,
                    "disk_total": disk.total,
                    "disk_free": disk.free,
                    "disk_percent": disk.percent
                },
                "process": {
                    "pid": process.pid,
                    "memory_rss": process_memory.rss,
                    "memory_vms": process_memory.vms,
                    "cpu_percent": process.cpu_percent(),
                    "num_threads": process.num_threads(),
                    "create_time": process.create_time()
                },
                "bot": {
                    "status": self.bot_status,
                    "uptime": str(datetime.now() - self.start_time)
                }
            }
            
            return web.json_response(metrics_data)
            
        except Exception as e:
            logger.error(f"Metrics collection failed: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def root(self, request):
        """Root endpoint with basic info"""
        info_data = {
            "service": "Personal System Telegram Bot Health Check",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "status": "/status", 
                "metrics": "/metrics"
            },
            "timestamp": datetime.now().isoformat()
        }
        return web.json_response(info_data)
    
    async def check_bot_status(self) -> bool:
        """Check if the bot is running properly"""
        try:
            # Check if bot process is running
            # This is a simple check - in production you might want more sophisticated monitoring
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if not bot_token:
                self.bot_status = "no_token"
                return False
                
            # Check if we can import the bot module
            try:
                import sys
                sys.path.append('/app')
                from bot.bot import PersonalSystemBot
                self.bot_status = "imported"
                return True
            except ImportError as e:
                self.bot_status = f"import_error: {str(e)}"
                return False
                
        except Exception as e:
            self.bot_status = f"error: {str(e)}"
            return False
    
    async def check_telegram_api(self) -> str:
        """Check Telegram API connectivity"""
        try:
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if not bot_token:
                return "no_token"
                
            # Simple API check
            async with ClientSession() as session:
                url = f"https://api.telegram.org/bot{bot_token}/getMe"
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        return "connected"
                    else:
                        return f"error_{response.status}"
        except Exception as e:
            return f"error: {str(e)}"
    
    async def start(self):
        """Start the health check server"""
        try:
            logger.info(f"Starting health check server on port {self.port}")
            runner = web.AppRunner(self.app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', self.port)
            await site.start()
            logger.info(f"Health check server started successfully on port {self.port}")
            
            # Keep the server running
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Failed to start health check server: {e}")
            raise

async def main():
    """Main function to run the health check server"""
    port = int(os.getenv('HEALTH_CHECK_PORT', 8000))
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the health check server
    server = HealthCheckServer(port)
    await server.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Health check server stopped by user")
    except Exception as e:
        logger.error(f"Health check server error: {e}")
        sys.exit(1)