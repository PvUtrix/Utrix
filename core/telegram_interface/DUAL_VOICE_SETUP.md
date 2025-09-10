# 🎤 Dual Voice Transcription Setup

## Overview
Your bot now supports **dual voice transcription services** with ElevenLabs Scribe as the primary service and OpenAI Whisper as the fallback! This provides the best of both worlds - industry-leading accuracy from ElevenLabs with reliable fallback from OpenAI.

## 🎯 Benefits
- ✅ **ElevenLabs Scribe** - Industry-leading accuracy (98%+ in major languages)
- ✅ **OpenAI Whisper Fallback** - Reliable backup when ElevenLabs is unavailable
- ✅ **99 Languages Support** - ElevenLabs supports 99 languages
- ✅ **Smart Processing** - Health, learning, tasks, notes recognition
- ✅ **Cost Optimization** - ElevenLabs free tier + OpenAI fallback
- ✅ **Automatic Switching** - Seamless fallback when needed

## 🏗️ Architecture

```
Telegram Bot → ElevenLabs Scribe (Primary) → Smart Processing
                    ↓ (if fails/unavailable)
                OpenAI Whisper (Fallback) → Smart Processing
```

### Service Priority:
1. **ElevenLabs Scribe** - Tried first for all voice messages
2. **OpenAI Whisper** - Used if ElevenLabs fails or hits limits

## 🚀 Quick Setup

### 1. Configure API Keys

Update your `config.yaml`:

```yaml
# ElevenLabs Configuration (Primary)
elevenlabs:
  api_key: "sk_9382e4b7a49fa13e8334898360f9e3bd75ee67cfb27492fc"  # Your ElevenLabs API key
  enable_speech_to_text: true  # Set to true to use ElevenLabs Scribe
  enable_text_to_speech: false  # Set to true for TTS features

# OpenAI Configuration (Fallback)
openai:
  api_key: "your_openai_api_key_here"  # Your OpenAI API key for Whisper
  model: "whisper-1"  # Whisper model to use
  max_file_size: 25  # Maximum audio file size in MB
  supported_formats: ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
  enable_voice_transcription: true  # Set to true to enable OpenAI fallback
```

### 2. Get Your API Keys

#### ElevenLabs API Key
1. Go to [ElevenLabs.io](https://elevenlabs.io)
2. Sign up for a free account
3. Go to your [Profile Settings](https://elevenlabs.io/app/settings/api-keys)
4. Copy your API key (starts with `sk_`)

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Create a new API key

### 3. Test the Setup

1. **Restart your bot**:
   ```bash
   cd core/telegram_interface
   python3 main.py
   ```

2. **Send a voice message** saying: **"I took 8500 steps today"**

3. **Expected response**:
   ```
   🎤 Voice Message Transcribed (ElevenLabs Scribe):
   "I took 8500 steps today"
   
   ✅ Health Data Logged
   Steps: 8500
   ```

## 💰 Cost Comparison

### ElevenLabs Scribe (Primary)
- **Free Tier**: 2.5 hours/month (free)
- **Starter**: $5/month for 12.5 hours
- **Creator**: $11/month for 62.5 hours
- **Cost per hour**: $0.40 (after free tier)

### OpenAI Whisper (Fallback)
- **Cost**: $0.006 per minute of audio
- **Cost per hour**: $0.36

### Your Usage Estimate
- **1000 voice messages/month** (30 seconds each):
  - ElevenLabs: Free (within 2.5 hour limit)
  - OpenAI fallback: $3.00/month (if needed)

**Total estimated cost: $0-3.00/month**

## 🔧 Configuration Options

### Enable Both Services (Recommended)
```yaml
elevenlabs:
  enable_speech_to_text: true
openai:
  enable_voice_transcription: true
```

### ElevenLabs Only
```yaml
elevenlabs:
  enable_speech_to_text: true
openai:
  enable_voice_transcription: false
```

### OpenAI Only
```yaml
elevenlabs:
  enable_speech_to_text: false
openai:
  enable_voice_transcription: true
```

## 🧪 Testing

### Test ElevenLabs Scribe
Send a voice message and look for:
```
🎤 Voice Message Transcribed (ElevenLabs Scribe):
```

### Test OpenAI Fallback
If ElevenLabs fails, you'll see:
```
🎤 Voice Message Transcribed (OpenAI Whisper):
```

### Test Smart Processing
Try these voice commands:
- **Health**: "I took 8500 steps today"
- **Learning**: "I learned about Python for 2 hours"
- **Tasks**: "Add task: finish project"
- **Notes**: "Note: great idea about automation"

## 🛠️ Troubleshooting

### Common Issues

1. **ElevenLabs Not Working**:
   - Check API key is correct
   - Verify account has credits
   - Check file size (max 25MB)

2. **OpenAI Fallback Not Working**:
   - Check OpenAI API key
   - Verify account has credits
   - Check file format is supported

3. **Both Services Failing**:
   - Check internet connection
   - Verify API keys are valid
   - Check audio file quality

### Debug Mode
Enable debug logging:
```yaml
logging:
  level: "DEBUG"
```

## 📊 Service Comparison

| Feature | ElevenLabs Scribe | OpenAI Whisper |
|---------|------------------|----------------|
| **Accuracy** | 98%+ (industry-leading) | 95%+ (very good) |
| **Languages** | 99 languages | 99+ languages |
| **Speed** | Fast | Fast |
| **Cost** | $0.40/hour | $0.36/hour |
| **Free Tier** | 2.5 hours/month | Pay-per-use |
| **File Size** | 25MB max | 25MB max |
| **Formats** | MP3, WAV, M4A, etc. | MP3, WAV, M4A, etc. |

## 🔄 Switching Services

### Force ElevenLabs Only
```yaml
elevenlabs:
  enable_speech_to_text: true
openai:
  enable_voice_transcription: false
```

### Force OpenAI Only
```yaml
elevenlabs:
  enable_speech_to_text: false
openai:
  enable_voice_transcription: true
```

### Disable Voice Transcription
```yaml
elevenlabs:
  enable_speech_to_text: false
openai:
  enable_voice_transcription: false
```

## 🚀 Advanced Features

### Custom Processing
You can extend the voice processing to:
- Add custom voice command recognition
- Integrate with other AI services
- Add voice emotion detection
- Implement custom health metrics

### Multiple Languages
Both services support multiple languages:
- **ElevenLabs**: 99 languages with excellent accuracy
- **OpenAI**: 99+ languages with good accuracy

### Real-time Processing
- **ElevenLabs**: Currently batch processing (real-time coming soon)
- **OpenAI**: Batch processing

## 📝 Next Steps

1. **Configure** both API keys in your config
2. **Test** with sample voice messages
3. **Monitor** which service is being used
4. **Optimize** based on your usage patterns
5. **Scale** as your usage grows

## 🎉 Success!

Your bot now has enterprise-grade dual voice transcription capabilities with:
- **Industry-leading accuracy** from ElevenLabs Scribe
- **Reliable fallback** from OpenAI Whisper
- **Smart command processing** for all your daily operations
- **Cost-effective** pricing with free tiers

**Enjoy your enhanced voice-powered personal system! 🎤✨**

