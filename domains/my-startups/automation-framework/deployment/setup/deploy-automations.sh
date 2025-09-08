#!/bin/bash

# Startup Automation Framework - Deployment Script
# Usage: ./deploy-automations.sh --startup "<startup_name>" --template <template_name>

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
STARTUP_NAME=""
TEMPLATE_NAME=""
STARTUP_DIR=""
CONFIG_FILE=""

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 --startup \"<startup_name>\" --template <template_name>"
    echo ""
    echo "Available Templates:"
    echo "  sales          - Sales automation (lead generation, qualification, sales process)"
    echo "  marketing      - Marketing automation (campaigns, content, social media)"
    echo "  operations     - Operations automation (project management, resource management)"
    echo "  team           - Team management automation (communication, performance, tasks)"
    echo "  finance        - Financial automation (invoicing, payments, reporting)"
    echo "  customer-success - Customer success automation (onboarding, support, retention)"
    echo ""
    echo "Examples:"
    echo "  $0 --startup \"Tango.Vision\" --template sales"
    echo "  $0 --startup \"MySaaS\" --template operations"
    echo "  $0 --startup \"MyStore\" --template team"
}

# Function to validate startup directory
validate_startup() {
    if [ -z "$STARTUP_NAME" ]; then
        print_error "Startup name is required"
        show_usage
        exit 1
    fi
    
    STARTUP_DIR="../${STARTUP_NAME// /_}"
    CONFIG_FILE="$STARTUP_DIR/configs/startup-config.yaml"
    
    if [ ! -d "$STARTUP_DIR" ]; then
        print_error "Startup directory not found: $STARTUP_DIR"
        echo "Please run init-startup.sh first to create the startup structure"
        exit 1
    fi
    
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "Startup configuration not found: $CONFIG_FILE"
        echo "Please run configure-startup.sh first to configure the startup"
        exit 1
    fi
    
    print_success "Startup validated: $STARTUP_NAME"
}

# Function to validate template
validate_template() {
    case $TEMPLATE_NAME in
        sales|marketing|operations|team|finance|customer-success)
            return 0
            ;;
        *)
            print_error "Invalid template: $TEMPLATE_NAME"
            show_usage
            exit 1
            ;;
    esac
}

# Function to deploy sales automation
deploy_sales_automation() {
    print_status "Deploying sales automation for $STARTUP_NAME..."
    
    # Copy sales templates
    if [ -d "templates/sales" ]; then
        cp -r "templates/sales" "$STARTUP_DIR/automation/"
        print_success "Copied sales templates"
    else
        print_warning "Sales templates not found"
    fi
    
    # Create sales automation scripts
    cat > "$STARTUP_DIR/automation/scripts/sales-automation.py" << 'EOF'
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
EOF
    
    # Make script executable
    chmod +x "$STARTUP_DIR/automation/scripts/sales-automation.py"
    
    # Run the automation setup
    cd "$STARTUP_DIR"
    python3 automation/scripts/sales-automation.py
    
    print_success "Sales automation deployed successfully"
}

# Function to deploy operations automation
deploy_operations_automation() {
    print_status "Deploying operations automation for $STARTUP_NAME..."
    
    # Copy operations templates
    if [ -d "templates/operations" ]; then
        cp -r "templates/operations" "$STARTUP_DIR/automation/"
        print_success "Copied operations templates"
    else
        print_warning "Operations templates not found"
    fi
    
    # Create operations automation scripts
    cat > "$STARTUP_DIR/automation/scripts/operations-automation.py" << 'EOF'
#!/usr/bin/env python3
"""
Operations Automation Script
Automates operations processes for the startup
"""

import yaml
import json
from datetime import datetime
from pathlib import Path

class OperationsAutomation:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.operations_dir = Path("automation/operations")
        self.operations_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_project_management(self):
        """Set up automated project management"""
        print("Setting up project management...")
        
        # Create project management configuration
        pm_config = {
            "project_templates": {
                "digital_twin": {
                    "phases": [
                        "requirements_gathering",
                        "data_collection",
                        "3d_modeling",
                        "system_integration",
                        "testing",
                        "deployment"
                    ],
                    "timeline": 56,
                    "team_size": 5
                },
                "building_automation": {
                    "phases": [
                        "assessment",
                        "system_design",
                        "equipment_selection",
                        "installation",
                        "configuration",
                        "testing"
                    ],
                    "timeline": 45,
                    "team_size": 4
                }
            },
            "automation": {
                "task_assignment": True,
                "progress_tracking": True,
                "milestone_notifications": True,
                "resource_allocation": True
            }
        }
        
        # Save configuration
        with open(self.operations_dir / "project-management-config.json", 'w') as f:
            json.dump(pm_config, f, indent=2)
        
        print("Project management configured")
    
    def setup_resource_management(self):
        """Set up automated resource management"""
        print("Setting up resource management...")
        
        # Create resource management configuration
        rm_config = {
            "team_allocation": {
                "rules": [
                    "skill_based_assignment",
                    "workload_balancing",
                    "availability_checking",
                    "performance_consideration"
                ]
            },
            "capacity_planning": {
                "metrics": [
                    "team_utilization",
                    "project_capacity",
                    "skill_availability",
                    "workload_distribution"
                ]
            },
            "optimization": {
                "algorithms": [
                    "workload_balancing",
                    "skill_matching",
                    "deadline_optimization",
                    "resource_efficiency"
                ]
            }
        }
        
        # Save configuration
        with open(self.operations_dir / "resource-management-config.json", 'w') as f:
            json.dump(rm_config, f, indent=2)
        
        print("Resource management configured")
    
    def setup_quality_assurance(self):
        """Set up automated quality assurance"""
        print("Setting up quality assurance...")
        
        # Create quality assurance configuration
        qa_config = {
            "quality_standards": {
                "project_completion_rate": 95,
                "client_satisfaction_score": 8,
                "team_efficiency_score": 8,
                "error_rate": 5
            },
            "processes": [
                "quality_checkpoints",
                "client_feedback_collection",
                "performance_monitoring",
                "continuous_improvement"
            ],
            "automation": {
                "quality_checks": True,
                "performance_tracking": True,
                "feedback_collection": True,
                "improvement_suggestions": True
            }
        }
        
        # Save configuration
        with open(self.operations_dir / "quality-assurance-config.json", 'w') as f:
            json.dump(qa_config, f, indent=2)
        
        print("Quality assurance configured")
    
    def run_automation(self):
        """Run operations automation setup"""
        print("Setting up operations automation...")
        
        self.setup_project_management()
        self.setup_resource_management()
        self.setup_quality_assurance()
        
        print("Operations automation setup completed!")

def main():
    """Main function"""
    automation = OperationsAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main()
EOF
    
    # Make script executable
    chmod +x "$STARTUP_DIR/automation/scripts/operations-automation.py"
    
    # Run the automation setup
    cd "$STARTUP_DIR"
    python3 automation/scripts/operations-automation.py
    
    print_success "Operations automation deployed successfully"
}

# Function to deploy team automation
deploy_team_automation() {
    print_status "Deploying team automation for $STARTUP_NAME..."
    
    # Copy team templates
    if [ -d "templates/team" ]; then
        cp -r "templates/team" "$STARTUP_DIR/automation/"
        print_success "Copied team templates"
    else
        print_warning "Team templates not found"
    fi
    
    # Create team automation scripts
    cat > "$STARTUP_DIR/automation/scripts/team-automation.py" << 'EOF'
#!/usr/bin/env python3
"""
Team Automation Script
Automates team management processes for the startup
"""

import yaml
import json
from datetime import datetime
from pathlib import Path

class TeamAutomation:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.team_dir = Path("automation/team")
        self.team_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_communication(self):
        """Set up automated team communication"""
        print("Setting up team communication...")
        
        # Create communication configuration
        comm_config = {
            "daily_standup": {
                "enabled": True,
                "time": "09:00",
                "questions": [
                    "What did you accomplish yesterday?",
                    "What are you working on today?",
                    "Any blockers or challenges?",
                    "How can the team help?"
                ],
                "automation": {
                    "reminder": True,
                    "summary_generation": True,
                    "follow_up": True
                }
            },
            "team_coordination": {
                "enabled": True,
                "channels": ["slack", "teams", "email"],
                "automation": {
                    "task_assignment": True,
                    "progress_tracking": True,
                    "meeting_scheduling": True
                }
            }
        }
        
        # Save configuration
        with open(self.team_dir / "communication-config.json", 'w') as f:
            json.dump(comm_config, f, indent=2)
        
        print("Team communication configured")
    
    def setup_performance_management(self):
        """Set up automated performance management"""
        print("Setting up performance management...")
        
        # Create performance management configuration
        perf_config = {
            "goal_setting": {
                "enabled": True,
                "frequency": "quarterly",
                "automation": {
                    "goal_tracking": True,
                    "progress_monitoring": True,
                    "reminder_notifications": True
                }
            },
            "performance_reviews": {
                "enabled": True,
                "frequency": "quarterly",
                "automation": {
                    "review_scheduling": True,
                    "feedback_collection": True,
                    "report_generation": True
                }
            },
            "recognition": {
                "enabled": True,
                "automation": {
                    "achievement_tracking": True,
                    "recognition_notifications": True,
                    "reward_management": True
                }
            }
        }
        
        # Save configuration
        with open(self.team_dir / "performance-config.json", 'w') as f:
            json.dump(perf_config, f, indent=2)
        
        print("Performance management configured")
    
    def setup_task_management(self):
        """Set up automated task management"""
        print("Setting up task management...")
        
        # Create task management configuration
        task_config = {
            "task_assignment": {
                "enabled": True,
                "rules": [
                    "skill_based_assignment",
                    "workload_balancing",
                    "availability_checking",
                    "deadline_consideration"
                ]
            },
            "progress_tracking": {
                "enabled": True,
                "automation": {
                    "status_updates": True,
                    "milestone_tracking": True,
                    "deadline_monitoring": True
                }
            },
            "workload_balancing": {
                "enabled": True,
                "algorithms": [
                    "capacity_planning",
                    "skill_matching",
                    "priority_balancing",
                    "deadline_optimization"
                ]
            }
        }
        
        # Save configuration
        with open(self.team_dir / "task-management-config.json", 'w') as f:
            json.dump(task_config, f, indent=2)
        
        print("Task management configured")
    
    def run_automation(self):
        """Run team automation setup"""
        print("Setting up team automation...")
        
        self.setup_communication()
        self.setup_performance_management()
        self.setup_task_management()
        
        print("Team automation setup completed!")

def main():
    """Main function"""
    automation = TeamAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main()
EOF
    
    # Make script executable
    chmod +x "$STARTUP_DIR/automation/scripts/team-automation.py"
    
    # Run the automation setup
    cd "$STARTUP_DIR"
    python3 automation/scripts/team-automation.py
    
    print_success "Team automation deployed successfully"
}

# Function to deploy finance automation
deploy_finance_automation() {
    print_status "Deploying finance automation for $STARTUP_NAME..."
    
    # Copy finance templates
    if [ -d "templates/finance" ]; then
        cp -r "templates/finance" "$STARTUP_DIR/automation/"
        print_success "Copied finance templates"
    else
        print_warning "Finance templates not found"
    fi
    
    # Create finance automation scripts
    cat > "$STARTUP_DIR/automation/scripts/finance-automation.py" << 'EOF'
#!/usr/bin/env python3
"""
Finance Automation Script
Automates financial processes for the startup
"""

import yaml
import json
from datetime import datetime
from pathlib import Path

class FinanceAutomation:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.finance_dir = Path("automation/finance")
        self.finance_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_invoicing(self):
        """Set up automated invoicing"""
        print("Setting up automated invoicing...")
        
        # Create invoicing configuration
        invoice_config = {
            "automation": {
                "invoice_generation": True,
                "payment_tracking": True,
                "reminder_notifications": True,
                "late_payment_handling": True
            },
            "templates": {
                "project_based": {
                    "template": "project_invoice_template",
                    "automation": True
                },
                "subscription_based": {
                    "template": "subscription_invoice_template",
                    "automation": True
                }
            },
            "payment_tracking": {
                "enabled": True,
                "notifications": {
                    "payment_received": True,
                    "payment_overdue": True,
                    "payment_reminder": True
                }
            }
        }
        
        # Save configuration
        with open(self.finance_dir / "invoicing-config.json", 'w') as f:
            json.dump(invoice_config, f, indent=2)
        
        print("Invoicing automation configured")
    
    def setup_financial_reporting(self):
        """Set up automated financial reporting"""
        print("Setting up financial reporting...")
        
        # Create financial reporting configuration
        reporting_config = {
            "reports": {
                "daily": {
                    "enabled": True,
                    "metrics": ["revenue", "expenses", "cash_flow"]
                },
                "weekly": {
                    "enabled": True,
                    "metrics": ["revenue_growth", "expense_analysis", "profitability"]
                },
                "monthly": {
                    "enabled": True,
                    "metrics": ["financial_summary", "budget_variance", "forecasting"]
                },
                "quarterly": {
                    "enabled": True,
                    "metrics": ["comprehensive_financial_review", "trend_analysis", "planning"]
                }
            },
            "automation": {
                "report_generation": True,
                "distribution": True,
                "dashboard_updates": True,
                "alert_notifications": True
            }
        }
        
        # Save configuration
        with open(self.finance_dir / "reporting-config.json", 'w') as f:
            json.dump(reporting_config, f, indent=2)
        
        print("Financial reporting configured")
    
    def setup_budget_monitoring(self):
        """Set up automated budget monitoring"""
        print("Setting up budget monitoring...")
        
        # Create budget monitoring configuration
        budget_config = {
            "monitoring": {
                "enabled": True,
                "frequency": "daily",
                "thresholds": {
                    "expense_limit": 90,
                    "revenue_target": 80,
                    "cash_flow_warning": 30
                }
            },
            "alerts": {
                "enabled": True,
                "notifications": {
                    "budget_exceeded": True,
                    "revenue_shortfall": True,
                    "cash_flow_issues": True
                }
            },
            "automation": {
                "budget_tracking": True,
                "variance_analysis": True,
                "forecasting": True,
                "optimization_suggestions": True
            }
        }
        
        # Save configuration
        with open(self.finance_dir / "budget-config.json", 'w') as f:
            json.dump(budget_config, f, indent=2)
        
        print("Budget monitoring configured")
    
    def run_automation(self):
        """Run finance automation setup"""
        print("Setting up finance automation...")
        
        self.setup_invoicing()
        self.setup_financial_reporting()
        self.setup_budget_monitoring()
        
        print("Finance automation setup completed!")

def main():
    """Main function"""
    automation = FinanceAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main()
EOF
    
    # Make script executable
    chmod +x "$STARTUP_DIR/automation/scripts/finance-automation.py"
    
    # Run the automation setup
    cd "$STARTUP_DIR"
    python3 automation/scripts/finance-automation.py
    
    print_success "Finance automation deployed successfully"
}

# Function to deploy customer success automation
deploy_customer_success_automation() {
    print_status "Deploying customer success automation for $STARTUP_NAME..."
    
    # Copy customer success templates
    if [ -d "templates/customer-success" ]; then
        cp -r "templates/customer-success" "$STARTUP_DIR/automation/"
        print_success "Copied customer success templates"
    else
        print_warning "Customer success templates not found"
    fi
    
    # Create customer success automation scripts
    cat > "$STARTUP_DIR/automation/scripts/customer-success-automation.py" << 'EOF'
#!/usr/bin/env python3
"""
Customer Success Automation Script
Automates customer success processes for the startup
"""

import yaml
import json
from datetime import datetime
from pathlib import Path

class CustomerSuccessAutomation:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.cs_dir = Path("automation/customer-success")
        self.cs_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_onboarding(self):
        """Set up automated customer onboarding"""
        print("Setting up customer onboarding...")
        
        # Create onboarding configuration
        onboarding_config = {
            "phases": [
                {
                    "name": "Initial Setup",
                    "duration": 3,
                    "tasks": [
                        "Create customer account",
                        "Set up project workspace",
                        "Assign team members",
                        "Schedule kickoff meeting"
                    ]
                },
                {
                    "name": "Requirements Gathering",
                    "duration": 7,
                    "tasks": [
                        "Conduct discovery call",
                        "Gather requirements",
                        "Define project scope",
                        "Create project plan"
                    ]
                },
                {
                    "name": "System Setup",
                    "duration": 5,
                    "tasks": [
                        "Configure system",
                        "Set up integrations",
                        "Create documentation",
                        "Schedule training"
                    ]
                },
                {
                    "name": "Go Live",
                    "duration": 3,
                    "tasks": [
                        "Final testing",
                        "User training",
                        "Go live support",
                        "Success review"
                    ]
                }
            ],
            "automation": {
                "task_assignment": True,
                "progress_tracking": True,
                "milestone_notifications": True,
                "success_celebration": True
            }
        }
        
        # Save configuration
        with open(self.cs_dir / "onboarding-config.json", 'w') as f:
            json.dump(onboarding_config, f, indent=2)
        
        print("Customer onboarding configured")
    
    def setup_usage_tracking(self):
        """Set up automated usage tracking"""
        print("Setting up usage tracking...")
        
        # Create usage tracking configuration
        usage_config = {
            "tracking": {
                "enabled": True,
                "metrics": [
                    "feature_usage",
                    "user_engagement",
                    "system_performance",
                    "customer_satisfaction"
                ]
            },
            "automation": {
                "data_collection": True,
                "analysis": True,
                "reporting": True,
                "alerting": True
            },
            "alerts": {
                "low_usage": True,
                "performance_issues": True,
                "satisfaction_drops": True,
                "engagement_decline": True
            }
        }
        
        # Save configuration
        with open(self.cs_dir / "usage-tracking-config.json", 'w') as f:
            json.dump(usage_config, f, indent=2)
        
        print("Usage tracking configured")
    
    def setup_renewal_management(self):
        """Set up automated renewal management"""
        print("Setting up renewal management...")
        
        # Create renewal management configuration
        renewal_config = {
            "automation": {
                "renewal_tracking": True,
                "renewal_reminders": True,
                "renewal_negotiation": True,
                "renewal_celebration": True
            },
            "timeline": {
                "renewal_reminder": 90,  # days before
                "negotiation_start": 60,  # days before
                "final_reminder": 30,  # days before
                "renewal_deadline": 0  # days before
            },
            "processes": [
                "renewal_eligibility_check",
                "renewal_offer_generation",
                "renewal_negotiation",
                "renewal_completion"
            ]
        }
        
        # Save configuration
        with open(self.cs_dir / "renewal-config.json", 'w') as f:
            json.dump(renewal_config, f, indent=2)
        
        print("Renewal management configured")
    
    def run_automation(self):
        """Run customer success automation setup"""
        print("Setting up customer success automation...")
        
        self.setup_onboarding()
        self.setup_usage_tracking()
        self.setup_renewal_management()
        
        print("Customer success automation setup completed!")

def main():
    """Main function"""
    automation = CustomerSuccessAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main()
EOF
    
    # Make script executable
    chmod +x "$STARTUP_DIR/automation/scripts/customer-success-automation.py"
    
    # Run the automation setup
    cd "$STARTUP_DIR"
    python3 automation/scripts/customer-success-automation.py
    
    print_success "Customer success automation deployed successfully"
}

# Function to update startup configuration
update_startup_config() {
    print_status "Updating startup configuration..."
    
    # Add deployed template to configuration
    if [ -f "$CONFIG_FILE" ]; then
        # Create backup
        cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
        
        # Add template to configuration
        sed -i '' "/automation:/a\\
  deployed_templates:\\
    - $TEMPLATE_NAME" "$CONFIG_FILE"
        
        print_success "Startup configuration updated"
    else
        print_warning "Configuration file not found"
    fi
}

# Function to display deployment summary
display_deployment_summary() {
    echo ""
    print_success "Automation deployment completed!"
    echo ""
    echo "Deployment Summary:"
    echo "  Startup: $STARTUP_NAME"
    echo "  Template: $TEMPLATE_NAME"
    echo "  Directory: $STARTUP_DIR"
    echo ""
    echo "Next steps:"
    echo "1. Review deployed automation:"
    echo "   cd $STARTUP_DIR"
    echo "   ls -la automation/"
    echo ""
    echo "2. Configure integrations:"
    echo "   ./configure-startup.sh"
    echo ""
    echo "3. Set up monitoring:"
    echo "   ./setup-monitoring.sh --startup \"$STARTUP_NAME\""
    echo ""
    echo "4. Test automation:"
    echo "   python3 automation/scripts/${TEMPLATE_NAME}-automation.py"
    echo ""
    print_status "Your automation is ready to use!"
}

# Main execution
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --startup)
                STARTUP_NAME="$2"
                shift 2
                ;;
            --template)
                TEMPLATE_NAME="$2"
                shift 2
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Validate parameters
    validate_startup
    validate_template
    
    # Display deployment information
    echo ""
    print_status "Deploying automation for startup..."
    echo "Startup: $STARTUP_NAME"
    echo "Template: $TEMPLATE_NAME"
    echo ""
    
    # Deploy based on template
    case $TEMPLATE_NAME in
        sales)
            deploy_sales_automation
            ;;
        operations)
            deploy_operations_automation
            ;;
        team)
            deploy_team_automation
            ;;
        finance)
            deploy_finance_automation
            ;;
        customer-success)
            deploy_customer_success_automation
            ;;
        *)
            print_error "Template deployment not implemented: $TEMPLATE_NAME"
            exit 1
            ;;
    esac
    
    # Update configuration
    update_startup_config
    
    # Display summary
    display_deployment_summary
}

# Run main function
main "$@"
