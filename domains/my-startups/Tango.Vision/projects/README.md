# Tango.Vision Project Management System

## Overview
This is a comprehensive project management system designed specifically for Tango.Vision startup projects. It integrates with your personal system to provide seamless task management, financial tracking, and daily workflow integration.

## Features
- **Project Management**: Create, track, and manage multiple projects
- **Priority System**: Critical, High, Medium, Low priority levels
- **Financial Tracking**: Budget, spending, revenue potential, and ROI tracking
- **Daily Tasks**: Mark tasks as daily recurring items
- **ClickUp Integration**: Automatic sync with ClickUp for enhanced project management
- **Document Management**: Upload and sync documents with ClickUp
- **Integration**: Seamless integration with personal automation system
- **Reporting**: Comprehensive project and financial reports

## Quick Start

### 1. Set Up ClickUp Integration (Recommended)
```bash
# Run the ClickUp setup script
python3 setup_clickup.py

# Test the integration
python3 setup_clickup.py --test-only --create-sample
```

### 2. Create a New Project
```bash
# Interactive project creation (local only)
python3 create_project.py

# Create project with ClickUp sync
python3 clickup_integrated_manager.py create "Project Name" --description "Project description" --priority high --budget 10000 --revenue 50000

# Or use the basic project manager
python3 project_manager.py create "Project Name" --description "Project description" --priority high --budget 10000 --revenue 50000
```

### 3. Add Tasks to Projects
```bash
# Add a regular task (with ClickUp sync)
python3 clickup_integrated_manager.py add-task proj_001_my_project "Implement feature X" --priority high --hours 8

# Add a daily task (with ClickUp sync)
python3 clickup_integrated_manager.py add-task proj_001_my_project "Daily standup" --priority medium --daily

# Or use the basic project manager (local only)
python3 project_manager.py add-task proj_001_my_project "Implement feature X" --priority high --hours 8
```

### 4. Manage Daily Workflow
```bash
# View today's tasks
python3 project_manager.py daily

# Generate daily summary
python3 daily_workflow.py --action summary

# Sync with personal system
python3 daily_workflow.py --action sync
```

### 5. Track Progress
```bash
# List all projects (with ClickUp sync status)
python3 clickup_integrated_manager.py list

# Complete a task (with ClickUp sync)
python3 clickup_integrated_manager.py complete proj_001_my_project task_001

# Generate comprehensive report (includes ClickUp data)
python3 clickup_integrated_manager.py report --save project_report.md
```

### 6. ClickUp-Specific Operations
```bash
# Upload documents to ClickUp
python3 clickup_integrated_manager.py upload proj_001_my_project /path/to/document.pdf

# Add comments to ClickUp projects
python3 clickup_integrated_manager.py comment proj_001_my_project "Important update"

# Sync existing project to ClickUp
python3 clickup_integrated_manager.py sync proj_001_my_project
```

## Project Structure

Each project follows this structure:
```
projects/
├── project_manager.py          # Main project management system
├── create_project.py           # Interactive project creation
├── daily_workflow.py           # Daily workflow integration
├── project_template.yaml       # Project template and guidelines
├── projects_data.json          # Project data storage
├── README.md                   # This file
└── proj_XXX_project_name/      # Individual project directories
    ├── README.md               # Project-specific documentation
    ├── project_config.yaml     # Project configuration
    ├── docs/                   # Project documentation
    ├── tasks/                  # Task-related files
    ├── financial/              # Financial tracking
    ├── reports/                # Progress reports
    └── assets/                 # Project assets
```

## Project Data Model

### Project
- **ID**: Unique project identifier
- **Name**: Project name
- **Description**: Project description
- **Priority**: Critical, High, Medium, Low
- **Status**: Planning, Active, On Hold, Completed, Cancelled
- **Owner**: Project owner
- **Team Members**: List of team members
- **Financial Metrics**: Budget, spending, revenue potential
- **Tasks**: List of project tasks
- **Timeline**: Start date, target completion, actual completion

### Task
- **ID**: Unique task identifier
- **Title**: Task title
- **Description**: Task description
- **Priority**: Critical, High, Medium, Low
- **Status**: Pending, In Progress, Completed, Blocked
- **Daily Task**: Boolean flag for recurring daily tasks
- **Time Tracking**: Estimated and actual hours
- **Dependencies**: List of dependent tasks

### Financial Metrics
- **Budget**: Total project budget
- **Spent**: Amount spent so far
- **Revenue Potential**: Expected revenue
- **ROI Estimate**: Return on investment estimate
- **Break Even Date**: Projected break-even date

## Integration with Personal System

### ClickUp Integration
- **Automatic Sync**: Projects and tasks automatically sync with ClickUp
- **Document Management**: Upload and manage documents in ClickUp
- **Comment System**: Add comments that sync between systems
- **Financial Tracking**: Budget and revenue data sync as custom fields
- **Real-time Updates**: Changes reflect immediately in both systems

### Daily Workflow Integration
The system automatically integrates with your personal daily workflows:
- Daily tasks appear in your daily workflow
- Project summaries are generated daily
- Tasks sync with your personal task manager

### Automation Integration
- Projects integrate with your automation scripts
- Daily summaries are saved to `automation/outputs/daily_summaries/`
- Reports are generated automatically
- ClickUp sync runs with daily automation

### Task Manager Integration
- Project tasks can sync with the personal task manager
- Unified task tracking across personal and business activities
- Priority-based task organization
- ClickUp tasks appear in local reports

## Usage Examples

### Creating a Product Development Project
```bash
python create_project.py
# Follow the interactive prompts to create a new project
```

### Managing Daily Tasks
```bash
# View all daily tasks across projects
python project_manager.py daily

# Complete a daily task
python project_manager.py complete proj_001_my_project task_001
```

### Financial Tracking
```bash
# Update spending for a project
python project_manager.py financial proj_001_my_project --spent 2500

# Update revenue potential
python project_manager.py financial proj_001_my_project --revenue 15000
```

### Reporting
```bash
# Generate and save a comprehensive report
python project_manager.py report --save monthly_report.md

# View project summary
python project_manager.py list --status active
```

## Configuration

### Project Template
Edit `project_template.yaml` to customize:
- Default project settings
- Task categories and priorities
- Financial tracking guidelines
- Integration settings

### Daily Workflow
The system automatically updates your personal daily workflow file with:
- Today's project tasks
- Daily recurring tasks
- Due today tasks
- Quick action commands

## Best Practices

### Project Creation
1. Use descriptive project names
2. Set realistic budgets and timelines
3. Define clear success metrics
4. Assign appropriate priorities

### Task Management
1. Break large tasks into smaller, manageable pieces
2. Use daily tasks for recurring activities
3. Set realistic time estimates
4. Update task status regularly

### Financial Tracking
1. Update spending regularly
2. Track both direct and indirect costs
3. Monitor revenue potential vs. actual
4. Review financial metrics weekly

### Daily Workflow
1. Review daily tasks each morning
2. Complete high-priority tasks first
3. Update task status throughout the day
4. Generate daily summaries for reflection

## Troubleshooting

### Common Issues
- **File not found**: Ensure you're running scripts from the projects directory
- **Permission errors**: Check file write permissions
- **Date format errors**: Use YYYY-MM-DD format for dates
- **JSON errors**: Check for valid JSON in data files

### Data Recovery
- Project data is stored in `projects_data.json`
- Daily summaries are saved in `automation/outputs/daily_summaries/`
- Reports are saved in the projects directory

## Support

### Documentation
- Project template: `project_template.yaml`
- ClickUp integration: `CLICKUP_INTEGRATION.md`
- Personal system integration: See main system documentation
- Automation scripts: See `automation/` directory

### Integration Points
- Personal task manager: `automation/tools/task_manager/`
- Daily workflows: `core/workflows/daily.md`
- Automation outputs: `automation/outputs/`
- ClickUp API: `clickup_client.py`
- Integrated manager: `clickup_integrated_manager.py`

### ClickUp Setup
- Configuration: `clickup_config.json`
- Setup script: `setup_clickup.py`
- Client library: `clickup_client.py`

---

*This system is designed to integrate seamlessly with your personal knowledge management and automation system while providing specialized project management capabilities for Tango.Vision startup activities.*
