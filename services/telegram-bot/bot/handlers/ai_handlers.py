"""
AI-powered handlers for the Personal System Telegram Bot.
Handles conversational interactions and intelligent responses.
"""

import logging
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import get_logger, log_command
from integrations.ai_assistant import AIAssistant
from integrations.personal_system import PersonalSystemIntegration


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle conversational chat with the AI assistant."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    # Get the message text
    message_text = update.message.text.replace('/chat', '').strip()
    
    if not message_text:
        await update.message.reply_text(
            "🤖 **AI Assistant Chat**\n\n"
            "I'm here to help you with your personal system! Ask me anything about:\n\n"
            "• Your shadow work and archetypes\n"
            "• Projects and tasks\n"
            "• Health and learning progress\n"
            "• Journal insights and patterns\n"
            "• System recommendations\n\n"
            "**Examples:**\n"
            "• \"What are my shadow archetypes?\"\n"
            "• \"What projects should I work on today?\"\n"
            "• \"How am I doing with my health goals?\"\n"
            "• \"What patterns do you see in my journal?\"\n\n"
            "Just send me a message or use `/chat [your question]`",
            parse_mode='Markdown'
        )
        return
    
    log_command(get_logger(__name__), user_id, username, "/chat", message_text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Get AI response
        ai_assistant = AIAssistant({})
        response = await ai_assistant.get_response(message_text, user_id)
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        get_logger(__name__).error(f"Error in AI chat: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error processing your request. Please try again."
        )


async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages and convert to text for AI processing."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    if not update.message.voice:
        return
    
    log_command(get_logger(__name__), user_id, username, "voice_message")
    
    try:
        # Show processing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Download and process voice message
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        voice_path = f"data/cache/voice_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg"
        
        # Download the file
        await voice_file.download_to_drive(voice_path)
        
        # Convert speech to text
        ai_assistant = AIAssistant({})
        transcribed_text = await ai_assistant.transcribe_voice(voice_path)
        
        if not transcribed_text:
            await update.message.reply_text(
                "❌ Sorry, I couldn't understand the voice message. Please try again or send a text message."
            )
            return
        
        # Send the transcribed text back to user
        await update.message.reply_text(
            f"🎤 **Voice Message Transcribed:**\n\n"
            f"\"{transcribed_text}\"\n\n"
            "🔍 **Analyzing intent and processing your request...**",
            parse_mode='Markdown'
        )
        
        # Analyze intent and get AI response
        response = await ai_assistant.get_response(transcribed_text, user_id)
        
        # Send the response with intent analysis
        await update.message.reply_text(
            f"🤖 **AI Response:**\n\n{response}",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        get_logger(__name__).error(f"Error processing voice message: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error processing your voice message. Please try again."
        )


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle analysis requests for the user's data."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    # Get the analysis request
    message_text = update.message.text.replace('/analyze', '').strip()
    
    if not message_text:
        await update.message.reply_text(
            "📊 **Data Analysis**\n\n"
            "I can analyze your personal data and provide insights. What would you like me to analyze?\n\n"
            "**Examples:**\n"
            "• `/analyze my shadow work patterns`\n"
            "• `/analyze my productivity trends`\n"
            "• `/analyze my health progress`\n"
            "• `/analyze my learning journey`\n"
            "• `/analyze my journal themes`\n\n"
            "Just tell me what you'd like analyzed!",
            parse_mode='Markdown'
        )
        return
    
    log_command(get_logger(__name__), user_id, username, "/analyze", message_text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Get AI analysis
        ai_assistant = AIAssistant({})
        analysis = await ai_assistant.analyze_data(message_text, user_id)
        
        await update.message.reply_text(analysis, parse_mode='Markdown')
        
    except Exception as e:
        get_logger(__name__).error(f"Error in data analysis: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error analyzing your data. Please try again."
        )


async def recommend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle recommendation requests."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    # Get the recommendation request
    message_text = update.message.text.replace('/recommend', '').strip()
    
    if not message_text:
        await update.message.reply_text(
            "💡 **Personal Recommendations**\n\n"
            "I can provide personalized recommendations based on your data. What would you like recommendations for?\n\n"
            "**Examples:**\n"
            "• `/recommend shadow work practices`\n"
            "• `/recommend productivity improvements`\n"
            "• `/recommend health habits`\n"
            "• `/recommend learning topics`\n"
            "• `/recommend today's priorities`\n\n"
            "Just tell me what you'd like recommendations for!",
            parse_mode='Markdown'
        )
        return
    
    log_command(get_logger(__name__), user_id, username, "/recommend", message_text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Get AI recommendations
        ai_assistant = AIAssistant({})
        recommendations = await ai_assistant.get_recommendations(message_text, user_id)
        
        await update.message.reply_text(recommendations, parse_mode='Markdown')
        
    except Exception as e:
        get_logger(__name__).error(f"Error getting recommendations: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error generating recommendations. Please try again."
        )


async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general questions about the user's system."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    # Get the question
    message_text = update.message.text.replace('/question', '').strip()
    
    if not message_text:
        await update.message.reply_text(
            "❓ **Ask Me Anything**\n\n"
            "I can answer questions about your personal system and data. What would you like to know?\n\n"
            "**Examples:**\n"
            "• `/question What are my shadow archetypes?`\n"
            "• `/question What projects should I work on today?`\n"
            "• `/question How am I doing with my goals?`\n"
            "• `/question What patterns do you see in my data?`\n\n"
            "Just ask me anything!",
            parse_mode='Markdown'
        )
        return
    
    log_command(get_logger(__name__), user_id, username, "/question", message_text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Get AI answer
        ai_assistant = AIAssistant({})
        answer = await ai_assistant.answer_question(message_text, user_id)
        
        await update.message.reply_text(answer, parse_mode='Markdown')
        
    except Exception as e:
        get_logger(__name__).error(f"Error answering question: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error answering your question. Please try again."
        )


async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general text messages as conversational AI."""
    user_id = context.user_data.get('user_id')
    username = context.user_data.get('username', 'unknown')
    
    message_text = update.message.text
    log_command(get_logger(__name__), user_id, username, "text_message", message_text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Get AI response
        ai_assistant = AIAssistant({})
        response = await ai_assistant.get_response(message_text, user_id)
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        get_logger(__name__).error(f"Error in text message handling: {e}")
        await update.message.reply_text(
            "I'm here to help! Try asking me about your shadow archetypes, projects, or use one of the commands like `/help`"
        )
