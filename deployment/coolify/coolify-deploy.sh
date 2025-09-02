#!/bin/bash

# Coolify Deployment Helper Script
# Automates deployment steps for the personal system

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}🚀 Personal System Coolify Deployment${NC}"
    echo "========================================"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_step "Checking prerequisites..."

    # Check if we're in the project root
    if [[ ! -f "automation/serverless/requirements.txt" ]]; then
        print_error "Please run this script from the personal-system project root"
        exit 1
    fi

    # Check Python environment
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3."
        exit 1
    else
        echo "✅ Python 3 found: $(python3 --version)"

        # Check if in virtual environment
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            echo "✅ Running in virtual environment: $(basename $VIRTUAL_ENV)"
        else
            echo "ℹ️  Not in virtual environment - will use --user installation"
        fi
    fi

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_warning "Docker not found. Please install Docker first."
    else
        echo "✅ Docker found: $(docker --version)"
    fi

    # Check Node.js for serverless
    if ! command -v node &> /dev/null; then
        print_warning "Node.js not found. Please install Node.js for serverless deployment."
    else
        echo "✅ Node.js found: $(node --version)"
    fi
}

setup_environment() {
    print_step "Setting up environment..."

    # Check for .env file
    if [[ ! -f ".env" ]]; then
        print_warning "No .env file found!"
        echo "📖 Please see docs/setup/environment-setup.md for complete configuration guide"
        echo ""
        echo "Quick setup:"
        echo "1. Copy the template from docs/setup/environment-setup.md"
        echo "2. Create .env file with your credentials"
        echo "3. Fill in all required API keys"
        echo ""
        print_error "Please create .env file with your credentials first"
        exit 1
    fi

    # Load environment variables
    if [[ -f ".env" ]]; then
        export $(grep -v '^#' .env | xargs)
        echo "✅ Environment variables loaded from .env"

        # Quick validation
        if [[ -z "$ELEVENLABS_API_KEY" ]]; then
            print_warning "ELEVENLABS_API_KEY not set - voice features will be disabled"
        fi

        if [[ -z "$TELEGRAM_BOT_TOKEN" ]]; then
            print_warning "TELEGRAM_BOT_TOKEN not set - notifications will be disabled"
        fi
