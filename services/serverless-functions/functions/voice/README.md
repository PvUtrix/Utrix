# 🎤 Voice Transcription Serverless Function

## Overview
This serverless function handles voice message transcription using OpenAI Whisper API. It can be deployed to AWS Lambda or Vercel.

## Features
- ✅ **OpenAI Whisper Integration** - High-quality voice transcription
- ✅ **Multiple Format Support** - OGG, MP3, WAV, M4A, WebM
- ✅ **Base64 Audio Processing** - Handles audio data from Telegram
- ✅ **Error Handling** - Robust error handling and logging
- ✅ **Dual Platform Support** - AWS Lambda and Vercel compatible

## Deployment Options

### AWS Lambda
1. **Package the function**:
   ```bash
   pip install -r requirements.txt -t .
   zip -r voice-transcription.zip .
   ```

2. **Deploy to Lambda**:
   - Create new Lambda function
   - Upload the zip file
   - Set environment variables:
     - `OPENAI_API_KEY`: Your OpenAI API key
   - Set timeout to 30 seconds
   - Set memory to 512MB

3. **Create API Gateway**:
   - Create REST API
   - Create POST method
   - Link to Lambda function
   - Deploy API

### Vercel
1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

3. **Set Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key

## API Usage

### Request Format
```json
{
  "audio_data": "base64_encoded_audio_data",
  "file_format": "ogg",
  "user_id": "telegram_user_id",
  "message_id": "telegram_message_id"
}
```

### Response Format
```json
{
  "success": true,
  "transcription": "Transcribed text here",
  "user_id": "telegram_user_id",
  "message_id": "telegram_message_id",
  "service": "openai_whisper"
}
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for Whisper transcription

## Cost Estimation
- **AWS Lambda**: ~$0.20 per 1M requests + compute time
- **Vercel**: Free tier includes 100GB-hours/month
- **OpenAI Whisper**: $0.006 per minute of audio

## Integration with Telegram Bot
1. Update your bot's `config.yaml`:
   ```yaml
   serverless:
     transcription_url: "https://your-function-url.com/voice-transcription"
     enable_serverless_transcription: true
   ```

2. Update bot handler in `bot.py`:
   ```python
   from bot.handlers import serverless_voice_handlers
   serverless_voice_handlers.initialize_voice_handler(self.config)
   self.application.add_handler(MessageHandler(filters.VOICE, self._with_auth(serverless_voice_handlers.voice_message_handler)))
   ```

## Testing
Test the function with a sample audio file:
```bash
# Encode audio to base64
base64 -i test_audio.ogg

# Send POST request
curl -X POST https://your-function-url.com/voice-transcription \
  -H "Content-Type: application/json" \
  -d '{
    "audio_data": "base64_encoded_audio_here",
    "file_format": "ogg",
    "user_id": "test_user",
    "message_id": "test_message"
  }'
```

## Troubleshooting
- **Timeout errors**: Increase Lambda timeout to 30 seconds
- **Memory errors**: Increase Lambda memory to 512MB
- **API key errors**: Verify OPENAI_API_KEY is set correctly
- **Audio format errors**: Ensure audio is in supported format