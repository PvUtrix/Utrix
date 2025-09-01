# 🚀 Complete Coolify Deployment Guide

Deploy your entire personal system with voice-enabled automation to Coolify. This comprehensive guide covers everything from initial setup to production deployment.

## 🎯 What You'll Deploy

### Core Services
- **Personal System API** - Your main application
- **Supabase** - Database and authentication
- **Gitea** - Git server for CI/CD
- **ElevenLabs Integration** - Voice services
- **Telegram Bot** - Voice notifications
- **AWS Lambda** - Serverless functions

### Automation Features
- **Daily Voice Messages** - Morning planning with ElevenLabs
- **CI/CD Pipeline** - Voice-enabled deployments
- **Multi-Tier Database** - Smart data management
- **Health Monitoring** - System status tracking

---

## 📋 Prerequisites

### Coolify Server Requirements
- **Coolify v4.x** installed and running
- **Docker** enabled on host server
- **Domain/SSL** configured
- **At least 4GB RAM, 2 CPU cores**
- **50GB+ storage** for databases and logs

### External Services
- **AWS Account** (for Lambda functions)
- **ElevenLabs Account** (for voice generation)
- **Telegram Bot Token** (for notifications)

### Your Environment
- **Git repository** with your personal-system code
- **SSH access** to Coolify server
- **Basic Linux/Docker knowledge**

---

## 🚀 Phase 1: Coolify Initial Setup

### Step 1: Access Coolify Dashboard

1. Open your Coolify dashboard: `https://coolify.yourdomain.com`
2. Login with your admin credentials
3. Create a new project: **"Personal System"**

### Step 2: Configure Project Settings

```yaml
# In Coolify Project Settings:
Project Name: personal-system
Domain: personal.yourdomain.com
Git Repository: https://git.yourdomain.com/yourusername/personal-system.git
Branch: main
Build Pack: Docker
```

### Step 3: Set Up Environment Variables

In Coolify → Project → Environment Variables:

```bash
# Core Database (Supabase)
CORE_SUPABASE_URL=https://core-personal.supabase.co
CORE_SUPABASE_ANON_KEY=your_core_anon_key

# Main Database (Self-hosted)
MAIN_SUPABASE_URL=http://supabase:54321
MAIN_SUPABASE_ANON_KEY=your_main_anon_key

# ElevenLabs Voice
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Gitea (if self-hosted)
GITEA_URL=https://git.yourdomain.com
GITEA_TOKEN=your_gitea_token

# Coolify API
COOLIFY_API_TOKEN=your_coolify_token
```

---

## 🗄️ Phase 2: Database Setup

### Option A: Self-Hosted Supabase (Recommended)

#### Step 1: Deploy Supabase via Coolify

1. In Coolify → Add Resource → Database → Supabase
2. Configure:
   ```yaml
   Name: personal-supabase
   Version: latest
   Domain: supabase.yourdomain.com
   Database Password: your_secure_password
   JWT Secret: your_jwt_secret
   Anon Key: auto-generated
   Service Role Key: auto-generated
   ```

#### Step 2: Initialize Database Schema

```bash
# Connect to Supabase container
docker exec -it personal-supabase psql -U postgres

# Create required tables
CREATE DATABASE personal_system;
\c personal_system;

-- Daily summaries
CREATE TABLE daily_summaries (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    summary_text TEXT,
    health_data JSONB,
    productivity_data JSONB,
    learning_data JSONB,
    finance_data JSONB,
    insights JSONB,
    recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_type TEXT DEFAULT 'daily_summary',
    size_kb DECIMAL DEFAULT 0
);

-- Shadow work data
CREATE TABLE shadow_work_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    shadow_aspect TEXT,
    pattern_observed TEXT,
    integration_insight TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_type TEXT DEFAULT 'shadow_work'
);

-- Journal entries
CREATE TABLE journal_entries (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    content TEXT,
    tags TEXT[],
    mood INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_type TEXT DEFAULT 'journal'
);

-- Tasks
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',
    priority INTEGER DEFAULT 3,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    data_type TEXT DEFAULT 'task'
);

-- Voice messages log
CREATE TABLE voice_messages (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    content_preview TEXT,
    word_count INTEGER,
    audio_size_bytes INTEGER,
    elevenlabs_cost DECIMAL,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT DEFAULT 'sent'
);

-- Data sync log
CREATE TABLE data_sync_log (
    id SERIAL PRIMARY KEY,
    data_id TEXT NOT NULL,
    from_tier TEXT,
    to_tier TEXT,
    data_type TEXT,
    operation TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Data lifecycle log
CREATE TABLE data_lifecycle_log (
    id SERIAL PRIMARY KEY,
    item_id TEXT NOT NULL,
    table_name TEXT,
    operation TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Data inventory
CREATE TABLE data_inventory (
    id SERIAL PRIMARY KEY,
    data_type TEXT NOT NULL,
    core_count INTEGER DEFAULT 0,
    core_size_kb DECIMAL DEFAULT 0,
    main_count INTEGER DEFAULT 0,
    main_size_kb DECIMAL DEFAULT 0,
    total_size_kb DECIMAL DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Step 3: Create Indexes

```sql
-- Performance indexes
CREATE INDEX idx_daily_summaries_date ON daily_summaries(date);
CREATE INDEX idx_shadow_work_date ON shadow_work_data(date);
CREATE INDEX idx_journal_date ON journal_entries(date);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created ON tasks(created_at);
CREATE INDEX idx_voice_messages_date ON voice_messages(date);
```

### Option B: External Supabase (Free Tier)

1. Create account at https://supabase.com
2. Create new project: `personal-system-core`
3. Note the URL and API keys
4. Update environment variables in Coolify

---

## 🐙 Phase 3: Gitea Setup

### Option A: Self-Hosted Gitea (Recommended)

#### Step 1: Deploy Gitea via Coolify

1. In Coolify → Add Resource → Application
2. Configure:
   ```yaml
   Name: personal-gitea
   Git Repository: https://github.com/go-gitea/gitea
   Build Pack: Docker
   Domain: git.yourdomain.com
   Environment:
     - GITEA__database__DB_TYPE=postgres
     - GITEA__database__HOST=supabase
     - GITEA__database__NAME=gitea
     - GITEA__database__USER=gitea
     - GITEA__database__PASSWD=your_gitea_password
   ```

#### Step 2: Configure Gitea

1. Access Gitea at `https://git.yourdomain.com`
2. Complete initial setup
3. Create user and repository: `personal-system`
4. Generate personal access token for CI/CD

#### Step 3: Push Your Code

```bash
# Clone your repository
git clone https://git.yourdomain.com/yourusername/personal-system.git
cd personal-system

# Copy all your files
cp -r /path/to/your/current/personal-system/* .

# Commit and push
git add .
git commit -m "Initial deployment to Coolify"
git push origin main
```

### Option B: Use Existing Gitea

If you already have Gitea running:
1. Create repository: `personal-system`
2. Push your code to it
3. Update `GITEA_URL` environment variable

---

## 🤖 Phase 4: Telegram Bot Setup

### Step 1: Create Telegram Bot

1. Message `@BotFather` on Telegram
2. Send `/newbot`
3. Follow instructions to create bot
4. Save the bot token

### Step 2: Get Your Chat ID

```bash
# Send a message to your bot
# Then get chat ID:
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
```

### Step 3: Configure Bot Permissions

Your bot will need:
- Send voice messages
- Send text messages
- Receive commands (optional)

---

## 🎤 Phase 5: ElevenLabs Setup

### Step 1: Create ElevenLabs Account

1. Sign up at https://elevenlabs.io
2. Add credits to your account ($5 minimum)
3. Get your API key from profile settings

### Step 2: Choose Voice

Available voices:
- `21m00Tcm4TlvDq8ikWAM` - Rachel (warm, professional)
- `29vD33N1CtxCmqQRPOHJ` - Drew (friendly, energetic)
- `2EiwWnXFnvU5JabPnv8n` - Clyde (deep, authoritative)

### Step 3: Test Voice Generation

```bash
# Test your ElevenLabs setup
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "Accept: audio/mpeg" \
  -H "Content-Type: application/json" \
  -H "xi-api-key: YOUR_API_KEY" \
  -d '{"text": "Hello from your personal system!", "model_id": "eleven_monolingual_v1"}' \
  --output test_voice.mp3
```

---

## ⚙️ Phase 6: AWS Lambda Setup

### Step 1: Install Serverless Framework

```bash
# Install globally
npm install -g serverless

# Configure AWS credentials
aws configure
```

### Step 2: Deploy Lambda Functions

```bash
cd automation/serverless

# Deploy all functions
serverless deploy --stage prod

# Note the webhook URL for Gitea
serverless info --stage prod
```

### Step 3: Configure Lambda Environment

Update your Lambda environment variables:
```bash
CORE_SUPABASE_URL=https://core-personal.supabase.co
CORE_SUPABASE_ANON_KEY=your_core_key
ELEVENLABS_API_KEY=your_elevenlabs_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GITEA_WEBHOOK_SECRET=your_webhook_secret
```

---

## 🚀 Phase 7: Deploy Personal System

### Quick Deployment (Recommended)

Use the automated deployment script:

```bash
# Run complete setup
./coolify-deploy.sh all

# Or run individual steps
./coolify-deploy.sh setup    # Configure environment
./coolify-deploy.sh docker   # Create Docker files
./coolify-deploy.sh test     # Test components
./coolify-deploy.sh deploy   # Deploy serverless functions
```

### Manual Deployment

#### Step 1: Create Coolify Application

1. In Coolify → Add Resource → Application
2. Configure:
   ```yaml
   Name: personal-system-api
   Git Repository: https://git.yourdomain.com/yourusername/personal-system.git
   Build Pack: Docker
   Domain: api.yourdomain.com
   Environment: Production
   ```

### Step 2: Docker Configuration

Create `Dockerfile` in your repository root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

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
```

### Step 3: Docker Compose (Optional)

```yaml
version: '3.8'

services:
  personal-system:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CORE_SUPABASE_URL=${CORE_SUPABASE_URL}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

### Step 4: Deploy via Coolify

1. Push your Docker configuration to Git
2. Coolify will automatically build and deploy
3. Monitor deployment logs in Coolify dashboard

### Step 5: Verify Deployment

```bash
# Test API endpoints
curl https://api.yourdomain.com/health
curl https://api.yourdomain.com/system/info

# Test voice preview
curl https://api.yourdomain.com/voice/preview

# Check monitoring
curl https://api.yourdomain.com/monitor/status
```

---

## 🔗 Phase 8: Configure CI/CD Webhooks

### Step 1: Set Up Gitea Webhook

1. Go to your repository in Gitea
2. Settings → Webhooks → Add Webhook
3. Configure:
   ```yaml
   Target URL: https://your-lambda-webhook-url.amazonaws.com/prod/webhook/gitea
   Content Type: application/json
   Secret: your_webhook_secret
   Events: Push, Pull Request
   Active: ✅
   ```

### Step 2: Test Webhook

```bash
# Make a small change and push
echo "# Test CI/CD" >> README.md
git add README.md
git commit -m "Test CI/CD pipeline"
git push origin main
```

You should receive a voice message about the deployment!

---

## 📊 Phase 9: Monitoring & Testing

### Step 1: Test All Components

```bash
# Test database connection
cd automation/serverless
python3 -c "from voice_content_generator import VoiceContentGenerator; print('✅ Database OK')"

# Test voice generation
python3 elevenlabs_tts.py test

# Test Lambda functions
serverless invoke --function daily-voice-message --stage prod

# Test CI/CD pipeline
python3 cicd_orchestrator.py
```

### Step 2: Set Up Monitoring

```bash
# Daily monitoring
0 9 * * * cd /path/to/personal-system/automation/serverless && python3 data_monitor.py --alert

# Weekly cleanup
0 2 * * 0 cd /path/to/personal-system/automation/serverless && python3 data_lifecycle_manager.py --process

# Monthly reports
0 9 1 * * cd /path/to/personal-system/automation/serverless && python3 data_monitor.py --report
```

### Step 3: Health Checks

Create health check endpoints in your application:

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": check_database_connection(),
        "elevenlabs": check_elevenlabs_connection(),
        "telegram": check_telegram_connection()
    }
```

---

## 🔧 Phase 10: Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check Supabase connection
curl -H "apikey: YOUR_ANON_KEY" https://your-project.supabase.co/rest/v1/

# Test database credentials
psql -h supabase -U postgres -d personal_system
```

#### Voice Generation Failed
```bash
# Check ElevenLabs API key
curl -H "xi-api-key: YOUR_API_KEY" https://api.elevenlabs.io/v1/voices

# Test voice generation
python3 elevenlabs_tts.py test
```

#### CI/CD Webhook Failed
```bash
# Check webhook delivery in Gitea
# Repository Settings → Webhooks → Recent Deliveries

# Test webhook manually
curl -X POST https://your-lambda-webhook-url.amazonaws.com/prod/webhook/gitea \
  -H "Content-Type: application/json" \
  -d '{"test": "webhook"}'
```

#### Coolify Deployment Failed
```bash
# Check Coolify logs
# Coolify Dashboard → Applications → personal-system-api → Logs

# Check Docker build
docker build -t personal-system .
```

### Performance Optimization

#### Database Indexes
```sql
-- Add performance indexes
CREATE INDEX CONCURRENTLY idx_daily_summaries_date ON daily_summaries(date);
CREATE INDEX CONCURRENTLY idx_shadow_work_date ON shadow_work_data(date);
CREATE INDEX CONCURRENTLY idx_journal_date ON journal_entries(date);
```

#### Caching
```python
# Add Redis caching for frequently accessed data
from redis import Redis
redis_client = Redis(host='redis', port=6379, db=0)

@cache(expire=3600)
def get_daily_summary(date):
    # Cached database query
    pass
```

---

## 🎯 Phase 11: Production Checklist

### Services
- [ ] Coolify server running and accessible
- [ ] Supabase database initialized and accessible
- [ ] Gitea repository created and configured
- [ ] ElevenLabs API key configured and tested
- [ ] Telegram bot created and configured
- [ ] AWS Lambda functions deployed and working

### Configuration
- [ ] All environment variables set in Coolify
- [ ] Database schema created and populated
- [ ] Gitea webhook configured and tested
- [ ] SSL certificates configured for all domains
- [ ] Backup strategy implemented

### Testing
- [ ] Voice message generation working
- [ ] CI/CD pipeline triggers on push
- [ ] Database connections stable
- [ ] Application health checks passing
- [ ] Monitoring and alerting configured

### Security
- [ ] API keys stored securely
- [ ] Database passwords strong
- [ ] Network security configured
- [ ] Access controls in place
- [ ] Regular security updates scheduled

---

## 🚀 Going Live

### Final Steps

1. **Test Complete System**
   ```bash
   # Test all components
   cd automation/serverless
   ./run.sh monitor
   ./run.sh voice-preview
   ./run.sh cicd-deploy
   ```

2. **Set Up Production Monitoring**
   ```bash
   # Add to crontab
   crontab -e

   # Add these lines:
   0 9 * * * cd /path/to/personal-system/automation/serverless && python3 data_monitor.py --alert
   0 */4 * * * cd /path/to/personal-system/automation/serverless && python3 data_sync_manager.py
   0 2 * * 0 cd /path/to/personal-system/automation/serverless && python3 data_lifecycle_manager.py --process
   ```

3. **First Production Deployment**
   ```bash
   # Make your first production commit
   echo "# Production Ready" >> README.md
   git add README.md
   git commit -m "🚀 Production deployment with voice CI/CD"
   git push origin main
   ```

4. **Verify Everything Works**
   - ✅ Voice message received about deployment
   - ✅ Application accessible at your domain
   - ✅ Database connections working
   - ✅ All monitoring alerts configured

---

## 🎉 Your System is Live!

### What You Now Have

🎯 **Personal System**: Fully deployed on Coolify
🎤 **Voice Messages**: Daily planning with ElevenLabs
🚀 **CI/CD Pipeline**: Voice-enabled automated deployments
🗄️ **Multi-Tier Database**: Smart data management
📊 **Monitoring**: Real-time health and performance tracking
🔒 **Security**: Production-ready with SSL and access controls

### Daily Experience
- **7 AM**: Wake up to personalized voice planning
- **Code Push**: Voice notification of successful deployment
- **24/7**: System monitoring and health checks
- **Zero Maintenance**: Fully automated operations

### Cost Breakdown
- **Coolify Server**: ~$10-20/month (your existing server)
- **ElevenLabs**: ~$0.30/month (daily + CI/CD voice)
- **AWS Lambda**: Free tier (1M requests/month)
- **Supabase**: Free tier (500MB)
- **Total**: ~$10-21/month

**Your personal system is now a complete, voice-enabled, automated platform running on Coolify!** 🎊

---

*This guide assumes you have basic knowledge of Docker, Git, and Linux. If you need help with any step, feel free to ask for clarification.*
