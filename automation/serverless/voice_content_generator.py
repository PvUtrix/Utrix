#!/usr/bin/env python3
"""
Voice Content Generator
Creates personalized daily voice messages with plans and affirmations
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from supabase import create_client, Client
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceContentGenerator:
    def __init__(self):
        # Get database clients
        self.core_db = create_client(
            os.getenv('CORE_SUPABASE_URL'),
            os.getenv('CORE_SUPABASE_ANON_KEY')
        )
        self.main_db = create_client(
            os.getenv('MAIN_SUPABASE_URL'),
            os.getenv('MAIN_SUPABASE_ANON_KEY')
        )

        # Voice message templates
        self.templates = {
            'greeting': [
                "Good morning! Here's your personalized plan for today.",
                "Hello! Ready for an amazing day? Here's what's on your agenda.",
                "Good morning! I've prepared your daily guidance and plan.",
                "Hi there! Let's start this beautiful day with purpose and intention."
            ],
            'transitions': [
                "Moving on to your priorities...",
                "Now, let's focus on what matters most today...",
                "Here's what you should concentrate on...",
                "Your main focus areas for today are..."
            ],
            'affirmations': [
                "Remember, you are capable of achieving great things today.",
                "Trust in your abilities and the progress you've already made.",
                "Every step you take brings you closer to your goals.",
                "You have the strength and wisdom to handle whatever comes your way.",
                "Your dedication and consistency are creating real change.",
                "You deserve success and happiness in all your endeavors.",
                "Your unique perspective and talents make a difference.",
                "You are exactly where you need to be in your journey."
            ],
            'closing': [
                "You've got this! Have a wonderful and productive day.",
                "Go forth with confidence and make today amazing.",
                "Remember to celebrate your wins, big and small.",
                "Stay present, stay focused, and enjoy the journey.",
                "You've prepared well - now go create something amazing."
            ]
        }

    def generate_daily_voice_content(self) -> str:
        """Generate the full text content for today's voice message"""
        logger.info("🎤 Generating daily voice content")

        # Get today's data
        today_data = self._get_today_data()
        yesterday_summary = self._get_yesterday_summary()
        weekly_context = self._get_weekly_context()

        # Build content sections
        sections = []

        # Greeting
        sections.append(random.choice(self.templates['greeting']))

        # Yesterday's reflection (if available)
        if yesterday_summary:
            sections.append(self._generate_yesterday_reflection(yesterday_summary))

        # Today's main priorities
        sections.append(self._generate_today_priorities(today_data))

        # Weekly context
        if weekly_context:
            sections.append(self._generate_weekly_context(weekly_context))

        # Affirmations
        sections.append(self._generate_affirmations())

        # Closing
        sections.append(random.choice(self.templates['closing']))

        # Combine and format
        full_content = " ".join(sections)

        # Ensure it's not too long (aim for 2-3 minutes of speech)
        max_words = 600  # ~2.5 minutes at 240 words/minute
        if len(full_content.split()) > max_words:
            full_content = self._truncate_content(full_content, max_words)

        logger.info(f"✅ Generated voice content: {len(full_content.split())} words")
        return full_content

    def _get_today_data(self) -> Dict[str, Any]:
        """Get today's data from the database"""
        today = datetime.now().strftime('%Y-%m-%d')

        try:
            # Get daily summary if it exists
            response = self.core_db.table('daily_summaries') \
                .select('*') \
                .eq('date', today) \
                .single() \
                .execute()

            if response.data:
                return {
                    'summary': response.data,
                    'health': json.loads(response.data.get('health_data', '{}')),
                    'productivity': json.loads(response.data.get('productivity_data', '{}')),
                    'learning': json.loads(response.data.get('learning_data', '{}')),
                    'tasks': self._get_today_tasks()
                }
        except Exception as e:
            logger.warning(f"Could not get today's data: {e}")

        # Fallback: get basic tasks
        return {
            'tasks': self._get_today_tasks(),
            'fallback': True
        }

    def _get_today_tasks(self) -> List[str]:
        """Get today's tasks"""
        try:
            response = self.core_db.table('tasks') \
                .select('title, priority') \
                .eq('status', 'active') \
                .order('priority', desc=True) \
                .limit(5) \
                .execute()

            return [task['title'] for task in response.data]
        except Exception as e:
            logger.warning(f"Could not get tasks: {e}")
            return []

    def _get_yesterday_summary(self) -> Dict[str, Any]:
        """Get yesterday's summary for reflection"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        try:
            response = self.core_db.table('daily_summaries') \
                .select('*') \
                .eq('date', yesterday) \
                .single() \
                .execute()

            return response.data if response.data else None
        except:
            return None

    def _get_weekly_context(self) -> Dict[str, Any]:
        """Get weekly context and patterns"""
        try:
            # Get last 7 days of summaries
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

            response = self.core_db.table('daily_summaries') \
                .select('date, productivity_data, health_data') \
                .gte('date', week_ago) \
                .execute()

            if len(response.data) >= 3:
                return self._analyze_weekly_patterns(response.data)
        except Exception as e:
            logger.warning(f"Could not get weekly context: {e}")

        return None

    def _analyze_weekly_patterns(self, weekly_data: List[Dict]) -> Dict[str, Any]:
        """Analyze weekly patterns for insights"""
        total_days = len(weekly_data)

        # Calculate averages
        avg_energy = sum([
            json.loads(day.get('health_data', '{}')).get('energy_level', 5)
            for day in weekly_data if day.get('health_data')
        ]) / total_days

        avg_tasks = sum([
            json.loads(day.get('productivity_data', '{}')).get('tasks_completed', 0)
            for day in weekly_data if day.get('productivity_data')
        ]) / total_days

        return {
            'avg_energy': round(avg_energy, 1),
            'avg_tasks': round(avg_tasks, 1),
            'total_days': total_days,
            'trend': 'improving' if avg_energy > 6 else 'maintaining' if avg_energy > 4 else 'focus_needed'
        }

    def _generate_yesterday_reflection(self, yesterday_data: Dict) -> str:
        """Generate reflection on yesterday's performance"""
        try:
            productivity = json.loads(yesterday_data.get('productivity_data', '{}'))
            tasks_completed = productivity.get('tasks_completed', 0)

            if tasks_completed > 8:
                return "Yesterday was highly productive with many tasks completed. Great work maintaining that momentum!"
            elif tasks_completed > 5:
                return "Yesterday was solid with good progress on your goals. You're building positive momentum."
            else:
                return "Yesterday had some challenges, but every day is a new opportunity to make progress."
        except:
            return "Yesterday brought valuable experiences and lessons for today."

    def _generate_today_priorities(self, today_data: Dict) -> str:
        """Generate today's main priorities section"""
        content = random.choice(self.templates['transitions']) + " "

        # Get tasks
        tasks = today_data.get('tasks', [])
        if tasks:
            if len(tasks) <= 3:
                task_list = ", ".join(tasks)
                content += f"Your main priorities today are: {task_list}. "
            else:
                top_tasks = tasks[:3]
                remaining = len(tasks) - 3
                task_list = ", ".join(top_tasks)
                content += f"Your top priorities are: {task_list}. You also have {remaining} additional tasks to consider. "

            content += "Focus on completing your highest priority items first. "
        else:
            content += "Take some time to identify your top 3 priorities for the day. What matters most right now? "

        # Add context from summary if available
        if 'summary' in today_data and not today_data.get('fallback'):
            insights = json.loads(today_data['summary'].get('insights', '[]'))
            if insights:
                random_insight = random.choice(insights)
                content += f"Remember: {random_insight.lower()} "

        return content

    def _generate_weekly_context(self, weekly_data: Dict) -> str:
        """Generate weekly context and patterns"""
        avg_energy = weekly_data['avg_energy']
        avg_tasks = weekly_data['avg_tasks']
        trend = weekly_data['trend']

        context = "Looking at your week so far, "

        if trend == 'improving':
            context += f"you're maintaining good energy levels around {avg_energy} out of 10, and completing about {avg_tasks} tasks per day. "
        elif trend == 'maintaining':
            context += f"you're keeping steady with energy levels around {avg_energy} out of 10. "
        else:
            context += "consider focusing on rest and recovery to maintain your energy for the important work ahead. "

        context += "Use this momentum to tackle today's priorities with confidence. "
        return context

    def _generate_affirmations(self) -> str:
        """Generate personalized affirmations"""
        affirmations = random.sample(self.templates['affirmations'], 2)
        affirmation_text = " ".join(affirmations)

        return f"Remember: {affirmation_text} "

    def _truncate_content(self, content: str, max_words: int) -> str:
        """Truncate content to fit within word limit"""
        words = content.split()
        if len(words) <= max_words:
            return content

        truncated = " ".join(words[:max_words])

        # Try to end at a sentence boundary
        last_sentence_end = max(
            truncated.rfind('. '),
            truncated.rfind('! '),
            truncated.rfind('? ')
        )

        if last_sentence_end > max_words * 0.8:  # If we can keep most content
            return truncated[:last_sentence_end + 1]
        else:
            return truncated + "."

def lambda_handler(event, context):
    """AWS Lambda handler for voice content generation"""
    generator = VoiceContentGenerator()

    if event.get('action') == 'generate':
        content = generator.generate_daily_voice_content()
        return {
            'statusCode': 200,
            'body': json.dumps({
                'content': content,
                'word_count': len(content.split()),
                'estimated_duration_seconds': len(content.split()) * 0.25  # Rough estimate
            })
        }

    return {'statusCode': 400, 'body': 'Invalid action'}

if __name__ == "__main__":
    # Local testing
    generator = VoiceContentGenerator()
    content = generator.generate_daily_voice_content()
    print("Generated content:")
    print(content)
    print(f"\nWord count: {len(content.split())}")
    print(f"Estimated duration: {len(content.split()) * 0.25} seconds")
