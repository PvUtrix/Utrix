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
