# Backups

This directory is for storing backups of your personal system.

## Backup Strategy
A good backup strategy has multiple layers. Consider the 3-2-1 rule:
-   **3** copies of your data.
-   **2** different media types (e.g., local hard drive + cloud).
-   **1** copy off-site.

## Automated Backup Solution

We've created an automated backup script that creates password-protected zip files and syncs them to Google Drive.

### Features
- **Password Protection**: Creates encrypted zip files with your chosen password
- **Secure Password Storage**: Stores passwords securely in your system keychain (macOS Keychain)
- **Smart Exclusions**: Automatically excludes unnecessary files (`.git`, `__pycache__`, `venv`, etc.)
- **Google Drive Sync**: Automatically uploads backups to Google Drive
- **Automatic Cleanup**: Can remove old backups to save space
- **Progress Tracking**: Shows backup progress and file counts
- **7zip Support**: Optional 7zip compression for better file size and stronger encryption

### Usage

#### Basic Backup (with Google Drive sync)
```bash
cd automation/scripts
python create_backup.py
```

#### Backup without Google Drive sync
```bash
python create_backup.py --no-gdrive
```

#### Custom backup name
```bash
python create_backup.py --name "my_custom_backup.zip"
```

#### Backup with cleanup (keep only 3 most recent)
```bash
python create_backup.py --cleanup --keep 3
```

#### Backup from specific directory
```bash
python create_backup.py --path /path/to/personal_system
```

#### Use 7zip for better compression (if installed)
```bash
python create_backup.py --use-7zip
```

#### Password Management
```bash
# Set or update stored password
python create_backup.py --set-password

# Remove stored password
python create_backup.py --clear-password
```

### What Gets Backed Up
- All your personal system files and directories
- Excludes: `.git`, `backups/`, `venv/`, `__pycache__/`, temporary files
- Creates timestamped backup files in `backups/weekly/`

### What Gets Synced to Google Drive
- Password-protected zip files are uploaded to a `backups` folder in Google Drive
- Requires Google Drive API setup (see `automation/SETUP_GOOGLE_DRIVE.md`)

## Manual Backup Process (Alternative)
If you prefer manual backups:

1.  **Weekly**: Run a script to create a compressed, encrypted archive of the entire `personal_system` directory (excluding the `backups` folder itself).
2.  **Local Copy**: Store this archive in `/backups/weekly`.
3.  **Off-site Copy**: Sync the weekly archive to a secure, private cloud storage provider (e.g., Proton Drive, Sync.com) or a physical drive you store elsewhere.

## Security Notes
- **Password Management**: Store your backup passwords securely (password manager recommended)
- **Google Drive Security**: Ensure your Google account has 2FA enabled
- **Backup Encryption**: All automated backups are password-protected using zip encryption
- **Access Control**: Limit access to backup files and Google Drive backup folder

## Recovery Process
To restore from a backup:
1. Download the backup file from Google Drive (if synced)
2. Extract using your backup password
3. Replace the current personal system directory or merge specific files as needed
