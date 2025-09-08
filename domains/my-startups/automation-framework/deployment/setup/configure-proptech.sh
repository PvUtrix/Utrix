#!/bin/bash

# PropTech Startup Configuration Script
# Optimized for Tango.Vision and similar PropTech companies

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# Function to configure PropTech-specific settings
configure_proptech() {
    local startup_name="$1"
    local config_file="configs/startup-config.yaml"
    
    print_status "Configuring PropTech startup: $startup_name"
    
    # Update configuration with PropTech-specific settings
    cat >> "$config_file" << 'EOF'

# PropTech-specific configuration
proptech:
  focus_areas:
    - digital_twins
    - building_automation
    - property_management
    - tenant_experience
    - facility_management
  
  target_clients:
    - commercial_real_estate_owners
    - property_managers
    - facility_managers
    - building_operators
    - real_estate_developers
  
  key_metrics:
    - project_completion_rate
    - client_satisfaction_score
    - revenue_per_project
    - lead_to_close_time
    - team_efficiency_score
  
  automation_priorities:
    - lead_scoring_and_qualification
    - project_template_generation
    - client_communication_automation
    - team_coordination
    - financial_management

# Team configuration for PropTech
team:
  roles:
    - ceo_founder
    - sales_team
    - project_managers
    - developers
    - customer_success
    - operations
    - technical_specialists
  
  communication:
    daily_standup: automated_collection
    weekly_reviews: automated_reports
    monthly_planning: automated_templates
    quarterly_reviews: automated_dashboards
  
  automation:
    - task_assignment
    - progress_tracking
    - performance_monitoring
    - team_coordination

# Integration configuration for PropTech
integrations:
  crm: hubspot_or_salesforce
  email_marketing: mailchimp_or_hubspot
  project_management: asana_or_monday
  communication: slack_or_teams
  analytics: google_analytics
  automation: n8n_or_zapier
  document_management: google_drive_or_sharepoint
  calendar: google_calendar_or_outlook
  
  proptech_specific:
    - building_management_systems
    - iot_device_integration
    - 3d_modeling_tools
    - property_database_apis
    - real_estate_platforms

# Automation configuration for PropTech
automation:
  enabled: true
  level: high
  templates:
    - sales/lead-generation
    - sales/lead-qualification
    - sales/sales-process
    - operations/project-management
    - team/communication
    - finance/invoicing
    - customer-success/onboarding
  
  proptech_specific:
    - project_template_generation
    - client_onboarding_automation
    - progress_tracking
    - milestone_notifications
    - success_celebration
    - referral_requests

# Monitoring configuration for PropTech
monitoring:
  enabled: true
  dashboards:
    - sales_performance
    - project_delivery
    - team_efficiency
    - financial_health
    - customer_success
    - proptech_metrics
  
  alerts:
    - low_conversion_rates
    - project_delays
    - team_performance_issues
    - financial_thresholds
    - customer_satisfaction_drops
    - proptech_specific_alerts
  
  reports:
    - daily_sales_summary
    - weekly_team_performance
    - monthly_financial_review
    - quarterly_business_review
    - annual_strategy_review
    - proptech_performance_reports

# Success metrics for PropTech
success_metrics:
  primary:
    - lead_conversion_rate
    - project_completion_rate
    - client_satisfaction_score
    - revenue_per_project
    - team_efficiency_score
  
  secondary:
    - lead_to_close_time
    - project_profitability
    - customer_lifetime_value
    - team_productivity
    - automation_roi
  
  proptech_specific:
    - digital_twin_accuracy
    - building_automation_efficiency
    - tenant_satisfaction
    - facility_management_improvement
    - property_value_enhancement
  
  targets:
    lead_conversion_rate: 25_percent
    project_completion_rate: 95_percent
    client_satisfaction_score: 8_out_of_10
    revenue_per_project: 50000_usd
    team_efficiency_score: 8_out_of_10
EOF
    
    print_success "PropTech configuration added to startup config"
}

# Function to create PropTech-specific templates
create_proptech_templates() {
    print_status "Creating PropTech-specific templates..."
    
    # Create project template generator
    mkdir -p "automation/templates/proptech"
    
    cat > "automation/templates/proptech/project-template-generator.py" << 'EOF'
#!/usr/bin/env python3
"""
PropTech Project Template Generator
Automatically generates project templates for new clients
"""

import yaml
import json
from datetime import datetime
from pathlib import Path

class PropTechProjectTemplateGenerator:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.templates_dir = Path("automation/templates/proptech")
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def generate_project_template(self, client_info):
        """Generate project template for new client"""
        template = {
            "project_id": f"PT-{datetime.now().strftime('%Y%m%d')}-{client_info['id']}",
            "client_name": client_info["name"],
            "project_type": client_info["project_type"],
            "created_date": datetime.now().isoformat(),
            "status": "initiated",
            "phases": self.get_project_phases(client_info["project_type"]),
            "team_assignments": self.assign_team_members(client_info),
            "milestones": self.define_milestones(client_info["project_type"]),
            "deliverables": self.define_deliverables(client_info["project_type"]),
            "timeline": self.estimate_timeline(client_info["project_type"]),
            "budget": self.estimate_budget(client_info),
            "risks": self.identify_risks(client_info["project_type"]),
            "success_metrics": self.define_success_metrics(client_info["project_type"])
        }
        
        return template
    
    def get_project_phases(self, project_type):
        """Get project phases based on type"""
        phases = {
            "digital_twin": [
                "requirements_gathering",
                "data_collection",
                "3d_modeling",
                "system_integration",
                "testing",
                "deployment",
                "training",
                "go_live"
            ],
            "building_automation": [
                "assessment",
                "system_design",
                "equipment_selection",
                "installation",
                "configuration",
                "testing",
                "commissioning",
                "training"
            ],
            "property_management": [
                "current_state_analysis",
                "system_design",
                "implementation_planning",
                "system_setup",
                "data_migration",
                "user_training",
                "go_live",
                "support"
            ]
        }
        
        return phases.get(project_type, phases["digital_twin"])
    
    def assign_team_members(self, client_info):
        """Assign team members based on project requirements"""
        assignments = {
            "project_manager": "auto_assign",
            "technical_lead": "auto_assign",
            "customer_success": "auto_assign",
            "developer": "auto_assign"
        }
        
        # Add specific assignments based on project type
        if client_info["project_type"] == "digital_twin":
            assignments["3d_modeler"] = "auto_assign"
            assignments["iot_specialist"] = "auto_assign"
        elif client_info["project_type"] == "building_automation":
            assignments["automation_specialist"] = "auto_assign"
            assignments["electrical_engineer"] = "auto_assign"
        
        return assignments
    
    def define_milestones(self, project_type):
        """Define project milestones"""
        milestones = {
            "digital_twin": [
                {"name": "Requirements Complete", "days": 7},
                {"name": "Data Collection Complete", "days": 14},
                {"name": "3D Model Complete", "days": 21},
                {"name": "System Integration Complete", "days": 28},
                {"name": "Testing Complete", "days": 35},
                {"name": "Deployment Complete", "days": 42},
                {"name": "Training Complete", "days": 49},
                {"name": "Go Live", "days": 56}
            ],
            "building_automation": [
                {"name": "Assessment Complete", "days": 5},
                {"name": "System Design Complete", "days": 10},
                {"name": "Equipment Selected", "days": 15},
                {"name": "Installation Complete", "days": 25},
                {"name": "Configuration Complete", "days": 30},
                {"name": "Testing Complete", "days": 35},
                {"name": "Commissioning Complete", "days": 40},
                {"name": "Training Complete", "days": 45}
            ]
        }
        
        return milestones.get(project_type, milestones["digital_twin"])
    
    def define_deliverables(self, project_type):
        """Define project deliverables"""
        deliverables = {
            "digital_twin": [
                "3D digital twin model",
                "Interactive navigation system",
                "IoT device integration",
                "Analytics dashboard",
                "User training materials",
                "Documentation"
            ],
            "building_automation": [
                "Automation system design",
                "Equipment specifications",
                "Installation guide",
                "Configuration documentation",
                "User manual",
                "Training materials"
            ]
        }
        
        return deliverables.get(project_type, deliverables["digital_twin"])
    
    def estimate_timeline(self, project_type):
        """Estimate project timeline"""
        timelines = {
            "digital_twin": 56,  # 8 weeks
            "building_automation": 45,  # 6.5 weeks
            "property_management": 30  # 4 weeks
        }
        
        return timelines.get(project_type, 30)
    
    def estimate_budget(self, client_info):
        """Estimate project budget"""
        base_costs = {
            "digital_twin": 50000,
            "building_automation": 75000,
            "property_management": 25000
        }
        
        base_cost = base_costs.get(client_info["project_type"], 25000)
        
        # Adjust based on building size
        if "building_size" in client_info:
            size_multiplier = client_info["building_size"] / 10000  # per 10k sq ft
            base_cost *= size_multiplier
        
        return {
            "base_cost": base_cost,
            "complexity_multiplier": 1.0,
            "total_estimated": base_cost
        }
    
    def identify_risks(self, project_type):
        """Identify project risks"""
        risks = {
            "digital_twin": [
                "Data quality issues",
                "3D modeling complexity",
                "IoT device compatibility",
                "Client change requests",
                "Timeline delays"
            ],
            "building_automation": [
                "Equipment availability",
                "Installation access",
                "Electrical compatibility",
                "Regulatory compliance",
                "Client training"
            ]
        }
        
        return risks.get(project_type, risks["digital_twin"])
    
    def define_success_metrics(self, project_type):
        """Define project success metrics"""
        metrics = {
            "digital_twin": [
                "Model accuracy > 95%",
                "User satisfaction > 8/10",
                "System uptime > 99%",
                "Training completion > 90%"
            ],
            "building_automation": [
                "Energy savings > 20%",
                "System reliability > 99%",
                "User adoption > 90%",
                "ROI > 200%"
            ]
        }
        
        return metrics.get(project_type, metrics["digital_twin"])
    
    def save_template(self, template, output_file):
        """Save project template to file"""
        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"Project template saved to: {output_file}")

def main():
    """Main function"""
    generator = PropTechProjectTemplateGenerator()
    
    # Example client info
    client_info = {
        "id": "001",
        "name": "Example Client",
        "project_type": "digital_twin",
        "building_size": 50000  # sq ft
    }
    
    # Generate template
    template = generator.generate_project_template(client_info)
    
    # Save template
    output_file = f"automation/templates/proptech/project-template-{client_info['id']}.json"
    generator.save_template(template, output_file)
    
    print("Project template generated successfully!")

if __name__ == "__main__":
    main()
EOF
    
    # Create client onboarding automation
    cat > "automation/templates/proptech/client-onboarding-automation.py" << 'EOF'
#!/usr/bin/env python3
"""
PropTech Client Onboarding Automation
Automates the client onboarding process for PropTech projects
"""

import yaml
import json
from datetime import datetime, timedelta
from pathlib import Path

class PropTechClientOnboarding:
    def __init__(self, config_file="configs/startup-config.yaml"):
        self.config = self.load_config(config_file)
        self.onboarding_dir = Path("automation/templates/proptech/onboarding")
        self.onboarding_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load startup configuration"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def start_onboarding(self, client_info):
        """Start client onboarding process"""
        onboarding_plan = {
            "client_id": client_info["id"],
            "client_name": client_info["name"],
            "start_date": datetime.now().isoformat(),
            "status": "initiated",
            "phases": self.get_onboarding_phases(),
            "tasks": self.generate_onboarding_tasks(client_info),
            "timeline": self.estimate_onboarding_timeline(),
            "success_metrics": self.define_onboarding_metrics()
        }
        
        return onboarding_plan
    
    def get_onboarding_phases(self):
        """Get onboarding phases"""
        return [
            {
                "name": "Initial Setup",
                "duration": 3,
                "tasks": [
                    "Create client account",
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
                    "Gather building information",
                    "Define project scope",
                    "Create project plan"
                ]
            },
            {
                "name": "System Setup",
                "duration": 5,
                "tasks": [
                    "Configure project tools",
                    "Set up communication channels",
                    "Create project documentation",
                    "Schedule team training"
                ]
            },
            {
                "name": "Go Live Preparation",
                "duration": 3,
                "tasks": [
                    "Final system testing",
                    "User training",
                    "Documentation review",
                    "Go live planning"
                ]
            }
        ]
    
    def generate_onboarding_tasks(self, client_info):
        """Generate onboarding tasks"""
        tasks = []
        
        # Phase 1: Initial Setup
        tasks.extend([
            {
                "name": "Create client account",
                "phase": "Initial Setup",
                "assignee": "customer_success",
                "due_date": datetime.now() + timedelta(days=1),
                "status": "pending"
            },
            {
                "name": "Set up project workspace",
                "phase": "Initial Setup",
                "assignee": "project_manager",
                "due_date": datetime.now() + timedelta(days=2),
                "status": "pending"
            },
            {
                "name": "Assign team members",
                "phase": "Initial Setup",
                "assignee": "ceo_founder",
                "due_date": datetime.now() + timedelta(days=1),
                "status": "pending"
            },
            {
                "name": "Schedule kickoff meeting",
                "phase": "Initial Setup",
                "assignee": "project_manager",
                "due_date": datetime.now() + timedelta(days=3),
                "status": "pending"
            }
        ])
        
        # Phase 2: Requirements Gathering
        tasks.extend([
            {
                "name": "Conduct discovery call",
                "phase": "Requirements Gathering",
                "assignee": "project_manager",
                "due_date": datetime.now() + timedelta(days=5),
                "status": "pending"
            },
            {
                "name": "Gather building information",
                "phase": "Requirements Gathering",
                "assignee": "technical_lead",
                "due_date": datetime.now() + timedelta(days=7),
                "status": "pending"
            },
            {
                "name": "Define project scope",
                "phase": "Requirements Gathering",
                "assignee": "project_manager",
                "due_date": datetime.now() + timedelta(days=10),
                "status": "pending"
            },
            {
                "name": "Create project plan",
                "phase": "Requirements Gathering",
                "assignee": "project_manager",
                "due_date": datetime.now() + timedelta(days=12),
                "status": "pending"
            }
        ])
        
        return tasks
    
    def estimate_onboarding_timeline(self):
        """Estimate onboarding timeline"""
        return {
            "total_duration": 18,  # days
            "phases": [
                {"name": "Initial Setup", "duration": 3},
                {"name": "Requirements Gathering", "duration": 7},
                {"name": "System Setup", "duration": 5},
                {"name": "Go Live Preparation", "duration": 3}
            ]
        }
    
    def define_onboarding_metrics(self):
        """Define onboarding success metrics"""
        return [
            "Onboarding completion rate > 95%",
            "Client satisfaction > 8/10",
            "Time to first value < 30 days",
            "Team efficiency > 8/10"
        ]
    
    def save_onboarding_plan(self, plan, output_file):
        """Save onboarding plan to file"""
        with open(output_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"Onboarding plan saved to: {output_file}")

def main():
    """Main function"""
    onboarding = PropTechClientOnboarding()
    
    # Example client info
    client_info = {
        "id": "001",
        "name": "Example Client"
    }
    
    # Start onboarding
    plan = onboarding.start_onboarding(client_info)
    
    # Save plan
    output_file = f"automation/templates/proptech/onboarding/onboarding-plan-{client_info['id']}.json"
    onboarding.save_onboarding_plan(plan, output_file)
    
    print("Client onboarding plan generated successfully!")

if __name__ == "__main__":
    main()
EOF
    
    # Make scripts executable
    chmod +x "automation/templates/proptech"/*.py
    
    print_success "PropTech-specific templates created"
}

# Function to set up PropTech monitoring
setup_proptech_monitoring() {
    print_status "Setting up PropTech-specific monitoring..."
    
    # Create PropTech metrics dashboard
    mkdir -p "monitoring/dashboards/proptech"
    
    cat > "monitoring/dashboards/proptech/proptech-metrics.json" << 'EOF'
{
  "dashboard": {
    "name": "PropTech Metrics Dashboard",
    "description": "Key metrics for PropTech startup performance",
    "widgets": [
      {
        "name": "Project Completion Rate",
        "type": "gauge",
        "metric": "project_completion_rate",
        "target": 95,
        "current": 0
      },
      {
        "name": "Client Satisfaction Score",
        "type": "gauge",
        "metric": "client_satisfaction_score",
        "target": 8,
        "current": 0
      },
      {
        "name": "Revenue per Project",
        "type": "number",
        "metric": "revenue_per_project",
        "target": 50000,
        "current": 0
      },
      {
        "name": "Lead Conversion Rate",
        "type": "gauge",
        "metric": "lead_conversion_rate",
        "target": 25,
        "current": 0
      },
      {
        "name": "Team Efficiency Score",
        "type": "gauge",
        "metric": "team_efficiency_score",
        "target": 8,
        "current": 0
      }
    ]
  }
}
EOF
    
    # Create PropTech alerts configuration
    mkdir -p "monitoring/alerts/proptech"
    
    cat > "monitoring/alerts/proptech/proptech-alerts.yaml" << 'EOF'
alerts:
  project_completion_rate:
    threshold: 90
    condition: below
    severity: high
    message: "Project completion rate below 90%"
    
  client_satisfaction_score:
    threshold: 7
    condition: below
    severity: medium
    message: "Client satisfaction score below 7/10"
    
  revenue_per_project:
    threshold: 40000
    condition: below
    severity: medium
    message: "Revenue per project below $40,000"
    
  lead_conversion_rate:
    threshold: 20
    condition: below
    severity: high
    message: "Lead conversion rate below 20%"
    
  team_efficiency_score:
    threshold: 7
    condition: below
    severity: medium
    message: "Team efficiency score below 7/10"
EOF
    
    print_success "PropTech monitoring setup completed"
}

# Function to create PropTech documentation
create_proptech_documentation() {
    print_status "Creating PropTech-specific documentation..."
    
    mkdir -p "documentation/proptech"
    
    cat > "documentation/proptech/README.md" << 'EOF'
# PropTech Startup Automation Guide

## Overview
This guide provides specific automation strategies for PropTech startups like Tango.Vision.

## Key Focus Areas

### 1. Digital Twins
- 3D modeling automation
- IoT device integration
- Real-time data processing
- Interactive navigation systems

### 2. Building Automation
- System design automation
- Equipment selection
- Installation planning
- Commissioning processes

### 3. Property Management
- Tenant experience automation
- Facility management
- Maintenance scheduling
- Performance monitoring

## Automation Templates

### Sales Automation
- Lead scoring for PropTech clients
- Industry-specific email sequences
- Demo scheduling for building tours
- Proposal generation for projects

### Operations Automation
- Project template generation
- Client onboarding automation
- Progress tracking
- Milestone notifications

### Team Automation
- Daily standup for project teams
- Task assignment based on expertise
- Performance monitoring
- Team coordination

### Finance Automation
- Project-based invoicing
- Payment tracking
- Budget monitoring
- Financial reporting

## Best Practices

### 1. Client Onboarding
- Automate project template generation
- Set up automated progress tracking
- Create milestone notifications
- Implement success celebration

### 2. Project Management
- Use automated task assignment
- Set up progress monitoring
- Create automated reporting
- Implement team coordination

### 3. Customer Success
- Automate onboarding sequences
- Set up usage tracking
- Create renewal management
- Implement upsell automation

## Metrics to Track

### Primary Metrics
- Project completion rate
- Client satisfaction score
- Revenue per project
- Lead conversion rate
- Team efficiency score

### Secondary Metrics
- Lead to close time
- Project profitability
- Customer lifetime value
- Team productivity
- Automation ROI

## Implementation Guide

### Phase 1: Foundation (Week 1)
1. Set up basic sales automation
2. Implement lead scoring
3. Create email sequences
4. Set up daily standup

### Phase 2: Operations (Week 2)
1. Deploy project templates
2. Set up client onboarding
3. Implement progress tracking
4. Create team coordination

### Phase 3: Optimization (Week 3)
1. Set up advanced analytics
2. Implement financial automation
3. Create customer success automation
4. Optimize all processes

## Support and Maintenance

### Regular Updates
- Update templates based on best practices
- Add new PropTech-specific features
- Improve automation based on feedback
- Maintain industry-specific content

### Training and Support
- Provide PropTech-specific training
- Create industry-specific documentation
- Offer ongoing support
- Share best practices

---

*This guide is specifically designed for PropTech startups and can be customized for your specific needs.*
EOF
    
    print_success "PropTech documentation created"
}

# Main execution
main() {
    local startup_name="$1"
    
    if [ -z "$startup_name" ]; then
        print_error "Startup name is required"
        echo "Usage: $0 <startup_name>"
        exit 1
    fi
    
    print_status "Configuring PropTech startup: $startup_name"
    
    # Configure PropTech-specific settings
    configure_proptech "$startup_name"
    
    # Create PropTech-specific templates
    create_proptech_templates
    
    # Set up PropTech monitoring
    setup_proptech_monitoring
    
    # Create PropTech documentation
    create_proptech_documentation
    
    print_success "PropTech startup configuration completed!"
    echo ""
    echo "Next steps:"
    echo "1. Review configuration: configs/startup-config.yaml"
    echo "2. Deploy automations: ./deploy-automations.sh --startup \"$startup_name\" --template sales"
    echo "3. Set up monitoring: ./setup-monitoring.sh --startup \"$startup_name\""
    echo "4. Review documentation: documentation/proptech/README.md"
}

# Run main function
main "$@"
