#!/bin/bash

# Personal System Telegram Bot - Coolify Deployment Script
# This script prepares and deploys the Telegram bot to Coolify

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOT_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$(dirname "$BOT_DIR")")"

echo -e "${BLUE}🚀 Personal System Telegram Bot - Coolify Deployment${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory structure
check_directory() {
    print_info "Checking directory structure..."
    
    if [ ! -f "$BOT_DIR/main.py" ]; then
        print_error "main.py not found in $BOT_DIR"
        print_error "Please run this script from the coolify-deployment directory"
        exit 1
    fi
    
    if [ ! -f "$BOT_DIR/requirements.txt" ]; then
        print_error "requirements.txt not found in $BOT_DIR"
        exit 1
    fi
    
    print_status "Directory structure verified"
}

# Create necessary files
create_deployment_files() {
    print_info "Creating deployment files..."
    
    # Copy Dockerfile to bot directory if it doesn't exist
    if [ ! -f "$BOT_DIR/Dockerfile" ]; then
        cp "$SCRIPT_DIR/Dockerfile" "$BOT_DIR/"
        print_status "Dockerfile created"
    else
        print_warning "Dockerfile already exists, skipping"
    fi
    
    # Copy docker-compose.yml to bot directory if it doesn't exist
    if [ ! -f "$BOT_DIR/docker-compose.yml" ]; then
        cp "$SCRIPT_DIR/docker-compose.yml" "$BOT_DIR/"
        print_status "docker-compose.yml created"
    else
        print_warning "docker-compose.yml already exists, skipping"
    fi
    
    # Create .env file from template if it doesn't exist
    if [ ! -f "$BOT_DIR/.env" ]; then
        if [ -f "$SCRIPT_DIR/env.example" ]; then
            cp "$SCRIPT_DIR/env.example" "$BOT_DIR/.env"
            print_status ".env file created from template"
            print_warning "Please edit .env file with your actual values!"
        else
            print_warning "env.example not found, creating basic .env file"
            cat > "$BOT_DIR/.env" << EOF
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_USER_ID=your_user_id_here

# Optional API Keys
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# System Configuration
HEALTH_CHECK_PORT=8000
EOF
        fi
    else
        print_warning ".env file already exists, skipping"
    fi
}

# Validate configuration
validate_config() {
    print_info "Validating configuration..."
    
    # Check if .env file exists and has required values
    if [ -f "$BOT_DIR/.env" ]; then
        source "$BOT_DIR/.env"
        
        if [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ] || [ -z "$TELEGRAM_BOT_TOKEN" ]; then
            print_error "TELEGRAM_BOT_TOKEN not set in .env file"
            print_info "Please edit .env file with your actual bot token"
            exit 1
        fi
        
        if [ "$TELEGRAM_USER_ID" = "your_user_id_here" ] || [ -z "$TELEGRAM_USER_ID" ]; then
            print_error "TELEGRAM_USER_ID not set in .env file"
            print_info "Please edit .env file with your actual user ID"
            exit 1
        fi
        
        print_status "Configuration validated"
    else
        print_error ".env file not found"
        exit 1
    fi
}

# Check Git status and commit changes
handle_git() {
    print_info "Checking Git status..."
    
    cd "$PROJECT_ROOT"
    
    # Check if we're in a git repository
    if [ ! -d ".git" ]; then
        print_warning "Not in a Git repository, initializing..."
        git init
        git add .
        git commit -m "Initial commit: Personal System with Telegram Bot"
        print_status "Git repository initialized"
    else
        # Check for uncommitted changes
        if [ -n "$(git status --porcelain)" ]; then
            print_info "Uncommitted changes found, committing them..."
            git add .
            git commit -m "🚀 Prepare Telegram Bot for Coolify deployment"
            print_status "Changes committed"
        else
            print_status "No uncommitted changes"
        fi
    fi
}

# Display deployment instructions
show_deployment_instructions() {
    echo ""
    echo -e "${PURPLE}🎯 Coolify Deployment Instructions${NC}"
    echo -e "${PURPLE}===================================${NC}"
    echo ""
    echo -e "${BLUE}1. Repository Setup:${NC}"
    echo "   - Push your repository to Git (GitHub, GitLab, or Gitea)"
    echo "   - Repository URL: $(git remote get-url origin 2>/dev/null || echo 'Not set - please add remote')"
    echo ""
    echo -e "${BLUE}2. Coolify Configuration:${NC}"
    echo "   - Log into your Coolify dashboard"
    echo "   - Create new application"
    echo "   - Choose 'Docker Compose' or 'Dockerfile'"
    echo "   - Set repository URL and branch (main)"
    echo "   - Set build path to: core/telegram_interface"
    echo ""
    echo -e "${BLUE}3. Environment Variables:${NC}"
    echo "   Add these in Coolify environment variables:"
    echo "   - TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_USER_ID=$TELEGRAM_USER_ID"
    if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your_openai_key_here" ]; then
        echo "   - OPENAI_API_KEY=$OPENAI_API_KEY"
    fi
    if [ -n "$ELEVENLABS_API_KEY" ] && [ "$ELEVENLABS_API_KEY" != "your_elevenlabs_key_here" ]; then
        echo "   - ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY"
    fi
    echo "   - HEALTH_CHECK_PORT=8000"
    echo ""
    echo -e "${BLUE}4. Build Configuration:${NC}"
    echo "   - Port: 8000"
    echo "   - Health Check: http://localhost:8000/health"
    echo "   - Volume Mounts:"
    echo "     * /app/data -> ./data"
    echo "     * /app/logs -> ./logs"
    echo "     * /app/config -> ./config"
    echo ""
    echo -e "${BLUE}5. Deploy:${NC}"
    echo "   - Click 'Deploy' in Coolify"
    echo "   - Monitor build logs"
    echo "   - Test bot functionality"
    echo ""
    echo -e "${GREEN}🎉 Your Telegram Bot is ready for Coolify deployment!${NC}"
}

# Main execution
main() {
    check_directory
    create_deployment_files
    validate_config
    handle_git
    show_deployment_instructions
}

# Run main function
main "$@"
