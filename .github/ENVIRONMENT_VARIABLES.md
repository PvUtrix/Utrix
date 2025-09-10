# 🔐 GitHub Environment Variables Setup

This guide shows you how to set up all required environment variables in GitHub for your Personal System.

## 📋 Required GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → Repository secrets

### 🔑 Core Secrets (Required)

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications | Message @BotFather on Telegram |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Send message to bot, get from API |
| `CORE_SUPABASE_URL` | Supabase project URL | Create project at supabase.com |
| `CORE_SUPABASE_ANON_KEY` | Supabase anonymous key | From Supabase project settings |

### 🎤 Voice & AI Services (Optional)

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `ELEVENLABS_API_KEY` | ElevenLabs voice synthesis | Sign up at elevenlabs.io |
| `OPENAI_API_KEY` | OpenAI API for AI features | Get from platform.openai.com |
| `ELEVENLABS_VOICE_ID` | Voice ID for TTS | Use default: `21m00Tcm4TlvDq8ikWAM` |

### ☁️ AWS & Serverless (Optional)

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `AWS_ACCESS_KEY_ID` | AWS access key | Create IAM user in AWS Console |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | From IAM user creation |
| `AWS_REGION` | AWS region | Use: `eu-central-1` |

### 🚀 Deployment (Optional)

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `COOLIFY_URL` | Coolify instance URL | Your self-hosted Coolify |
| `COOLIFY_API_TOKEN` | Coolify API token | From Coolify dashboard |
| `COOLIFY_PROJECT_UUID` | Coolify project UUID | From Coolify project settings |
| `COOLIFY_APPLICATION_UUID` | Coolify app UUID | From Coolify application settings |

### 🔧 Development (Optional)

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `GITEA_URL` | Gitea instance URL | Your self-hosted Gitea |
| `GITEA_TOKEN` | Gitea API token | From Gitea user settings |
| `GITEA_WEBHOOK_SECRET` | Webhook secret | Generate random string |

## 🚀 Quick Setup Steps

### 1. Set Up Core Secrets

```bash
# Go to your GitHub repository
# Settings → Secrets and variables → Actions → Repository secrets
# Click "New repository secret" for each:

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Supabase Database
CORE_SUPABASE_URL=https://your-project.supabase.co
CORE_SUPABASE_ANON_KEY=your_anon_key_here
```

### 2. Test the Setup

```bash
# Push to main branch to trigger health check
git add .
git commit -m "🔧 Add GitHub Actions health monitoring"
git push origin main

# Check Actions tab in GitHub to see health check results
```

### 3. Optional Services

Add these if you want voice features, AI, or serverless functions:

```bash
# Voice Generation
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# AI Features
OPENAI_API_KEY=your_openai_key

# AWS Serverless
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=eu-central-1
```

## 🔍 How to Get Each Secret

### Telegram Bot Token
1. Message `@BotFather` on Telegram
2. Send `/newbot`
3. Follow instructions to create bot
4. Copy the token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Telegram Chat ID
1. Send a message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find your chat ID in the response

### Supabase Credentials
1. Go to [supabase.com](https://supabase.com)
2. Create new project: "personal-system-core"
3. Go to Settings → API
4. Copy Project URL and anon/public key

### ElevenLabs API Key
1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Add $5+ credits to your account
3. Go to Profile → API Key
4. Copy your API key

### OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create account and add billing
3. Go to API Keys section
4. Create new secret key

### AWS Credentials
1. Go to AWS Console → IAM
2. Create new user with programmatic access
3. Attach policy: `AWSLambdaFullAccess`
4. Copy Access Key ID and Secret Access Key

## 🏥 Health Check Integration

The GitHub Actions workflow will automatically:

- ✅ Check all configured services
- 📊 Generate health reports
- 🚨 Create issues for critical problems
- 📱 Send Telegram notifications on failures
- 📈 Track system health over time

## 🔒 Security Best Practices

1. **Never commit secrets** to your repository
2. **Use GitHub Secrets** for all sensitive data
3. **Rotate keys regularly** (every 90 days)
4. **Use least privilege** for AWS IAM users
5. **Monitor usage** in service dashboards

## 🐛 Troubleshooting

### Health Check Fails
- Check if all required secrets are set
- Verify secret values are correct
- Check service status (Supabase, Telegram, etc.)
- Review GitHub Actions logs

### Missing Environment Variables
- Ensure secrets are set in GitHub repository settings
- Check secret names match exactly (case-sensitive)
- Verify repository has Actions enabled

### Service Connection Issues
- Test API keys manually first
- Check service status pages
- Verify network connectivity
- Review rate limits and quotas

## 📊 Monitoring Dashboard

Once set up, you can:

1. **View health reports** in GitHub Actions artifacts
2. **Monitor trends** over time
3. **Get notifications** for issues
4. **Track component status** automatically

The system will run health checks:
- ⏰ Every hour automatically
- 🔄 On every push/PR
- 🎯 On manual trigger
- 🚨 With failure notifications

---

*Your Personal System is now configured with GitHub's secure environment variable management!* 🔐✨

