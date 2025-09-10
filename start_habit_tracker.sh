#!/bin/bash
# Start script for Habit Tracker Flask App
# This script sets up the virtual environment and runs the habit tracker web app

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
HABIT_TRACKER_DIR="$PROJECT_ROOT/projects/habit_tracker"

echo -e "${BLUE}📊 Starting Habit Tracker Web App${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Habit tracker directory: $HABIT_TRACKER_DIR"

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
if [ -f "$HABIT_TRACKER_DIR/requirements.txt" ]; then
    pip install -r "$HABIT_TRACKER_DIR/requirements.txt"
fi
echo -e "${GREEN}✅ Requirements installed${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p "$HABIT_TRACKER_DIR/data"
mkdir -p "$HABIT_TRACKER_DIR/templates"
mkdir -p "$HABIT_TRACKER_DIR/static"

# Set environment variables if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${BLUE}🔧 Loading environment variables from .env...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Run the habit tracker Flask app
echo -e "${GREEN}📊 Starting Habit Tracker Web App...${NC}"
echo -e "${BLUE}Web app will be available at: http://localhost:5000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the app${NC}"
echo ""

cd "$HABIT_TRACKER_DIR"
python app.py
