#!/bin/bash
# Master start script for Personal System
# This script lists all available start scripts and provides easy access

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${PURPLE}🚀 Personal System - Start Scripts${NC}"
echo -e "${BLUE}====================================${NC}"
echo ""

# Function to check if a script exists and is executable
check_script() {
    local script_name="$1"
    local script_path="$SCRIPT_DIR/$script_name"
    
    if [ -f "$script_path" ] && [ -x "$script_path" ]; then
        echo -e "${GREEN}✅ $script_name${NC}"
        return 0
    else
        echo -e "${RED}❌ $script_name${NC}"
        return 1
    fi
}

# Function to run a script
run_script() {
    local script_name="$1"
    local script_path="$SCRIPT_DIR/$script_name"
    
    if [ -f "$script_path" ] && [ -x "$script_path" ]; then
        echo -e "${BLUE}🚀 Running $script_name...${NC}"
        "$script_path" "${@:2}"
    else
        echo -e "${RED}❌ Script $script_name not found or not executable${NC}"
        exit 1
    fi
}

# List all available scripts
echo -e "${CYAN}📋 Available Start Scripts:${NC}"
echo ""

# Core applications
echo -e "${YELLOW}🏗️  Core Applications:${NC}"
check_script "start_main_api.sh"
check_script "start_telegram_bot.sh"
echo ""

# Projects
echo -e "${YELLOW}📁 Projects:${NC}"
check_script "start_habit_tracker.sh"
check_script "start_presentation_analyzer.sh"
echo ""

# Automation tools
echo -e "${YELLOW}🔧 Automation Tools:${NC}"
check_script "start_task_manager.sh"
check_script "start_daily_summary.sh"
check_script "start_cleanup_tool.sh"
check_script "start_code_quality_checker.sh"
check_script "start_lab_analyzer.sh"
check_script "start_reminder_system.sh"
echo ""

# Show usage information
echo -e "${CYAN}📖 Usage:${NC}"
echo "  ./start_all.sh [script_name] [arguments...]"
echo ""
echo -e "${CYAN}Examples:${NC}"
echo "  ./start_all.sh start_main_api.sh"
echo "  ./start_all.sh start_telegram_bot.sh"
echo "  ./start_all.sh start_task_manager.sh --add 'New task' --priority high"
echo "  ./start_all.sh start_daily_summary.sh"
echo ""

# If no arguments provided, show this help
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}💡 Tip: Run a specific script by providing its name as an argument${NC}"
    echo -e "${YELLOW}   Example: ./start_all.sh start_main_api.sh${NC}"
    exit 0
fi

# If script name provided, run it
if [ $# -gt 0 ]; then
    script_name="$1"
    shift  # Remove first argument (script name) from arguments
    run_script "$script_name" "$@"
fi
