#!/usr/bin/env python3
"""
Google Drive Sync Script

Easy-to-use script for syncing Google Drive folders to your personal system.
Respects privacy markers and integrates with your knowledge management workflow.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Add the parent directory to the path to import the integration
sys.path.append(str(Path(__file__).parent.parent))

from integrations.google_drive import GoogleDriveIntegration

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/google_drive_sync.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_config(config_path: str = "automation/configs/google_drive_config.json") -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"Loaded configuration from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
        sys.exit(1)

def sync_folder(gdrive: GoogleDriveIntegration, folder_config: dict, folder_name: str) -> dict:
    """Sync a specific folder"""
    logger.info(f"Starting sync for folder: {folder_name}")
    
    folder_id = folder_config.get('folder_id')
    if folder_id == f"YOUR_{folder_name.upper()}_FOLDER_ID":
        logger.warning(f"Folder ID not configured for {folder_name}. Skipping.")
        return {'status': 'skipped', 'reason': 'not_configured'}
    
    local_path = folder_config.get('local_path', f"resources/{folder_name}")
    file_types = folder_config.get('file_types', [])
    
    try:
        results = gdrive.sync_folder(
            folder_id=folder_id,
            local_path=local_path,
            file_types=file_types,
            respect_privacy=True
        )
        
        logger.info(f"Sync completed for {folder_name}: "
                   f"{results['downloaded']} downloaded, "
                   f"{results['skipped']} skipped, "
                   f"{results['errors']} errors")
        
        return {'status': 'completed', 'results': results}
        
    except Exception as e:
        logger.error(f"Error syncing folder {folder_name}: {e}")
        return {'status': 'error', 'error': str(e)}

def list_files(gdrive: GoogleDriveIntegration, folder_id: str = None, query: str = None):
    """List files from Google Drive"""
    try:
        files = gdrive.list_files(folder_id=folder_id, query=query)
        
        print(f"\nFound {len(files)} files:")
        print("-" * 80)
        
        for file_info in files:
            name = file_info.get('name', 'Unknown')
            mime_type = file_info.get('mimeType', 'Unknown')
            size = file_info.get('size', 'Unknown')
            modified = file_info.get('modifiedTime', 'Unknown')
            
            print(f"Name: {name}")
            print(f"Type: {mime_type}")
            print(f"Size: {size} bytes")
            print(f"Modified: {modified}")
            print(f"Link: {file_info.get('webViewLink', 'N/A')}")
            print("-" * 40)
            
    except Exception as e:
        logger.error(f"Error listing files: {e}")

def search_files(gdrive: GoogleDriveIntegration, query: str, file_types: list = None):
    """Search for files in Google Drive"""
    try:
        files = gdrive.search_files(query=query, file_types=file_types)
        
        print(f"\nSearch results for '{query}':")
        print(f"Found {len(files)} matching files:")
        print("-" * 80)
        
        for file_info in files:
            name = file_info.get('name', 'Unknown')
            mime_type = file_info.get('mimeType', 'Unknown')
            print(f"• {name} ({mime_type})")
            print(f"  Link: {file_info.get('webViewLink', 'N/A')}")
            
    except Exception as e:
        logger.error(f"Error searching files: {e}")

def main():
    parser = argparse.ArgumentParser(description="Google Drive Sync for Personal System")
    parser.add_argument('--config', default="automation/configs/google_drive_config.json",
                       help="Path to configuration file")
    parser.add_argument('--folder', help="Specific folder to sync (e.g., documents, presentations)")
    parser.add_argument('--list', action='store_true', help="List files instead of syncing")
    parser.add_argument('--search', help="Search for files with given query")
    parser.add_argument('--folder-id', help="Specific folder ID for list/search operations")
    parser.add_argument('--all', action='store_true', help="Sync all configured folders")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize Google Drive integration
    try:
        gdrive = GoogleDriveIntegration(
            credentials_path=config['credentials_path'],
            scope_level=config['scope_level'],
            workspace_root=config['workspace_root']
        )
    except Exception as e:
        logger.error(f"Failed to initialize Google Drive integration: {e}")
        sys.exit(1)
    
    # Handle different operations
    if args.list:
        list_files(gdrive, folder_id=args.folder_id)
    elif args.search:
        search_files(gdrive, args.search)
    elif args.folder:
        # Sync specific folder
        if args.folder not in config['folders']:
            logger.error(f"Unknown folder: {args.folder}")
            logger.info(f"Available folders: {list(config['folders'].keys())}")
            sys.exit(1)
        
        folder_config = config['folders'][args.folder]
        sync_folder(gdrive, folder_config, args.folder)
    elif args.all:
        # Sync all configured folders
        logger.info("Starting sync for all configured folders...")
        
        for folder_name, folder_config in config['folders'].items():
            sync_folder(gdrive, folder_config, folder_name)
            print()  # Add spacing between folders
    else:
        # Default: show help
        parser.print_help()
        print("\nExample usage:")
        print("  python google_drive_sync.py --all                    # Sync all folders")
        print("  python google_drive_sync.py --folder documents       # Sync documents folder")
        print("  python google_drive_sync.py --list                   # List all files")
        print("  python google_drive_sync.py --search 'project'       # Search for files")
        print("  python google_drive_sync.py --list --folder-id FOLDER_ID  # List files in specific folder")

if __name__ == "__main__":
    main()
