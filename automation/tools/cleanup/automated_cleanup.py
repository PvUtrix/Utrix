#!/usr/bin/env python3
"""
🧹 Automated Cleanup System
Intelligent file cleanup with marking, archiving, and safety features
"""

import os
import yaml
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional
import fnmatch
import json

class AutomatedCleanup:
    def __init__(self, config_path: str = "automation/tools/cleanup/cleanup_config.yaml"):
        """Initialize the automated cleanup system."""
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.cleanup_stats = {
            'removed': [],
            'marked': [],
            'archived': [],
            'errors': []
        }
        
    def _load_config(self) -> Dict:
        """Load cleanup configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Config file not found: {self.config_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"❌ Error parsing config: {e}")
            return {}
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for cleanup operations."""
        logger = logging.getLogger('automated_cleanup')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        fh = logging.FileHandler('logs/cleanup.log')
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def _matches_pattern(self, file_path: str, patterns: List[str]) -> bool:
        """Check if file matches any of the given patterns."""
        for pattern in patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False
    
    def _is_preserved(self, file_path: str) -> bool:
        """Check if file should be preserved."""
        preserve_patterns = self.config.get('preserve', [])
        return self._matches_pattern(file_path, preserve_patterns)
    
    def _should_auto_remove(self, file_path: str) -> bool:
        """Check if file should be automatically removed."""
        if self._is_preserved(file_path):
            return False
            
        auto_remove = self.config.get('auto_remove', {})
        for category, patterns in auto_remove.items():
            if self._matches_pattern(file_path, patterns):
                return True
        return False
    
    def _should_mark_for_review(self, file_path: str) -> bool:
        """Check if file should be marked for review."""
        if self._is_preserved(file_path):
            return False
            
        mark_patterns = self.config.get('mark_for_review', {})
        for category, patterns in mark_patterns.items():
            if self._matches_pattern(file_path, patterns):
                return True
        return False
    
    def _create_backup(self, file_path: str) -> bool:
        """Create backup of file before removal."""
        if not self.config.get('actions', {}).get('backup', {}).get('enabled', False):
            return True
            
        backup_dir = Path(self.config.get('actions', {}).get('backup', {}).get('backup_dir', '.cleanup_backup'))
        backup_dir.mkdir(exist_ok=True)
        
        try:
            source = Path(file_path)
            backup_path = backup_dir / source.name
            
            # Handle duplicate names
            counter = 1
            while backup_path.exists():
                backup_path = backup_dir / f"{source.stem}_{counter}{source.suffix}"
                counter += 1
            
            shutil.copy2(source, backup_path)
            self.logger.info(f"📦 Backed up: {file_path} -> {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Backup failed for {file_path}: {e}")
            return False
    
    def _archive_file(self, file_path: str) -> bool:
        """Archive file instead of removing."""
        archive_dir = Path(self.config.get('actions', {}).get('marked_files', {}).get('archive_dir', '.cleanup_archive'))
        archive_dir.mkdir(exist_ok=True)
        
        try:
            source = Path(file_path)
            archive_path = archive_dir / source.name
            
            # Handle duplicate names
            counter = 1
            while archive_path.exists():
                archive_path = archive_dir / f"{source.stem}_{counter}{source.suffix}"
                counter += 1
            
            shutil.move(str(source), str(archive_path))
            self.logger.info(f"📁 Archived: {file_path} -> {archive_path}")
            self.cleanup_stats['archived'].append(str(archive_path))
            return True
        except Exception as e:
            self.logger.error(f"❌ Archive failed for {file_path}: {e}")
            return False
    
    def _remove_file(self, file_path: str) -> bool:
        """Remove file safely."""
        try:
            path = Path(file_path)
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
            
            self.logger.info(f"🗑️  Removed: {file_path}")
            self.cleanup_stats['removed'].append(file_path)
            return True
        except Exception as e:
            self.logger.error(f"❌ Removal failed for {file_path}: {e}")
            self.cleanup_stats['errors'].append(f"{file_path}: {e}")
            return False
    
    def _mark_file(self, file_path: str) -> bool:
        """Mark file for review."""
        try:
            # Create a marker file
            marker_path = Path(file_path + ".CLEANUP_MARKER")
            with open(marker_path, 'w') as f:
                f.write(f"Marked for cleanup review on {datetime.now().isoformat()}\n")
                f.write(f"Original file: {file_path}\n")
                f.write(f"Reason: Matches cleanup pattern\n")
            
            self.logger.info(f"🏷️  Marked for review: {file_path}")
            self.cleanup_stats['marked'].append(file_path)
            return True
        except Exception as e:
            self.logger.error(f"❌ Marking failed for {file_path}: {e}")
            return False
    
    def scan_directory(self, directory: str = ".") -> Dict[str, List[str]]:
        """Scan directory and categorize files."""
        results = {
            'auto_remove': [],
            'mark_for_review': [],
            'preserved': [],
            'unknown': []
        }
        
        # Directories to skip entirely
        skip_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 'myenv', '.cleanup_archive', '.cleanup_backup', '.cleanup_temp'}
        
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in skip_dirs]
            
            # Skip if we're in a virtual environment or other excluded directory
            if any(skip_dir in root for skip_dir in skip_dirs):
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                
                # Skip files in virtual environments
                if any(skip_dir in relative_path for skip_dir in skip_dirs):
                    continue
                
                if self._is_preserved(relative_path):
                    results['preserved'].append(relative_path)
                elif self._should_auto_remove(relative_path):
                    results['auto_remove'].append(relative_path)
                elif self._should_mark_for_review(relative_path):
                    results['mark_for_review'].append(relative_path)
                else:
                    results['unknown'].append(relative_path)
        
        return results
    
    def cleanup_files(self, dry_run: bool = False) -> Dict:
        """Perform cleanup operations."""
        self.logger.info("🧹 Starting automated cleanup...")
        
        if dry_run:
            self.logger.info("🔍 DRY RUN MODE - No files will be modified")
        
        # Scan for files
        scan_results = self.scan_directory()
        
        # Process auto-remove files
        for file_path in scan_results['auto_remove']:
            if dry_run:
                self.logger.info(f"🔍 Would remove: {file_path}")
            else:
                if self._create_backup(file_path):
                    self._remove_file(file_path)
        
        # Process mark-for-review files
        for file_path in scan_results['mark_for_review']:
            if dry_run:
                self.logger.info(f"🔍 Would mark for review: {file_path}")
            else:
                self._mark_file(file_path)
        
        # Generate summary
        summary = self._generate_summary(scan_results, dry_run)
        self._save_summary(summary)
        
        return summary
    
    def _generate_summary(self, scan_results: Dict, dry_run: bool) -> Dict:
        """Generate cleanup summary."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': dry_run,
            'scan_results': scan_results,
            'cleanup_stats': self.cleanup_stats,
            'total_files_scanned': sum(len(files) for files in scan_results.values()),
            'files_to_remove': len(scan_results['auto_remove']),
            'files_to_mark': len(scan_results['mark_for_review']),
            'preserved_files': len(scan_results['preserved'])
        }
        
        return summary
    
    def _save_summary(self, summary: Dict):
        """Save cleanup summary to file."""
        try:
            summary_file = self.config.get('notifications', {}).get('report_file', 'logs/cleanup_summary.md')
            summary_dir = Path(summary_file).parent
            summary_dir.mkdir(exist_ok=True)
            
            with open(summary_file, 'w') as f:
                f.write(f"# 🧹 Cleanup Summary - {summary['timestamp']}\n\n")
                f.write(f"**Mode**: {'Dry Run' if summary['dry_run'] else 'Live Cleanup'}\n\n")
                f.write(f"## 📊 Statistics\n\n")
                f.write(f"- **Total files scanned**: {summary['total_files_scanned']}\n")
                f.write(f"- **Files to remove**: {summary['files_to_remove']}\n")
                f.write(f"- **Files to mark**: {summary['files_to_mark']}\n")
                f.write(f"- **Preserved files**: {summary['preserved_files']}\n\n")
                
                if summary['cleanup_stats']['removed']:
                    f.write(f"## 🗑️ Removed Files\n\n")
                    for file in summary['cleanup_stats']['removed']:
                        f.write(f"- `{file}`\n")
                    f.write("\n")
                
                if summary['cleanup_stats']['marked']:
                    f.write(f"## 🏷️ Marked Files\n\n")
                    for file in summary['cleanup_stats']['marked']:
                        f.write(f"- `{file}`\n")
                    f.write("\n")
                
                if summary['cleanup_stats']['errors']:
                    f.write(f"## ❌ Errors\n\n")
                    for error in summary['cleanup_stats']['errors']:
                        f.write(f"- {error}\n")
                    f.write("\n")
            
            self.logger.info(f"📄 Summary saved to: {summary_file}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save summary: {e}")
    
    def interactive_cleanup(self):
        """Interactive cleanup mode with user confirmation."""
        print("🧹 Interactive Cleanup Mode")
        print("=" * 50)
        
        scan_results = self.scan_directory()
        
        # Show files to be removed
        if scan_results['auto_remove']:
            print(f"\n🗑️  Files to be removed ({len(scan_results['auto_remove'])}):")
            for file in scan_results['auto_remove']:
                print(f"  - {file}")
            
            response = input("\n❓ Remove these files? (y/N): ").lower()
            if response == 'y':
                for file in scan_results['auto_remove']:
                    if self._create_backup(file):
                        self._remove_file(file)
        
        # Show files to be marked
        if scan_results['mark_for_review']:
            print(f"\n🏷️  Files to be marked for review ({len(scan_results['mark_for_review'])}):")
            for file in scan_results['mark_for_review']:
                print(f"  - {file}")
            
            response = input("\n❓ Mark these files for review? (y/N): ").lower()
            if response == 'y':
                for file in scan_results['mark_for_review']:
                    self._mark_file(file)
        
        # Generate summary
        summary = self._generate_summary(scan_results, False)
        self._save_summary(summary)
        
        print(f"\n✅ Cleanup completed! Check logs/cleanup_summary.md for details.")

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Cleanup System')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be cleaned without making changes')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode with user confirmation')
    parser.add_argument('--config', default='automation/tools/cleanup/cleanup_config.yaml', help='Path to config file')
    
    args = parser.parse_args()
    
    cleanup = AutomatedCleanup(args.config)
    
    if args.interactive:
        cleanup.interactive_cleanup()
    else:
        summary = cleanup.cleanup_files(dry_run=args.dry_run)
        
        if args.dry_run:
            print("🔍 Dry run completed. Use --interactive for guided cleanup or remove --dry-run for live cleanup.")
        else:
            print("✅ Cleanup completed! Check logs/cleanup_summary.md for details.")

if __name__ == "__main__":
    main()
