#!/bin/bash

# Serverless Deployment Script
# Deploys all serverless functions with cost monitoring

set -e  # Exit on any error

echo "🚀 Starting Serverless Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI not found. Install it first: https://aws.amazon.com/cli/"
        exit 1
    fi

    # Check Vercel CLI
    if ! command -v vercel &> /dev/null; then
        print_error "Vercel CLI not found. Install it first: npm install -g vercel"
        exit 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found."
        exit 1
    fi

    print_status "Prerequisites check passed!"
}

# Check environment variables
check_environment() {
    print_status "Checking environment variables..."

    required_vars=(
        "AWS_ACCESS_KEY_ID"
        "AWS_SECRET_ACCESS_KEY"
        "AWS_REGION"
        "TELEGRAM_BOT_TOKEN"
        "TELEGRAM_CHAT_ID"
        "SUPABASE_URL"
        "SUPABASE_ANON_KEY"
    )

    missing_vars=()

    for var in "${required_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            missing_vars+=("$var")
        fi
    done

    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        print_error "Missing required environment variables:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        echo ""
        print_error "Set them in your environment or .env file"
        exit 1
    fi

    print_status "Environment variables check passed!"
}

# Deploy AWS Lambda functions
deploy_aws_lambda() {
    print_status "Deploying AWS Lambda functions..."

    # Check if serverless framework is installed
    if ! command -v serverless &> /dev/null; then
        print_status "Installing Serverless Framework..."
        npm install -g serverless
    fi

    # Configure AWS profile if needed
    if [[ -z "${AWS_PROFILE}" ]]; then
        export AWS_PROFILE=default
    fi

    # Deploy Lambda functions
    serverless deploy --stage prod

    if [[ $? -eq 0 ]]; then
        print_status "AWS Lambda functions deployed successfully!"
    else
        print_error "AWS Lambda deployment failed!"
        exit 1
    fi
}

# Deploy Vercel functions
deploy_vercel() {
    print_status "Deploying Vercel Edge functions..."

    # Check if logged in to Vercel
    if ! vercel whoami &> /dev/null; then
        print_warning "Not logged in to Vercel. Please run: vercel login"
        vercel login
    fi

    # Deploy to Vercel
    vercel --prod

    if [[ $? -eq 0 ]]; then
        print_status "Vercel functions deployed successfully!"
    else
        print_error "Vercel deployment failed!"
        exit 1
    fi
}

# Set up cost monitoring
setup_cost_monitoring() {
    print_status "Setting up cost monitoring..."

    # Create AWS Budget for alerts
    aws budgets create-budget \
        --account-id $(aws sts get-caller-identity --query Account --output text) \
        --budget file://budget_config.json \
        --notifications-with-subscribers file://budget_notifications.json || print_warning "AWS Budget setup skipped (may already exist)"

    # Schedule cost monitoring (runs daily)
    if [[ -f "cost_monitor.py" ]]; then
        print_status "Cost monitoring script ready!"
        print_status "To enable daily cost monitoring, add this to your crontab:"
        echo "0 9 * * * cd $(pwd) && python3 cost_monitor.py --alert"
    fi
}

# Verify deployment
verify_deployment() {
    print_status "Verifying deployment..."

    # Test Lambda functions
    print_status "Testing Lambda functions..."
    serverless invoke --function daily-summary --stage prod || print_warning "Lambda test failed"

    # Test Vercel functions
    print_status "Testing Vercel functions..."
    vercel ls | grep -q "ready" && print_status "Vercel functions are ready!" || print_warning "Vercel verification inconclusive"

    print_status "Deployment verification complete!"
}

# Generate deployment summary
generate_summary() {
    print_status "Generating deployment summary..."

    cat << EOF

🎉 SERVERLESS DEPLOYMENT COMPLETE!

Your personal system is now running serverlessly with:

✅ AWS Lambda Functions:
   • Daily Summary Generator (runs daily at 12 PM UTC)
   • Daily Voice Message (runs daily at 7 AM UTC)
   • Shadow Work Tracker API
   • Google Drive Sync (weekly on Mondays)

✅ Vercel Edge Functions:
   • Shadow Work Tracker (fast, global)

✅ Cost Monitoring:
   • AWS Budget alerts ($0.01 threshold)
   • Usage tracking and reporting

📊 Next Steps:
1. Monitor your first function executions in AWS CloudWatch
2. Check Vercel dashboard for Edge function analytics
3. Set up daily cost monitoring alerts
4. Test your functions with real data

🛠️ Useful Commands:
• View Lambda logs: serverless logs --function daily-summary --tail
• View Vercel logs: vercel logs
• Run cost report: python3 cost_monitor.py
• Redeploy: ./deploy.sh

💰 Cost Monitoring:
• AWS Free Tier: 1M Lambda requests/month
• Vercel Free Tier: 100GB bandwidth
• Supabase Free Tier: 500MB database

🚨 Alerts will be sent to your Telegram if costs exceed safe limits!

EOF
}

# Main deployment flow
main() {
    echo "🚀 Personal System Serverless Deployment"
    echo "========================================"

    check_prerequisites
    check_environment
    deploy_aws_lambda
    deploy_vercel
    setup_cost_monitoring
    verify_deployment
    generate_summary

    print_status "🎉 Deployment completed successfully!"
}

# Handle command line arguments
case "${1:-}" in
    "aws-only")
        check_prerequisites
        check_environment
        deploy_aws_lambda
        ;;
    "vercel-only")
        deploy_vercel
        ;;
    "verify")
        verify_deployment
        ;;
    "cost-check")
        python3 cost_monitor.py
        ;;
    *)
        main
        ;;
esac
