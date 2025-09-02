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
./deployment/coolify/coolify-deploy.sh all

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
docker build -t personal-system -f deployment/docker/Dockerfile .
docker run -p 8000:8000 --env-file .env personal-system

# Or use docker-compose (recommended)
cd deployment/docker
docker-compose up -d
```

---

## 🔧 External Services Configuration

### 1. ElevenLabs (Voice Generation)

```bash
# 1. Sign up at https://elevenlabs.io
# 2. Add credits ($5 minimum)
# 3. Get your API key from profile settings
```
