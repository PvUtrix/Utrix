#!/bin/bash
# Start script for Presentation Analyzer
# This script sets up the virtual environment and runs the presentation analyzer

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
PRESENTATION_ANALYZER_DIR="$PROJECT_ROOT/projects/presentation_analyzer"

echo -e "${BLUE}📊 Starting Presentation Analyzer${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Presentation analyzer directory: $PRESENTATION_ANALYZER_DIR"

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
if [ -f "$PRESENTATION_ANALYZER_DIR/requirements.txt" ]; then
    pip install -r "$PRESENTATION_ANALYZER_DIR/requirements.txt"
fi
echo -e "${GREEN}✅ Requirements installed${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p "$PRESENTATION_ANALYZER_DIR/logs"
mkdir -p "$PRESENTATION_ANALYZER_DIR/data/raw"
mkdir -p "$PRESENTATION_ANALYZER_DIR/data/processed"
mkdir -p "$PRESENTATION_ANALYZER_DIR/knowledge_base"

# Set environment variables if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${BLUE}🔧 Loading environment variables from .env...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Check for required configuration
if [ ! -f "$PRESENTATION_ANALYZER_DIR/config/settings.yaml" ]; then
    echo -e "${YELLOW}⚠️  Configuration file not found. Please configure settings.yaml${NC}"
    echo "Copy config/settings.yaml.example to config/settings.yaml and update the settings"
fi

# Run the presentation analyzer
echo -e "${GREEN}📊 Starting Presentation Analyzer...${NC}"
echo -e "${BLUE}This will analyze presentations from Google Drive${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the analyzer${NC}"
echo ""

cd "$PRESENTATION_ANALYZER_DIR"
python src/main.py
