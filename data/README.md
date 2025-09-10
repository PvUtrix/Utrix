# Data Directory

## Purpose
The data directory contains runtime data, temporary files, and application-specific storage for the personal system services.

## Contents
- `storage/` - Persistent data storage for applications
- `cache/` - Temporary cache files and data
- `backups/` - Local backup files and snapshots
- `keys/` - Encryption keys and security certificates

## Usage
This directory is used by various services for:

- **Telegram Bot**: User data, conversation history, and cache
- **Personal API**: Application data and temporary storage
- **Presentation Analyzer**: Raw and processed presentation data
- **Serverless Functions**: Archive data and temporary processing files

## Structure
```
data/
├── storage/          # Persistent application data
├── cache/            # Temporary cache files
├── backups/          # Local backup files
└── keys/             # Encryption keys and certificates
```

## Privacy & Security
- **Local Storage**: All data stored locally on your system
- **Encryption**: Sensitive data can be encrypted using stored keys
- **Backup**: Regular backups to ensure data safety
- **Git Ignored**: Runtime data is excluded from version control

## Related
- `../services/telegram-bot/config/` - Telegram bot data configuration
- `../services/personal-api/` - Personal API data storage
- `../projects/presentation_analyzer/config/` - Presentation analyzer data paths
- `../services/serverless-functions/configs/` - Serverless function data configuration

## Last Updated
2024-12-19 - Initial README creation
