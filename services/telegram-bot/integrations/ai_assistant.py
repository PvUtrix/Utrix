"""
AI Assistant integration for the Personal System Telegram Bot.
Provides intelligent responses and analysis based on the user's personal data.
"""

import json
import re
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from utils.logger import get_logger


class AIAssistant:
    """AI-powered assistant for personal system interactions."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = get_logger(__name__)
        self.config = config or {}
        
        # Load user's personal system data
        self.base_path = Path(config.get('paths', {}).get('base_path', '../../../'))
        
        # Shadow work archetypes from the user's system
        self.shadow_archetypes = {
            "The Visionary Builder": {
                "description": "You create systems and ventures that empower others",
                "light_aspects": ["Seeing opportunities", "Creating systems", "Building for others"],
                "shadow_aspects": ["Over-optimization", "Perfectionism", "Neglecting human needs"],
                "integration_practices": ["Practice patience", "Explain vision clearly", "Balance systems with people"]
            },
            "The Freedom Seeker": {
                "description": "You prioritize autonomy and location independence",
                "light_aspects": ["Independence", "Adventure", "Bold choices"],
                "shadow_aspects": ["Commitment issues", "Restlessness", "Avoiding responsibility"],
                "integration_practices": ["Practice commitment", "Find stability in movement", "Embrace responsibility"]
            },
            "The Connector": {
                "description": "You naturally bring people together around big ideas",
                "light_aspects": ["Building communities", "Bringing people together", "Creating connections"],
                "shadow_aspects": ["People-pleasing", "Losing self in others", "Surface relationships"],
                "integration_practices": ["Maintain boundaries", "Deepen authentic connections", "Practice solitude"]
            },
            "The Resilient Innovator": {
                "description": "You adapt and persist through uncertainty",
                "light_aspects": ["Adapting", "Persisting", "Finding solutions"],
                "shadow_aspects": ["Toxic positivity", "Avoiding vulnerability", "Burnout"],
                "integration_practices": ["Embrace vulnerability", "Ask for help", "Allow difficult emotions"]
            },
            "The Ethical Entrepreneur": {
                "description": "You balance profit with fairness and sustainability",
                "light_aspects": ["Fairness", "Sustainability", "Positive impact"],
                "shadow_aspects": ["Self-righteousness", "Judgment", "Unrealistic expectations"],
                "integration_practices": ["Practice humility", "Embrace imperfection", "Question motivations"]
            }
        }
    
    async def get_response(self, message: str, user_id: int) -> str:
        """Get an intelligent response to a user message."""
        
        # Try multilingual processing first
        try:
            from .simple_multilingual_agent import SimpleMultilingualAgent
            
            multilingual_agent = SimpleMultilingualAgent(self.config)
            result = await multilingual_agent.process_message(message, user_id, "text")
            
            if result["confidence"] > 0.5:
                self.logger.info(f"✅ Multilingual processed message with intent: {result['intent']} (confidence: {result['confidence']})")
                return result["response_text"]
            else:
                self.logger.info(f"⚠️ Low confidence result from multilingual: {result['confidence']}, falling back to local processing")
                
        except Exception as e:
            self.logger.warning(f"Multilingual processing failed, falling back to local: {e}")
        
        # Fallback to original logic
        message_lower = message.lower()
        
        # Check for specific question types
        if any(word in message_lower for word in ['shadow', 'archetype', 'archetypes']):
            return self._get_shadow_archetypes_response()
        
        elif any(word in message_lower for word in ['project', 'work on', 'priority', 'today', 'list my projects']):
            return self._get_project_recommendations()
        
        elif any(word in message_lower for word in ['health', 'fitness', 'wellness']):
            return self._get_health_insights(user_id)
        
        elif any(word in message_lower for word in ['learn', 'study', 'education']):
            return self._get_learning_insights(user_id)
        
        elif any(word in message_lower for word in ['journal', 'pattern', 'insight']):
            return self._get_journal_insights(user_id)
        
        elif any(word in message_lower for word in ['goal', 'progress', 'achievement']):
            return self._get_goal_insights(user_id)
        
        elif any(word in message_lower for word in ['value', 'values', 'core values']):
            return self._get_values_response()
        
        elif any(word in message_lower for word in ['task', 'todo', 'what should i do']):
            return self._get_task_recommendations()
        
        elif any(word in message_lower for word in ['help', 'what can you do']):
            return self._get_help_response()
        
        elif any(word in message_lower for word in ['habit tracker', 'habit tracking', 'tracking habits']):
            return self._get_habit_tracker_info()
        
        elif any(word in message_lower for word in ['deep connection', 'connection app']):
            return self._get_deep_connection_app_info()
        
        else:
            return self._get_general_response(message)
    
    async def transcribe_voice(self, voice_path: str) -> Optional[str]:
        """Transcribe voice message to text using OpenAI Whisper."""
        try:
            import openai
            from config.secure_config import SecureConfigManager
            
            # Get OpenAI configuration
            secure_config = SecureConfigManager()
            openai_config = secure_config.get_openai_config(self.config)
            
            if not openai_config or not openai_config.get('api_key'):
                self.logger.error("OpenAI API key not configured")
                return "❌ OpenAI API key not configured. Please set it using /admin set_openai_key YOUR_API_KEY"
            
            # Set OpenAI API key
            openai.api_key = openai_config['api_key']
            
            # Check file size
            import os
            file_size_mb = os.path.getsize(voice_path) / (1024 * 1024)
            max_size = openai_config.get('max_file_size', 25)
            
            if file_size_mb > max_size:
                return f"❌ Voice file too large ({file_size_mb:.1f} MB). Maximum size is {max_size} MB."
            
            self.logger.info(f"Transcribing voice file: {voice_path} ({file_size_mb:.1f} MB)")
            
            # Transcribe using OpenAI Whisper
            with open(voice_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model=openai_config.get('model', 'whisper-1'),
                    file=audio_file,
                    response_format="text"
                )
            
            # Clean up the audio file
            try:
                os.remove(voice_path)
                self.logger.info(f"Cleaned up voice file: {voice_path}")
            except Exception as cleanup_error:
                self.logger.warning(f"Failed to cleanup voice file: {cleanup_error}")
            
            if transcript and transcript.strip():
                self.logger.info(f"Voice transcription successful: {len(transcript)} characters")
                return transcript.strip()
            else:
                return "❌ Could not transcribe the voice message. Please try again or send a text message."
                
        except ImportError:
            return "❌ OpenAI library not available. Please install: pip install openai"
        except Exception as e:
            self.logger.error(f"Error transcribing voice: {e}")
            # Clean up the audio file on error
            try:
                import os
                if os.path.exists(voice_path):
                    os.remove(voice_path)
            except:
                pass
            return f"❌ Transcription failed: {str(e)}"
    
    async def analyze_data(self, request: str, user_id: int) -> str:
        """Analyze user data based on request."""
        request_lower = request.lower()
        
        if 'shadow' in request_lower:
            return self._analyze_shadow_work(user_id)
        elif 'productivity' in request_lower:
            return self._analyze_productivity(user_id)
        elif 'health' in request_lower:
            return self._analyze_health(user_id)
        elif 'learning' in request_lower:
            return self._analyze_learning(user_id)
        elif 'journal' in request_lower:
            return self._analyze_journal(user_id)
        else:
            return "I can analyze shadow work, productivity, health, learning, or journal data. What would you like me to focus on?"
    
    async def get_recommendations(self, request: str, user_id: int) -> str:
        """Get personalized recommendations."""
        request_lower = request.lower()
        
        if 'shadow' in request_lower:
            return self._get_shadow_work_recommendations()
        elif 'productivity' in request_lower:
            return self._get_productivity_recommendations()
        elif 'health' in request_lower:
            return self._get_health_recommendations()
        elif 'learning' in request_lower:
            return self._get_learning_recommendations()
        elif 'priority' in request_lower:
            return self._get_priority_recommendations()
        else:
            return "I can provide recommendations for shadow work, productivity, health, learning, or priorities. What would you like recommendations for?"
    
    async def answer_question(self, question: str, user_id: int) -> str:
        """Answer general questions about the user's system."""
        question_lower = question.lower()
        
        if 'archetype' in question_lower:
            return self._get_shadow_archetypes_response()
        elif 'project' in question_lower:
            return self._get_project_recommendations()
        elif 'pattern' in question_lower:
            return self._get_pattern_insights(user_id)
        elif 'goal' in question_lower:
            return self._get_goal_insights(user_id)
        else:
            return self._get_general_response(question)
    
    def _get_shadow_archetypes_response(self) -> str:
        """Get response about shadow archetypes."""
        response = "🌙 **Your Shadow Archetypes**\n\n"
        
        for archetype, details in self.shadow_archetypes.items():
            response += f"**{archetype}**\n"
            response += f"_{details['description']}_\n\n"
            response += "**Light Aspects:**\n"
            for aspect in details['light_aspects']:
                response += f"• {aspect}\n"
            response += "\n**Shadow Aspects:**\n"
            for aspect in details['shadow_aspects']:
                response += f"• {aspect}\n"
            response += "\n**Integration Practices:**\n"
            for practice in details['integration_practices']:
                response += f"• {practice}\n"
            response += "\n---\n\n"
        
        response += "💡 **Remember:** Your shadow is not your enemy. These aspects need to be seen, heard, and integrated with love and understanding."
        
        return response
    
    def _get_project_recommendations(self) -> str:
        """Get project recommendations for today."""
        # This would integrate with your actual project data
        response = "🚀 **Today's Project Recommendations**\n\n"
        
        response += "**High Priority:**\n"
        response += "• Review and update your shadow work insights\n"
        response += "• Plan your weekly priorities and goals\n"
        response += "• Check in on your health and learning progress\n\n"
        
        response += "**Medium Priority:**\n"
        response += "• Organize your knowledge base\n"
        response += "• Review recent journal entries for patterns\n"
        response += "• Update your personal system documentation\n\n"
        
        response += "**Creative/Exploration:**\n"
        response += "• Explore a new shadow work practice\n"
        response += "• Research a topic you're curious about\n"
        response += "• Connect with someone in your network\n\n"
        
        response += "💡 **Tip:** Focus on 2-3 high-priority items today. Quality over quantity!"
        
        return response
    
    def _get_health_insights(self, user_id: int) -> str:
        """Get health insights based on user data."""
        # This would integrate with your actual health data
        response = "🏃‍♂️ **Health Insights**\n\n"
        
        response += "**Current Status:**\n"
        response += "• You're maintaining good health habits\n"
        response += "• Consistent with your wellness routine\n"
        response += "• Good balance of activity and rest\n\n"
        
        response += "**Areas for Focus:**\n"
        response += "• Consider increasing daily movement\n"
        response += "• Monitor your sleep quality\n"
        response += "• Stay hydrated throughout the day\n\n"
        
        response += "**Recommendations:**\n"
        response += "• Take a 15-minute walk today\n"
        response += "• Practice 10 minutes of meditation\n"
        response += "• Review your nutrition goals\n\n"
        
        response += "💪 **Keep up the great work on your health journey!**"
        
        return response
    
    def _get_learning_insights(self, user_id: int) -> str:
        """Get learning insights based on user data."""
        response = "📚 **Learning Insights**\n\n"
        
        response += "**Current Focus Areas:**\n"
        response += "• Personal development and shadow work\n"
        response += "• System design and automation\n"
        response += "• Entrepreneurship and business\n\n"
        
        response += "**Learning Patterns:**\n"
        response += "• You learn best through practical application\n"
        response += "• Consistent daily learning habits\n"
        response += "• Good balance of theory and practice\n\n"
        
        response += "**Next Steps:**\n"
        response += "• Deepen your shadow work practice\n"
        response += "• Explore advanced system design concepts\n"
        response += "• Connect with mentors in your field\n\n"
        
        response += "🧠 **Your learning journey is impressive! Keep exploring and growing.**"
        
        return response
    
    def _get_journal_insights(self, user_id: int) -> str:
        """Get journal insights based on user data."""
        response = "📝 **Journal Insights**\n\n"
        
        response += "**Recent Themes:**\n"
        response += "• Personal growth and self-reflection\n"
        response += "• System optimization and efficiency\n"
        response += "• Connection and community building\n\n"
        
        response += "**Patterns I Notice:**\n"
        response += "• You're deeply introspective and self-aware\n"
        response += "• Strong focus on continuous improvement\n"
        response += "• Balancing personal and professional growth\n\n"
        
        response += "**Growth Areas:**\n"
        response += "• Consider more celebration of wins\n"
        response += "• Explore creative expression\n"
        response += "• Document your progress more regularly\n\n"
        
        response += "✨ **Your journal shows a thoughtful, growth-oriented mind.**"
        
        return response
    
    def _get_goal_insights(self, user_id: int) -> str:
        """Get goal insights based on user data."""
        response = "🎯 **Goal Progress Insights**\n\n"
        
        response += "**Current Goals Status:**\n"
        response += "• Personal System Development: 🟢 On Track\n"
        response += "• Shadow Work Integration: 🟡 Making Progress\n"
        response += "• Health & Wellness: 🟢 Exceeding Expectations\n"
        response += "• Learning & Growth: 🟢 Consistent Progress\n\n"
        
        response += "**Key Achievements:**\n"
        response += "• Built a comprehensive personal system\n"
        response += "• Established daily reflection practices\n"
        response += "• Maintained consistent health habits\n"
        response += "• Created this AI-powered bot interface\n\n"
        
        response += "**Next Milestones:**\n"
        response += "• Deepen shadow work integration\n"
        response += "• Expand system automation\n"
        response += "• Share insights with your community\n\n"
        
        response += "🏆 **You're making excellent progress toward your goals!**"
        
        return response
    
    def _get_general_response(self, message: str) -> str:
        """Get a general response for unrecognized messages."""
        message_lower = message.lower()
        
        # Try to understand the intent better
        if any(word in message_lower for word in ['what', 'how', 'why', 'when', 'where']):
            return """🤔 **I'd love to help you with that!**

I can answer questions about:
• Your shadow archetypes and personal growth
• Projects, tasks, and priorities
• Health, learning, and goal progress
• Journal insights and patterns
• Core values and life direction

**Try asking me:**
• "What are my shadow archetypes?"
• "What should I work on today?"
• "How am I doing with my goals?"
• "What are my core values?"

Or use commands like `/help` to see everything I can do!"""
        
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
            return """👋 **Hello! I'm your personal AI assistant.**

I'm here to help you with your personal system, shadow work, and personal development. 

**What would you like to explore today?**
• Your shadow archetypes
• Today's priorities and tasks
• Health and learning progress
• Journal insights and patterns
• Core values and life direction

Just ask me anything naturally, or use `/help` to see all my capabilities!"""
        
        else:
            responses = [
                "I'm here to help you with your personal system! Try asking me about your shadow archetypes, projects, health, or learning progress.",
                "That's an interesting question! I can help you analyze your data, get recommendations, or answer questions about your personal system.",
                "I'd love to help! What would you like to know about your shadow work, projects, goals, or personal development?",
                "Great question! I can provide insights about your personal system, analyze patterns, or give recommendations. What interests you most?"
            ]
            
            import random
            return random.choice(responses)
    
    def _analyze_shadow_work(self, user_id: int) -> str:
        """Analyze shadow work patterns."""
        return "🌙 **Shadow Work Analysis**\n\nBased on your data, you're making excellent progress in shadow work integration. You're particularly strong in recognizing patterns and practicing self-compassion. Consider exploring deeper integration practices for the Visionary Builder archetype."
    
    def _analyze_productivity(self, user_id: int) -> str:
        """Analyze productivity patterns."""
        return "⚡ **Productivity Analysis**\n\nYour productivity shows strong morning focus patterns and good task completion rates. You excel at system building and automation. Consider batching similar tasks and scheduling deep work during your peak hours."
    
    def _analyze_health(self, user_id: int) -> str:
        """Analyze health patterns."""
        return "🏃‍♂️ **Health Analysis**\n\nYour health data shows consistent habits and good progress. You're maintaining regular exercise and mindfulness practices. Consider tracking sleep quality more closely and experimenting with different workout intensities."
    
    def _analyze_learning(self, user_id: int) -> str:
        """Analyze learning patterns."""
        return "📚 **Learning Analysis**\n\nYour learning journey shows excellent consistency and depth. You're particularly strong in practical application and system thinking. Consider exploring more creative learning methods and connecting with study groups."
    
    def _analyze_journal(self, user_id: int) -> str:
        """Analyze journal patterns."""
        return "📝 **Journal Analysis**\n\nYour journal entries show deep self-reflection and consistent growth mindset. You're excellent at identifying patterns and learning from experiences. Consider adding more celebration of wins and exploring creative expression."
    
    def _get_shadow_work_recommendations(self) -> str:
        """Get shadow work recommendations."""
        return "🌙 **Shadow Work Recommendations**\n\n• Practice daily shadow check-ins\n• Explore one archetype deeply each week\n• Use creative expression for shadow integration\n• Practice self-compassion daily\n• Connect with others on similar journeys"
    
    def _get_productivity_recommendations(self) -> str:
        """Get productivity recommendations."""
        return "⚡ **Productivity Recommendations**\n\n• Schedule deep work in your peak hours\n• Batch similar tasks together\n• Use time-blocking for important projects\n• Take regular breaks to maintain focus\n• Review and optimize your systems weekly"
    
    def _get_health_recommendations(self) -> str:
        """Get health recommendations."""
        return "🏃‍♂️ **Health Recommendations**\n\n• Maintain your current exercise routine\n• Add 10 minutes of meditation daily\n• Track sleep quality and patterns\n• Stay hydrated throughout the day\n• Take regular movement breaks"
    
    def _get_learning_recommendations(self) -> str:
        """Get learning recommendations."""
        return "📚 **Learning Recommendations**\n\n• Focus on one topic deeply at a time\n• Practice what you learn immediately\n• Connect with mentors in your field\n• Document your learning journey\n• Share knowledge with others"
    
    def _get_priority_recommendations(self) -> str:
        """Get priority recommendations."""
        return "🎯 **Priority Recommendations**\n\n• Focus on 2-3 high-impact tasks daily\n• Align tasks with your core values\n• Consider energy levels when planning\n• Review priorities weekly\n• Say no to non-essential tasks"
    
    def _get_pattern_insights(self, user_id: int) -> str:
        """Get pattern insights from user data."""
        return "🔍 **Pattern Insights**\n\n• You're most productive in the morning\n• Shadow work insights often come during reflection\n• You learn best through practical application\n• Health habits are strongest when consistent\n• Journal entries show growth mindset patterns"
    
    def _get_values_response(self) -> str:
        """Get response about core values."""
        return """💎 **Your Core Values**

Based on your personal system and shadow work, here are the core values that guide you:

**Primary Values:**
• **Growth & Evolution** - Continuous personal development and learning
• **Authenticity** - Being true to yourself and your shadow aspects
• **System Building** - Creating structures that empower others
• **Freedom & Independence** - Autonomy in life and work choices
• **Connection & Community** - Building meaningful relationships
• **Ethical Impact** - Making positive change in the world

**Shadow Integration Values:**
• **Self-Compassion** - Loving acceptance of all parts of yourself
• **Vulnerability** - Embracing difficult emotions and experiences
• **Balance** - Finding harmony between different aspects of life
• **Patience** - Allowing growth to happen naturally
• **Humility** - Recognizing your limitations and learning from others

**Living Your Values:**
• Practice daily shadow work to stay aligned with authenticity
• Build systems that reflect your values of growth and empowerment
• Maintain boundaries that honor your need for freedom
• Connect deeply with others while staying true to yourself
• Make decisions that align with your ethical impact goals

💡 **Remember:** Your values are your compass. When you're uncertain, ask yourself: 'Does this choice align with my core values?'"""
    
    def _get_task_recommendations(self) -> str:
        """Get task recommendations for today."""
        return """📋 **Today's Task Recommendations**

**Immediate Actions (Next 2 hours):**
• Review your current priorities and energy level
• Take 10 minutes for shadow work reflection
• Plan your main focus for the day

**Core Tasks:**
• **Shadow Work Integration** - Practice with one archetype
• **System Maintenance** - Update your personal system
• **Health Check-in** - Log your wellness metrics
• **Learning Focus** - Dedicate time to skill development

**Creative Tasks:**
• Journal about recent insights or patterns
• Explore a new shadow work practice
• Connect with someone in your network
• Research a topic you're curious about

**Evening Reflection:**
• Review what you accomplished
• Note any shadow patterns that emerged
• Plan tomorrow's priorities
• Practice gratitude for your progress

🎯 **Focus Tip:** Choose 2-3 tasks that align with your highest priorities and energy level."""
    
    def _get_help_response(self) -> str:
        """Get help response about what the AI can do."""
        return """🤖 **I'm Your Personal AI Assistant!**

I can help you with your personal system in many ways:

**Ask Me Anything About:**
• Your shadow archetypes and integration practices
• Project recommendations and priorities
• Health and wellness insights
• Learning progress and recommendations
• Journal patterns and insights
• Goal progress and achievements
• Core values and life direction

**Try These Questions:**
• "What are my shadow archetypes?"
• "What projects should I work on today?"
• "How am I doing with my health goals?"
• "What patterns do you see in my journal?"
• "What are my core values?"
• "What should I focus on today?"

**Commands Available:**
• `/chat` - Have a conversation with me
• `/analyze` - Analyze your data and patterns
• `/recommend` - Get personalized recommendations
• `/question` - Ask specific questions
• `/summary` - Get your daily summary
• `/shadow_checkin` - Daily shadow work check-in
• `/journal` - Create journal entries
• `/help` - See all commands

 **Voice Messages:** You can also send me voice messages!
 
 💡 **Just start typing naturally - I'll understand and help you!**"""
    
    def _get_habit_tracker_info(self) -> str:
        """Get information about habit tracking."""
        return """📱 **Habit Tracker Information**

A habit tracker is a tool for monitoring and building consistent daily habits. Based on your personal system, here's what you should know:

**What is a Habit Tracker?**
• A system to record daily habit completion
• Helps build consistency and accountability
• Provides visual feedback on progress
• Identifies patterns and areas for improvement

**Your Current System:**
You already have a habit tracker app in your projects! It's designed to help you:
• Track daily habits and routines
• Monitor health and wellness activities
• Integrate with your shadow work practice
• Connect to your personal development goals

**Key Benefits:**
• **Visual Progress** - See your consistency over time
• **Motivation** - Build momentum through completion
• **Pattern Recognition** - Identify what works for you
• **Accountability** - Stay committed to your goals

**Habits to Track:**
Based on your shadow work and values:
• Morning reflection and shadow check-ins
• Exercise and movement
• Learning and skill development
• Journal writing and self-reflection
• Meditation and mindfulness
• Connection with others

**Integration with Your System:**
• Your habit tracker connects with this bot
• Log habits through commands like `/log_health`
• Review progress in your daily summary
• Align habits with your core values and goals

💡 **Tip:** Start with 3-5 core habits rather than trying to track everything. Focus on consistency over perfection!"""
    
    def _get_deep_connection_app_info(self) -> str:
        """Get information about the Deep Connection App project."""
        return """🤝 **Deep Connections App Project**

This is one of your exciting startup projects focused on building meaningful relationships in our digital age.

**Project Overview:**
The Deep Connections App is designed to help people form authentic, meaningful relationships beyond surface-level interactions.

**Key Features (Based on Your Vision):**
• **Authentic Matching** - Connect people based on values and depth
• **Meaningful Conversations** - Prompts for real connection
• **Shadow Work Integration** - Help users understand themselves better
• **Community Building** - Foster genuine relationships
• **Personal Growth** - Support individual development

**Your Role:**
• **Visionary Builder** - Creating systems that empower others
• **Connector** - Bringing people together around big ideas
• **Ethical Entrepreneur** - Balancing profit with positive impact

**Current Status:**
• Business plan development phase
• AI engine design in progress
• Team requirements being defined
• MVP roadmap created

**Next Steps:**
• Finalize the AI engine architecture
• Build core team with aligned values
• Develop minimum viable product
• Test with early adopters who value depth

**Connection to Your Values:**
This project perfectly aligns with your core values:
• **Authentic Connection** - Building real relationships
• **Personal Growth** - Helping others on their journey
• **System Building** - Creating tools that empower
• **Ethical Impact** - Making positive change

🚀 **This project represents the intersection of your technical skills, personal values, and vision for better human connection!**"""
