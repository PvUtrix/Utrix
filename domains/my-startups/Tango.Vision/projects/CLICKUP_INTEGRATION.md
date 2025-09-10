# ClickUp Integration for Tango.Vision

## Overview
The ClickUp integration allows you to automatically sync your Tango.Vision projects with ClickUp, enabling seamless project management across both platforms. All projects, tasks, comments, and documents are synchronized in real-time.

## Features
- **Automatic Project Sync**: New projects are automatically created in ClickUp
- **Task Synchronization**: Tasks are synced with proper priorities and due dates
- **Document Upload**: Upload files directly to ClickUp projects
- **Comment Integration**: Add comments that sync to ClickUp
- **Financial Tracking**: Budget and revenue data sync as custom fields
- **Daily Task Management**: Daily tasks are properly categorized in ClickUp
- **Bidirectional Updates**: Changes in ClickUp can be reflected locally

## Quick Setup

### 1. Get ClickUp API Credentials
1. Go to ClickUp Settings (click your avatar → Settings)
2. Navigate to Apps → API Token
3. Click 'Generate' to create a new token
4. Copy the token for configuration

### 2. Run Setup Script
```bash
cd domains/my-startups/Tango.Vision/projects
python3 setup_clickup.py
```

### 3. Test Integration
```bash
python3 setup_clickup.py --test-only --create-sample
```

## Configuration

### Configuration File (`clickup_config.json`)
```json
{
  "api_token": "your_clickup_api_token",
  "team_id": "your_team_id",
  "space_id": "your_space_id",
  "rate_limit_delay": 0.1,
  "custom_fields": {
    "budget": "Budget Amount",
    "revenue_potential": "Revenue Potential",
    "roi_estimate": "ROI Estimate"
  },
  "list_mappings": {
    "planning": "📋 Planning",
    "in_progress": "🚀 In Progress",
    "completed": "✅ Completed",
    "documentation": "📝 Documentation",
    "financial": "💰 Financial"
  }
}
```

## Usage

### Using the Integrated Manager

#### Create a Project with ClickUp Sync
```bash
python3 clickup_integrated_manager.py create "My New Project" \
  --description "Project description" \
  --priority high \
  --budget 10000 \
  --revenue 50000
```

#### Add Tasks with ClickUp Sync
```bash
# Regular task
python3 clickup_integrated_manager.py add-task proj_001_my_project "Implement feature X" \
  --priority high \
  --hours 8 \
  --due 2024-12-31

# Daily task
python3 clickup_integrated_manager.py add-task proj_001_my_project "Daily standup" \
  --priority medium \
  --daily
```

#### Complete Tasks
```bash
python3 clickup_integrated_manager.py complete proj_001_my_project task_001
```

#### Upload Documents
```bash
python3 clickup_integrated_manager.py upload proj_001_my_project /path/to/document.pdf \
  --task-name "Project Documentation"
```

#### Add Comments
```bash
python3 clickup_integrated_manager.py comment proj_001_my_project "Important project update"
```

#### Sync Existing Projects
```bash
python3 clickup_integrated_manager.py sync proj_001_my_project
```

#### Generate Reports
```bash
python3 clickup_integrated_manager.py report --save integrated_report.md
```

### Using the ClickUp Client Directly

#### Basic Operations
```python
from clickup_client import ClickUpClient, ClickUpConfig

# Initialize client
config = ClickUpConfig(
    api_token="your_token",
    team_id="your_team_id",
    space_id="your_space_id"
)
client = ClickUpClient(config)

# Create a folder (project)
folder = client.create_folder(space_id, "My Project")

# Create a list
list_obj = client.create_list(folder['id'], "Task List")

# Create a task
task = client.create_task(
    list_id=list_obj['id'],
    name="My Task",
    description="Task description",
    priority=2
)

# Upload attachment
attachment = client.upload_attachment(task['id'], "/path/to/file.pdf")
```

## Project Structure in ClickUp

When you create a project in Tango.Vision, it automatically creates the following structure in ClickUp:

```
📁 Project Name (Folder)
├── 📋 Planning (List)
├── 🚀 In Progress (List)
├── ✅ Completed (List)
├── 📝 Documentation (List)
└── 💰 Financial (List)
```

### List Purposes
- **📋 Planning**: Project planning and requirements
- **🚀 In Progress**: Active development tasks
- **✅ Completed**: Finished tasks
- **📝 Documentation**: Project documentation and notes
- **💰 Financial**: Budget and financial tracking

## Task Synchronization

### Priority Mapping
- **Critical** → Priority 1 (Urgent)
- **High** → Priority 2 (High)
- **Medium** → Priority 3 (Normal)
- **Low** → Priority 4 (Low)

### Task Placement
- **Daily Tasks** → 🚀 In Progress
- **Tasks with Due Dates** → 🚀 In Progress
- **Completed Tasks** → ✅ Completed
- **Regular Tasks** → 📋 Planning

### Custom Fields
The integration automatically creates custom fields for:
- Budget Amount
- Revenue Potential
- ROI Estimate
- Project Priority
- Estimated Hours
- Actual Hours

## Document Management

### Uploading Documents
Documents can be uploaded to ClickUp projects in several ways:

1. **Direct Upload**: Use the upload command
2. **Task Attachments**: Documents are attached to specific tasks
3. **Project Documentation**: Documents are placed in the Documentation list

### Supported File Types
- PDF documents
- Images (PNG, JPG, GIF)
- Office documents (DOC, DOCX, XLS, XLSX, PPT, PPTX)
- Text files
- Code files
- Any other file type supported by ClickUp

## Financial Integration

### Budget Tracking
- Project budgets are synced as custom fields
- Spending can be tracked through task updates
- Revenue potential is maintained in ClickUp

### Financial Reports
- Budget vs. actual spending
- ROI calculations
- Revenue projections
- Cost breakdown by project phase

## Daily Workflow Integration

### Daily Tasks
- Daily tasks are automatically placed in the "In Progress" list
- They maintain their daily flag for local tracking
- Comments and updates sync bidirectionally

### Progress Tracking
- Task completion status syncs between systems
- Time tracking can be maintained in ClickUp
- Progress reports include both local and ClickUp data

## Error Handling

### Common Issues
1. **API Rate Limits**: The client automatically handles rate limiting
2. **Network Errors**: Retry logic is built into the client
3. **Authentication Errors**: Clear error messages for token issues
4. **File Upload Errors**: Detailed error reporting for upload failures

### Troubleshooting
```bash
# Test connection
python3 clickup_client.py --test-connection

# List teams and spaces
python3 clickup_client.py --list-teams
python3 clickup_client.py --list-spaces

# Check configuration
python3 setup_clickup.py --test-only
```

## Advanced Features

### Custom Field Management
```python
# Create custom field
field = client.create_custom_field(
    list_id="list_id",
    name="Custom Field",
    field_type="text"
)

# Set custom field value
client.set_custom_field_value(
    task_id="task_id",
    field_id=field['id'],
    value="Field Value"
)
```

### Search and Filtering
```python
# Search tasks
tasks = client.search_tasks("search query")

# Get tasks by list
tasks = client.get_tasks_in_list("list_id")

# Get lists in folder
lists = client.get_lists_in_folder("folder_id")
```

### Bulk Operations
```python
# Create multiple tasks
for task_data in task_list:
    client.create_task(list_id, **task_data)

# Update multiple tasks
for task_id, updates in task_updates.items():
    client.update_task(task_id, **updates)
```

## Best Practices

### Project Organization
1. Use descriptive project names
2. Set appropriate priorities
3. Include detailed descriptions
4. Set realistic budgets and timelines

### Task Management
1. Break large tasks into smaller ones
2. Use daily tasks for recurring activities
3. Set clear due dates
4. Add detailed descriptions

### Document Management
1. Use consistent naming conventions
2. Upload documents to appropriate lists
3. Add descriptive task names for uploads
4. Keep file sizes reasonable

### Financial Tracking
1. Update budgets regularly
2. Track both direct and indirect costs
3. Monitor revenue potential vs. actual
4. Review financial metrics weekly

## Security Considerations

### API Token Security
- Store API tokens securely
- Use environment variables in production
- Rotate tokens regularly
- Limit token permissions

### Data Privacy
- Be mindful of sensitive data in comments
- Use private spaces for confidential projects
- Review data sharing settings
- Implement access controls

## Monitoring and Maintenance

### Regular Checks
1. Monitor API usage and rate limits
2. Check for failed syncs
3. Review error logs
4. Update configurations as needed

### Performance Optimization
1. Batch operations when possible
2. Use appropriate rate limiting
3. Cache frequently accessed data
4. Monitor response times

## Support and Troubleshooting

### Getting Help
1. Check the logs for error messages
2. Verify API credentials
3. Test with the setup script
4. Review ClickUp API documentation

### Common Solutions
- **Connection Issues**: Verify API token and network
- **Sync Failures**: Check project mappings and permissions
- **Upload Errors**: Verify file paths and permissions
- **Rate Limiting**: Increase delay between requests

---

*This integration provides seamless synchronization between your Tango.Vision project management system and ClickUp, enabling you to leverage the best of both platforms for comprehensive project management.*
