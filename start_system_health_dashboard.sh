#!/bin/bash
# Start script for System Health Dashboard
# This script sets up the virtual environment and runs the health dashboard

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
DASHBOARD_DIR="$PROJECT_ROOT/automation/tools/system_health_dashboard"

echo -e "${BLUE}🏥 Starting Personal System Health Dashboard${NC}"
echo "Project root: $PROJECT_ROOT"
echo "Dashboard directory: $DASHBOARD_DIR"

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

# Install dashboard-specific requirements
echo -e "${BLUE}📋 Installing dashboard dependencies...${NC}"
pip install psutil requests pyyaml

echo -e "${GREEN}✅ Requirements installed${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/automation/outputs/health_dashboard"

# Set environment variables if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${BLUE}🔧 Loading environment variables from .env...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Check for required environment variables
echo -e "${BLUE}🔍 Checking environment variables...${NC}"
MISSING_VARS=()

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    MISSING_VARS+=("TELEGRAM_BOT_TOKEN")
fi

if [ -z "$CORE_SUPABASE_URL" ]; then
    MISSING_VARS+=("CORE_SUPABASE_URL")
fi

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Missing environment variables: ${MISSING_VARS[*]}${NC}"
    echo -e "${YELLOW}   Some components may not be monitored properly${NC}"
else
    echo -e "${GREEN}✅ All required environment variables are set${NC}"
fi

# Check if dashboard script exists
if [ ! -f "$DASHBOARD_DIR/main.py" ]; then
    echo -e "${RED}❌ Dashboard script not found at $DASHBOARD_DIR/main.py${NC}"
    exit 1
fi

# Make the script executable
chmod +x "$DASHBOARD_DIR/main.py"

echo -e "${GREEN}🏥 Starting Personal System Health Dashboard...${NC}"
echo -e "${BLUE}Dashboard will show system health overview${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the dashboard${NC}"
echo ""

# Run the dashboard
cd "$PROJECT_ROOT"
python3 "$DASHBOARD_DIR/main.py" --dashboard "${@}"
