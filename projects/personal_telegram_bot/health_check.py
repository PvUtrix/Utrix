#!/usr/bin/env python3
"""
Health check endpoint for the Personal System Telegram Bot.
Provides a simple HTTP endpoint for monitoring and health checks.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from utils.logger import get_logger

logger = get_logger(__name__)


class HealthCheck:
    """Simple health check server for monitoring."""
    
    def __init__(self, port: int = 8001):
        self.port = port
        self.start_time = datetime.now()
    
    async def handle_health_check(self, reader, writer):
        """Handle health check requests."""
        try:
            # Read request
            request = await reader.read(1024)
            request_line = request.decode().split('\n')[0]
            
            # Parse request
            method, path, _ = request_line.split(' ')
            
            if method == 'GET' and path == '/health':
                # Health check response
                response = f"""HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: {len(self._get_health_data())}

{self._get_health_data()}"""
                
                writer.write(response.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                
                logger.info("Health check request handled successfully")
            else:
                # 404 for other requests
                response = """HTTP/1.1 404 Not Found
Content-Type: text/plain
Content-Length: 13

Not Found"""
                
                writer.write(response.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                
        except Exception as e:
            logger.error(f"Error handling health check: {e}")
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass
    
    def _get_health_data(self) -> str:
        """Get health check data."""
        import json
        
        health_data = {
            "status": "healthy",
            "service": "personal-telegram-bot",
            "timestamp": datetime.now().isoformat(),
            "uptime": str(datetime.now() - self.start_time),
            "version": "1.0.0"
        }
        
        return json.dumps(health_data, indent=2)
    
    async def start(self):
        """Start the health check server."""
        try:
            server = await asyncio.start_server(
                self.handle_health_check,
                '0.0.0.0',
                self.port
            )
            
            logger.info(f"Health check server started on port {self.port}")
            
            async with server:
                await server.serve_forever()
                
        except Exception as e:
            logger.error(f"Error starting health check server: {e}")
            raise


async def main():
    """Main function for health check server."""
    try:
        port = int(os.getenv('HEALTH_CHECK_PORT', '8000'))
        health_check = HealthCheck(port)
        await health_check.start()
    except Exception as e:
        logger.error(f"Health check server failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
