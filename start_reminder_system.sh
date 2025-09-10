#!/bin/bash
# Start script for Reminder System
# This script sets up the virtual environment and runs the reminder system

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
REMINDER_SYSTEM_DIR="$PROJECT_ROOT/automation/tools/reminder_system"

echo -e "${BLUE}⏰ Starting Reminder System${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Reminder system directory: $REMINDER_SYSTEM_DIR"

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
if [ -f "$PROJECT_ROOT/automation/requirements.txt" ]; then
    pip install -r "$PROJECT_ROOT/automation/requirements.txt"
fi
echo -e "${GREEN}✅ Requirements installed${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p "$PROJECT_ROOT/logs"

# Set environment variables if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${BLUE}🔧 Loading environment variables from .env...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Show usage information
echo -e "${GREEN}⏰ Reminder System Ready${NC}"
echo -e "${BLUE}This system will manage your reminders and notifications${NC}"
echo ""

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}No arguments provided. Running reminder system with default settings...${NC}"
    cd "$REMINDER_SYSTEM_DIR"
    python main.py
else
    echo -e "${BLUE}Running reminder system with arguments: $@${NC}"
    cd "$REMINDER_SYSTEM_DIR"
    python main.py "$@"
fi
