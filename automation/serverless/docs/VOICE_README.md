# 🎤 Daily Voice Messages with ElevenLabs

A serverless system that sends personalized daily voice messages via Telegram using ElevenLabs' high-quality text-to-speech.

## 🎯 Overview

Every morning at 7 AM UTC (adjustable), you'll receive a **3-minute personalized voice message** containing:

- **Today's priorities** from your task list
- **Daily affirmations** and positive reinforcement
- **Weekly context** and progress insights
- **Personalized guidance** based on your data
- **Motivational content** to start your day right

## 🎵 Voice Features

### ElevenLabs Integration
- **High-quality voices**: Natural, human-like speech
- **Multiple voice options**: Rachel (default), Drew, Clyde, Paul, etc.
- **Voice settings**: Optimized for clarity and engagement
- **Cost-effective**: ~$0.00015 per character

### Message Structure (2.5 minutes)
```
🎤 "Good morning! Here's your personalized plan for today."

📋 "Your main priorities today are: [top 3 tasks]"

📊 "Looking at your week so far, you're maintaining good energy..."

💪 "Remember: [personalized affirmations]"

✨ "You've got this! Have a wonderful and productive day."
```

## 🚀 Quick Setup

### 1. Get ElevenLabs API Key
```bash
# Sign up at https://elevenlabs.io
# Get your API key from the dashboard
export ELEVENLABS_API_KEY="your_api_key_here"
```

### 2. Choose Your Voice
```bash
# List available voices
cd automation/serverless
python3 elevenlabs_tts.py voices

# Set your preferred voice ID
export ELEVENLABS_VOICE_ID="21m00Tcm4TlvDq8ikWAM"  # Rachel (default)
```

### 3. Configure Telegram
```bash
# Set your Telegram bot credentials
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

### 4. Test the System
```bash
# Preview today's message (text only)
./run.sh voice-preview

# Test ElevenLabs integration
./run.sh voice-test

# Send a test voice message
./run.sh voice-send
```

### 5. Deploy to Production
```bash
# Deploy all Lambda functions
./run.sh deploy

# Check voice message history
./run.sh voice-history
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Optional
CORE_SUPABASE_URL=your_supabase_url      # For personalized content
CORE_SUPABASE_ANON_KEY=your_supabase_key
```

### Voice Settings
```python
# Optimized settings in elevenlabs_tts.py
voice_settings = {
    "stability": 0.5,        # Voice consistency
    "similarity_boost": 0.8, # How similar to original voice
    "style": 0.0,           # Style exaggeration
    "use_speaker_boost": True  # Speaker enhancement
}
```

## 📊 Content Personalization

### Data Sources
The voice message uses your personal data to create relevant content:

1. **Tasks & Priorities**: From your active task list
2. **Health Metrics**: Energy levels and wellness insights
3. **Weekly Patterns**: Progress analysis and trends
4. **Historical Data**: Performance insights and reflections
5. **Custom Affirmations**: Personalized positive reinforcement

### Sample Message Flow
```
1. Greeting (15 sec)
   "Good morning! Here's your personalized plan for today."

2. Priorities (45 sec)
   "Your main priorities today are: Finish project proposal,
    Review quarterly goals, and Schedule team meeting."

3. Context (30 sec)
   "Looking at your week so far, you're maintaining good energy
    levels and completing about 12 tasks per day."

4. Affirmations (30 sec)
   "Remember: You are capable of achieving great things today.
    Your dedication and consistency are creating real change."

5. Closing (15 sec)
   "You've got this! Have a wonderful and productive day."
```

## 🎛️ Customization Options

### Voice Selection
```bash
# Popular ElevenLabs voices
export ELEVENLABS_VOICE_ID="21m00Tcm4TlvDq8ikWAM"  # Rachel (warm, professional)
export ELEVENLABS_VOICE_ID="29vD33N1CtxCmqQRPOHJ"  # Drew (friendly, energetic)
export ELEVENLABS_VOICE_ID="2EiwWnXFnvU5JabPnv8n"  # Clyde (deep, authoritative)
```

### Message Length Control
```python
# Adjust in voice_content_generator.py
max_words = 600  # ~2.5 minutes at 240 words/minute
```

### Scheduling
```yaml
# Adjust timing in serverless.yml
daily-voice-message:
  events:
    - schedule:
        rate: cron(0 7 * * ? *)  # 7 AM UTC (change hour as needed)
```

## 💰 Cost Analysis

### ElevenLabs Pricing
- **Free Tier**: 10,000 characters/month
- **Pay-as-you-go**: ~$0.00015 per character
- **Your Usage**: ~4,000-6,000 characters/day
- **Monthly Cost**: ~$0.60-0.90

### Total Daily Cost
- **ElevenLabs**: ~$0.006
- **AWS Lambda**: ~$0.0002 (free tier)
- **Telegram**: Free
- **Database**: Free
- **Total**: ~$0.006/day (~$0.18/month)

### Cost Optimization
- **Text compression**: Automatic content optimization
- **Caching**: Reuse common phrases
- **Batch processing**: Efficient API usage
- **Free tier limits**: Stay within ElevenLabs free tier

## 🔧 Testing & Debugging

### Local Testing
```bash
# Generate content preview (no voice)
python3 daily_voice_lambda.py preview

# Test ElevenLabs connection
python3 elevenlabs_tts.py test

# Send test message
python3 daily_voice_lambda.py send_daily
```

### Voice Quality Testing
```bash
# Generate sample audio file
python3 elevenlabs_tts.py test

# Check audio file: test_output.mp3
# Adjust voice settings if needed
```

### Troubleshooting
```bash
# Check API key
echo $ELEVENLABS_API_KEY

# Test ElevenLabs API
curl -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"

# Check Lambda logs
serverless logs --function daily-voice-message --tail
```

## 📈 Monitoring & Analytics

### Voice Message History
```bash
# View recent messages
./run.sh voice-history

# Check delivery status
./run.sh monitor
```

### Performance Metrics
- **Generation time**: < 30 seconds
- **Audio quality**: 128kbps MP3
- **Success rate**: > 99%
- **User engagement**: Track message opens

### Cost Tracking
```bash
# Monitor ElevenLabs usage
./run.sh monitor

# View cost breakdown
python3 elevenlabs_tts.py estimate --text "sample message"
```

## 🔒 Security & Privacy

### Data Protection
- **API keys**: Stored as environment variables
- **Audio files**: Temporary, not stored long-term
- **Personal data**: Used only for personalization
- **No tracking**: No analytics or usage tracking

### Access Control
- **Telegram authentication**: Bot restricted to your chat
- **Lambda permissions**: Minimal required permissions
- **Database access**: Read-only for personalization

## 🎯 Advanced Features

### Custom Affirmations
Add personalized affirmations to your database:

```sql
INSERT INTO affirmations (text, category, active)
VALUES ('You are capable of achieving great things today', 'motivation', true);
```

### Dynamic Content
- **Weather integration**: Include local weather
- **Calendar sync**: Mention upcoming events
- **Goal tracking**: Progress toward objectives
- **Habit reminders**: Personal habit nudges

### Multi-language Support
ElevenLabs supports multiple languages - easily switch voice and language.

## 🚀 Production Deployment

### Automated Schedule
```yaml
# In serverless.yml
daily-voice-message:
  handler: daily_voice_lambda.lambda_handler
  events:
    - schedule: cron(0 7 * * ? *)  # 7 AM UTC daily
```

### Error Handling
- **Retry logic**: Automatic retry on failures
- **Fallback content**: Simple message if personalization fails
- **Monitoring alerts**: Notifications for delivery failures

### Scaling Considerations
- **Concurrent users**: Lambda handles multiple users
- **Rate limiting**: ElevenLabs API rate limits
- **Cost monitoring**: Automatic cost alerts

## 🎉 Getting Started Checklist

- [ ] Sign up for ElevenLabs account
- [ ] Get API key and choose voice
- [ ] Set up Telegram bot
- [ ] Configure environment variables
- [ ] Test voice generation locally
- [ ] Deploy Lambda functions
- [ ] Set up daily schedule
- [ ] Monitor first few messages
- [ ] Adjust voice settings as needed

## 💡 Pro Tips

1. **Voice Selection**: Test different voices to find your favorite
2. **Timing**: Schedule for your optimal morning time
3. **Content Length**: Keep under 3 minutes for best engagement
4. **Personalization**: The more data you have, the better the messages
5. **Testing**: Always test new voices/settings before going live

---

## 🎤 Your Daily Voice Companion

**Start your day with purpose, motivation, and clarity.**

Your personalized voice message will be ready every morning, combining the power of AI-driven content generation with ElevenLabs' premium voice quality, all delivered seamlessly through Telegram.

**Cost**: ~$0.006/day | **Time**: 2.5 minutes | **Value**: Priceless daily motivation! 🌟
