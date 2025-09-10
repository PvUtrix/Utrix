#!/usr/bin/env python3
"""
Shadow Work Tracker
Automated tracking and reminders for shadow work practices
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import argparse

class ShadowWorkTracker:
    def __init__(self, data_dir="automation/outputs"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.shadow_data_file = self.data_dir / "shadow_work_data.json"
        self.load_data()
    
    def load_data(self):
        """Load existing shadow work data"""
        if self.shadow_data_file.exists():
            with open(self.shadow_data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "daily_checkins": {},
                "weekly_explorations": {},
                "monthly_ceremonies": {},
                "quarterly_dives": {},
                "current_focus": {},
                "insights": [],
                "integration_wins": []
            }
    
    def save_data(self):
        """Save shadow work data"""
        with open(self.shadow_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_daily_checkin(self, date=None, shadow_aspect=None, pattern_observed=None, integration_insight=None):
        """Record daily shadow check-in"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.data["daily_checkins"][date] = {
            "shadow_aspect": shadow_aspect,
            "pattern_observed": pattern_observed,
            "integration_insight": integration_insight,
            "timestamp": datetime.now().isoformat()
        }
        self.save_data()
        print(f"✅ Daily shadow check-in recorded for {date}")
    
    def add_weekly_exploration(self, week_start=None, archetype=None, light_aspects=None, shadow_aspects=None, integration_practice=None):
        """Record weekly shadow archetype exploration"""
        if week_start is None:
            week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        
        self.data["weekly_explorations"][week_start] = {
            "archetype": archetype,
            "light_aspects": light_aspects or [],
            "shadow_aspects": shadow_aspects or [],
            "integration_practice": integration_practice,
            "timestamp": datetime.now().isoformat()
        }
        self.save_data()
        print(f"✅ Weekly shadow exploration recorded for week of {week_start}")
    
    def add_monthly_ceremony(self, month=None, shadow_aspect=None, breakthrough=None, integration_ritual=None):
        """Record monthly shadow integration ceremony"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        self.data["monthly_ceremonies"][month] = {
            "shadow_aspect": shadow_aspect,
            "breakthrough": breakthrough,
            "integration_ritual": integration_ritual,
            "timestamp": datetime.now().isoformat()
        }
        self.save_data()
        print(f"✅ Monthly shadow ceremony recorded for {month}")
    
    def add_quarterly_dive(self, quarter=None, focus_aspect=None, modalities_used=None, integration_plan=None):
        """Record quarterly deep shadow dive"""
        if quarter is None:
            current_month = datetime.now().month
            if current_month <= 3:
                quarter = f"{datetime.now().year}-Q1"
            elif current_month <= 6:
                quarter = f"{datetime.now().year}-Q2"
            elif current_month <= 9:
                quarter = f"{datetime.now().year}-Q3"
            else:
                quarter = f"{datetime.now().year}-Q4"
        
        self.data["quarterly_dives"][quarter] = {
            "focus_aspect": focus_aspect,
            "modalities_used": modalities_used or [],
            "integration_plan": integration_plan,
            "timestamp": datetime.now().isoformat()
        }
        self.save_data()
        print(f"✅ Quarterly shadow dive recorded for {quarter}")
    
    def add_insight(self, insight, category="general"):
        """Add a shadow work insight"""
        self.data["insights"].append({
            "insight": insight,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        self.save_data()
        print(f"💡 Insight recorded: {insight}")
    
    def add_integration_win(self, win_description, shadow_aspect=None):
        """Record a shadow integration win"""
        self.data["integration_wins"].append({
            "description": win_description,
            "shadow_aspect": shadow_aspect,
            "timestamp": datetime.now().isoformat()
        })
        self.save_data()
        print(f"🎉 Integration win recorded: {win_description}")
    
    def set_current_focus(self, shadow_aspect, integration_goal, timeline="monthly"):
        """Set current shadow work focus"""
        self.data["current_focus"] = {
            "shadow_aspect": shadow_aspect,
            "integration_goal": integration_goal,
            "timeline": timeline,
            "set_date": datetime.now().isoformat()
        }
        self.save_data()
        print(f"🎯 Current focus set: {shadow_aspect}")
    
    def get_streak(self, practice_type="daily"):
        """Get current streak for a practice type"""
        if practice_type == "daily":
            dates = sorted(self.data["daily_checkins"].keys(), reverse=True)
        elif practice_type == "weekly":
            dates = sorted(self.data["weekly_explorations"].keys(), reverse=True)
        elif practice_type == "monthly":
            dates = sorted(self.data["monthly_ceremonies"].keys(), reverse=True)
        else:
            return 0
        
        if not dates:
            return 0
        
        streak = 0
        current_date = datetime.now()
        
        for date_str in dates:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if practice_type == "daily":
                expected_date = current_date - timedelta(days=streak)
            elif practice_type == "weekly":
                expected_date = current_date - timedelta(weeks=streak)
            elif practice_type == "monthly":
                expected_date = current_date - timedelta(days=30*streak)
            
            if abs((date - expected_date).days) <= 1:  # Allow 1 day flexibility
                streak += 1
            else:
                break
        
        return streak
    
    def generate_report(self, days=30):
        """Generate a shadow work report"""
        report = []
        report.append("=" * 50)
        report.append("SHADOW WORK REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # Current streaks
        daily_streak = self.get_streak("daily")
        weekly_streak = self.get_streak("weekly")
        monthly_streak = self.get_streak("monthly")
        
        report.append("📊 CURRENT STREAKS:")
        report.append(f"   Daily check-ins: {daily_streak} days")
        report.append(f"   Weekly explorations: {weekly_streak} weeks")
        report.append(f"   Monthly ceremonies: {monthly_streak} months")
        report.append("")
        
        # Current focus
        if self.data["current_focus"]:
            focus = self.data["current_focus"]
            report.append("🎯 CURRENT FOCUS:")
            report.append(f"   Shadow aspect: {focus['shadow_aspect']}")
            report.append(f"   Integration goal: {focus['integration_goal']}")
            report.append(f"   Timeline: {focus['timeline']}")
            report.append("")
        
        # Recent insights
        recent_insights = self.data["insights"][-5:]  # Last 5 insights
        if recent_insights:
            report.append("💡 RECENT INSIGHTS:")
            for insight in recent_insights:
                date = datetime.fromisoformat(insight["timestamp"]).strftime("%m-%d")
                report.append(f"   [{date}] {insight['insight']}")
            report.append("")
        
        # Recent wins
        recent_wins = self.data["integration_wins"][-3:]  # Last 3 wins
        if recent_wins:
            report.append("🎉 RECENT INTEGRATION WINS:")
            for win in recent_wins:
                date = datetime.fromisoformat(win["timestamp"]).strftime("%m-%d")
                report.append(f"   [{date}] {win['description']}")
            report.append("")
        
        # Practice frequency
        report.append("📈 PRACTICE FREQUENCY (Last 30 days):")
        daily_count = len([d for d in self.data["daily_checkins"].keys() 
                          if (datetime.now() - datetime.strptime(d, "%Y-%m-%d")).days <= days])
        report.append(f"   Daily check-ins: {daily_count}/{days} days ({daily_count/days*100:.1f}%)")
        report.append("")
        
        return "\n".join(report)
    
    def get_reminders(self):
        """Get current reminders based on practice schedule"""
        reminders = []
        
        # Check daily practice
        last_daily = max(self.data["daily_checkins"].keys()) if self.data["daily_checkins"] else None
        if not last_daily or (datetime.now() - datetime.strptime(last_daily, "%Y-%m-%d")).days > 1:
            reminders.append("🔍 Daily shadow check-in due")
        
        # Check weekly practice
        last_weekly = max(self.data["weekly_explorations"].keys()) if self.data["weekly_explorations"] else None
        if not last_weekly or (datetime.now() - datetime.strptime(last_weekly, "%Y-%m-%d")).days > 7:
            reminders.append("📝 Weekly shadow archetype exploration due")
        
        # Check monthly practice
        current_month = datetime.now().strftime("%Y-%m")
        if current_month not in self.data["monthly_ceremonies"]:
            reminders.append("🕯️ Monthly shadow integration ceremony due")
        
        return reminders

def main():
    parser = argparse.ArgumentParser(description="Shadow Work Tracker")
    parser.add_argument("--action", choices=["checkin", "explore", "ceremony", "dive", "insight", "win", "focus", "report", "reminders"], 
                       help="Action to perform")
    parser.add_argument("--shadow-aspect", help="Shadow aspect to work with")
    parser.add_argument("--insight", help="Insight to record")
    parser.add_argument("--win", help="Integration win to record")
    parser.add_argument("--goal", help="Integration goal")
    
    args = parser.parse_args()
    
    tracker = ShadowWorkTracker()
    
    if args.action == "checkin":
        tracker.add_daily_checkin(shadow_aspect=args.shadow_aspect)
    elif args.action == "explore":
        tracker.add_weekly_exploration(archetype=args.shadow_aspect)
    elif args.action == "ceremony":
        tracker.add_monthly_ceremony(shadow_aspect=args.shadow_aspect)
    elif args.action == "dive":
        tracker.add_quarterly_dive(focus_aspect=args.shadow_aspect)
    elif args.action == "insight":
        tracker.add_insight(args.insight)
    elif args.action == "win":
        tracker.add_integration_win(args.win, args.shadow_aspect)
    elif args.action == "focus":
        tracker.set_current_focus(args.shadow_aspect, args.goal)
    elif args.action == "report":
        print(tracker.generate_report())
    elif args.action == "reminders":
        reminders = tracker.get_reminders()
        if reminders:
            print("🔔 REMINDERS:")
            for reminder in reminders:
                print(f"   {reminder}")
        else:
            print("✅ All practices up to date!")
    else:
        print("Please specify an action. Use --help for options.")

if __name__ == "__main__":
    main()
