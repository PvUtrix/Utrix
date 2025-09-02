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
        echo "📖 Please see ENVIRONMENT_SETUP.md for complete configuration guide"
        echo ""
        echo "Quick setup:"
        echo "1. Copy the template from ENVIRONMENT_SETUP.md"
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

        if [[ -z "$CORE_SUPABASE_ANON_KEY" ]]; then
            print_warning "CORE_SUPABASE_ANON_KEY not set - database features will be disabled"
        fi
    fi
}

setup_python_environment() {
    print_step "Setting up Python environment..."

    # Install Python dependencies for serverless
    cd automation/serverless
    if [[ -f "requirements.txt" ]]; then
        # Check if we're in a virtual environment
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            # Inside virtual environment - install normally
            python3 -m pip install -r requirements.txt
            echo "✅ Python dependencies installed in virtual environment"
        else
            # Not in virtual environment - use --user
            python3 -m pip install --user -r requirements.txt
            echo "✅ Python dependencies installed with --user"
        fi
    fi

    # Go back to project root
    cd ../..
}

setup_serverless() {
    print_step "Setting up serverless framework..."

    # Install serverless framework if not present
    if ! command -v serverless &> /dev/null; then
        npm install -g serverless
        echo "✅ Serverless framework installed"
    else
        echo "✅ Serverless framework already installed"
    fi

    # Configure AWS if credentials are available
    if [[ -n "$AWS_ACCESS_KEY_ID" && -n "$AWS_SECRET_ACCESS_KEY" ]]; then
        aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
        aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
        aws configure set region "$AWS_REGION"
        echo "✅ AWS credentials configured"
    else
        print_warning "AWS credentials not found in .env. Please configure manually."
    fi
}

test_components() {
    print_step "Testing components..."

    cd automation/serverless

    # Test Python imports
    echo "Testing Python imports..."
    python3 -c "from voice_content_generator import VoiceContentGenerator; print('✅ Voice generator OK')"
    python3 -c "from elevenlabs_tts import ElevenLabsTTS; print('✅ ElevenLabs OK')"
    python3 -c "from cicd_orchestrator import CICDVoiceOrchestrator; print('✅ CI/CD orchestrator OK')"

    # Test ElevenLabs connection if API key is available
    if [[ -n "$ELEVENLABS_API_KEY" ]]; then
        echo "Testing ElevenLabs connection..."
        python3 elevenlabs_tts.py test 2>/dev/null && echo "✅ ElevenLabs connection OK" || print_warning "ElevenLabs test failed - check API key"
    fi

    cd ../..
}

deploy_serverless() {
    print_step "Deploying serverless functions..."

    cd automation/serverless

    # Deploy to AWS Lambda
    if [[ -n "$AWS_ACCESS_KEY_ID" ]]; then
        serverless deploy --stage prod
        echo "✅ Serverless functions deployed"

        # Show webhook URL
        serverless info --stage prod | grep -A 5 "endpoints:"
    else
        print_warning "AWS credentials not configured. Skipping serverless deployment."
        echo "Run: serverless deploy --stage prod (after configuring AWS)"
    fi

    cd ../..
}

create_dockerfile() {
    print_step "Creating Dockerfile..."

    if [[ ! -f "Dockerfile" ]]; then
        cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data and logs directories
RUN mkdir -p /app/data /app/logs

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "main.py"]
EOF
        echo "✅ Dockerfile created"
    else
        echo "✅ Dockerfile already exists"
    fi
}

create_docker_compose() {
    print_step "Creating docker-compose.yml..."

    if [[ ! -f "docker-compose.yml" ]]; then
        cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  personal-system:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CORE_SUPABASE_URL=${CORE_SUPABASE_URL}
      - CORE_SUPABASE_ANON_KEY=${CORE_SUPABASE_ANON_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - ELEVENLABS_VOICE_ID=${ELEVENLABS_VOICE_ID}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes

volumes:
  redis_data:
EOF
        echo "✅ docker-compose.yml created"
    else
        echo "✅ docker-compose.yml already exists"
    fi
}

create_coolify_config() {
    print_step "Creating Coolify configuration..."

    if [[ ! -f "coolify.yaml" ]]; then
        cat > coolify.yaml << 'EOF'
# Coolify Deployment Configuration
version: '1'

services:
  personal-system:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - CORE_SUPABASE_URL=${CORE_SUPABASE_URL}
      - CORE_SUPABASE_ANON_KEY=${CORE_SUPABASE_ANON_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - ELEVENLABS_VOICE_ID=${ELEVENLABS_VOICE_ID}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
EOF
        echo "✅ coolify.yaml created"
    else
        echo "✅ coolify.yaml already exists"
    fi
}

setup_monitoring() {
    print_step "Setting up monitoring..."

    # Create monitoring script
    cat > setup_monitoring.sh << 'EOF'
#!/bin/bash

# Set up monitoring cron jobs
echo "Setting up monitoring cron jobs..."

# Add to crontab
crontab -l > current_cron 2>/dev/null || true

# Add monitoring jobs if not already present
if ! grep -q "data_monitor.py" current_cron; then
    echo "0 9 * * * cd $(pwd)/automation/serverless && python3 data_monitor.py --alert" >> current_cron
    echo "0 */4 * * * cd $(pwd)/automation/serverless && python3 data_sync_manager.py" >> current_cron
    echo "0 2 * * 0 cd $(pwd)/automation/serverless && python3 data_lifecycle_manager.py --process" >> current_cron
    echo "0 9 1 * * cd $(pwd)/automation/serverless && python3 data_monitor.py --report" >> current_cron
fi

crontab current_cron
rm -f current_cron

echo "✅ Monitoring cron jobs configured"
EOF

    chmod +x setup_monitoring.sh
    echo "✅ Monitoring setup script created"
}

create_deployment_summary() {
    print_step "Creating deployment summary..."

    cat > DEPLOYMENT_SUMMARY.md << EOF
# 🚀 Deployment Summary

## Services Deployed
- ✅ Personal System API (Port 8000)
- ✅ Multi-Tier Database System
- ✅ Voice Generation (ElevenLabs)
- ✅ CI/CD Pipeline (AWS Lambda)
- ✅ Telegram Bot Integration

## Key URLs
- **API Endpoint**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Gitea Repository**: $GITEA_URL
- **Coolify Dashboard**: $COOLIFY_URL

## Environment Variables
$(cat .env | grep -v '^#' | grep -v '^$')

## Next Steps
1. Configure Gitea webhook for CI/CD
2. Test voice message generation
3. Set up monitoring alerts
4. Configure SSL certificates
5. Set up automated backups

## Quick Tests
\`\`\`bash
# Test API
curl http://localhost:8000/health

# Test voice generation
cd automation/serverless
python3 voice_content_generator.py

# Test CI/CD
python3 cicd_orchestrator.py
\`\`\`

## Monitoring
- Daily health checks: 9 AM
- Data synchronization: Every 4 hours
- Weekly cleanup: Sunday 2 AM
- Monthly reports: 1st of month

---
*Generated on: $(date)*
EOF

    echo "✅ Deployment summary created"
}

main() {
    print_header

    case "${1:-}" in
        "setup")
            check_prerequisites
            setup_environment
            setup_python_environment
            setup_serverless
            ;;
        "docker")
            create_dockerfile
            create_docker_compose
            create_coolify_config
            ;;
        "test")
            test_components
            ;;
        "deploy")
            deploy_serverless
            ;;
        "monitoring")
            setup_monitoring
            ;;
        "summary")
            create_deployment_summary
            ;;
        "all")
            check_prerequisites
            setup_environment
            setup_python_environment
            setup_serverless
            create_dockerfile
            create_docker_compose
            create_coolify_config
            test_components
            deploy_serverless
            setup_monitoring
            create_deployment_summary
            ;;
        "help"|"-h"|"--help"|"")
            echo "Usage: $0 <command>"
            echo ""
            echo "Commands:"
            echo "  setup      - Configure environment and dependencies"
            echo "  docker     - Create Docker and Coolify configuration"
            echo "  test       - Test all components"
            echo "  deploy     - Deploy serverless functions"
            echo "  monitoring - Set up monitoring cron jobs"
            echo "  summary    - Create deployment summary"
            echo "  all        - Run complete deployment setup"
            echo ""
            echo "Example: $0 all"
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac

    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ Command completed successfully!${NC}"
    else
        echo -e "${RED}❌ Command failed!${NC}"
        exit 1
    fi
}

main "$@"
