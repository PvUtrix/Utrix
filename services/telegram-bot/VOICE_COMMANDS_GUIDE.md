# 🎤 Voice Commands Guide

## 🚀 Quick Start

Your Telegram bot now supports voice message transcription! Simply send a voice message and the bot will:

1. **Transcribe** your voice to text using OpenAI Whisper
2. **Analyze** the content for commands and actions
3. **Execute** the appropriate automation scripts
4. **Provide** interactive responses with quick action buttons

## 🎯 Supported Voice Commands

### 💪 Health & Wellness
**Voice Commands:**
- "Log my health metrics"
- "I took 8500 steps today"
- "I slept 7.5 hours last night"
- "I drank 8 glasses of water"
- "My mood is 8 out of 10"
- "I did cardio workout"

**What it does:**
- Automatically extracts health metrics from your speech
- Logs the data to your health tracker
- Shows today's health statistics

### 📚 Learning & Education
**Voice Commands:**
- "Log learning activity"
- "I studied for 45 minutes"
- "I took a course for 2 hours"
- "I practiced coding for 30 minutes"
- "I worked on my project for 1 hour"

**What it does:**
- Identifies learning activity type (reading, course, practice, project)
- Extracts duration from your speech
- Logs to your learning tracker

### ✅ Task Management
**Voice Commands:**
- "Add a task"
- "I need to finish the report"
- "Urgent: Call the client"
- "Low priority: Buy groceries"
- "Important: Review the proposal"

**What it does:**
- Creates tasks from your voice input
- Automatically assigns priority levels
- Adds to your task manager

### 📝 Quick Notes
**Voice Commands:**
- "Quick note"
- "I have an idea"
- "Reminder: Check email"
- "Note: Meeting at 3 PM"
- "Idea: New feature for the app"

**What it does:**
- Captures your thoughts and ideas
- Categorizes notes automatically
- Stores in your quick notes system

### 🌅 Daily Routines
**Voice Commands:**
- "Generate morning routine"
- "Show my daily summary"
- "What's my routine for today?"

**What it does:**
- Creates personalized morning routines
- Shows daily summaries with your data
- Provides daily intentions and reflections

## 🎤 How Voice Transcription Works

### 1. **Send Voice Message**
Record and send a voice message to your bot

### 2. **Automatic Transcription**
The bot uses OpenAI Whisper to convert speech to text

### 3. **Smart Analysis**
The bot analyzes the transcribed text for:
- Command keywords
- Data extraction (numbers, metrics, priorities)
- Intent recognition

### 4. **Action Execution**
Based on the analysis, the bot:
- Executes the appropriate automation script
- Shows confirmation messages
- Provides interactive buttons for follow-up actions

### 5. **Interactive Response**
You get:
- Transcribed text confirmation
- Execution results
- Quick action buttons for related tasks

## 🎯 Voice Command Examples

### Health Logging Examples
```
"I took 8500 steps today"
→ Logs: steps: 8500

"I slept 7.5 hours last night"
→ Logs: sleep: 7.5

"I drank 8 glasses of water"
→ Logs: water: 8

"My mood is 8 out of 10"
→ Logs: mood: 8

"I did cardio workout"
→ Logs: workout: cardio
```

### Learning Tracking Examples
```
"I studied for 45 minutes"
→ Logs: reading, 45 minutes

"I took a course for 2 hours"
→ Logs: course, 120 minutes

"I practiced coding for 30 minutes"
→ Logs: practice, 30 minutes

"I worked on my project for 1 hour"
→ Logs: project, 60 minutes
```

### Task Management Examples
```
"I need to finish the report"
→ Creates task: "finish the report", priority: medium

"Urgent: Call the client"
→ Creates task: "Call the client", priority: high

"Low priority: Buy groceries"
→ Creates task: "Buy groceries", priority: low
```

### Note Capture Examples
```
"I have an idea for a new feature"
→ Captures note: "I have an idea for a new feature", category: idea

"Reminder: Check email at 3 PM"
→ Captures note: "Check email at 3 PM", category: reminder

"Note: Meeting with team tomorrow"
→ Captures note: "Meeting with team tomorrow", category: general
```

## 🔧 Technical Details

### Supported Audio Formats
- OGG (Telegram's default format)
- MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM

### File Size Limits
- Maximum: 25 MB per voice message
- Recommended: Under 10 MB for best performance

### Transcription Quality
- Uses OpenAI Whisper-1 model
- High accuracy for clear speech
- Works best with minimal background noise

### Privacy & Security
- Voice files are temporarily downloaded for transcription
- Files are automatically deleted after processing
- Only transcribed text is processed and stored
- No voice data is permanently stored

## 🎯 Best Practices

### For Better Transcription
1. **Speak clearly** and at a moderate pace
2. **Reduce background noise** when possible
3. **Use specific keywords** for commands
4. **Keep messages concise** (under 2 minutes)
5. **Include numbers** for metrics and durations

### For Better Command Recognition
1. **Use action words**: "log", "add", "create", "show"
2. **Include context**: "health", "learning", "task", "note"
3. **Be specific**: "8500 steps" vs "many steps"
4. **Use natural language**: "I took 8500 steps" vs "steps 8500"

### For Better Results
1. **Test with simple commands** first
2. **Use the interactive buttons** for follow-up actions
3. **Check the transcribed text** for accuracy
4. **Use text commands** for complex requests

## 🚀 Advanced Features

### Smart Data Extraction
The bot automatically extracts:
- **Numbers**: Steps, hours, minutes, ratings
- **Priorities**: Urgent, important, low priority
- **Categories**: Health, learning, tasks, notes
- **Durations**: Minutes, hours, time periods

### Interactive Responses
After processing voice commands, you get:
- **Quick action buttons** for related tasks
- **Confirmation messages** with extracted data
- **Follow-up suggestions** for next steps
- **Error handling** with helpful guidance

### Integration with Daily Operations
Voice commands integrate with:
- **Health Logger**: Automatic metric extraction
- **Learning Tracker**: Activity type recognition
- **Task Manager**: Priority assignment
- **Quick Notes**: Category classification
- **Morning Routine**: Daily planning
- **Daily Summary**: Progress tracking

## 🛠️ Troubleshooting

### Common Issues

**Transcription Not Working:**
- Check OpenAI API key is configured
- Verify API key has sufficient credits
- Ensure voice message is clear and not too long

**Commands Not Recognized:**
- Use specific keywords (log, add, create, show)
- Include context words (health, learning, task, note)
- Check the transcribed text for accuracy

**Data Not Extracted:**
- Speak numbers clearly
- Use specific units (steps, hours, minutes)
- Include action words (took, did, completed)

**Scripts Not Executing:**
- Check automation script paths
- Verify script permissions
- Ensure Python environment is correct

### Getting Help
1. **Check transcribed text** - Make sure it's accurate
2. **Use interactive buttons** - For follow-up actions
3. **Try text commands** - For complex requests
4. **Check logs** - For technical issues

## 🎉 Getting Started

1. **Send a voice message** to your bot
2. **Wait for transcription** (usually 2-5 seconds)
3. **Check the transcribed text** for accuracy
4. **Use the interactive buttons** for follow-up actions
5. **Try different commands** to explore features

**Example First Voice Message:**
> "Log my health metrics"

This will show you the health logger interface and help you get started!

---

**Enjoy your voice-controlled personal system! 🎤✨**
