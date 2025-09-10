# 🚀 Serverless Voice Transcription Setup

## Overview
Your bot now supports **dual voice transcription services** with both local and serverless options! 

**Local Processing**: ElevenLabs Scribe (primary) + OpenAI Whisper (fallback)
**Serverless Processing**: Same dual services running in the cloud

This gives you the flexibility to choose between local processing or cloud-based processing based on your needs.

## 🎯 Benefits
- ✅ **Reduced Local Load** - Voice processing happens in the cloud
- ✅ **Better Scalability** - Handle multiple voice messages simultaneously
- ✅ **Cost Optimization** - Pay only for actual usage
- ✅ **Reliability** - Cloud infrastructure with automatic scaling
- ✅ **Same Smart Processing** - Health, learning, tasks, notes recognition

## 🏗️ Architecture

### Local Processing
```
Telegram Bot → ElevenLabs Scribe (primary) → Smart Processing
                    ↓ (if fails)
                OpenAI Whisper (fallback) → Smart Processing
```

### Serverless Processing
```
Telegram Bot → Serverless Function → ElevenLabs Scribe (primary) → Smart Processing
                    ↓ (if fails)
                OpenAI Whisper (fallback) → Smart Processing
```

1. **Voice Message** sent to Telegram bot
2. **Audio Data** processed locally or sent to serverless function
3. **Transcription** performed by ElevenLabs Scribe (primary) or OpenAI Whisper (fallback)
4. **Smart Processing** handles health, learning, tasks, notes
5. **Response** sent back to user

## 🚀 Quick Setup

### Option 1: AWS Lambda (Recommended)

1. **Deploy the function**:
   ```bash
   cd automation/serverless/functions/voice
   ./deploy.sh
   # Choose option 1 (AWS Lambda)
   ```

2. **Upload to AWS Lambda**:
   - Create new Lambda function
   - Upload `voice-transcription.zip`
   - Set environment variable: `OPENAI_API_KEY`
   - Set timeout: 30 seconds
   - Set memory: 512MB

3. **Create API Gateway**:
   - Create REST API
   - Create POST method
   - Link to Lambda function
   - Deploy API

4. **Update bot configuration**:
   ```yaml
   serverless:
     transcription_url: "https://your-api-gateway-url.amazonaws.com/prod/voice-transcription"
     enable_serverless_transcription: true
   ```

### Option 2: Vercel

1. **Deploy the function**:
   ```bash
   cd automation/serverless/functions/voice
   ./deploy.sh
   # Choose option 2 (Vercel)
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel --prod
   ```

3. **Set environment variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key

4. **Update bot configuration**:
   ```yaml
   serverless:
     transcription_url: "https://your-vercel-app.vercel.app/voice-transcription"
     enable_serverless_transcription: true
   ```

## 🔧 Configuration

### Bot Configuration (`config.yaml`)
```yaml
# Serverless Configuration
serverless:
  transcription_url: "https://your-function-url.com/voice-transcription"
  api_key: "your_serverless_api_key"  # Optional: for authentication
  enable_serverless_transcription: true  # Set to true to enable
```

### Environment Variables (Serverless Function)
- `OPENAI_API_KEY`: Your OpenAI API key for Whisper transcription

## 💰 Cost Estimation

### AWS Lambda
- **Requests**: $0.20 per 1M requests
- **Compute**: $0.0000166667 per GB-second
- **Example**: 1000 voice messages/month = ~$0.20

### Vercel
- **Free Tier**: 100GB-hours/month
- **Pro**: $20/month for unlimited functions
- **Example**: 1000 voice messages/month = Free

### OpenAI Whisper
- **Cost**: $0.006 per minute of audio
- **Example**: 1000 messages (30s each) = $3.00/month

**Total estimated cost: $3.20/month for 1000 voice messages**

## 🧪 Testing

### Test the Serverless Function
```bash
# Encode a test audio file
base64 -i test_audio.ogg

# Send test request
curl -X POST https://your-function-url.com/voice-transcription \
  -H "Content-Type: application/json" \
  -d '{
    "audio_data": "base64_encoded_audio_here",
    "file_format": "ogg",
    "user_id": "test_user",
    "message_id": "test_message"
  }'
```

### Test with Telegram Bot
1. **Restart your bot**:
   ```bash
   cd core/telegram_interface
   python3 main.py
   ```

2. **Send a voice message** saying: **"I took 8500 steps today"**

3. **Expected response**:
   ```
   🎤 Voice Message Transcribed:
   "I took 8500 steps today"
   
   ✅ Health Data Logged
   Steps: 8500
   ```

## 🔄 Switching Between Local and Serverless

### Enable Serverless
```yaml
serverless:
  enable_serverless_transcription: true
```

### Disable Serverless (Use Local)
```yaml
serverless:
  enable_serverless_transcription: false
```

## 🛠️ Troubleshooting

### Common Issues

1. **Function Timeout**:
   - Increase Lambda timeout to 30 seconds
   - Increase Vercel function timeout

2. **Memory Errors**:
   - Increase Lambda memory to 512MB
   - Check audio file size (max 25MB)

3. **API Key Errors**:
   - Verify `OPENAI_API_KEY` is set in environment
   - Check API key permissions

4. **Audio Format Issues**:
   - Ensure audio is in supported format (OGG, MP3, WAV, M4A, WebM)
   - Check base64 encoding

5. **Network Issues**:
   - Verify serverless function URL is correct
   - Check API Gateway/Vercel deployment status

### Debug Mode
Enable debug logging in your bot:
```yaml
logging:
  level: "DEBUG"
```

## 📊 Monitoring

### AWS Lambda
- Monitor in AWS CloudWatch
- Check function logs and metrics
- Set up CloudWatch alarms

### Vercel
- Monitor in Vercel dashboard
- Check function logs
- Monitor usage and performance

## 🔒 Security

### API Key Protection
- Store API keys in environment variables
- Use IAM roles for AWS Lambda
- Use Vercel environment variables

### Request Authentication
- Add API key authentication to serverless function
- Implement rate limiting
- Validate request payloads

## 🚀 Advanced Features

### Custom Processing
You can extend the serverless function to:
- Add custom voice command recognition
- Integrate with other AI services
- Add voice emotion detection
- Implement custom health metrics

### Multiple Providers
Support multiple transcription providers:
- OpenAI Whisper (current)
- Google Speech-to-Text
- Azure Speech Services
- AWS Transcribe

## 📝 Next Steps

1. **Deploy** your chosen serverless platform
2. **Configure** your bot with the function URL
3. **Test** with sample voice messages
4. **Monitor** usage and performance
5. **Optimize** based on your usage patterns

**Your bot now has enterprise-grade voice processing capabilities! 🎤✨**
