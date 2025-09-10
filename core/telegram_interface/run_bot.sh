#!/bin/bash

# Personal System Telegram Bot Runner Script
# This script sets up the virtual environment and starts the bot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🤖 Personal System Telegram Bot${NC}"
echo -e "${BLUE}================================${NC}"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Python version:${NC} $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}🔧 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment found${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔌 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if required packages are installed
echo -e "${YELLOW}📦 Checking dependencies...${NC}"

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📥 Installing dependencies from requirements.txt...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ All dependencies installed${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi

# Check if config file exists
if [ ! -f "config/config.yaml" ]; then
    echo -e "${RED}❌ Configuration file not found at config/config.yaml${NC}"
    echo -e "${YELLOW}💡 Please create the configuration file first${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All dependencies are ready${NC}"

# Test bot import
echo -e "${YELLOW}🧪 Testing bot import...${NC}"
if python3 -c "from bot.bot import PersonalSystemBot; print('✅ Bot imports successfully')" 2>/dev/null; then
    echo -e "${GREEN}✅ Bot is ready to start${NC}"
else
    echo -e "${RED}❌ Bot import failed${NC}"
    echo -e "${YELLOW}💡 Check the error messages above${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 Starting Personal System Telegram Bot...${NC}"
echo -e "${BLUE}===========================================${NC}"

# Start the bot
python3 main.py
