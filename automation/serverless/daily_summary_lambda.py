#!/usr/bin/env python3
"""
AWS Lambda function for Daily Summary Generation
Multi-tier database architecture with Core/Main/Archive tiers
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import boto3
from botocore.exceptions import ClientError
import requests
from supabase import create_client, Client

# Database tier clients
def get_core_db() -> Client:
    """Get Core database client (Supabase Free Tier)"""
    return create_client(
        os.getenv('CORE_SUPABASE_URL'),
        os.getenv('CORE_SUPABASE_ANON_KEY')
    )

def get_main_db() -> Client:
    """Get Main database client (Self-hosted Supabase)"""
    return create_client(
        os.getenv('MAIN_SUPABASE_URL'),
        os.getenv('MAIN_SUPABASE_ANON_KEY')
    )

def get_secret(secret_name: str) -> str:
    """Get secret from AWS Secrets Manager"""
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return ""

def collect_health_data() -> Dict[str, Any]:
    """Collect health metrics from various sources"""
    # Use environment variables for API endpoints/keys
    health_api_key = get_secret('HEALTH_API_KEY')

    return {
        "steps": 8500,  # Mock data - replace with real API calls
        "sleep_hours": 7.5,
        "water_glasses": 8,
        "workout_completed": True,
        "meditation_minutes": 15,
        "energy_level": 8
    }

def collect_productivity_data() -> Dict[str, Any]:
    """Collect productivity metrics"""
    return {
        "tasks_completed": 12,
        "focus_time_hours": 6.5,
        "meetings_attended": 3,
        "code_commits": 8,
        "documents_created": 2,
        "emails_processed": 45
    }

def collect_learning_data() -> Dict[str, Any]:
    """Collect learning progress"""
    return {
        "reading_minutes": 45,
        "courses_progress": "2 lessons completed",
        "notes_created": 8,
        "topics_studied": ["Python", "System Design"]
    }

def collect_finance_data() -> Dict[str, Any]:
    """Collect financial data"""
    return {
        "spending_today": 67.50,
        "budget_remaining": 1832.50,
        "investment_change": 1.2,
        "savings_rate": "42%"
    }

def analyze_patterns() -> List[str]:
    """Generate insights based on data patterns"""
    insights = [
        "Your most productive hours were 9 AM - 12 PM",
        "Sleep quality improved by 12% this week",
        "You're on track with your monthly savings goal",
        "Consider scheduling deep work in the morning"
    ]
    return insights

def generate_recommendations() -> List[str]:
    """Generate personalized recommendations"""
    recommendations = [
        "Try to get to bed 30 minutes earlier tonight",
        "Schedule tomorrow's most important task for 9 AM",
        "Take a 15-minute walk to boost afternoon energy",
        "Review your investment portfolio this weekend"
    ]
    return recommendations

def send_telegram_notification(summary: str, bot_token: str, chat_id: str):
    """Send summary via Telegram"""
    if not bot_token or not chat_id:
        print("Telegram credentials not available, skipping notification")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": summary,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram notification sent successfully")
        else:
            print(f"❌ Failed to send Telegram notification: {response.status_code}")
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")

def save_daily_summary_to_db(summary_data: Dict[str, Any], summary_text: str) -> bool:
    """Save daily summary to appropriate database tier"""
    try:
        # Prepare data for storage
        db_record = {
            'date': summary_data['date'],
            'summary_text': summary_text,
            'health_data': json.dumps(summary_data['sections']['health']),
            'productivity_data': json.dumps(summary_data['sections']['productivity']),
            'learning_data': json.dumps(summary_data['sections']['learning']),
            'finance_data': json.dumps(summary_data['sections']['finance']),
            'insights': json.dumps(summary_data['insights']),
            'recommendations': json.dumps(summary_data['recommendations']),
            'created_at': datetime.now().isoformat(),
            'data_type': 'daily_summary',
            'size_kb': len(json.dumps(summary_data)) / 1024
        }

        # Always save to Core database first (frequently accessed)
        core_db = get_core_db()
        response = core_db.table('daily_summaries').insert(db_record).execute()

        if response.data:
            print("✅ Daily summary saved to Core database")
            return True
        else:
            print("❌ Failed to save to Core database")
            return False

    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

def lambda_handler(event, context):
    """Main Lambda function handler"""
    print("🚀 Starting Daily Summary Generation...")

    # Initialize data structure
    today = datetime.now()
    summary_data = {
        "date": today.strftime("%Y-%m-%d"),
        "sections": {}
    }

    try:
        # Collect all data (keep execution time minimal)
        summary_data["sections"]["health"] = collect_health_data()
        summary_data["sections"]["productivity"] = collect_productivity_data()
        summary_data["sections"]["learning"] = collect_learning_data()
        summary_data["sections"]["finance"] = collect_finance_data()

        # Generate insights and recommendations
        summary_data["insights"] = analyze_patterns()
        summary_data["recommendations"] = generate_recommendations()

        # Create formatted summary
        health_data = summary_data['sections']['health']
        prod_data = summary_data['sections']['productivity']
        learn_data = summary_data['sections']['learning']
        finance_data = summary_data['sections']['finance']

        summary = ".1f"".1f".1f"f"""# Daily Summary - {today.strftime('%B %d, %Y')}

## 📊 Quick Stats

### 🏃 Health & Wellness
- **Steps**: {health_data['steps']:,}
- **Sleep**: {health_data['sleep_hours']} hours
- **Water**: {health_data['water_glasses']} glasses
- **Workout**: {'✅ Completed' if health_data['workout_completed'] else '❌ Missed'}
- **Meditation**: {health_data['meditation_minutes']} minutes
- **Energy**: {health_data['energy_level']}/10

### 💼 Productivity
- **Tasks Completed**: {prod_data['tasks_completed']}
- **Focus Time**: {prod_data['focus_time_hours']} hours
- **Meetings**: {prod_data['meetings_attended']}
- **Code Commits**: {prod_data['code_commits']}
- **Documents**: {prod_data['documents_created']}
- **Emails**: {prod_data['emails_processed']}

### 📚 Learning & Growth
- **Reading**: {learn_data['reading_minutes']} minutes
- **Course Progress**: {learn_data['courses_progress']}
- **Notes Created**: {learn_data['notes_created']}
- **Topics**: {', '.join(learn_data['topics_studied'])}

### 💰 Finance
- **Spent Today**: ${finance_data['spending_today']}
- **Budget Remaining**: ${finance_data['budget_remaining']}
- **Investment Change**: {finance_data['investment_change']}%
- **Savings Rate**: {finance_data['savings_rate']}

## 💡 Insights
{chr(10).join(f"- {insight}" for insight in summary_data['insights'])}

## 🎯 Recommendations for Tomorrow
{chr(10).join(f"{i+1}. {rec}" for i, rec in enumerate(summary_data['recommendations']))}

---
*Generated by AWS Lambda at {datetime.now().strftime('%H:%M')} | Next summary in 24 hours*
"""

        # Save to database
        db_success = save_daily_summary_to_db(summary_data, summary)

        # Send notification
        bot_token = get_secret('TELEGRAM_BOT_TOKEN')
        chat_id = get_secret('TELEGRAM_CHAT_ID')
        send_telegram_notification(summary, bot_token, chat_id)

        print("✅ Daily summary generation complete!")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Daily summary generated successfully',
                'summary': summary,
                'data': summary_data,
                'database_saved': db_success
            })
        }

    except Exception as e:
        print(f"❌ Error generating daily summary: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to generate daily summary'
            })
        }
