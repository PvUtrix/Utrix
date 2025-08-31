# Initial Setup Guide

## Welcome!

This guide will walk you through setting up your personal knowledge and automation system.

## Prerequisites

Before starting, ensure you have:
- A text editor (VS Code recommended)
- Git installed (optional, for version control)
- Python 3.8+ (optional, for automation scripts)
- 30 minutes for initial setup

## Step 1: Download and Extract

1. Download the system archive
2. Extract to your desired location
3. Rename the folder to something meaningful (e.g., "my-life-system")

## Step 2: Personalize Core Identity

This is the most important step. Your identity forms the foundation.

### Edit Your Values
Open `core/identity/values.md` and:
1. List your top 3-5 core values
2. Define what each means to you
3. Describe how you practice them

### Set Your Goals
Open `core/identity/goals.md` and:
1. Write your 10-year vision
2. Set long-term goals (5-10 years)
3. Define medium-term targets (1-5 years)
4. Create 90-day action plans

### Document Your Strengths
Open `core/identity/strengths.md` and:
1. List natural talents
2. Document developed skills
3. Identify growth areas

## Step 3: Configure Privacy

### Create Private Directories
```bash
mkdir -p privacy/local/credentials
mkdir -p privacy/local/personal
mkdir -p privacy/local/sensitive
```

### Review .gitignore
Ensure sensitive directories are excluded from version control.

## Step 4: Select Your Domains

Review the domains in `domains/` and:
1. Keep relevant ones
2. Delete irrelevant ones
3. Add custom domains as needed

Each domain should reflect an important area of your life.

## Step 5: Set Up Workflows

### Daily Workflow
Edit `core/workflows/daily.md` to match your routine:
- Morning rituals
- Work blocks
- Evening routine

### Weekly Review
Customize `core/workflows/weekly.md` for your weekly planning.

## Step 6: Configure Automation (Optional)

If using automation:
1. Review scripts in `automation/scripts/`
2. Modify for your needs
3. Set up cron jobs or task scheduler

## Step 7: Initial Data Entry

Start populating your system:
1. Current projects → `projects/active/`
2. Learning goals → `domains/learning/`
3. Health metrics → `domains/health/`
4. Financial goals → `domains/finance/`

## Step 8: Establish Routines

### Daily
- Morning: Review daily workflow
- Evening: Update daily metrics

### Weekly
- Sunday: Weekly review and planning

### Monthly
- Last Sunday: Monthly review
- Update goals and metrics

## Next Steps

1. **Commit to daily use** for 30 days
2. **Iterate and improve** based on what works
3. **Share feedback** to help others
4. **Make it yours** - this is YOUR system

## Troubleshooting

### Common Issues

**Issue**: Too overwhelming  
**Solution**: Start with just core/ and one domain

**Issue**: Not sure what to track  
**Solution**: Begin with daily notes, expand gradually

**Issue**: Automation not working  
**Solution**: Check script permissions and paths

## Support

- Check `docs/usage/` for detailed guides
- Review `resources/templates/` for examples
- Customize everything to fit your life

---

*Remember: Perfect is the enemy of good. Start simple, evolve gradually.*
