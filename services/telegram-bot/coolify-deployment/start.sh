#!/bin/bash

# Personal System Telegram Bot - Coolify Startup Script
# This script starts both the bot and health check server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Personal System Telegram Bot${NC}"
echo -e "${BLUE}=====================================${NC}"

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

# Check required environment variables
check_environment() {
    print_info "Checking environment variables..."
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        print_error "TELEGRAM_BOT_TOKEN environment variable is required"
        exit 1
    fi
    
    if [ -z "$TELEGRAM_USER_ID" ]; then
        print_error "TELEGRAM_USER_ID environment variable is required"
        exit 1
    fi
    
    print_status "Environment variables validated"
}

# Create necessary directories
create_directories() {
    print_info "Creating necessary directories..."
    
    mkdir -p /app/data/storage
    mkdir -p /app/data/cache
    mkdir -p /app/data/backups
    mkdir -p /app/data/keys
    mkdir -p /app/logs
    mkdir -p /app/config
    
    # Set proper permissions
    chmod -R 755 /app/data
    chmod -R 755 /app/logs
    chmod -R 755 /app/config
    
    print_status "Directories created and permissions set"
}

# Start health check server in background
start_health_server() {
    print_info "Starting health check server..."
    
    # Start health check server in background
    python health_check.py &
    HEALTH_PID=$!
    
    # Wait a moment for the server to start
    sleep 2
    
    # Check if health server is running
    if kill -0 $HEALTH_PID 2>/dev/null; then
        print_status "Health check server started (PID: $HEALTH_PID)"
    else
        print_error "Failed to start health check server"
        exit 1
    fi
}

# Start the main bot
start_bot() {
    print_info "Starting Telegram bot..."
    
    # Start the main bot
    python main.py &
    BOT_PID=$!
    
    # Wait a moment for the bot to start
    sleep 3
    
    # Check if bot is running
    if kill -0 $BOT_PID 2>/dev/null; then
        print_status "Telegram bot started (PID: $BOT_PID)"
    else
        print_error "Failed to start Telegram bot"
        exit 1
    fi
}

# Setup signal handlers for graceful shutdown
setup_signal_handlers() {
    print_info "Setting up signal handlers..."
    
    cleanup() {
        print_info "Shutting down services..."
        
        if [ ! -z "$BOT_PID" ]; then
            print_info "Stopping Telegram bot (PID: $BOT_PID)..."
            kill -TERM $BOT_PID 2>/dev/null || true
        fi
        
        if [ ! -z "$HEALTH_PID" ]; then
            print_info "Stopping health check server (PID: $HEALTH_PID)..."
            kill -TERM $HEALTH_PID 2>/dev/null || true
        fi
        
        # Wait for processes to terminate
        sleep 2
        
        # Force kill if still running
        if [ ! -z "$BOT_PID" ] && kill -0 $BOT_PID 2>/dev/null; then
            print_warning "Force killing Telegram bot..."
            kill -KILL $BOT_PID 2>/dev/null || true
        fi
        
        if [ ! -z "$HEALTH_PID" ] && kill -0 $HEALTH_PID 2>/dev/null; then
            print_warning "Force killing health check server..."
            kill -KILL $HEALTH_PID 2>/dev/null || true
        fi
        
        print_status "Shutdown complete"
        exit 0
    }
    
    # Trap signals
    trap cleanup SIGTERM SIGINT
}

# Monitor processes
monitor_processes() {
    print_info "Starting process monitoring..."
    
    while true; do
        # Check if bot is still running
        if [ ! -z "$BOT_PID" ] && ! kill -0 $BOT_PID 2>/dev/null; then
            print_error "Telegram bot process died, restarting..."
            start_bot
        fi
        
        # Check if health server is still running
        if [ ! -z "$HEALTH_PID" ] && ! kill -0 $HEALTH_PID 2>/dev/null; then
            print_error "Health check server process died, restarting..."
            start_health_server
        fi
        
        # Sleep before next check
        sleep 10
    done
}

# Main execution
main() {
    print_info "Initializing Personal System Telegram Bot..."
    
    check_environment
    create_directories
    setup_signal_handlers
    start_health_server
    start_bot
    
    print_status "All services started successfully!"
    print_info "Bot is now running and ready to receive messages"
    print_info "Health check available at: http://localhost:${HEALTH_CHECK_PORT:-8000}/health"
    print_info "Press Ctrl+C to stop all services"
    
    # Start monitoring
    monitor_processes
}

# Run main function
main "$@"
