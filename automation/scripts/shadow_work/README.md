# Shadow Work Scripts

Scripts for shadow work, self-development, and inner work tracking.

## 📁 Structure

```
shadow_work/
└── shadow_work_tracker.py    # Shadow work tracking and insights
```

## 🧠 Shadow Work Tracker

**shadow_work_tracker.py** - Comprehensive shadow work tracking system

### Features
- **Daily Check-ins**: Regular shadow work reflection and check-ins
- **Insight Logging**: Capture shadow work insights and observations
- **Prompt Generation**: Get reflection prompts for deeper exploration
- **Progress Reports**: Track shadow work progress and patterns
- **Reminder System**: Stay consistent with shadow work practice
- **Focus Setting**: Set specific shadow work focus areas

### Capabilities
- Daily shadow work check-ins with structured prompts
- Insight logging with categorization and tagging
- Random prompt generation for exploration
- Progress tracking and pattern identification
- Reminder system for consistent practice
- Focus area setting and tracking

### Usage

#### Daily Check-in
```bash
python3 shadow_work_tracker.py --action checkin
```

#### Log Insight
```bash
python3 shadow_work_tracker.py --action insight --insight "I noticed I avoid difficult conversations"
```

#### Get Prompt
```bash
python3 shadow_work_tracker.py --action explore
```

#### Generate Report
```bash
python3 shadow_work_tracker.py --action report
```

#### Set Focus
```bash
python3 shadow_work_tracker.py --action focus --shadow-aspect "emotional regulation"
```

#### Get Reminders
```bash
python3 shadow_work_tracker.py --action reminders
```

## 🎯 Shadow Work Categories

### Emotional Patterns
- Emotional triggers and responses
- Emotional regulation and awareness
- Emotional processing and healing

### Behavioral Patterns
- Automatic behaviors and habits
- Behavioral triggers and responses
- Pattern recognition and change

### Self-Awareness
- Self-discovery and exploration
- Inner dialogue and self-talk
- Self-acceptance and compassion

### Growth Areas
- Areas for development
- Challenges and obstacles
- Growth opportunities

## 🔧 Telegram Bot Integration

All shadow work functionality is integrated with the Telegram bot:

### Shadow Work Menu
- ✅ **Daily Check-in** - Daily shadow work reflection
- 💡 **Log Insight** - Capture shadow work insights
- 🎯 **Get Prompt** - Get reflection prompts
- 📊 **Progress Report** - View shadow work progress
- 🔔 **Reminders** - Get shadow work reminders
- 🎭 **Set Focus** - Set shadow work focus area

### Voice Commands
Shadow work supports voice commands:
- "Log shadow work insight: I noticed I avoid difficult conversations"
- "Get shadow work prompt"
- "Daily shadow work check-in"
- "Show shadow work progress"
- "Set shadow work focus on emotional regulation"

## 📊 Data Storage

Shadow work data is stored in `automation/outputs/shadow_work_data.json`:

```json
[
  {
    "date": "2024-12-19",
    "timestamp": "2024-12-19T10:00:00",
    "checkins": [
      {
        "timestamp": "2024-12-19T10:00:00",
        "prompt": "What emotion am I avoiding today?",
        "response": "I'm avoiding feeling vulnerable",
        "insights": ["I notice I deflect when asked personal questions"]
      }
    ],
    "insights": [
      {
        "timestamp": "2024-12-19T14:30:00",
        "insight": "I noticed I avoid difficult conversations",
        "category": "behavioral",
        "tags": ["communication", "avoidance"],
        "notes": "This happens especially with authority figures"
      }
    ],
    "focus_areas": ["emotional regulation", "communication"],
    "reminders": [
      {
        "timestamp": "2024-12-19T09:00:00",
        "message": "Time for your daily shadow work check-in"
      }
    ]
  }
]
```

## 🎯 Shadow Work Prompts

### Emotional Awareness
- "What emotion am I avoiding today?"
- "What am I feeling right now and why?"
- "What emotional pattern do I notice in myself?"

### Behavioral Patterns
- "What behavior do I want to change about myself?"
- "What automatic response do I have that doesn't serve me?"
- "What do I do when I feel threatened or unsafe?"

### Self-Discovery
- "What part of myself am I rejecting?"
- "What would I do if I wasn't afraid?"
- "What am I hiding from others and why?"

### Growth and Change
- "What old belief is no longer serving me?"
- "What would my shadow self want me to acknowledge?"
- "What pattern in my behavior do I want to change?"

## 🔄 Daily Shadow Work Routine

### Morning (5 minutes)
1. **Check-in**: Use daily check-in prompt
2. **Set Focus**: Choose focus area for the day
3. **Intention**: Set intention for shadow work practice

### Throughout Day
1. **Notice**: Pay attention to triggers and patterns
2. **Log Insights**: Capture observations as they arise
3. **Reflect**: Take moments to reflect on experiences

### Evening (10 minutes)
1. **Review**: Review the day's insights and patterns
2. **Process**: Process any difficult emotions or experiences
3. **Plan**: Plan tomorrow's shadow work focus

## 📈 Progress Tracking

### Daily Metrics
- Check-ins completed
- Insights logged
- Focus areas worked on
- Reminders followed

### Weekly Review
- Pattern identification
- Progress assessment
- Focus area evaluation
- Goal setting for next week

### Monthly Analysis
- Long-term pattern recognition
- Growth area assessment
- Shadow work effectiveness
- Strategy adjustment

## 🎯 Best Practices

### Consistency
- Daily check-ins, even if brief
- Regular insight logging
- Consistent focus area work

### Compassion
- Be gentle with yourself
- Accept all parts of yourself
- Practice self-compassion

### Integration
- Connect shadow work to daily life
- Apply insights to real situations
- Use shadow work for growth

### Privacy
- Keep shadow work data private
- Respect your own boundaries
- Share only what feels safe

---

*Last Updated: 2024-12-19*
*Status: Shadow work system fully functional and integrated*
