#!/usr/bin/env python3
"""
Sales Automation Script
Automates sales processes for the startup
"""

import yaml
import json
from datetime import datetime
from pathlib import Path

class SalesAutomation:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.sales_dir = Path("automation/sales")
        self.sales_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_lead_scoring(self):
        """Set up automated lead scoring"""
        print("Setting up lead scoring system...")
        
        # Create lead scoring configuration
        scoring_config = {
            "engagement_weight": 0.35,
            "qualification_weight": 0.65,
            "thresholds": {
                "hot_lead": 80,
                "warm_lead": 60,
                "cold_lead": 40
            },
            "criteria": {
                "engagement": {
                    "website_visits": 5,
                    "email_opens": 2,
                    "email_clicks": 5,
                    "demo_requests": 20
                },
                "qualification": {
                    "company_size": 10,
                    "budget_range": 15,
                    "decision_timeline": 10,
                    "authority_level": 15
                }
            }
        }
        
        # Save configuration
        with open(self.sales_dir / "lead-scoring-config.json", 'w') as f:
            json.dump(scoring_config, f, indent=2)
        
        print("Lead scoring system configured")
    
    def setup_email_sequences(self):
        """Set up automated email sequences"""
        print("Setting up email sequences...")
        
        # Create email sequence templates
        sequences = {
            "welcome": {
                "emails": [
                    {
                        "subject": "Welcome to {company_name}",
                        "delay": 0,
                        "content": "Welcome message and company overview"
                    },
                    {
                        "subject": "How {company_name} can help you",
                        "delay": 2,
                        "content": "Value proposition and case studies"
                    },
                    {
                        "subject": "Ready to see {company_name} in action?",
                        "delay": 5,
                        "content": "Demo invitation and next steps"
                    }
                ]
            },
            "nurture": {
                "emails": [
                    {
                        "subject": "Industry insights from {company_name}",
                        "delay": 0,
                        "content": "Industry trends and insights"
                    },
                    {
                        "subject": "Success story: {company_name} client",
                        "delay": 7,
                        "content": "Customer success story"
                    },
                    {
                        "subject": "5 ways {company_name} saves time",
                        "delay": 14,
                        "content": "Key features and benefits"
                    }
                ]
            }
        }
        
        # Save sequences
        with open(self.sales_dir / "email-sequences.json", 'w') as f:
            json.dump(sequences, f, indent=2)
        
        print("Email sequences configured")
    
    def setup_sales_dashboard(self):
        """Set up sales performance dashboard"""
        print("Setting up sales dashboard...")
        
        # Create dashboard configuration
        dashboard_config = {
            "name": "Sales Performance Dashboard",
            "widgets": [
                {
                    "name": "Lead Conversion Rate",
                    "type": "gauge",
                    "metric": "lead_conversion_rate",
                    "target": 25
                },
                {
                    "name": "Sales Pipeline",
                    "type": "funnel",
                    "metric": "sales_pipeline",
                    "stages": ["leads", "qualified", "proposals", "closed"]
                },
                {
                    "name": "Revenue Growth",
                    "type": "line",
                    "metric": "revenue_growth",
                    "period": "monthly"
                }
            ]
        }
        
        # Save dashboard configuration
        with open(self.sales_dir / "sales-dashboard.json", 'w') as f:
            json.dump(dashboard_config, f, indent=2)
        
        print("Sales dashboard configured")
    
    def run_automation(self):
        """Run sales automation setup"""
        print("Setting up sales automation...")
        
        self.setup_lead_scoring()
        self.setup_email_sequences()
        self.setup_sales_dashboard()
        
        print("Sales automation setup completed!")

def main():
    """Main function"""
    automation = SalesAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main()
