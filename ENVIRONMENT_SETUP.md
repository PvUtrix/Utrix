# 🔧 Environment Configuration Guide

Complete guide to setting up all environment variables for your Personal System.

## 📋 Quick Setup

1. **Copy the template**:
   ```bash
   cp .env.template .env
   ```

2. **Edit with your values**:
   ```bash
   nano .env
   ```

3. **Test the configuration**:
   ```bash
   source venv/bin/activate
   python -c "import os; print('✅ Environment loaded successfully!' if os.getenv('ELEVENLABS_API_KEY') else '❌ Missing ElevenLabs key')"
   ```

---

## 🔑 Required Environment Variables

### Core Database (Supabase Free Tier)

```bash
# Get these from https://supabase.com
CORE_SUPABASE_URL=https://your-project.supabase.co
CORE_SUPABASE_ANON_KEY=your_core_anon_key_here
```

**How to get Supabase credentials:**
1. Sign up at https://supabase.com
2. Create new project: "personal-system-core"
3. Go to Settings → API
4. Copy Project URL and anon/public key

---

### Voice Generation (ElevenLabs)

```bash
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel voice (recommended)
```

**How to get ElevenLabs credentials:**
1. Sign up at https://elevenlabs.io
2. Add $5+ credits to your account
3. Go to Profile → API Key
4. Copy your API key

**Voice Options:**
- `21m00Tcm4TlvDq8ikWAM` - Rachel (warm, professional)
- `29vD33N1CtxCmqQRPOHJ` - Drew (friendly, energetic)
- `2EiwWnXFnvU5JabPnv8n` - Clyde (deep, authoritative)

---

### Telegram Bot (Notifications)

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

**How to get Telegram credentials:**
1. Message `@BotFather` on Telegram
2. Send `/newbot` and follow instructions
3. Save the bot token
4. Send a message to your bot
5. Get chat ID: `curl "https://api.telegram.org/bot<TOKEN>/getUpdates"`

---

### CI/CD Configuration (Gitea/GitHub)

```bash
GITEA_URL=https://git.yourdomain.com
GITEA_TOKEN=your_gitea_token_here
GITEA_WEBHOOK_SECRET=your_webhook_secret_here
```

**How to get Gitea credentials:**
1. Create repository in Gitea
2. Go to Settings → Applications → Generate Token
3. Copy the token
4. Repository URL format: `https://git.yourdomain.com/username/repo`

---

### AWS Lambda (Optional)

```bash
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
```

**How to get AWS credentials:**
1. Sign up at https://aws.amazon.com
2. Go to IAM → Users → Create user
3. Attach `AWSLambda_FullAccess` policy
4. Create access keys
5. Download or copy the keys

---

## 📝 Complete .env Template

```bash
# ===========================================
# Personal System Environment Configuration
# ===========================================

# Core Database (Supabase Free Tier - Required)
CORE_SUPABASE_URL=https://your-project.supabase.co
CORE_SUPABASE_ANON_KEY=your_core_anon_key_here

# Main Database (Self-hosted Supabase - Optional)
MAIN_SUPABASE_URL=http://supabase:54321
MAIN_SUPABASE_ANON_KEY=your_main_anon_key_here

# Voice Generation (ElevenLabs - Required)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Telegram Bot (Notifications - Required)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# CI/CD (Gitea/GitHub - Optional)
GITEA_URL=https://git.yourdomain.com
GITEA_TOKEN=your_gitea_token_here
GITEA_WEBHOOK_SECRET=your_webhook_secret_here

# AWS Lambda (Optional)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1

# Coolify (Optional)
COOLIFY_URL=https://coolify.yourdomain.com
COOLIFY_API_TOKEN=your_coolify_token_here

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
```

---

## ✅ Verification Commands

### Test All Services

```bash
# Test ElevenLabs
curl -H "xi-api-key: $ELEVENLABS_API_KEY" https://api.elevenlabs.io/v1/voices

# Test Telegram
curl "https://api.telegram.org/bot$ELEVENLABS_API_KEY/getMe"

# Test Supabase
curl -H "apikey: $CORE_SUPABASE_ANON_KEY" $CORE_SUPABASE_URL/rest/v1/
```

### Python Environment Test

```bash
# Activate virtual environment
source venv/bin/activate

# Test imports
python -c "from automation.serverless.voice_content_generator import VoiceContentGenerator; print('✅ Voice generator OK')"
python -c "from automation.serverless.elevenlabs_tts import ElevenLabsTTS; print('✅ ElevenLabs OK')"
```

---

## 🔒 Security Best Practices

### File Permissions
```bash
# Secure .env file
chmod 600 .env

# Ensure it's in .gitignore
echo ".env" >> .gitignore
```

### API Key Rotation
- Rotate ElevenLabs keys every 3 months
- Use separate tokens for different environments
- Monitor usage and set up alerts

### Environment Separation
- Use different credentials for development/production
- Never commit secrets to version control
- Use environment-specific configuration

---

## 🚨 Common Issues

### "Environment variable not found"
```bash
# Check if .env is loaded
cat .env | grep ELEVENLABS_API_KEY

# Reload environment
source .env
```

### "Permission denied"
```bash
# Fix file permissions
chmod 644 .env
chmod 755 coolify-deploy.sh
```

### "Invalid API key"
```bash
# Test specific service
curl -H "xi-api-key: YOUR_KEY" https://api.elevenlabs.io/v1/voices
```

---

## 📊 Cost Monitoring

Track your usage to stay within free tiers:

| Service | Free Tier | Cost after |
|---------|-----------|------------|
| Supabase | 500MB | $0.125/GB |
| ElevenLabs | 10,000 chars | $0.30/1K chars |
| AWS Lambda | 1M requests | $0.20/1M requests |
| Telegram | Unlimited | Free |

---

## 🎯 Next Steps

1. ✅ **Configure all environment variables**
2. ✅ **Test each service individually**
3. ✅ **Run the deployment script**
4. ✅ **Push to trigger Coolify deployment**
5. ✅ **Monitor your voice messages at 7 AM**

---

## 💡 Pro Tips

- **Backup your .env file** securely
- **Use strong, unique API keys**
- **Monitor usage regularly** to avoid unexpected costs
- **Test in development** before deploying to production
- **Keep credentials updated** and rotate regularly

---

*Environment configured? Run `./coolify-deploy.sh all` to deploy! 🚀*
