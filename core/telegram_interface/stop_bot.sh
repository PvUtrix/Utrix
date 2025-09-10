#!/bin/bash

# Personal System Telegram Bot Stop Script
# This script stops the running bot process

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 Stopping Personal System Telegram Bot${NC}"
echo -e "${BLUE}=====================================${NC}"

# Find and kill the bot process
BOT_PID=$(ps aux | grep "python3 main.py" | grep -v grep | awk '{print $2}')

if [ -z "$BOT_PID" ]; then
    echo -e "${YELLOW}⚠️  No bot process found running${NC}"
else
    echo -e "${YELLOW}🔍 Found bot process with PID: $BOT_PID${NC}"
    kill "$BOT_PID"
    
    # Wait a moment and check if it's still running
    sleep 2
    if ps -p "$BOT_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Process still running, force killing...${NC}"
        kill -9 "$BOT_PID"
    fi
    
    echo -e "${GREEN}✅ Bot stopped successfully${NC}"
fi

echo -e "${BLUE}=====================================${NC}"
