# 🚀 Complete Setup Guide - Personal System with Voice Automation

This guide covers everything you need to set up your **voice-enabled personal automation system** with Coolify deployment, serverless functions, and AI-powered features.

## 🎯 Prerequisites

### Required Software
- ✅ **Git** for version control
- ✅ **Python 3.9+** for automation scripts
- ✅ **Docker** (optional, for local development)
- ✅ **Text Editor** (VS Code with Cursor recommended)

### Required Accounts & Services
- ✅ **ElevenLabs Account** (voice generation)
- ✅ **Telegram Bot** (notifications)
- ✅ **Supabase Account** (database - free tier available)
- ✅ **Coolify Server** (your own deployment server)
- ✅ **Gitea/GitHub** (code repository)
- ⏳ **AWS Account** (optional - for serverless functions)

### System Requirements
- ✅ **RAM**: 4GB+ for Coolify server
- ✅ **Storage**: 50GB+ for databases and logs
- ✅ **Network**: Stable internet connection

---

## 📋 Setup Methods

### Method 1: Coolify Automated Deployment (Recommended)

```bash
# 1. Clone your repository
git clone https://git.yourdomain.com/yourusername/personal-system.git
cd personal-system

# 2. Run complete automated setup
./coolify-deploy.sh all

# 3. Configure environment variables
nano .env  # Fill in your API keys and credentials

# 4. Push to trigger Coolify deployment
git add .
git commit -m "🚀 Production deployment with voice automation"
git push origin main
```

**✅ That's it!** Coolify handles the rest automatically.

### Method 2: Local Development Setup

```bash
# 1. Clone and setup
git clone https://git.yourdomain.com/yourusername/personal-system.git
cd personal-system

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env  # If it exists
nano .env  # Add your credentials

# 5. Run locally
python main.py
```

### Method 3: Docker Local Development

```bash
# 1. Clone repository
git clone https://git.yourdomain.com/yourusername/personal-system.git
cd personal-system

# 2. Configure environment
nano .env  # Add your credentials

# 3. Build and run with Docker
docker build -t personal-system .
docker run -p 8000:8000 --env-file .env personal-system

# Or use docker-compose (recommended)
docker-compose up -d
```

---

## 🔧 External Services Configuration

### 1. ElevenLabs (Voice Generation)

```bash
# 1. Sign up at https://elevenlabs.io
# 2. Add credits ($5 minimum)
# 3. Get your API key from profile settings
# 4. Choose a voice (Rachel recommended: 21m00Tcm4TlvDq8ikWAM)

# Add to .env
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

### 2. Telegram Bot (Notifications)

```bash
# 1. Message @BotFather on Telegram
# 2. Send /newbot and follow instructions
# 3. Save your bot token
# 4. Send a message to your bot
# 5. Get chat ID: curl "https://api.telegram.org/bot<TOKEN>/getUpdates"

# Add to .env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Supabase Database (Free Tier)

```bash
# 1. Sign up at https://supabase.com
# 2. Create new project: "personal-system-core"
# 3. Get Project URL and API keys from Settings > API

# Add to .env
CORE_SUPABASE_URL=https://your-project.supabase.co
CORE_SUPABASE_ANON_KEY=your_anon_key_here
```

### 4. Gitea Repository (CI/CD)

```bash
# Option A: Self-hosted Gitea
# 1. Access your Gitea instance
# 2. Create repository: "personal-system"
# 3. Generate personal access token
# 4. Push your code

# Option B: GitHub/GitLab
# 1. Create repository on your preferred platform
# 2. Push your code
# 3. Configure webhooks for CI/CD

# Add to .env
GITEA_URL=https://git.yourdomain.com
GITEA_TOKEN=your_token_here
GITEA_WEBHOOK_SECRET=your_webhook_secret_here
```

### 5. AWS Account (Optional - Serverless)

```bash
# Only needed for Lambda functions
# 1. Sign up at https://aws.amazon.com
# 2. Create IAM user with Lambda permissions
# 3. Get access keys

# Add to .env (optional)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
```

---

## ⚙️ Coolify Server Setup

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
Build Pack: Dockerfile  ← Choose this!
```

### Step 3: Set Environment Variables in Coolify

In Coolify → Project → Environment Variables, add:

```bash
# Core Database
CORE_SUPABASE_URL=https://your-project.supabase.co
CORE_SUPABASE_ANON_KEY=your_core_anon_key

# Voice Generation
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Gitea (if using)
GITEA_URL=https://git.yourdomain.com
GITEA_TOKEN=your_gitea_token
```

### Step 4: Deploy

1. Push your code to Git
2. Coolify automatically:
   - ✅ Pulls your code
   - ✅ Builds the Docker container
   - ✅ Deploys your application
   - ✅ Sets up health monitoring

---

## 🎵 Voice System Setup

### Daily Voice Messages

Once deployed, your system will send personalized voice messages at 7 AM including:

- ✅ **Daily Planning**: Tasks and priorities
- ✅ **Affirmations**: Motivational messages
- ✅ **Health Insights**: Wellness reminders
- ✅ **Productivity Tips**: Optimization suggestions

### CI/CD Voice Notifications

The system provides voice updates for:
- ✅ **Deployment Success**: "Version 1.2.3 deployed successfully"
- ✅ **Build Failures**: Immediate failure notifications
- ✅ **System Status**: Health check summaries

---

## 🗄️ Database Setup

### Option 1: Supabase Free Tier (Recommended)

```sql
-- Database schema is created automatically
-- No manual setup required
-- Free tier: 500MB storage
```

### Option 2: Self-Hosted Supabase (Advanced)

```bash
# Deploy Supabase via Coolify
# 1. Add Supabase resource in Coolify
# 2. Configure database settings
# 3. Update environment variables
```

### Database Tables Created

- ✅ `daily_summaries` - Daily activity logs
- ✅ `shadow_work_data` - Personal growth tracking
- ✅ `journal_entries` - Daily reflections
- ✅ `tasks` - Task management
- ✅ `voice_messages` - Voice generation logs
- ✅ `data_sync_log` - Synchronization tracking

---

## 🔄 CI/CD Pipeline Setup

### Gitea Webhook Configuration

1. Go to your repository in Gitea
2. **Settings** → **Webhooks** → **Add Webhook**
3. Configure:
   ```yaml
   Target URL: https://your-lambda-webhook-url.amazonaws.com/prod/webhook/gitea
   Content Type: application/json
   Secret: your_webhook_secret
   Events: Push, Pull Request
   Active: ✅
   ```

### Automated Voice Deployments

Every git push will trigger:
1. ✅ **Code Analysis** - Lint and security checks
2. ✅ **Testing** - Automated test execution
3. ✅ **Deployment** - Server updates
4. ✅ **Voice Notification** - Success/failure alerts

---

## 📊 System Monitoring

### Health Endpoints

Once deployed, monitor your system:

```bash
# Health check
curl https://api.yourdomain.com/health

# System info
curl https://api.yourdomain.com/system/info

# Voice preview
curl https://api.yourdomain.com/voice/preview

# Monitoring status
curl https://api.yourdomain.com/monitor/status
```

### Automated Monitoring

The system includes:
- ✅ **Health Checks**: Every 30 seconds
- ✅ **Database Monitoring**: Storage and performance
- ✅ **Cost Tracking**: AWS Lambda and ElevenLabs usage
- ✅ **Error Alerts**: Automatic notifications

---

## 🚨 Troubleshooting

### Common Issues & Solutions

**❌ "Permission denied on script"**
```bash
chmod +x coolify-deploy.sh
```

**❌ "Virtual environment error"**
```bash
# Deactivate and reactivate
deactivate
source venv/bin/activate
```

**❌ "Docker build fails"**
```bash
# Clear cache and retry
docker system prune -a
docker build -t personal-system .
```

**❌ "Environment variables not loading"**
```bash
# Check .env file
cat .env
# Ensure no spaces around = signs
```

**❌ "Voice generation fails"**
```bash
# Check ElevenLabs API key
curl -H "xi-api-key: YOUR_KEY" https://api.elevenlabs.io/v1/voices
```

**❌ "Database connection fails"**
```bash
# Test Supabase connection
curl -H "apikey: YOUR_KEY" https://your-project.supabase.co/rest/v1/
```

**❌ "Coolify deployment fails"**
```bash
# Check Coolify logs
# Dashboard → Applications → personal-system-api → Logs
```

---

## 🎯 Verification Checklist

After setup, verify everything works:

### ✅ Basic Functionality
- [ ] API accessible at `https://api.yourdomain.com/health`
- [ ] System info endpoint returns correct data
- [ ] Voice preview endpoint works

### ✅ Voice Features
- [ ] ElevenLabs integration configured
- [ ] Telegram bot responds to commands
- [ ] Voice message generation works

### ✅ Database
- [ ] Supabase connection established
- [ ] Tables created successfully
- [ ] Data sync working

### ✅ Automation
- [ ] Serverless functions deployed (if using AWS)
- [ ] CI/CD pipeline active
- [ ] Monitoring alerts configured

### ✅ Coolify
- [ ] Application deployed successfully
- [ ] Environment variables loaded
- [ ] Health checks passing

---

## 📚 Next Steps

### Immediate Actions
1. ✅ **Test all endpoints** using the API
2. ✅ **Send a test voice message** via Telegram
3. ✅ **Push a code change** to test CI/CD
4. ✅ **Review monitoring dashboards**

### Daily Usage
1. ✅ **Receive daily voice messages** at 7 AM
2. ✅ **Monitor system health** via API endpoints
3. ✅ **Track costs** and usage patterns
4. ✅ **Update knowledge base** in core/identity/

### Advanced Configuration
1. ✅ **Customize voice content** in automation scripts
2. ✅ **Add new API endpoints** for specific needs
3. ✅ **Configure additional domains** in domains/
4. ✅ **Set up advanced monitoring** and alerts

---

## 💰 Cost Monitoring

| Service | Monthly Cost | Usage Tracking |
|---------|-------------|----------------|
| **Coolify Server** | $10-20 | Your existing server |
| **ElevenLabs** | $0.30 | ~10 voice messages |
| **AWS Lambda** | Free | 1M requests/month |
| **Supabase** | Free | 500MB storage |
| **Telegram** | Free | Unlimited messages |
| **Total** | ~$10-21 | Enterprise features |

---

## 🎉 You're All Set!

**Your personal system is now live with:**

- 🎵 **Voice-powered daily planning**
- 🚀 **Automated CI/CD deployments**
- 🗄️ **Smart multi-tier database**
- 📊 **Real-time monitoring**
- 🔒 **Privacy-first architecture**

**Welcome to your automated future!** 🎯✨

---

*Need help? Check the [troubleshooting section](#troubleshooting) or visit our [documentation](COOLIFY_DEPLOYMENT_COMPLETE.md)*
