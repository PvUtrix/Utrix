#!/bin/bash
# Start script for Personal System Telegram Bot
# This script sets up the virtual environment and runs the Telegram bot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
BOT_DIR="$PROJECT_ROOT/services/telegram-bot"

echo -e "${BLUE}🤖 Starting Personal System Telegram Bot${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Bot directory: $BOT_DIR"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    cd "$PROJECT_ROOT"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}📦 Activating virtual environment...${NC}"
source "$PROJECT_ROOT/venv/bin/activate"

# Install requirements
echo -e "${BLUE}📋 Installing/updating requirements...${NC}"
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    pip install -r "$PROJECT_ROOT/requirements.txt"
fi
if [ -f "$BOT_DIR/requirements.txt" ]; then
    pip install -r "$BOT_DIR/requirements.txt"
fi
echo -e "${GREEN}✅ Requirements installed${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/data"
mkdir -p "$PROJECT_ROOT/automation/outputs"

# Set environment variables if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${BLUE}🔧 Loading environment variables from .env...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Check for required environment variables
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo -e "${RED}❌ TELEGRAM_BOT_TOKEN environment variable is required${NC}"
    echo "Please set it in your .env file or environment"
    exit 1
fi

# Run the Telegram bot
echo -e "${GREEN}🤖 Starting Personal System Telegram Bot...${NC}"
echo -e "${BLUE}Bot will be available on Telegram${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the bot${NC}"
echo ""

cd "$BOT_DIR"
python main.py
