# 🌅 Morning Routine Guide

## Overview
Your Personal System Telegram Bot now includes a voice-guided morning routine feature that helps you start each day with intention and purpose.

## Features

### 🎤 Voice-Guided Routine
- **Automatic Delivery**: Receive your morning routine at 6:00 AM daily
- **Voice-Friendly Format**: Text optimized for text-to-speech reading
- **Personalized Timing**: Adapts to your current time zone
- **Complete Workflow**: Includes all your morning activities from wake-up to work start

### 📱 Manual Access
- **Command**: `/morning_routine` - Get your routine anytime
- **Two Formats**: 
  - Formatted text version with checkboxes
  - Voice guide version for text-to-speech

## How It Works

### Automatic Delivery
1. **Setup**: Add your user ID to `allowed_users` in config.yaml
2. **Schedule**: Bot automatically sends routine at 6:00 AM daily
3. **Format**: Receives both formatted and voice-friendly versions
4. **Customization**: Time zone can be configured in settings

### Manual Access
```
/morning_routine
```
- Works anytime, not just in the morning
- Adapts greeting based on current time
- Provides complete routine with all details

## Routine Structure

### ⏰ 6:00 AM - Wake Up
- No snooze - feet on floor immediately
- Drink glass of water (on nightstand)
- 5 deep breaths with gratitude

### 🌡️ 6:03 AM - Digestive Warm-Up
- Prepare warm water (40-45°C) - 250ml
- Drink slowly, mindfully (5-7 minutes)
- Feel the gentle warmth activating digestion
- Express gratitude for body's natural processes

### 🧘 6:10 AM - Mindfulness
- 10-minute meditation (Headspace app)
- Set daily intention
- Visualize successful day

### 💪 6:25 AM - Movement
- 5-minute stretching routine
- 20 pushups
- 30 jumping jacks
- Cold shower (2 minutes)

### ☕ 6:45 AM - Fuel
- Prepare coffee/tea mindfully
- Healthy breakfast (protein + complex carbs)
- Vitamins and supplements

### 📝 7:05 AM - Planning
- Review calendar and priorities
- Choose 3 MITs (Most Important Tasks)
- Time block the day
- Check weather and news (5 min max)

### 📚 7:25 AM - Learning
- Read for 20 minutes
- Take 3 key notes
- Add to knowledge base
- Sync company presentations (5 min)

### 🚀 7:50 AM - Start Work
- Clean workspace
- Open required apps/tools
- Begin with MIT #1

## Configuration

### Time Zone Setup
Add to your `config.yaml`:
```yaml
timezone: "Europe/Moscow"  # Your timezone
```

### User Setup
Ensure your user ID is in the allowed users list:
```yaml
telegram:
  allowed_users: [YOUR_USER_ID]
```

## Tips for Best Experience

### 🎧 Voice Usage
1. **Text-to-Speech**: Use your phone's built-in TTS feature
2. **Reading Aloud**: Have the bot read the voice guide version
3. **Hands-Free**: Perfect for morning routine execution

### 📋 Routine Execution
1. **Follow the Flow**: Execute each block in sequence
2. **Mindful Transitions**: Take time between activities
3. **Track Progress**: Use the checkboxes to mark completion
4. **Adapt as Needed**: Modify timing based on your schedule

### 🔄 Customization
- **Timing**: Adjust routine times in the code
- **Activities**: Modify activities to match your preferences
- **Duration**: Change time blocks as needed

## Integration with Your System

### 📊 Tracking
- Routine completion can be logged via `/log_health`
- Progress tracked in daily summaries
- Patterns analyzed for optimization

### 🔗 Connected Features
- **Health Logging**: Track energy levels and mood
- **Learning Integration**: Connect with your reading goals
- **Task Management**: MITs integrate with your task system
- **Journal**: Morning reflections can be captured

## Troubleshooting

### Common Issues
1. **No Morning Message**: Check user ID in config and timezone settings
2. **Wrong Time**: Verify timezone configuration
3. **Bot Not Responding**: Ensure bot is running and connected

### Support Commands
- `/status` - Check bot status
- `/help` - View all available commands
- `/morning_routine` - Get routine manually

## Future Enhancements

### Planned Features
- **Voice Messages**: Actual voice recordings instead of text
- **Customization**: User-specific routine modifications
- **Progress Tracking**: Automatic completion tracking
- **Weather Integration**: Weather-aware routine adjustments
- **Calendar Integration**: Schedule-aware routine modifications

### Feedback
Share your experience and suggestions for improvements!

---

*Last updated: 2024-12-15*
