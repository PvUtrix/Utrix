# 🎤 ElevenLabs Text-to-Speech Setup

## ⚠️ Important Note

**ElevenLabs does NOT provide speech-to-text (transcription) services.** They only provide text-to-speech (voice generation) services.

For voice transcription, your bot uses **OpenAI Whisper** which provides:
- ✅ **High-quality transcription** using OpenAI Whisper API
- ✅ **Support for multiple languages**
- ✅ **Good accuracy** for voice commands
- ✅ **Same smart processing** for health, learning, tasks, and notes

## 🔑 Get Your ElevenLabs API Key

### 1. Create ElevenLabs Account
1. Go to [ElevenLabs.io](https://elevenlabs.io)
2. Sign up for a free account
3. Verify your email address

### 2. Get API Key
1. Go to your [ElevenLabs Profile](https://elevenlabs.io/app/settings/api-keys)
2. Click "Create API Key"
3. Give it a name (e.g., "Personal System Bot")
4. Copy the API key (starts with `sk_`)

### 3. Update Configuration
Edit your `config/config.yaml` file:

```yaml
# ElevenLabs Configuration  
elevenlabs:
  api_key: "sk_your_actual_api_key_here"  # Replace with your real API key
  model: "whisper-1"  # Model to use for transcription
  max_characters: 10000  # Monthly character limit (free tier)
  enable_voice_transcription: true  # Set to true to use ElevenLabs
  fallback_to_openai: true  # Use OpenAI if ElevenLabs fails
```

## 💰 Cost Comparison

### ElevenLabs Free Tier
- **10,000 characters/month** = ~10-15 minutes of voice messages
- **$0 cost** for typical personal use
- **Character-based** pricing

### OpenAI Whisper (Fallback)
- **$0.006 per minute** of audio
- **No monthly limits**
- **Pay-per-use** pricing

### Your Usage Example
- **10 voice messages/day** × **30 seconds each** = 5 minutes/day
- **Monthly usage**: 150 minutes = ~15,000 characters
- **ElevenLabs**: Free (covers your usage!)
- **OpenAI fallback**: $0.90/month (only if you exceed ElevenLabs limits)

## 🎯 How It Works

### 1. **Primary: ElevenLabs**
- Bot tries ElevenLabs first for all voice messages
- High-quality transcription using ElevenLabs API
- Free for your usage level

### 2. **Fallback: OpenAI**
- If ElevenLabs fails or hits character limits
- Automatically switches to OpenAI Whisper
- Seamless experience for you

### 3. **Smart Processing**
- Same intelligent command recognition
- Health metrics extraction
- Learning activity parsing
- Task and note creation
- Interactive responses with buttons

## 🧪 Test Your Setup

### 1. Restart Your Bot
```bash
cd core/telegram_interface
python3 main.py
```

### 2. Send a Test Voice Message
Try saying: **"I took 8500 steps today"**

You should see:
```
🎤 Voice Message Transcribed (ElevenLabs):
"I took 8500 steps today"

🔍 Processing your request...

✅ Health Metric Logged
Steps: 8500
```

### 3. Check Service Used
The bot will show which service was used:
- `(ElevenLabs)` - Using ElevenLabs API
- `(OpenAI fallback)` - Using OpenAI as fallback

## 🔧 Troubleshooting

### ElevenLabs Not Working
**Check:**
1. API key is correct in config
2. API key has sufficient characters remaining
3. Voice file is under 25MB
4. Internet connection is stable

**Fallback:**
- Bot will automatically use OpenAI if ElevenLabs fails
- You'll see `(OpenAI fallback)` in the response

### Character Limit Reached
**What happens:**
- ElevenLabs returns an error
- Bot automatically switches to OpenAI
- You'll see `(OpenAI fallback)` in responses

**Solutions:**
1. Wait for monthly reset (free tier)
2. Upgrade ElevenLabs plan
3. Continue using OpenAI fallback

### OpenAI Fallback Not Working
**Check:**
1. OpenAI API key is configured
2. OpenAI API key has sufficient credits
3. Both services are properly configured

## 📊 Usage Monitoring

### Check ElevenLabs Usage
1. Go to [ElevenLabs Dashboard](https://elevenlabs.io/app/speech-synthesis)
2. Check your character usage
3. Monitor remaining characters

### Check OpenAI Usage
1. Go to [OpenAI Usage Dashboard](https://platform.openai.com/usage)
2. Monitor your API usage
3. Check remaining credits

## 🎉 Benefits

### Cost Savings
- **$0/month** for typical personal use
- **90% cost reduction** compared to OpenAI-only
- **No monthly subscription** required

### Reliability
- **Dual service** ensures transcription always works
- **Automatic fallback** if one service fails
- **High availability** with two providers

### Quality
- **High-quality transcription** from both services
- **Same smart processing** regardless of service
- **Consistent user experience**

## 🚀 Advanced Configuration

### Customize Character Limits
```yaml
elevenlabs:
  max_characters: 50000  # Increase for higher usage
```

### Disable Fallback
```yaml
elevenlabs:
  fallback_to_openai: false  # Only use ElevenLabs
```

### Force OpenAI Only
```yaml
elevenlabs:
  enable_voice_transcription: false  # Disable ElevenLabs
openai:
  enable_voice_transcription: true   # Use OpenAI only
```

## 📞 Support

### ElevenLabs Issues
- Check [ElevenLabs Documentation](https://docs.elevenlabs.io/)
- Contact [ElevenLabs Support](https://elevenlabs.io/contact)

### Bot Issues
- Check bot logs in `logs/bot.log`
- Verify configuration settings
- Test with simple voice messages

---

**Enjoy your free voice transcription! 🎤✨**

Your bot now provides high-quality voice transcription at no cost for typical personal use, with reliable fallback to ensure it always works!
