#!/bin/bash
# Start script for Lab Analyzer Tool
# This script sets up the virtual environment and runs the lab analyzer

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
LAB_ANALYZER_DIR="$PROJECT_ROOT/automation/tools/lab_analyzer"

echo -e "${BLUE}🧪 Starting Lab Analyzer Tool${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Lab analyzer directory: $LAB_ANALYZER_DIR"

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
echo -e "${GREEN}🧪 Lab Analyzer Tool Ready${NC}"
echo -e "${BLUE}This tool will analyze lab results and health data${NC}"
echo ""

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}No arguments provided. Running lab analyzer with default settings...${NC}"
    cd "$LAB_ANALYZER_DIR"
    python main.py
else
    echo -e "${BLUE}Running lab analyzer with arguments: $@${NC}"
    cd "$LAB_ANALYZER_DIR"
    python main.py "$@"
fi
