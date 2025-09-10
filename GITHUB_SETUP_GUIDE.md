# 🔐 GitHub Environment Variables Setup Guide

You're absolutely right! Using GitHub's environment variables and secrets is much better than local `.env` files. Here's your complete setup guide.

## 🎯 **Why GitHub Environment Variables Are Better**

### ✅ **Advantages:**
- **🔒 Security**: Secrets are encrypted and never exposed in code
- **🌐 Centralized**: Manage all secrets in one place
- **🔄 Automated**: Works seamlessly with GitHub Actions
- **👥 Team-friendly**: Easy to share with collaborators
- **📊 Monitoring**: Built-in health checks and notifications
- **🚫 No local files**: No risk of accidentally committing secrets

### ❌ **Problems with Local .env Files:**
- Risk of committing secrets to repository
- Hard to manage across different environments
- No centralized monitoring or validation
- Difficult to share with team members
- Manual setup required on each machine

## 🚀 **Quick Setup (5 Minutes)**

### 1. **Set Up GitHub Secrets**

Go to your repository → **Settings** → **Secrets and variables** → **Actions** → **Repository secrets**

Click **"New repository secret"** for each:

#### 🔑 **Required Secrets (Core Functionality)**
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
CORE_SUPABASE_URL=https://your-project.supabase.co
CORE_SUPABASE_ANON_KEY=your_anon_key_here
```

#### 🎤 **Optional Secrets (Enhanced Features)**
```
ELEVENLABS_API_KEY=your_elevenlabs_key
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### 2. **Test the Setup**

```bash
# Push to trigger health check
git add .
git commit -m "🔧 Add GitHub Actions health monitoring"
git push origin main

# Check Actions tab in GitHub to see results
```

### 3. **Monitor Health**

The system will automatically:
- ✅ Check all configured services every hour
- 📊 Generate health reports
- 🚨 Create GitHub issues for critical problems
- 📱 Send Telegram notifications on failures
- 📈 Track system health over time

## 🏥 **Health Monitoring Features**

### **Automated Health Checks:**
- **⏰ Hourly**: Automatic health monitoring
- **🔄 On Push/PR**: Check on every code change
- **🎯 Manual**: Trigger checks on demand
- **🚨 Alerts**: Immediate notifications for issues

### **What Gets Monitored:**
- **🤖 Telegram Bot**: Connection and functionality
- **🗄️ Supabase**: Database connectivity
- **🎤 ElevenLabs**: Voice synthesis service
- **🤖 OpenAI**: AI service availability
- **☁️ AWS**: Serverless function status
- **🚀 Coolify**: Deployment service health

### **Health Reports Include:**
- Overall system health score (0-100)
- Individual component status
- Resource usage (CPU, memory, disk)
- Network connectivity
- Automated recommendations
- Historical trends

## 📊 **Current System Status**

Based on your current setup, here's what the health dashboard shows:

### **System Overview:**
- **Overall Health Score**: 0/100 (needs GitHub secrets)
- **Memory Usage**: 84.1% (high - consider cleanup)
- **CPU Usage**: 29.3% (moderate)
- **Disk Usage**: 48.7% (good)
- **Network**: ✅ Connected

### **Component Status:**
- **Total Components**: 19
- **✅ Healthy**: 1 (HabitTracker)
- **⚠️ Warning**: 7 (mostly automation tools)
- **🔴 Critical**: 1 (GitServer)
- **❌ Errors**: 10 (missing environment variables)

## 🔧 **How to Get Each Secret**

### **Telegram Bot Token**
1. Message `@BotFather` on Telegram
2. Send `/newbot`
3. Follow instructions to create bot
4. Copy the token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### **Telegram Chat ID**
1. Send a message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find your chat ID in the response

### **Supabase Credentials**
1. Go to [supabase.com](https://supabase.com)
2. Create new project: "personal-system-core"
3. Go to Settings → API
4. Copy Project URL and anon/public key

### **ElevenLabs API Key**
1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Add $5+ credits to your account
3. Go to Profile → API Key
4. Copy your API key

### **OpenAI API Key**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create account and add billing
3. Go to API Keys section
4. Create new secret key

### **AWS Credentials**
1. Go to AWS Console → IAM
2. Create new user with programmatic access
3. Attach policy: `AWSLambdaFullAccess`
4. Copy Access Key ID and Secret Access Key

## 🛠️ **Available Tools**

### **Local Health Dashboard**
```bash
# Start interactive dashboard
./start_system_health_dashboard.sh

# Generate one-time report
python3 automation/tools/system_health_dashboard/main.py --report

# Check GitHub environment variables
python3 automation/tools/system_health_dashboard/github_health_check.py
```

### **GitHub Actions Workflow**
- **File**: `.github/workflows/health-monitor.yml`
- **Triggers**: Hourly, on push/PR, manual
- **Features**: Health checks, notifications, issue creation

### **Environment Variables Guide**
- **File**: `.github/ENVIRONMENT_VARIABLES.md`
- **Content**: Complete setup guide for all secrets

## 🚨 **Troubleshooting**

### **Health Check Fails**
1. Check if all required secrets are set in GitHub
2. Verify secret values are correct
3. Check service status (Supabase, Telegram, etc.)
4. Review GitHub Actions logs

### **Missing Environment Variables**
1. Ensure secrets are set in GitHub repository settings
2. Check secret names match exactly (case-sensitive)
3. Verify repository has Actions enabled

### **Service Connection Issues**
1. Test API keys manually first
2. Check service status pages
3. Verify network connectivity
4. Review rate limits and quotas

## 🎉 **Benefits You'll Get**

### **Immediate Benefits:**
- ✅ Secure secret management
- ✅ Automated health monitoring
- ✅ Failure notifications
- ✅ No local configuration needed

### **Long-term Benefits:**
- 📊 Historical health trends
- 🔄 Automated issue creation
- 📱 Telegram notifications
- 🚀 Easy deployment
- 👥 Team collaboration

## 📈 **Next Steps**

1. **Set up GitHub secrets** (5 minutes)
2. **Push to trigger health check** (1 minute)
3. **Monitor health reports** (ongoing)
4. **Add optional services** (as needed)
5. **Enjoy automated monitoring** (forever!)

---

**Your Personal System is now ready for GitHub-based environment variable management!** 🎉

The system will automatically monitor all your components and notify you of any issues, all while keeping your secrets secure in GitHub's encrypted storage.

