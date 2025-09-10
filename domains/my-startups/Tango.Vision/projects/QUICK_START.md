# Tango.Vision Project Management - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. View Your Projects
```bash
cd domains/my-startups/Tango.Vision/projects
python3 project_manager.py list
```

### 2. Check Today's Tasks
```bash
python3 project_manager.py daily
```

### 3. Create a New Project
```bash
python3 create_project.py
# Follow the interactive prompts
```

### 4. Add Tasks to a Project
```bash
# Add a regular task
python3 project_manager.py add-task proj_001_resstrpo "Complete documentation" --priority high --hours 4

# Add a daily task
python3 project_manager.py add-task proj_001_resstrpo "Daily progress review" --priority medium --daily
```

### 5. Complete Tasks
```bash
python3 project_manager.py complete proj_001_resstrpo task_001
```

### 6. Generate Reports
```bash
python3 project_manager.py report
```

## 📊 Daily Workflow

### Morning Routine
1. **Check daily tasks**: `python3 project_manager.py daily`
2. **Review project status**: `python3 project_manager.py list`
3. **Plan your day** based on priorities

### During the Day
1. **Complete tasks** as you work on them
2. **Add new tasks** as they come up
3. **Update financials** when spending occurs

### Evening Routine
1. **Complete finished tasks**: `python3 project_manager.py complete <project_id> <task_id>`
2. **Generate daily summary**: `python3 daily_workflow.py --action summary`
3. **Review progress**: `python3 project_manager.py report`

## 🔧 Common Commands

### Project Management
```bash
# List all projects
python3 project_manager.py list

# List active projects only
python3 project_manager.py list --status active

# List high priority projects
python3 project_manager.py list --priority high
```

### Task Management
```bash
# View daily tasks
python3 project_manager.py daily

# Add task with due date
python3 project_manager.py add-task proj_001_resstrpo "Important task" --due 2024-12-31

# Complete a task
python3 project_manager.py complete proj_001_resstrpo task_001
```

### Financial Tracking
```bash
# Update spending
python3 project_manager.py financial proj_001_resstrpo --spent 1000

# Update revenue potential
python3 project_manager.py financial proj_001_resstrpo --revenue 5000
```

### Reporting
```bash
# Generate report
python3 project_manager.py report

# Save report to file
python3 project_manager.py report --save monthly_report.md
```

## 🔄 Automation

### Daily Automation
```bash
# Run daily automation (syncs with personal system)
python3 daily_automation.py
```

### Weekly Automation
```bash
# Run weekly automation (generates comprehensive reports)
python3 weekly_automation.py
```

## 📁 Project Structure

Each project gets its own directory:
```
proj_001_resstrpo/
├── README.md           # Project documentation
├── project_config.yaml # Project configuration
├── docs/              # Project documentation
├── tasks/             # Task-related files
├── financial/         # Financial tracking
├── reports/           # Progress reports
└── assets/            # Project assets
```

## 🎯 Best Practices

### Project Creation
- Use descriptive names
- Set realistic budgets
- Define clear priorities
- Add initial tasks

### Daily Tasks
- Mark recurring activities as daily tasks
- Review and complete daily tasks each day
- Update task status regularly

### Financial Tracking
- Update spending weekly
- Track both direct and indirect costs
- Monitor revenue potential vs actual

### Reporting
- Generate reports weekly
- Review project progress regularly
- Adjust priorities based on results

## 🆘 Troubleshooting

### Common Issues
- **Command not found**: Make sure you're in the projects directory
- **Permission errors**: Check file permissions
- **Date format errors**: Use YYYY-MM-DD format

### Getting Help
- Check the main README.md for detailed documentation
- Review project_template.yaml for configuration options
- Look at sample projects for examples

## 🔗 Integration

This system integrates with your personal system:
- **Daily workflows**: Tasks appear in your daily routine
- **Task manager**: Syncs with personal task management
- **Automation**: Runs with your daily automation scripts
- **Reports**: Saves to automation outputs directory

---

*For detailed documentation, see README.md*
