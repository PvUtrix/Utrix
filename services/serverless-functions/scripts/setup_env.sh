#!/bin/bash

# Environment Setup Script for Serverless Deployment
# This script helps you set up the required environment variables

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to prompt for user input
prompt_input() {
    local prompt="$1"
    local var_name="$2"
    local default_value="$3"
    
    if [[ -n "$default_value" ]]; then
        read -p "$prompt [$default_value]: " input
        eval "$var_name=\${input:-$default_value}"
    else
        read -p "$prompt: " input
        eval "$var_name=\"$input\""
    fi
}

# Function to prompt for sensitive input
prompt_secret() {
    local prompt="$1"
    local var_name="$2"
    
    read -s -p "$prompt: " input
    echo
    eval "$var_name=\"$input\""
}

print_header "Environment Variables Setup"

print_status "This script will help you set up the required environment variables for your serverless deployment."
echo

# Check if .env already exists
if [[ -f .env ]]; then
    print_warning ".env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " overwrite
    if [[ "$overwrite" != "y" && "$overwrite" != "Y" ]]; then
        print_status "Keeping existing .env file. Exiting."
        exit 0
    fi
fi

print_status "Let's set up your environment variables:"
echo

# AWS Configuration
print_header "AWS Configuration"
print_status "You'll need AWS credentials to deploy Lambda functions."
print_status "Get these from: AWS Console > IAM > Users > Your User > Security Credentials"
echo

prompt_input "AWS Access Key ID" AWS_ACCESS_KEY_ID
prompt_secret "AWS Secret Access Key" AWS_SECRET_ACCESS_KEY
prompt_input "AWS Region" AWS_REGION "us-east-1"

echo

# Supabase Configuration
print_header "Supabase Configuration"
print_status "You'll need Supabase projects for data storage."
print_status "Create free projects at: https://supabase.com"
echo

print_status "Core Database (Free Tier) - for basic data:"
prompt_input "Core Supabase URL" CORE_SUPABASE_URL
prompt_secret "Core Supabase Anon Key" CORE_SUPABASE_ANON_KEY

echo
print_status "Main Database (Optional) - for advanced features:"
prompt_input "Main Supabase URL (or press Enter to skip)" MAIN_SUPABASE_URL ""
prompt_secret "Main Supabase Anon Key (or press Enter to skip)" MAIN_SUPABASE_ANON_KEY ""

echo

# Telegram Configuration
print_header "Telegram Bot Configuration"
print_status "Create a Telegram bot for notifications:"
print_status "1. Message @BotFather on Telegram"
print_status "2. Send /newbot command"
print_status "3. Follow instructions to create your bot"
print_status "4. Get your bot token"
print_status "5. Get your chat ID by messaging @userinfobot"
echo

prompt_secret "Telegram Bot Token" TELEGRAM_BOT_TOKEN
prompt_input "Telegram Chat ID" TELEGRAM_CHAT_ID

echo

# Optional Services
print_header "Optional Services"
print_status "These services are optional but add functionality:"
echo

print_status "ElevenLabs Voice Generation (Optional):"
print_status "Get API key from: https://elevenlabs.io/"
prompt_input "ElevenLabs API Key (or press Enter to skip)" ELEVENLABS_API_KEY ""

echo
print_status "Gitea Webhook (Optional) - for CI/CD:"
prompt_input "Gitea URL (or press Enter to skip)" GITEA_URL ""
prompt_input "Gitea Token (or press Enter to skip)" GITEA_TOKEN ""

echo
print_status "Coolify Deployment (Optional):"
prompt_input "Coolify URL (or press Enter to skip)" COOLIFY_URL ""
prompt_input "Coolify API Token (or press Enter to skip)" COOLIFY_API_TOKEN ""

# Create .env file
print_header "Creating .env File"

cat > .env << EOF
# Personal System Serverless Environment Variables
# Generated on $(date)

# AWS Configuration
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
AWS_REGION=$AWS_REGION

# Supabase Configuration
CORE_SUPABASE_URL=$CORE_SUPABASE_URL
CORE_SUPABASE_ANON_KEY=$CORE_SUPABASE_ANON_KEY
MAIN_SUPABASE_URL=$MAIN_SUPABASE_URL
MAIN_SUPABASE_ANON_KEY=$MAIN_SUPABASE_ANON_KEY

# Telegram Configuration
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID

# Optional Services
ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
GITEA_URL=$GITEA_URL
GITEA_TOKEN=$GITEA_TOKEN
COOLIFY_URL=$COOLIFY_URL
COOLIFY_API_TOKEN=$COOLIFY_API_TOKEN

# Development Settings
NODE_ENV=production
DEBUG=false
EOF

print_status "✅ Environment file created: .env"
print_warning "⚠️  Keep your .env file secure and never commit it to version control!"

# Test the configuration
print_header "Testing Configuration"

print_status "Testing AWS connection..."
export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
export AWS_REGION="$AWS_REGION"

if aws sts get-caller-identity >/dev/null 2>&1; then
    print_status "✅ AWS connection successful!"
    aws sts get-caller-identity
else
    print_error "❌ AWS connection failed. Please check your credentials."
fi

print_status "✅ Environment setup completed!"
print_status "You can now run: ./setup_serverless.sh"
