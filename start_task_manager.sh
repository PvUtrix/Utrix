#!/bin/bash
# Start script for Task Manager Tool
# This script sets up the virtual environment and runs the task manager

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
TASK_MANAGER_DIR="$PROJECT_ROOT/automation/tools/task_manager"

echo -e "${BLUE}📋 Starting Task Manager Tool${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Task manager directory: $TASK_MANAGER_DIR"

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

# Install requirements (with error handling)
echo -e "${BLUE}📋 Installing/updating requirements...${NC}"
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    if pip install --timeout 30 -r "$PROJECT_ROOT/requirements.txt" 2>/dev/null; then
        echo -e "${GREEN}✅ Main requirements installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Failed to install main requirements (network issue?)${NC}"
    fi
fi
if [ -f "$PROJECT_ROOT/automation/requirements.txt" ]; then
    if pip install --timeout 30 -r "$PROJECT_ROOT/automation/requirements.txt" 2>/dev/null; then
        echo -e "${GREEN}✅ Automation requirements installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Failed to install automation requirements (network issue?)${NC}"
    fi
fi

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p "$PROJECT_ROOT/automation/outputs"

# Set environment variables if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${BLUE}🔧 Loading environment variables from .env...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Show usage information
echo -e "${GREEN}📋 Task Manager Tool Ready${NC}"
echo -e "${BLUE}Usage examples:${NC}"
echo "  ./start_task_manager.sh --add 'Fix bug in authentication' --priority high"
echo "  ./start_task_manager.sh --list"
echo "  ./start_task_manager.sh --complete task_001"
echo "  ./start_task_manager.sh --report"
echo ""

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}No arguments provided. Showing task summary...${NC}"
    cd "$TASK_MANAGER_DIR"
    python main.py
else
    echo -e "${BLUE}Running task manager with arguments: $@${NC}"
    cd "$TASK_MANAGER_DIR"
    python main.py "$@"
fi
