#!/usr/bin/env python3
"""
ClickUp Integration Setup Script for Tango.Vision
Helps configure ClickUp API integration and test the connection.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))
from clickup_client import ClickUpClient, ClickUpConfig

def get_user_input(prompt: str, default: str = "", required: bool = True) -> str:
    """Get user input with optional default value."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        value = input(full_prompt).strip()
        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("This field is required. Please enter a value.")

def get_choice(prompt: str, choices: List[str], default: str = "") -> str:
    """Get user choice from a list of options."""
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, 1):
        marker = " (default)" if choice == default else ""
        print(f"{i}. {choice}{marker}")
    
    while True:
        try:
            choice_input = input(f"Enter choice (1-{len(choices)}): ").strip()
            if not choice_input and default:
                return default
            
            choice_num = int(choice_input)
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print("Please enter a valid number")

def setup_clickup_config() -> Dict:
    """Interactive setup of ClickUp configuration."""
    print("=== ClickUp API Configuration Setup ===\n")
    
    print("To get your ClickUp API credentials:")
    print("1. Go to ClickUp Settings (click your avatar → Settings)")
    print("2. Navigate to Apps → API Token")
    print("3. Click 'Generate' to create a new token")
    print("4. Copy the token and paste it below\n")
    
    config = {}
    
    # Get API token
    config['api_token'] = get_user_input("Enter your ClickUp API token")
    
    # Test connection and get team/space info
    print("\nTesting connection and retrieving your ClickUp data...")
    
    try:
        temp_config = ClickUpConfig(api_token=config['api_token'])
        client = ClickUpClient(temp_config)
        
        # Get teams
        teams = client.get_teams()
        if not teams:
            print("❌ No teams found. Please check your API token.")
            return {}
        
        print(f"✅ Connection successful! Found {len(teams)} team(s).")
        
        # Select team
        if len(teams) == 1:
            selected_team = teams[0]
            print(f"Using team: {selected_team['name']}")
        else:
            team_names = [team['name'] for team in teams]
            selected_team_name = get_choice("Select your team:", team_names)
            selected_team = next(team for team in teams if team['name'] == selected_team_name)
        
        config['team_id'] = selected_team['id']
        
        # Get spaces
        spaces = client.get_spaces(selected_team['id'])
        if not spaces:
            print("❌ No spaces found in the selected team.")
            return {}
        
        print(f"Found {len(spaces)} space(s).")
        
        # Select space
        if len(spaces) == 1:
            selected_space = spaces[0]
            print(f"Using space: {selected_space['name']}")
        else:
            space_names = [space['name'] for space in spaces]
            selected_space_name = get_choice("Select your space:", space_names)
            selected_space = next(space for space in spaces if space['name'] == selected_space_name)
        
        config['space_id'] = selected_space['id']
        
        # Additional configuration
        config['rate_limit_delay'] = 0.1
        
        # Custom fields configuration
        config['custom_fields'] = {
            "budget": "Budget Amount",
            "revenue_potential": "Revenue Potential",
            "roi_estimate": "ROI Estimate",
            "project_priority": "Project Priority",
            "estimated_hours": "Estimated Hours",
            "actual_hours": "Actual Hours"
        }
        
        # List mappings
        config['list_mappings'] = {
            "planning": "📋 Planning",
            "in_progress": "🚀 In Progress", 
            "completed": "✅ Completed",
            "documentation": "📝 Documentation",
            "financial": "💰 Financial"
        }
        
        # Priority mappings
        config['priority_mappings'] = {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4
        }
        
        print(f"\n✅ Configuration completed successfully!")
        print(f"Team: {selected_team['name']} (ID: {selected_team['id']})")
        print(f"Space: {selected_space['name']} (ID: {selected_space['id']})")
        
        return config
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return {}

def save_config(config: Dict, config_file: str = None) -> bool:
    """Save configuration to file."""
    if config_file is None:
        config_file = Path(__file__).parent / "clickup_config.json"
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration saved to: {config_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False

def test_integration(config_file: str = None) -> bool:
    """Test the ClickUp integration."""
    if config_file is None:
        config_file = Path(__file__).parent / "clickup_config.json"
    
    if not Path(config_file).exists():
        print(f"❌ Configuration file not found: {config_file}")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        config = ClickUpConfig(**config_data)
        client = ClickUpClient(config)
        
        print("Testing ClickUp integration...")
        
        # Test basic connection
        teams = client.get_teams()
        print(f"✅ Connection test passed. Found {len(teams)} teams.")
        
        # Test space access
        spaces = client.get_spaces()
        print(f"✅ Space access test passed. Found {len(spaces)} spaces.")
        
        # Test creating a sample folder (optional)
        create_test = get_user_input("Create a test folder in ClickUp? (y/n)", "n", False).lower() == 'y'
        
        if create_test:
            test_folder = client.create_folder(
                space_id=config.space_id,
                name="Tango.Vision Test Folder"
            )
            print(f"✅ Test folder created: {test_folder['name']} (ID: {test_folder['id']})")
            print("You can delete this folder manually in ClickUp if needed.")
        
        print("\n🎉 ClickUp integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def create_sample_project() -> bool:
    """Create a sample project to test the integration."""
    try:
        from clickup_integrated_manager import ClickUpIntegratedManager
        
        print("\nCreating a sample project to test integration...")
        
        manager = ClickUpIntegratedManager()
        
        if not manager.clickup_enabled:
            print("❌ ClickUp integration not enabled. Please run setup first.")
            return False
        
        # Create sample project
        project_id = manager.create_project(
            name="ClickUp Integration Test",
            description="This is a test project to verify ClickUp integration is working correctly.",
            priority=Priority.MEDIUM,
            owner="System",
            budget=1000.0,
            revenue_potential=5000.0
        )
        
        print(f"✅ Sample project created: {project_id}")
        
        # Add sample tasks
        sample_tasks = [
            {
                "title": "Test task 1",
                "description": "This is a test task to verify task sync",
                "priority": Priority.HIGH,
                "daily_task": False
            },
            {
                "title": "Daily test task",
                "description": "This is a daily test task",
                "priority": Priority.MEDIUM,
                "daily_task": True
            }
        ]
        
        for task_data in sample_tasks:
            task_id = manager.add_task(
                project_id=project_id,
                title=task_data["title"],
                description=task_data["description"],
                priority=task_data["priority"],
                daily_task=task_data["daily_task"]
            )
            print(f"✅ Sample task created: {task_id}")
        
        # Generate report
        report = manager.generate_integrated_report()
        print("\n" + "="*50)
        print("INTEGRATION TEST REPORT")
        print("="*50)
        print(report)
        
        print(f"\n🎉 Sample project created successfully!")
        print(f"Check your ClickUp workspace to see the synced project and tasks.")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample project: {e}")
        return False

def main():
    """Main setup workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ClickUp Integration Setup for Tango.Vision")
    parser.add_argument("--config-file", help="Path to configuration file")
    parser.add_argument("--test-only", action="store_true", help="Only test existing configuration")
    parser.add_argument("--create-sample", action="store_true", help="Create sample project after setup")
    
    args = parser.parse_args()
    
    config_file = args.config_file or str(Path(__file__).parent / "clickup_config.json")
    
    if args.test_only:
        # Only test existing configuration
        if test_integration(config_file):
            if args.create_sample:
                create_sample_project()
        return
    
    # Full setup workflow
    print("🚀 ClickUp Integration Setup for Tango.Vision")
    print("=" * 50)
    
    # Step 1: Setup configuration
    print("\n1. Setting up ClickUp configuration...")
    config = setup_clickup_config()
    
    if not config:
        print("❌ Setup failed. Please check your API credentials and try again.")
        return
    
    # Step 2: Save configuration
    print("\n2. Saving configuration...")
    if not save_config(config, config_file):
        print("❌ Failed to save configuration.")
        return
    
    # Step 3: Test integration
    print("\n3. Testing integration...")
    if not test_integration(config_file):
        print("❌ Integration test failed.")
        return
    
    # Step 4: Create sample project (optional)
    if args.create_sample:
        print("\n4. Creating sample project...")
        create_sample_project()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 ClickUp Integration Setup Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Use the integrated manager: python clickup_integrated_manager.py")
    print("2. Create projects: python clickup_integrated_manager.py create 'Project Name'")
    print("3. Add tasks: python clickup_integrated_manager.py add-task <project_id> 'Task Title'")
    print("4. Upload documents: python clickup_integrated_manager.py upload <project_id> <file_path>")
    print("5. Generate reports: python clickup_integrated_manager.py report")
    print("\nYour projects will now automatically sync with ClickUp!")

if __name__ == "__main__":
    main()
