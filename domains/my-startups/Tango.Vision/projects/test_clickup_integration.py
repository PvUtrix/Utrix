#!/usr/bin/env python3
"""
Test Script for ClickUp Integration
Tests the ClickUp integration without requiring actual API credentials.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add the project manager to the path
sys.path.append(str(Path(__file__).parent))

def test_local_project_manager():
    """Test the local project manager functionality."""
    print("🧪 Testing Local Project Manager...")
    
    try:
        from project_manager import TangoVisionProjectManager, Priority
        
        manager = TangoVisionProjectManager()
        
        # Test project creation
        project_id = manager.create_project(
            name="Test Project",
            description="A test project for ClickUp integration",
            priority=Priority.HIGH,
            owner="Test User",
            budget=5000.0,
            revenue_potential=15000.0
        )
        
        print(f"✅ Created test project: {project_id}")
        
        # Test task creation
        task_id = manager.add_task(
            project_id=project_id,
            title="Test Task",
            description="A test task for ClickUp integration",
            priority=Priority.MEDIUM,
            daily_task=True
        )
        
        print(f"✅ Created test task: {task_id}")
        
        # Test daily tasks
        daily_tasks = manager.get_daily_tasks()
        print(f"✅ Found {len(daily_tasks)} daily tasks")
        
        # Test project summary
        summary = manager.get_project_summary()
        print(f"✅ Project summary: {summary['total_projects']} projects, {summary['total_tasks']} tasks")
        
        # Test report generation
        report = manager.generate_report()
        print(f"✅ Generated report ({len(report)} characters)")
        
        return True
        
    except Exception as e:
        print(f"❌ Local project manager test failed: {e}")
        return False

def test_clickup_client_structure():
    """Test the ClickUp client structure without API calls."""
    print("\n🧪 Testing ClickUp Client Structure...")
    
    try:
        from clickup_client import ClickUpConfig, ClickUpClient, ClickUpProjectManager
        
        # Test configuration
        config = ClickUpConfig(
            api_token="test_token",
            team_id="test_team",
            space_id="test_space"
        )
        
        print("✅ ClickUp configuration created")
        
        # Test client initialization (without API calls)
        client = ClickUpClient(config)
        print("✅ ClickUp client initialized")
        
        # Test project manager initialization
        project_manager = ClickUpProjectManager(client)
        print("✅ ClickUp project manager initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ ClickUp client structure test failed: {e}")
        return False

def test_integrated_manager_structure():
    """Test the integrated manager structure without API calls."""
    print("\n🧪 Testing Integrated Manager Structure...")
    
    try:
        from clickup_integrated_manager import ClickUpIntegratedManager
        
        # Test initialization (should work even without ClickUp config)
        manager = ClickUpIntegratedManager()
        print("✅ Integrated manager initialized")
        
        # Test local functionality
        from project_manager import Priority
        project_id = manager.local_manager.create_project(
            name="Integration Test Project",
            description="Testing integrated manager",
            priority=Priority.MEDIUM
        )
        
        print(f"✅ Created project via integrated manager: {project_id}")
        
        # Test ClickUp status (should return None without config)
        status = manager.get_clickup_status(project_id)
        print(f"✅ ClickUp status check: {status is None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integrated manager structure test failed: {e}")
        return False

def test_configuration_files():
    """Test configuration file structure."""
    print("\n🧪 Testing Configuration Files...")
    
    try:
        config_file = Path(__file__).parent / "clickup_config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            required_fields = ['api_token', 'team_id', 'space_id']
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print(f"⚠️  Configuration file exists but missing fields: {missing_fields}")
                print("   This is expected if you haven't set up ClickUp integration yet")
            else:
                print("✅ Configuration file has all required fields")
        else:
            print("⚠️  Configuration file not found (expected if not set up)")
        
        # Test template configuration
        template_file = Path(__file__).parent / "project_template.yaml"
        if template_file.exists():
            print("✅ Project template file exists")
        else:
            print("❌ Project template file missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration files test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        "project_manager.py",
        "clickup_client.py",
        "clickup_integrated_manager.py",
        "setup_clickup.py",
        "project_template.yaml",
        "README.md",
        "CLICKUP_INTEGRATION.md"
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = Path(__file__).parent / file_name
        if not file_path.exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all tests."""
    print("🚀 ClickUp Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Configuration Files", test_configuration_files),
        ("Local Project Manager", test_local_project_manager),
        ("ClickUp Client Structure", test_clickup_client_structure),
        ("Integrated Manager Structure", test_integrated_manager_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The ClickUp integration is ready to use.")
        print("\nNext steps:")
        print("1. Run: python3 setup_clickup.py")
        print("2. Configure your ClickUp API credentials")
        print("3. Test with: python3 setup_clickup.py --test-only --create-sample")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
