#!/usr/bin/env python3
"""
Personal System Backup Script

Creates a password-protected zip file of the personal system directory
and optionally syncs it to Google Drive.
"""

import os
import sys
import zipfile
import argparse
import logging
from datetime import datetime
from pathlib import Path
import getpass
import shutil
import subprocess

# Add the parent directory to the path to import google_drive_sync
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from integrations.google_drive import GoogleDriveSync
except ImportError:
    GoogleDriveSync = None

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False
    print("Warning: keyring not available. Install with: pip install keyring")
    print("Passwords will need to be entered manually each time.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PersonalSystemBackup:
    def __init__(self, personal_system_path=None):
        """Initialize the backup system."""
        if personal_system_path is None:
            # Try to find the personal system directory
            current_dir = Path.cwd()
            if current_dir.name == 'personal_system':
                self.personal_system_path = current_dir
            else:
                # Look for personal_system in parent directories
                for parent in current_dir.parents:
                    if parent.name == 'personal_system':
                        self.personal_system_path = parent
                        break
                else:
                    raise ValueError("Could not find personal_system directory")
        else:
            self.personal_system_path = Path(personal_system_path)
        
        self.backup_dir = self.personal_system_path / 'backups'
        self.backup_dir.mkdir(exist_ok=True)
        
        # Create weekly subdirectory
        self.weekly_backup_dir = self.backup_dir / 'weekly'
        self.weekly_backup_dir.mkdir(exist_ok=True)
        
        # Keyring service and username for password storage
        self.keyring_service = "personal_system_backup"
        self.keyring_username = "backup_password"
    
    def get_stored_password(self):
        """Retrieve the stored backup password from keyring."""
        if not KEYRING_AVAILABLE:
            return None
        
        try:
            password = keyring.get_password(self.keyring_service, self.keyring_username)
            return password
        except Exception as e:
            logger.warning(f"Could not retrieve stored password: {e}")
            return None
    
    def store_password(self, password):
        """Store the backup password in keyring."""
        if not KEYRING_AVAILABLE:
            logger.warning("Keyring not available. Password cannot be stored securely.")
            return False
        
        try:
            keyring.set_password(self.keyring_service, self.keyring_username, password)
            logger.info("Password stored securely in system keychain.")
            return True
        except Exception as e:
            logger.error(f"Failed to store password: {e}")
            return False
    
    def clear_stored_password(self):
        """Remove the stored backup password from keyring."""
        if not KEYRING_AVAILABLE:
            logger.warning("Keyring not available.")
            return False
        
        try:
            keyring.delete_password(self.keyring_service, self.keyring_username)
            logger.info("Stored password removed from system keychain.")
            return True
        except Exception as e:
            logger.error(f"Failed to remove stored password: {e}")
            return False
    
    def get_exclude_patterns(self):
        """Define patterns to exclude from backup."""
        return [
            'backups',           # Don't backup backups
            '.git',              # Git repository
            '__pycache__',       # Python cache
            '*.pyc',            # Python compiled files
            '.DS_Store',        # macOS system files
            'Thumbs.db',        # Windows system files
            'venv',             # Virtual environments
            'node_modules',     # Node.js dependencies
            '.env',             # Environment files
            '*.log',            # Log files
            '*.tmp',            # Temporary files
            '*.temp',           # Temporary files
        ]
    
    def should_exclude(self, file_path, exclude_patterns):
        """Check if a file should be excluded from backup."""
        file_path_str = str(file_path)
        
        for pattern in exclude_patterns:
            if pattern in file_path_str:
                return True
            
            # Check if it's a hidden file/directory (starts with .)
            if pattern.startswith('.') and file_path.name.startswith('.'):
                return True
        
        return False
    
    def create_backup_with_zip(self, password, backup_name=None):
        """Create a password-protected zip backup using Python's zipfile."""
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"personal_system_backup_{timestamp}.zip"
        
        backup_path = self.weekly_backup_dir / backup_name
        
        # Check if backup already exists
        if backup_path.exists():
            logger.warning(f"Backup {backup_path} already exists. Overwriting...")
        
        logger.info(f"Creating backup: {backup_path}")
        logger.info(f"Source directory: {self.personal_system_path}")
        
        # Create password-protected zip file
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            total_files = 0
            total_size = 0
            
            for root, dirs, files in os.walk(self.personal_system_path):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not self.should_exclude(Path(root) / d, self.get_exclude_patterns())]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip excluded files
                    if self.should_exclude(file_path, self.get_exclude_patterns()):
                        continue
                    
                    # Calculate relative path for the zip file
                    try:
                        relative_path = file_path.relative_to(self.personal_system_path)
                        
                        # Try to use password protection if available
                        try:
                            zipf.write(file_path, relative_path, pwd=password.encode('utf-8'))
                        except TypeError:
                            # Fallback for older Python versions
                            zipf.write(file_path, relative_path)
                        
                        total_files += 1
                        total_size += file_path.stat().st_size
                        
                        if total_files % 100 == 0:
                            logger.info(f"Processed {total_files} files...")
                            
                    except Exception as e:
                        logger.error(f"Error adding {file_path}: {e}")
        
        # Convert total size to human readable format
        size_mb = total_size / (1024 * 1024)
        logger.info(f"Backup completed successfully!")
        logger.info(f"Total files: {total_files}")
        logger.info(f"Total size: {size_mb:.2f} MB")
        logger.info(f"Backup location: {backup_path}")
        
        return backup_path
    
    def create_backup_with_7zip(self, password, backup_name=None):
        """Create a password-protected backup using 7zip (if available)."""
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"personal_system_backup_{timestamp}.7z"
        
        backup_path = self.weekly_backup_dir / backup_name
        
        # Check if backup already exists
        if backup_path.exists():
            logger.warning(f"Backup {backup_path} already exists. Overwriting...")
        
        logger.info(f"Creating 7zip backup: {backup_path}")
        logger.info(f"Source directory: {self.personal_system_path}")
        
        # Build 7zip command
        cmd = [
            '7z', 'a', '-t7z', '-m0=lzma2', '-mx=9', '-mhe=on',
            f'-p{password}', str(backup_path), str(self.personal_system_path)
        ]
        
        # Add exclusion patterns
        exclude_patterns = self.get_exclude_patterns()
        for pattern in exclude_patterns:
            if not pattern.startswith('*'):
                cmd.extend(['-x!', pattern])
            else:
                # Handle wildcard patterns
                cmd.extend(['-x!', pattern])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("7zip backup completed successfully!")
            logger.info(f"Backup location: {backup_path}")
            return backup_path
        except subprocess.CalledProcessError as e:
            logger.error(f"7zip backup failed: {e}")
            logger.error(f"7zip output: {e.stdout}")
            logger.error(f"7zip errors: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error("7zip not found. Please install 7zip first.")
            raise
    
    def create_backup(self, password, backup_name=None, use_7zip=False):
        """Create a password-protected backup."""
        if use_7zip:
            try:
                return self.create_backup_with_7zip(password, backup_name)
            except Exception as e:
                logger.warning(f"7zip backup failed, falling back to zip: {e}")
                use_7zip = False
        
        if not use_7zip:
            return self.create_backup_with_zip(password, backup_name)
    
    def sync_to_google_drive(self, backup_path):
        """Sync the backup file to Google Drive."""
        if GoogleDriveSync is None:
            logger.error("Google Drive sync not available. Install required dependencies.")
            return False
        
        try:
            # Initialize Google Drive sync
            gdrive_sync = GoogleDriveSync()
            
            # Upload the backup file
            logger.info(f"Syncing {backup_path} to Google Drive...")
            success = gdrive_sync.upload_file(str(backup_path), 'backups')
            
            if success:
                logger.info("Backup successfully synced to Google Drive!")
                return True
            else:
                logger.error("Failed to sync backup to Google Drive")
                return False
                
        except Exception as e:
            logger.error(f"Error syncing to Google Drive: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count=5):
        """Remove old backup files, keeping the most recent ones."""
        backup_files = list(self.weekly_backup_dir.glob('personal_system_backup_*.*'))
        
        if len(backup_files) <= keep_count:
            logger.info(f"Keeping all {len(backup_files)} backup files")
            return
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove old backups
        for old_backup in backup_files[keep_count:]:
            try:
                old_backup.unlink()
                logger.info(f"Removed old backup: {old_backup.name}")
            except Exception as e:
                logger.error(f"Error removing old backup {old_backup}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Create a backup of the personal system')
    parser.add_argument('--path', help='Path to personal system directory')
    parser.add_argument('--name', help='Custom backup filename')
    parser.add_argument('--no-gdrive', action='store_true', help='Skip Google Drive sync')
    parser.add_argument('--cleanup', action='store_true', help='Clean up old backups')
    parser.add_argument('--keep', type=int, default=5, help='Number of backups to keep (default: 5)')
    parser.add_argument('--set-password', action='store_true', help='Set or update the stored backup password')
    parser.add_argument('--clear-password', action='store_true', help='Remove the stored backup password')
    parser.add_argument('--use-7zip', action='store_true', help='Use 7zip for better compression and password protection')
    
    args = parser.parse_args()
    
    try:
        # Initialize backup system
        backup_system = PersonalSystemBackup(args.path)
        
        # Handle password management commands
        if args.set_password:
            print("Setting backup password...")
            password = getpass.getpass("Enter new backup password: ")
            password_confirm = getpass.getpass("Confirm password: ")
            
            if password != password_confirm:
                print("Passwords do not match!")
                sys.exit(1)
            
            if len(password) < 8:
                print("Warning: Password is less than 8 characters long.")
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(1)
            
            if backup_system.store_password(password):
                print("Password stored successfully!")
            else:
                print("Failed to store password.")
            return
        
        if args.clear_password:
            if backup_system.clear_stored_password():
                print("Password removed successfully!")
            else:
                print("Failed to remove password.")
            return
        
        # Get password (try stored first, then prompt)
        password = backup_system.get_stored_password()
        
        if password is None:
            print("No stored password found. Please enter backup password:")
            password = getpass.getpass("Enter backup password: ")
            password_confirm = getpass.getpass("Confirm password: ")
            
            if password != password_confirm:
                print("Passwords do not match!")
                sys.exit(1)
            
            if len(password) < 8:
                print("Warning: Password is less than 8 characters long.")
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(1)
            
            # Offer to store the password
            if KEYRING_AVAILABLE:
                store_response = input("Store this password securely for future use? (Y/n): ")
                if store_response.lower() != 'n':
                    backup_system.store_password(password)
        else:
            print("Using stored backup password.")
        
        # Create backup
        backup_path = backup_system.create_backup(password, args.name, args.use_7zip)
        
        # Sync to Google Drive (unless disabled)
        if not args.no_gdrive:
            backup_system.sync_to_google_drive(backup_path)
        
        # Cleanup old backups if requested
        if args.cleanup:
            backup_system.cleanup_old_backups(args.keep)
        
        print(f"\nBackup completed successfully!")
        print(f"Location: {backup_path}")
        if not backup_system.get_stored_password():
            print(f"Password: {password}")
            print("Tip: Use --set-password to store this password securely for future use.")
        
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
