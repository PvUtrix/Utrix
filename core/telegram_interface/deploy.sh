#!/bin/bash

# Personal Telegram Bot Deployment Script for Coolify
# This script helps prepare and deploy the bot to Coolify

set -e

echo "🚀 Personal Telegram Bot - Coolify Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "Dockerfile" ]; then
    print_error "Please run this script from the personal_telegram_bot directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check if git is available
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

# Check if docker is available (optional, for local testing)
if command -v docker &> /dev/null; then
    print_success "Docker found - you can test locally"
else
    print_warning "Docker not found - you can still deploy to Coolify"
fi

# Check if config file exists
if [ ! -f "config/config.yaml" ]; then
    print_warning "config/config.yaml not found. Creating from sample..."
    if [ -f "config/config.yaml.sample" ]; then
        cp config/config.yaml.sample config/config.yaml
        print_success "Created config/config.yaml from sample"
        print_warning "Please edit config/config.yaml with your settings before deploying"
    else
        print_error "config/config.yaml.sample not found"
        exit 1
    fi
fi

print_status "Preparing for deployment..."

# Create .gitkeep files for empty directories
mkdir -p data/storage data/cache data/backups data/keys logs
touch data/storage/.gitkeep data/cache/.gitkeep data/backups/.gitkeep data/keys/.gitkeep logs/.gitkeep

# Check git status
if [ -d ".git" ]; then
    print_status "Checking git status..."
    
    # Check if there are uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "You have uncommitted changes. Consider committing them before deploying."
        echo "Uncommitted files:"
        git status --porcelain
        echo ""
        read -p "Do you want to continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Deployment cancelled"
            exit 0
        fi
    fi
    
    # Check if we're on main branch
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "main" ]; then
        print_warning "You're not on the main branch (current: $current_branch)"
        read -p "Do you want to switch to main branch? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git checkout main
            print_success "Switched to main branch"
        fi
    fi
else
    print_warning "Not in a git repository. You'll need to initialize git and push to your repository."
fi

print_status "Validating configuration..."

# Check if required files exist
required_files=("main.py" "Dockerfile" "requirements.txt" "config/config.yaml")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file"
    else
        print_error "✗ $file (missing)"
        exit 1
    fi
done

print_status "Testing Docker build locally (if Docker is available)..."

if command -v docker &> /dev/null; then
    if docker build -t personal-telegram-bot .; then
        print_success "Docker build successful"
    else
        print_error "Docker build failed"
        exit 1
    fi
else
    print_warning "Skipping Docker build test (Docker not available)"
fi

print_status "Deployment preparation complete!"
echo ""
print_success "Your bot is ready for Coolify deployment!"
echo ""
echo "Next steps:"
echo "1. Push your code to your Git repository:"
echo "   git add ."
echo "   git commit -m 'Add Docker configuration for Coolify deployment'"
echo "   git push origin main"
echo ""
echo "2. In Coolify:"
echo "   - Create new application"
echo "   - Connect your Git repository"
echo "   - Set build path to: projects/personal_telegram_bot"
echo "   - Add environment variables:"
echo "     TELEGRAM_BOT_TOKEN=your_bot_token"
echo "     TELEGRAM_USER_ID=your_user_id"
echo "     OPENAI_API_KEY=your_openai_key (optional)"
echo ""
echo "3. Deploy and monitor the logs"
echo ""
echo "For detailed instructions, see: COOLIFY_DEPLOYMENT.md"
echo ""
print_success "Happy deploying! 🚀"
