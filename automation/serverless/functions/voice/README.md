# 🎤 Voice Functions

Voice generation and text-to-speech functions for your personal system.

## 📁 Contents

- `elevenlabs_tts.py` - Text-to-speech conversion using ElevenLabs
- `voice_content_generator.py` - Generate voice content from text

## 🎯 Purpose

These functions handle voice generation and audio content:

- **Text-to-Speech**: Convert text to natural-sounding speech
- **Voice Content**: Generate voice content from various text sources
- **Audio Processing**: Handle audio file generation and processing

## ⏰ Schedule

- **Voice Content Generator**: Runs daily at 7 AM UTC
- **ElevenLabs TTS**: Triggered by voice content generator

## 🔧 Configuration

```bash
# ElevenLabs Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id

# Voice Settings
VOICE_SPEED=1.0
VOICE_STABILITY=0.5
VOICE_SIMILARITY_BOOST=0.75

# Output Configuration
AUDIO_FORMAT=mp3
AUDIO_QUALITY=high
```

## 🚀 Usage

### Local Testing

```bash
# Test voice content generator
serverless invoke local --function voice-content-generator

# Test ElevenLabs TTS
serverless invoke local --function elevenlabs-tts
```

### Deployment

```bash
# Deploy voice functions
serverless deploy --function voice-content-generator
serverless deploy --function elevenlabs-tts
```

## 🎵 Voice Features

### ElevenLabs TTS
- **Natural Speech**: High-quality text-to-speech conversion
- **Voice Cloning**: Custom voice generation
- **Multiple Languages**: Support for various languages
- **Emotion Control**: Adjustable emotional tone

### Voice Content Generator
- **Daily Summaries**: Convert daily summaries to audio
- **News Updates**: Generate voice news updates
- **Reminders**: Create voice reminders
- **Custom Content**: Generate voice from any text

## 📊 Output

- **Audio Files**: MP3 format audio files
- **Metadata**: Audio file metadata and information
- **Storage**: Audio files stored in cloud storage
- **Delivery**: Audio sent via Telegram or email

## 💰 Cost Optimization

- **Free Tier**: Stays within ElevenLabs free tier limits
- **Caching**: Cache generated audio to reduce API calls
- **Compression**: Optimize audio file sizes
- **Batch Processing**: Process multiple texts in single call

## 🔒 Privacy

- **Local Processing**: Text processed locally when possible
- **Secure Storage**: Audio files stored securely
- **No Retention**: Audio files deleted after delivery
- **Encrypted Transfer**: Secure transmission of audio files

## 🛠️ Development

### Testing Voice Quality

```bash
# Test with sample text
python3 -c "
from elevenlabs_tts import ElevenLabsTTS
tts = ElevenLabsTTS()
audio = tts.generate_speech('Hello, this is a test.')
print('Audio generated successfully')
"
```

### Custom Voice Training

```bash
# Upload voice samples for custom voice
# (Requires ElevenLabs Pro account)
```

## 📚 Resources

- [ElevenLabs API Documentation](https://docs.elevenlabs.io/)
- [Voice Cloning Guide](https://docs.elevenlabs.io/voice-cloning)
- [Audio Format Options](https://docs.elevenlabs.io/audio-generation)
