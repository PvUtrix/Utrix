#!/usr/bin/env python3
# Manual Input Example
# This shows how to implement manual data entry forms
# to replace fake data generation

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class ManualDataCollector:
    """Example implementation of manual data collection"""
    
    def __init__(self):
        self.data_file = Path("manual_data.json")
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing manually entered data"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                self.existing_data = json.load(f)
        else:
            self.existing_data = {}
    
    def collect_health_data(self) -> Dict[str, Any]:
        """Collect health data through manual input"""
        print("\n🏃 Health & Wellness Data Entry")
        print("=" * 40)
        
        try:
            steps = int(input("Steps today: ") or "0")
            sleep_hours = float(input("Sleep hours: ") or "0")
            water_glasses = int(input("Water glasses: ") or "0")
            workout = input("Workout completed? (y/n): ").lower() == 'y'
            meditation = int(input("Meditation minutes: ") or "0")
            energy = int(input("Energy level (1-10): ") or "5")
            
            return {
                "steps": steps,
                "sleep_hours": sleep_hours,
                "water_glasses": water_glasses,
                "workout_completed": workout,
                "meditation_minutes": meditation,
                "energy_level": energy
            }
        except ValueError:
            print("❌ Invalid input. Please enter numbers only.")
            return None
    
    def collect_productivity_data(self) -> Dict[str, Any]:
        """Collect productivity data through manual input"""
        print("\n💼 Productivity Data Entry")
        print("=" * 40)
        
        try:
            tasks_completed = int(input("Tasks completed: ") or "0")
            focus_time = float(input("Focus time hours: ") or "0")
            meetings = int(input("Meetings attended: ") or "0")
            code_commits = int(input("Code commits: ") or "0")
            documents = int(input("Documents created: ") or "0")
            emails = int(input("Emails processed: ") or "0")
            
            return {
                "tasks_completed": tasks_completed,
                "focus_time_hours": focus_time,
                "meetings_attended": meetings,
                "code_commits": code_commits,
                "documents_created": documents,
                "emails_processed": emails
            }
        except ValueError:
            print("❌ Invalid input. Please enter numbers only.")
            return None
    
    def collect_learning_data(self) -> Dict[str, Any]:
        """Collect learning data through manual input"""
        print("\n📚 Learning & Growth Data Entry")
        print("=" * 40)
        
        try:
            reading_minutes = int(input("Reading minutes: ") or "0")
            lessons_completed = int(input("Lessons completed: ") or "0")
            notes_created = int(input("Notes created: ") or "0")
            topics = input("Topics studied (comma-separated): ").strip()
            topics_list = [t.strip() for t in topics.split(",") if t.strip()]
            
            return {
                "reading_minutes": reading_minutes,
                "courses_progress": f"{lessons_completed} lessons completed",
                "notes_created": notes_created,
                "topics_studied": topics_list
            }
        except (ValueError, KeyboardInterrupt):
            print("❌ Invalid input. Please enter numbers only.")
            return None
    
    def collect_finance_data(self) -> Dict[str, Any]:
        """Collect finance data through manual input"""
        print("\n💰 Finance Data Entry")
        print("=" * 40)
        
        try:
            spending = float(input("Spent today ($): ") or "0")
            budget_remaining = float(input("Budget remaining ($): ") or "0")
            investment_change = float(input("Investment change (%): ") or "0")
            savings_rate = int(input("Savings rate (%): ") or "0")
            
            return {
                "spending_today": spending,
                "budget_remaining": budget_remaining,
                "investment_change": investment_change,
                "savings_rate": f"{savings_rate}%"
            }
        except ValueError:
            print("❌ Invalid input. Please enter numbers only.")
            return None
    
    def save_data(self, data: Dict[str, Any]):
        """Save collected data to file"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.existing_data[today] = data
        
        with open(self.data_file, 'w') as f:
            json.dump(self.existing_data, f, indent=2)
        
        print(f"\n✅ Data saved for {today}")
    
    def run_collection(self):
        """Run the complete data collection process"""
        print("📊 Manual Data Collection")
        print("=" * 50)
        print("Enter your data for today. Press Enter to skip any field.\n")
        
        # Collect all data
        health_data = self.collect_health_data()
        productivity_data = self.collect_productivity_data()
        learning_data = self.collect_learning_data()
        finance_data = self.collect_finance_data()
        
        # Combine all data
        if all([health_data, productivity_data, learning_data, finance_data]):
            combined_data = {
                "health": health_data,
                "productivity": productivity_data,
                "learning": learning_data,
                "finance": finance_data,
                "collected_at": datetime.now().isoformat()
            }
            
            self.save_data(combined_data)
            print("\n🎉 All data collected successfully!")
        else:
            print("\n❌ Some data collection failed. Please try again.")

def main():
    """Main function to run manual data collection"""
    collector = ManualDataCollector()
    collector.run_collection()

if __name__ == "__main__":
    main()
