# 📅 Daily Functions

Daily automation functions for your personal system.

## 📁 Contents

- `daily_summary_lambda.py` - Generate daily health/productivity/finance summary
- `daily_voice_lambda.py` - Convert daily summaries to voice messages
- `daily_projection_calculator.py` - Calculate daily projections and trends

## 🎯 Purpose

These functions handle daily automation tasks that run on a schedule:

- **Daily Summaries**: Generate comprehensive daily reports
- **Voice Generation**: Convert text summaries to audio
- **Projections**: Calculate trends and future projections

## ⏰ Schedule

- **Daily Summary**: Runs daily at 12 PM UTC
- **Daily Voice**: Runs daily at 7 AM UTC  
- **Projection Calculator**: Runs daily at 6 AM UTC

## 🔧 Configuration

All functions use environment variables for configuration:

```bash
# Core Database
CORE_SUPABASE_URL=your_supabase_url
CORE_SUPABASE_ANON_KEY=your_supabase_key

# Voice Services
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id

# Notifications
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 🚀 Usage

### Local Testing

```bash
# Test daily summary
serverless invoke local --function daily-summary

# Test voice generation
serverless invoke local --function daily-voice

# Test projection calculator
serverless invoke local --function daily-projection
```

### Deployment

```bash
# Deploy all daily functions
serverless deploy --function daily-summary
serverless deploy --function daily-voice
serverless deploy --function daily-projection
```

## 📊 Output

- **Daily Summary**: JSON summary sent to Telegram
- **Voice Messages**: MP3 audio files generated
- **Projections**: Trend data stored in database

## 🔒 Privacy

- All personal data processed locally when possible
- Sensitive data encrypted before storage
- No external analytics or tracking
