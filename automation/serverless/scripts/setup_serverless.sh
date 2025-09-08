#!/bin/bash

# Personal System Serverless Setup Script
# This script will guide you through setting up your serverless infrastructure

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
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

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
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

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local missing_tools=()
    
    # Check AWS CLI
    if command_exists aws; then
        print_status "✅ AWS CLI is installed"
    else
        print_error "❌ AWS CLI not found"
        missing_tools+=("aws")
    fi
    
    # Check Vercel CLI
    if command_exists vercel; then
        print_status "✅ Vercel CLI is installed"
    else
        print_error "❌ Vercel CLI not found"
        missing_tools+=("vercel")
    fi
    
    # Check Serverless Framework
    if command_exists serverless; then
        print_status "✅ Serverless Framework is installed"
    else
        print_error "❌ Serverless Framework not found"
        missing_tools+=("serverless")
    fi
    
    # Check Node.js
    if command_exists node; then
        print_status "✅ Node.js is installed"
    else
        print_error "❌ Node.js not found"
        missing_tools+=("node")
    fi
    
    # Check Python
    if command_exists python3; then
        print_status "✅ Python 3 is installed"
    else
        print_error "❌ Python 3 not found"
        missing_tools+=("python3")
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_status "Please install the missing tools and run this script again."
        exit 1
    fi
    
    print_status "All prerequisites are installed! 🎉"
}

# Setup AWS credentials
setup_aws() {
    print_header "AWS Configuration"
    
    print_step "Setting up AWS credentials..."
    
    # Check if AWS is already configured
    if aws sts get-caller-identity >/dev/null 2>&1; then
        print_status "✅ AWS credentials are already configured"
        aws sts get-caller-identity
        return 0
    fi
    
    print_warning "AWS credentials not configured. Let's set them up:"
    echo
    print_status "You'll need to:"
    echo "1. Go to AWS Console > IAM > Users > Your User > Security Credentials"
    echo "2. Create Access Keys if you don't have them"
    echo "3. Download the credentials file"
    echo
    
    prompt_input "Enter your AWS Access Key ID" AWS_ACCESS_KEY_ID
    prompt_secret "Enter your AWS Secret Access Key" AWS_SECRET_ACCESS_KEY
    prompt_input "Enter your AWS Region" AWS_REGION "us-east-1"
    
    # Configure AWS
    aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
    aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
    aws configure set default.region "$AWS_REGION"
    
    # Test the configuration
    if aws sts get-caller-identity >/dev/null 2>&1; then
        print_status "✅ AWS credentials configured successfully!"
        aws sts get-caller-identity
    else
        print_error "❌ AWS credentials configuration failed"
        exit 1
    fi
}

# Setup Supabase
setup_supabase() {
    print_header "Supabase Configuration"
    
    print_step "Setting up Supabase databases..."
    
    print_status "You'll need to create Supabase projects for your databases:"
    echo "1. Core Database (Free Tier) - for basic data"
    echo "2. Main Database (Self-hosted or Premium) - for advanced features"
    echo
    
    print_status "Go to https://supabase.com and create your projects"
    echo
    
    prompt_input "Enter Core Supabase URL" CORE_SUPABASE_URL
    prompt_secret "Enter Core Supabase Anon Key" CORE_SUPABASE_ANON_KEY
    prompt_input "Enter Main Supabase URL" MAIN_SUPABASE_URL
    prompt_secret "Enter Main Supabase Anon Key" MAIN_SUPABASE_ANON_KEY
    
    print_status "✅ Supabase configuration completed!"
}

# Setup Telegram Bot
setup_telegram() {
    print_header "Telegram Bot Configuration"
    
    print_step "Setting up Telegram bot..."
    
    print_status "To create a Telegram bot:"
    echo "1. Message @BotFather on Telegram"
    echo "2. Send /newbot command"
    echo "3. Follow the instructions to create your bot"
    echo "4. Get your bot token"
    echo "5. Get your chat ID by messaging @userinfobot"
    echo
    
    prompt_secret "Enter your Telegram Bot Token" TELEGRAM_BOT_TOKEN
    prompt_input "Enter your Telegram Chat ID" TELEGRAM_CHAT_ID
    
    print_status "✅ Telegram bot configuration completed!"
}

# Setup optional services
setup_optional() {
    print_header "Optional Services Configuration"
    
    print_step "Setting up optional services..."
    
    # ElevenLabs
    echo
    print_status "ElevenLabs Voice Generation (Optional):"
    echo "Get API key from https://elevenlabs.io/"
    prompt_input "Enter ElevenLabs API Key (or press Enter to skip)" ELEVENLABS_API_KEY ""
    
    # Gitea
    echo
    print_status "Gitea Webhook Configuration (Optional):"
    echo "For CI/CD automation with your Gitea instance"
    prompt_input "Enter Gitea URL (or press Enter to skip)" GITEA_URL ""
    prompt_input "Enter Gitea Token (or press Enter to skip)" GITEA_TOKEN ""
    
    # Coolify
    echo
    print_status "Coolify Deployment (Optional):"
    echo "For automated deployments"
    prompt_input "Enter Coolify URL (or press Enter to skip)" COOLIFY_URL ""
    prompt_input "Enter Coolify API Token (or press Enter to skip)" COOLIFY_API_TOKEN ""
    
    print_status "✅ Optional services configuration completed!"
}

# Create environment file
create_env_file() {
    print_header "Creating Environment File"
    
    print_step "Creating .env file with your configuration..."
    
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
}

# Setup Vercel
setup_vercel() {
    print_header "Vercel Configuration"
    
    print_step "Setting up Vercel..."
    
    # Check if already logged in
    if vercel whoami >/dev/null 2>&1; then
        print_status "✅ Already logged in to Vercel"
        vercel whoami
    else
        print_status "Logging in to Vercel..."
        vercel login
    fi
    
    print_status "✅ Vercel configuration completed!"
}

# Deploy functions
deploy_functions() {
    print_header "Deploying Serverless Functions"
    
    print_step "Deploying AWS Lambda functions..."
    
    # Load environment variables
    if [[ -f .env ]]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    # Deploy with Serverless Framework
    serverless deploy --stage prod --config configs/serverless.yml
    
    if [[ $? -eq 0 ]]; then
        print_status "✅ AWS Lambda functions deployed successfully!"
    else
        print_error "❌ AWS Lambda deployment failed!"
        exit 1
    fi
    
    print_step "Deploying Vercel Edge functions..."
    
    # Deploy to Vercel
    cd vercel
    vercel --prod
    cd ..
    
    if [[ $? -eq 0 ]]; then
        print_status "✅ Vercel Edge functions deployed successfully!"
    else
        print_error "❌ Vercel deployment failed!"
        exit 1
    fi
}

# Test deployment
test_deployment() {
    print_header "Testing Deployment"
    
    print_step "Testing Lambda functions..."
    
    # Test daily summary function
    serverless invoke --function daily-summary --stage prod --config configs/serverless.yml
    
    print_step "Testing Vercel functions..."
    
    # Get Vercel deployment URL
    local vercel_url=$(vercel ls | grep "ready" | head -1 | awk '{print $2}')
    if [[ -n "$vercel_url" ]]; then
        print_status "Vercel deployment URL: $vercel_url"
        print_status "Test your Vercel functions at: $vercel_url/api/shadow-work"
    fi
    
    print_status "✅ Deployment testing completed!"
}

# Setup monitoring
setup_monitoring() {
    print_header "Setting Up Monitoring"
    
    print_step "Setting up cost monitoring..."
    
    # Create AWS Budget for cost alerts
    python3 functions/monitoring/cost_monitor.py --setup-budget || print_warning "Budget setup skipped (may already exist)"
    
    print_status "✅ Monitoring setup completed!"
}

# Generate summary
generate_summary() {
    print_header "Deployment Summary"
    
    cat << EOF

🎉 SERVERLESS DEPLOYMENT COMPLETE!

Your personal system is now running serverlessly with:

✅ AWS Lambda Functions:
   • Daily Summary Generator (runs daily at 12 PM UTC)
   • Daily Voice Message (runs daily at 7 AM UTC)
   • Shadow Work Tracker API
   • Google Drive Sync (weekly on Mondays)
   • CI/CD Orchestrator
   • Data Sync Manager

✅ Vercel Edge Functions:
   • Shadow Work Tracker (fast, global)

✅ Cost Monitoring:
   • AWS Budget alerts (\$0.01 threshold)
   • Usage tracking and reporting

📊 Next Steps:
1. Monitor your first function executions in AWS CloudWatch
2. Check Vercel dashboard for Edge function analytics
3. Test your Telegram bot integration
4. Set up daily cost monitoring alerts

🛠️ Useful Commands:
• View Lambda logs: serverless logs --function daily-summary --tail
• View Vercel logs: vercel logs
• Run cost report: python3 functions/monitoring/cost_monitor.py
• Redeploy: ./deploy.sh

💰 Cost Monitoring:
• AWS Free Tier: 1M Lambda requests/month
• Vercel Free Tier: 100GB bandwidth
• Supabase Free Tier: 500MB database

🚨 Alerts will be sent to your Telegram if costs exceed safe limits!

EOF
}

# Main setup flow
main() {
    print_header "Personal System Serverless Setup"
    
    check_prerequisites
    setup_aws
    setup_supabase
    setup_telegram
    setup_optional
    create_env_file
    setup_vercel
    deploy_functions
    test_deployment
    setup_monitoring
    generate_summary
    
    print_status "🎉 Setup completed successfully!"
    print_status "Your personal system is now running serverlessly!"
}

# Handle command line arguments
case "${1:-}" in
    "aws-only")
        check_prerequisites
        setup_aws
        ;;
    "deploy-only")
        deploy_functions
        test_deployment
        ;;
    "test-only")
        test_deployment
        ;;
    *)
        main
        ;;
esac
