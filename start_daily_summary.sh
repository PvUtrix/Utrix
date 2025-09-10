#!/bin/bash
# Start script for Daily Summary Generator
# This script sets up the virtual environment and runs the daily summary generator

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
DAILY_SUMMARY_SCRIPT="$PROJECT_ROOT/automation/scripts/daily_operations/daily_summary.py"

echo -e "${BLUE}📊 Starting Daily Summary Generator${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Daily summary script: $DAILY_SUMMARY_SCRIPT"

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
mkdir -p "$PROJECT_ROOT/automation/outputs/daily_summaries"
mkdir -p "$PROJECT_ROOT/logs"

# Set environment variables if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${BLUE}🔧 Loading environment variables from .env...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Run the daily summary generator
echo -e "${GREEN}📊 Starting Daily Summary Generator...${NC}"
echo -e "${BLUE}This will generate your daily summary with reflections${NC}"
echo -e "${YELLOW}Press Ctrl+C to cancel${NC}"
echo ""

cd "$PROJECT_ROOT"
python "$DAILY_SUMMARY_SCRIPT"
