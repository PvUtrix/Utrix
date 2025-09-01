# 🚀 Google Drive Integration Setup Guide

## 📋 Overview

This integration allows you to easily access and sync files from Google Drive to your personal system. It respects privacy markers and integrates seamlessly with your knowledge management workflow.

## 🏗 Architecture

The Google Drive integration is located in:
- **Integration**: `automation/integrations/google_drive.py`
- **Configuration**: `automation/configs/google_drive_config.json`
- **Sync Script**: `automation/scripts/google_drive_sync.py`
- **Setup Guide**: `automation/SETUP_GOOGLE_DRIVE.md`

## 🔧 Installation

### 1. Install Dependencies

```bash
cd automation
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Google Drive API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

### 3. Create Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Download the JSON file as `credentials.json`

### 4. Place Credentials

```bash
# Create the local config directory
mkdir -p config/local

# Move your credentials file
mv ~/Downloads/credentials.json config/local/google_drive_credentials.json
```

## ⚙️ Configuration

### 1. Update Configuration File

Edit `automation/configs/google_drive_config.json`:

```json
{
  "credentials_path": "config/local/google_drive_credentials.json",
  "scope_level": "readonly",
  "workspace_root": ".",
  "folders": {
    "documents": {
      "folder_id": "YOUR_ACTUAL_FOLDER_ID_HERE",
      "local_path": "resources/documents",
      "file_types": [
        "application/pdf",
        "application/vnd.google-apps.document"
      ]
    }
  }
}
```

### 2. Get Folder IDs

To find a folder ID:
1. Open the folder in Google Drive
2. Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Copy the `FOLDER_ID_HERE` part

### 3. Share Folders (if needed)

If using a service account, share the folders with the service account email.

## 🚀 Usage

### Basic Commands

```bash
# Sync all configured folders
python automation/scripts/google_drive_sync.py --all

# Sync specific folder
python automation/scripts/google_drive_sync.py --folder documents

# List all files
python automation/scripts/google_drive_sync.py --list

# Search for files
python automation/scripts/google_drive_sync.py --search "project"

# List files in specific folder
python automation/scripts/google_drive_sync.py --list --folder-id YOUR_FOLDER_ID
```

### Integration with Workflows

Add to your daily routine in `workflows/daily/morning_routine.md`:

```markdown
## 📚 Knowledge Management (7:30 AM)
- [ ] Sync Google Drive documents (3 min)
- [ ] Review new files and add to knowledge base
- [ ] Update connections and tags
```

### Automation

Create a cron job for automatic syncing:

```bash
# Edit crontab
crontab -e

# Add this line for daily sync at 7:30 AM
30 7 * * * cd /path/to/your/personal_system && python automation/scripts/google_drive_sync.py --all
```

## 📁 File Organization

Files will be synced to these locations:

- **Documents**: `resources/documents/`
- **Presentations**: `resources/presentations/`
- **Spreadsheets**: `resources/spreadsheets/`
- **Images**: `resources/images/`

## 🔒 Privacy & Security

### Privacy Markers

The integration automatically respects these privacy markers:
- `.private` - Files marked as private
- `.share` - Files marked for sharing
- `confidential` - Confidential files
- `internal` - Internal documents
- `sensitive` - Sensitive information

### Security Features

- **Read-only by default** - Uses minimal permissions
- **Local token storage** - Tokens stored in `config/local/`
- **Privacy filtering** - Automatically skips private files
- **Logging** - All operations logged to `logs/google_drive_sync.log`

## 🔄 Sync Strategies

### 1. Full Sync
Downloads all files from configured folders:
```bash
python automation/scripts/google_drive_sync.py --all
```

### 2. Selective Sync
Sync only specific file types or folders:
```bash
python automation/scripts/google_drive_sync.py --folder documents
```

### 3. Search and Download
Find and download specific files:
```bash
python automation/scripts/google_drive_sync.py --search "quarterly report"
```

## 🛠 Troubleshooting

### Common Issues

1. **Authentication Error**
   ```bash
   # Delete token and re-authenticate
   rm config/local/google_drive_token.json
   python automation/scripts/google_drive_sync.py --list
   ```

2. **Folder Not Found**
   - Check folder ID in configuration
   - Ensure folder is shared with your account

3. **Permission Denied**
   - Check folder sharing permissions
   - Verify API is enabled in Google Cloud Console

### Logs

Check logs for detailed information:
```bash
tail -f logs/google_drive_sync.log
```

## 📈 Advanced Usage

### Custom File Types

Add custom MIME types to configuration:

```json
{
  "folders": {
    "custom": {
      "folder_id": "YOUR_FOLDER_ID",
      "local_path": "resources/custom",
      "file_types": [
        "application/zip",
        "text/plain",
        "application/json"
      ]
    }
  }
}
```

### Integration with Other Systems

Use the integration in your own scripts:

```python
from automation.integrations.google_drive import GoogleDriveIntegration

# Initialize
gdrive = GoogleDriveIntegration(
    credentials_path="config/local/google_drive_credentials.json"
)

# List files
files = gdrive.list_files(folder_id="YOUR_FOLDER_ID")

# Download specific file
gdrive.download_file("FILE_ID", "local/path/file.pdf")
```

## 🔮 Future Enhancements

- [ ] Two-way sync (upload changes back to Drive)
- [ ] Real-time file watching
- [ ] Integration with knowledge base tagging
- [ ] Automatic file categorization
- [ ] Version control integration
- [ ] Collaborative editing support

## 📞 Support

For issues or questions:
1. Check the logs in `logs/google_drive_sync.log`
2. Review this setup guide
3. Check Google Drive API documentation
4. Create an issue in your project management system
