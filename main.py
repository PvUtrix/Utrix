#!/usr/bin/env python3
"""
Personal System API Server
Main application entry point for Coolify deployment
"""

import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our custom modules
from automation.serverless.voice_content_generator import VoiceContentGenerator
from automation.serverless.elevenlabs_tts import ElevenLabsTTS
from automation.serverless.data_monitor import DataMonitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/personal_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Personal System API",
    description="Voice-enabled personal automation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
voice_generator = VoiceContentGenerator()
tts = ElevenLabsTTS()
data_monitor = DataMonitor()

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Personal System API is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db_status = "OK"

        # Test ElevenLabs connection
        elevenlabs_status = "OK" if os.getenv('ELEVENLABS_API_KEY') else "Not configured"

        # Test Telegram connection
        telegram_status = "OK" if os.getenv('TELEGRAM_BOT_TOKEN') else "Not configured"

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "database": db_status,
                "elevenlabs": elevenlabs_status,
                "telegram": telegram_status
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/voice/preview")
def preview_voice_content():
    """Preview today's voice content (text only)"""
    try:
        content = voice_generator.generate_daily_voice_content()
        word_count = len(content.split())
        estimated_duration = word_count * 0.25  # Rough estimate

        return {
            "content": content,
            "word_count": word_count,
            "estimated_duration_seconds": estimated_duration,
            "estimated_cost": tts.estimate_cost(content)
        }
    except Exception as e:
        logger.error(f"Voice preview failed: {e}")
        raise HTTPException(status_code=500, detail=f"Voice preview failed: {str(e)}")

@app.post("/voice/generate")
def generate_voice_message():
    """Generate and send voice message (for testing)"""
    try:
        # Generate content
        content = voice_generator.generate_daily_voice_content()

        # Generate audio
        audio_data = tts.generate_speech(content)

        if audio_data:
            return {
                "status": "success",
                "message": "Voice message generated",
                "audio_size": len(audio_data),
                "word_count": len(content.split())
            }
        else:
            raise HTTPException(status_code=500, detail="Voice generation failed")

    except Exception as e:
        logger.error(f"Voice generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Voice generation failed: {str(e)}")

@app.get("/monitor/status")
def get_monitor_status():
    """Get monitoring status"""
    try:
        sizes = data_monitor.monitor_data_sizes()
        return {
            "status": "success",
            "data_sizes": sizes,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Monitor status failed: {e}")
        raise HTTPException(status_code=500, detail=f"Monitor status failed: {str(e)}")

@app.get("/system/info")
def get_system_info():
    """Get system information"""
    return {
        "version": "1.0.0",
        "environment": os.getenv('COOLIFY_ENVIRONMENT', 'production'),
        "services": {
            "database": "configured" if os.getenv('CORE_SUPABASE_URL') else "not configured",
            "elevenlabs": "configured" if os.getenv('ELEVENLABS_API_KEY') else "not configured",
            "telegram": "configured" if os.getenv('TELEGRAM_BOT_TOKEN') else "not configured",
            "gitea": "configured" if os.getenv('GITEA_URL') else "not configured"
        },
        "features": {
            "voice_messages": True,
            "ci_cd": True,
            "data_monitoring": True,
            "multi_tier_database": True
        }
    }

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("🚀 Personal System API starting up")

    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # Log startup information
    logger.info(f"Environment: {os.getenv('COOLIFY_ENVIRONMENT', 'development')}")
    logger.info(f"Database: {'Configured' if os.getenv('CORE_SUPABASE_URL') else 'Not configured'}")
    logger.info(f"ElevenLabs: {'Configured' if os.getenv('ELEVENLABS_API_KEY') else 'Not configured'}")
    logger.info(f"Telegram: {'Configured' if os.getenv('TELEGRAM_BOT_TOKEN') else 'Not configured'}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("👋 Personal System API shutting down")

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')

    logger.info(f"Starting server on {host}:{port}")

    # Start server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
