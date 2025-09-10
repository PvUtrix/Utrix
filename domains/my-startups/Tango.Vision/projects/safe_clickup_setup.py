#!/usr/bin/env python3
"""
Safe ClickUp Setup Script
This script ensures we don't overwrite existing data and provides backup options.
"""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime

def backup_existing_files():
    """Create backups of existing configuration files."""
    backup_dir = Path(__file__).parent / "backups" / f"clickup_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_backup = [
        "clickup_config.json",
        "projects_data.json",
        "clickup_mappings.json",
        "clickup_task_mappings.json"
    ]
    
    backed_up_files = []
    
    for filename in files_to_backup:
        file_path = Path(__file__).parent / filename
        if file_path.exists():
            backup_path = backup_dir / filename
            shutil.copy2(file_path, backup_path)
            backed_up_files.append(filename)
            print(f"✅ Backed up: {filename}")
    
    if backed_up_files:
        print(f"\n📁 Backup created in: {backup_dir}")
        print(f"Backed up files: {', '.join(backed_up_files)}")
    else:
        print("ℹ️  No existing configuration files to backup")
    
    return backup_dir

def check_existing_projects():
    """Check for existing projects and warn about potential conflicts."""
    projects_file = Path(__file__).parent / "projects_data.json"
    
    if not projects_file.exists():
        print("ℹ️  No existing projects found")
        return []
    
    try:
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects_data = json.load(f)
        
        existing_projects = list(projects_data.keys())
        print(f"📋 Found {len(existing_projects)} existing projects:")
        for project_id in existing_projects:
            project_name = projects_data[project_id].get('name', 'Unknown')
            print(f"  - {project_id}: {project_name}")
        
        return existing_projects
        
    except Exception as e:
        print(f"⚠️  Could not read existing projects: {e}")
        return []

def check_clickup_config():
    """Check if ClickUp is already configured."""
    config_file = Path(__file__).parent / "clickup_config.json"
    
    if not config_file.exists():
        print("ℹ️  No existing ClickUp configuration found")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check if configuration has real values (not placeholders)
        api_token = config.get('api_token', '')
        team_id = config.get('team_id', '')
        space_id = config.get('space_id', '')
        
        if (api_token and api_token != "YOUR_CLICKUP_API_TOKEN_HERE" and
            team_id and team_id != "YOUR_TEAM_ID_HERE" and
            space_id and space_id != "YOUR_SPACE_ID_HERE"):
            print("✅ ClickUp appears to be already configured")
            return True
        else:
            print("⚠️  ClickUp configuration exists but appears incomplete")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not read ClickUp configuration: {e}")
        return False

def safe_setup_clickup():
    """Safely set up ClickUp integration with backups and checks."""
    print("🛡️  Safe ClickUp Setup for Tango.Vision")
    print("=" * 50)
    
    # Step 1: Create backups
    print("\n1. Creating backups of existing files...")
    backup_dir = backup_existing_files()
    
    # Step 2: Check existing projects
    print("\n2. Checking existing projects...")
    existing_projects = check_existing_projects()
    
    # Step 3: Check ClickUp configuration
    print("\n3. Checking ClickUp configuration...")
    clickup_configured = check_clickup_config()
    
    # Step 4: Provide options
    print("\n4. Setup Options:")
    print("=" * 30)
    
    if clickup_configured:
        print("✅ ClickUp is already configured")
        print("Options:")
        print("  a) Test existing configuration")
        print("  b) Reconfigure ClickUp (will backup current config)")
        print("  c) Skip ClickUp setup")
        
        choice = input("\nEnter your choice (a/b/c): ").strip().lower()
        
        if choice == 'a':
            print("\n🧪 Testing existing ClickUp configuration...")
            try:
                import subprocess
                result = subprocess.run([
                    sys.executable, "setup_clickup.py", "--test-only"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ ClickUp configuration test passed!")
                    print(result.stdout)
                else:
                    print("❌ ClickUp configuration test failed:")
                    print(result.stderr)
                    
            except Exception as e:
                print(f"❌ Error testing configuration: {e}")
        
        elif choice == 'b':
            print("\n🔄 Reconfiguring ClickUp...")
            try:
                import subprocess
                subprocess.run([sys.executable, "setup_clickup.py"])
            except Exception as e:
                print(f"❌ Error during reconfiguration: {e}")
        
        elif choice == 'c':
            print("⏭️  Skipping ClickUp setup")
        
        else:
            print("❌ Invalid choice")
    
    else:
        print("ℹ️  ClickUp is not configured")
        print("Options:")
        print("  a) Set up ClickUp integration")
        print("  b) Skip ClickUp setup for now")
        
        choice = input("\nEnter your choice (a/b): ").strip().lower()
        
        if choice == 'a':
            print("\n🚀 Setting up ClickUp integration...")
            try:
                import subprocess
                subprocess.run([sys.executable, "setup_clickup.py"])
            except Exception as e:
                print(f"❌ Error during setup: {e}")
        
        elif choice == 'b':
            print("⏭️  Skipping ClickUp setup")
        
        else:
            print("❌ Invalid choice")
    
    # Step 5: Handle existing projects
    if existing_projects:
        print(f"\n5. Existing Projects Found ({len(existing_projects)})")
        print("=" * 40)
        print("You have existing projects that can be synced to ClickUp:")
        
        for project_id in existing_projects:
            print(f"  - {project_id}")
        
        sync_choice = input("\nWould you like to sync existing projects to ClickUp? (y/n): ").strip().lower()
        
        if sync_choice == 'y':
            print("\n🔄 Syncing existing projects to ClickUp...")
            try:
                from clickup_integrated_manager import ClickUpIntegratedManager
                manager = ClickUpIntegratedManager()
                
                if not manager.clickup_enabled:
                    print("❌ ClickUp integration not enabled. Please set up ClickUp first.")
                else:
                    for project_id in existing_projects:
                        print(f"Syncing {project_id}...")
                        if manager.sync_project_to_clickup(project_id):
                            print(f"✅ {project_id} synced successfully")
                        else:
                            print(f"❌ Failed to sync {project_id}")
                            
            except Exception as e:
                print(f"❌ Error syncing projects: {e}")
        else:
            print("⏭️  Skipping project sync")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Setup Summary")
    print("=" * 50)
    print(f"✅ Backups created in: {backup_dir}")
    print(f"📁 Existing projects: {len(existing_projects)}")
    print(f"🔧 ClickUp configured: {'Yes' if clickup_configured else 'No'}")
    
    print("\n🎯 Next Steps:")
    print("1. If ClickUp is configured, test it: python3 setup_clickup.py --test-only")
    print("2. Create new projects: python3 clickup_integrated_manager.py create 'Project Name'")
    print("3. Sync existing projects: python3 clickup_integrated_manager.py sync <project_id>")
    print("4. Generate reports: python3 clickup_integrated_manager.py report")
    
    print(f"\n🛡️  Your data is safely backed up in: {backup_dir}")

def main():
    """Main entry point."""
    try:
        safe_setup_clickup()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("Your data is still safe - check the backup directory")

if __name__ == "__main__":
    main()
