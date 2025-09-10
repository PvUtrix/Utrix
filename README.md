# 🎯 Personal System - Voice-Enabled Automation Platform

A **privacy-first, AI-powered system** for managing personal knowledge, projects, and automation across all life domains with **voice notifications** and **serverless deployment**.



[![Deploy with Coolify](https://img.shields.io/badge/Deploy-Coolify-blue)](deployment/coolify/deployment-complete.md)
[![Voice Enabled](https://img.shields.io/badge/Voice-ElevenLabs-green)](services/serverless-functions/docs/VOICE_README.md)
[![CI/CD Ready](https://img.shields.io/badge/CI/CD-Gitea-orange)](services/serverless-functions/docs/CICD_SETUP.md)

## 🎤 What Makes This Special

- **🎵 Voice Messages**: Daily personalized planning via ElevenLabs
- **🚀 Serverless**: AWS Lambda functions for cost-effective automation
- **🗄️ Multi-Tier Database**: Smart data management (Core/Main/Archive)
- **🔄 CI/CD Pipeline**: Voice-enabled automated deployments
- **🐳 Coolify Ready**: One-click deployment to your own server
- **🔒 Privacy First**: Local data stays local, encrypted options available
- **📊 Real Data Only**: No fake/random data - all metrics must come from actual sources
- **🔌 Integration Ready**: [Roadmap](automation/INTEGRATION_ROADMAP.md) for connecting real data sources

## 🚀 Quick Start (4 Options)

### Option 1: GitHub Actions (Recommended for GitHub Users)

```bash
# 1. Fork or clone this repository
git clone https://github.com/yourusername/personal-system.git
cd personal-system

# 2. Set up GitHub Secrets
# Go to: Settings → Secrets and variables → Actions → Repository secrets
# Add required secrets (see .github/ENVIRONMENT_VARIABLES.md)

# 3. Push to trigger health monitoring
git add .
git commit -m "🔧 Add GitHub Actions health monitoring"
git push origin main

# 4. Check Actions tab for health reports
```

**Benefits:**
- ✅ Secure environment variable management
- ✅ Automated health monitoring
- ✅ Failure notifications via Telegram
- ✅ No local .env files needed

### Option 2: Coolify Deployment

```bash
# 1. Clone and setup
git clone https://git.yourdomain.com/yourusername/personal-system.git
cd personal-system

# 2. Run automated deployment
./deployment/coolify/coolify-deploy.sh all

# 3. Configure environment variables
nano .env  # Add your API keys

# 4. Push to trigger deployment
git add .
git commit -m "🚀 Production deployment"
git push origin main
```

**That's it!** Coolify handles the rest automatically.

### Option 3: Local Development

```bash
# 1. Setup environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
nano .env  # Add your credentials

# 4. Run locally
python main.py
```

### Option 3: Docker Local

```bash
# Build and run with Docker
docker build -t personal-system -f deployment/docker/Dockerfile .
docker run -p 8000:8000 --env-file .env personal-system

# Or use docker-compose
cd deployment/docker
docker-compose up -d
```

## 📱 API Endpoints

Once deployed, your system provides:

- `GET /health` - System health check
- `GET /voice/preview` - Preview today's voice content
- `POST /voice/generate` - Generate voice message
- `GET /monitor/status` - Data monitoring status
- `GET /system/info` - System information

## 🎵 Voice Features

### Daily Voice Messages (7 AM)
- Personalized daily planning
- Affirmations and motivation
- Task prioritization
- Health and productivity insights

### CI/CD Notifications
- Deployment status updates
- Version announcements
- Build success/failure alerts

## 📊 Data Collection Rules

### 🚫 No Fake Data Policy
- **All metrics must come from real sources** - no random generation
- **Health data**: Connect to actual fitness trackers, health apps, or manual input
- **Productivity data**: Integrate with task managers, time trackers, git repositories
- **Learning data**: Connect to course platforms, reading apps, note-taking systems
- **Finance data**: Integrate with banking APIs, budget apps, or manual tracking

### 🔌 Required Integrations (To Be Implemented)
- **Health**: Apple Health, Google Fit, Fitbit, or manual input forms
- **Productivity**: Todoist, Notion, RescueTime, Toggl, GitHub
- **Learning**: Coursera, Udemy, Notion, Obsidian, or manual progress tracking
- **Finance**: Banking APIs, YNAB, Mint, or manual expense tracking

### 📝 Manual Input Fallback
When integrations aren't available, provide manual input forms rather than generating fake data.

### ✅ Current Status
- **Fake data generation**: ❌ DISABLED
- **Real data sources**: 🔌 NOT CONNECTED
- **Manual input forms**: 📝 EXAMPLE PROVIDED
- **Integration roadmap**: 📋 CREATED

## 🏗️ Architecture
│ • Supabase DB   │    │ • CI/CD Pipeline│    │ • Telegram Bot  │
│ • Gitea Repo    │    │ • Data Sync      │    │ • Gitea Webhook │
│ • Monitoring    │    │ • Webhook Handler│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
personal-system/
├── 📁 core/           # Your identity & knowledge base
│   ├── 📁 identity/   # values.md, goals.md, vision.md
│   └── 📁 telegram_interface/ # Primary user interface
├── 📁 domains/        # Life domains (health, finance, career)
├── 📁 projects/       # Active projects & startups
├── 📁 automation/     # Scripts & serverless functions
│   └── 📁 serverless/ # Lambda functions & configs
├── 📁 privacy/        # Encrypted & local private data
├── 📁 resources/      # Templates & learning materials
├── 🐳 Dockerfile      # Container configuration
├── 🐳 docker-compose.yml # Local development
├── ⚙️ coolify-deploy.sh # Deployment automation
└── 🎯 main.py        # FastAPI application
```

## 🔧 Configuration Required

### Environment Variables (.env)

```bash
# Core Database (Supabase Free Tier - 500MB)
CORE_SUPABASE_URL=https://your-project.supabase.co
CORE_SUPABASE_ANON_KEY=your_core_anon_key

# Main Database (Self-hosted Supabase)
MAIN_SUPABASE_URL=http://supabase:54321
MAIN_SUPABASE_ANON_KEY=your_main_anon_key

# Voice Generation (ElevenLabs)
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Notifications (Telegram)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# CI/CD (Gitea)
GITEA_URL=https://git.yourdomain.com
GITEA_TOKEN=your_gitea_token
GITEA_WEBHOOK_SECRET=your_webhook_secret

# Coolify API
COOLIFY_API_TOKEN=your_coolify_token
```

### External Services Setup

1. **ElevenLabs Account**: Get API key for voice generation
2. **Telegram Bot**: Create bot and get token/chat ID
3. **Supabase**: Free tier for core data, optional self-hosted
4. **Gitea**: For CI/CD (optional, can use GitHub/GitLab)
5. **AWS Account**: For Lambda functions (optional)

## 🎯 Features

### ✅ Voice & Communication
- Daily personalized voice messages
- CI/CD deployment notifications
- **Primary Telegram Interface** - Main system interaction gateway
- ElevenLabs text-to-speech

### ✅ Database & Data Management
- Multi-tier database architecture
- Automatic data lifecycle management
- Privacy-focused data handling
- Backup and synchronization

### ✅ Automation & CI/CD
- Serverless function deployment
- Automated testing and deployment
- Voice-enabled CI/CD pipeline
- Cost monitoring and optimization

### ✅ Personal Knowledge Management
- Identity and values tracking
- Project portfolio management
- Learning and skill development
- Health and finance tracking

## 📊 System Monitoring

### Health Checks
- API endpoint monitoring
- Database connectivity
- External service status
- Voice generation availability

### Cost Tracking
- AWS Lambda usage
- ElevenLabs voice generation costs
- Database storage monitoring
- Monthly cost summaries

## 🚨 Troubleshooting

### Common Issues

**"Virtual environment error"**
```bash
# Deactivate and reactivate
deactivate
source venv/bin/activate
```

**"Permission denied on script"**
```bash
chmod +x coolify-deploy.sh
```

**"Docker build fails"**
```bash
# Clear Docker cache
docker system prune -a
```

**"Environment variables not loading"**
```bash
# Check .env file exists and has correct values
cat .env
```

## 📚 Documentation

### 📖 User Guides
- [🚀 Getting Started](docs/guides/getting_started.md)
- [📚 Usage Guide](docs/usage/getting-started.md)
- [📖 Intro Management](docs/usage/intro-management.md)

### 🛠️ Setup & Deployment
- [⚙️ Initial Setup](docs/setup/initial-setup.md)
- [🌍 Environment Setup](docs/setup/environment-setup.md)
- [🐳 Gitea Setup](docs/setup/gitea-setup.md)
- [🚀 Gitea + Coolify Setup](docs/setup/gitea-coolify-setup.md)
- [🗄️ Shared Database Setup](docs/setup/shared-database-setup.md)
- [⚡ Quick Start Gitea](docs/setup/quick-start-gitea.md)

### 🔌 API & Integration
- [📡 API Reference](docs/api/README.md)

### 👥 Contributing
- [📋 Guidelines](docs/contributing/guidelines.md)

### 📚 Legacy Documentation
- [🚀 Complete Deployment Guide](deployment/coolify/deployment-complete.md)
- [🎵 Voice System Setup](services/serverless-functions/docs/VOICE_README.md)
- [🔄 CI/CD Pipeline](services/serverless-functions/docs/CICD_SETUP.md)
- [🗄️ Multi-Tier Database](services/serverless-functions/docs/MULTI_TIER_README.md)
- [📊 System Monitoring](services/serverless-functions/README.md)

## 💰 Cost Breakdown

| Service | Monthly Cost | Details |
|---------|-------------|---------|
| **Coolify Server** | $10-20 | Your existing server |
| **ElevenLabs** | $0.30 | ~10 voice messages |
| **AWS Lambda** | Free | 1M requests/month |
| **Supabase** | Free | 500MB storage |
| **Telegram** | Free | Unlimited messages |
| **Total** | ~$10-21 | Enterprise features |

## 🤝 Contributing

This system is designed to evolve with you:
- Add new domains in `domains/`
- Create custom automation scripts
- Build project templates
- Extend the API with new endpoints

## 📄 License

This system is open source and available for anyone to use and modify. See [LICENSE](LICENSE) for details.

---

## 🎉 Ready to Get Started?

**Choose your deployment method:**

1. **🚀 Coolify (Recommended)**: `./coolify-deploy.sh all`
2. **💻 Local Development**: `python main.py`
3. **🐳 Docker**: `docker-compose up`

**Your personal system is about to become your most powerful productivity tool!** 🎯✨

---

*Remember: This is YOUR system. It learns from you, adapts to you, and works for YOU.*
