/**
 * Vercel Edge Function for Shadow Work Tracking
 * Minimal cold start, privacy-focused
 */

import { createClient } from '@supabase/supabase-js'

// Environment variables (set in Vercel dashboard)
const SUPABASE_URL = process.env.SUPABASE_URL
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID

// Initialize Supabase client
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

export default async function handler(request, response) {
  console.log('🌓 Shadow Work Tracker activated')

  try {
    const { action, data } = await request.json()

    switch (action) {
      case 'daily_checkin':
        return await handleDailyCheckin(data, response)

      case 'weekly_exploration':
        return await handleWeeklyExploration(data, response)

      case 'get_reminders':
        return await handleGetReminders(response)

      case 'generate_report':
        return await handleGenerateReport(response)

      default:
        return response.status(400).json({
          error: 'Invalid action',
          supported_actions: ['daily_checkin', 'weekly_exploration', 'get_reminders', 'generate_report']
        })
    }

  } catch (error) {
    console.error('Shadow work error:', error)
    return response.status(500).json({
      error: 'Internal server error',
      message: error.message
    })
  }
}

async function handleDailyCheckin(data, response) {
  const { shadow_aspect, pattern_observed, integration_insight } = data

  // Insert into Supabase (encrypted storage)
  const { data: result, error } = await supabase
    .from('shadow_work_daily')
    .insert([{
      date: new Date().toISOString().split('T')[0],
      shadow_aspect: shadow_aspect,
      pattern_observed: pattern_observed,
      integration_insight: integration_insight,
      timestamp: new Date().toISOString()
    }])

  if (error) {
    console.error('Database error:', error)
    return response.status(500).json({ error: 'Failed to save daily check-in' })
  }

  // Send minimal Telegram notification
  await sendTelegramMessage(`✅ Daily shadow check-in recorded: ${shadow_aspect}`)

  return response.json({
    success: true,
    message: 'Daily shadow check-in recorded',
    data: result
  })
}

async function handleWeeklyExploration(data, response) {
  const { archetype, light_aspects, shadow_aspects, integration_practice } = data

  const weekStart = getWeekStart()
  const { data: result, error } = await supabase
    .from('shadow_work_weekly')
    .insert([{
      week_start: weekStart,
      archetype: archetype,
      light_aspects: light_aspects || [],
      shadow_aspects: shadow_aspects || [],
      integration_practice: integration_practice,
      timestamp: new Date().toISOString()
    }])

  if (error) {
    return response.status(500).json({ error: 'Failed to save weekly exploration' })
  }

  await sendTelegramMessage(`🌓 Weekly shadow exploration recorded for ${archetype}`)

  return response.json({
    success: true,
    message: 'Weekly shadow exploration recorded',
    data: result
  })
}

async function handleGetReminders(response) {
  const today = new Date().toISOString().split('T')[0]
  const weekStart = getWeekStart()
  const currentMonth = new Date().toISOString().slice(0, 7)

  // Check for missing daily, weekly, monthly practices
  const { data: dailyData } = await supabase
    .from('shadow_work_daily')
    .select('date')
    .eq('date', today)

  const { data: weeklyData } = await supabase
    .from('shadow_work_weekly')
    .select('week_start')
    .eq('week_start', weekStart)

  const { data: monthlyData } = await supabase
    .from('shadow_work_monthly')
    .select('month')
    .eq('month', currentMonth)

  const reminders = []

  if (!dailyData || dailyData.length === 0) {
    reminders.push('🔍 Daily shadow check-in due')
  }

  if (!weeklyData || weeklyData.length === 0) {
    reminders.push('📝 Weekly shadow archetype exploration due')
  }

  if (!monthlyData || monthlyData.length === 0) {
    reminders.push('🕯️ Monthly shadow integration ceremony due')
  }

  return response.json({
    reminders: reminders,
    message: reminders.length > 0 ? 'Reminders generated' : 'All practices up to date'
  })
}

async function handleGenerateReport(response) {
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

  // Get recent data
  const { data: dailyData } = await supabase
    .from('shadow_work_daily')
    .select('*')
    .gte('timestamp', thirtyDaysAgo.toISOString())

  const { data: weeklyData } = await supabase
    .from('shadow_work_weekly')
    .select('*')
    .gte('timestamp', thirtyDaysAgo.toISOString())

  // Generate simple report
  const report = {
    period: 'Last 30 days',
    daily_checkins: dailyData?.length || 0,
    weekly_explorations: weeklyData?.length || 0,
    streak: calculateStreak(dailyData),
    insights: generateInsights(dailyData, weeklyData)
  }

  return response.json({
    success: true,
    report: report
  })
}

function getWeekStart() {
  const now = new Date()
  const dayOfWeek = now.getDay()
  const diff = now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1)
  const monday = new Date(now.setDate(diff))
  return monday.toISOString().split('T')[0]
}

function calculateStreak(dailyData) {
  if (!dailyData || dailyData.length === 0) return 0

  // Simple streak calculation
  let streak = 0
  const sortedDates = dailyData
    .map(d => d.date)
    .sort()
    .reverse()

  const today = new Date().toISOString().split('T')[0]
  let currentDate = today

  for (const date of sortedDates) {
    if (date === currentDate) {
      streak++
      const prevDate = new Date(currentDate)
      prevDate.setDate(prevDate.getDate() - 1)
      currentDate = prevDate.toISOString().split('T')[0]
    } else {
      break
    }
  }

  return streak
}

function generateInsights(dailyData, weeklyData) {
  const insights = []

  if (dailyData && dailyData.length > 0) {
    insights.push(`Completed ${dailyData.length} daily check-ins`)
  }

  if (weeklyData && weeklyData.length > 0) {
    insights.push(`Explored ${weeklyData.length} shadow archetypes`)
  }

  return insights
}

async function sendTelegramMessage(text) {
  if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
    console.log('Telegram credentials not available')
    return
  }

  try {
    const response = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_id: TELEGRAM_CHAT_ID,
        text: text,
        disable_notification: true // Silent notification
      })
    })

    if (response.ok) {
      console.log('✅ Telegram notification sent')
    }
  } catch (error) {
    console.error('Telegram send error:', error)
  }
}

// Export for Vercel
export const config = {
  runtime: 'edge'
}
