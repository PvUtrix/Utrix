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
