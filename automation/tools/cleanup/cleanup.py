#!/usr/bin/env python3
"""
🧹 Quick Cleanup Wrapper
Simple interface for the automated cleanup system
"""

import sys
import os
from pathlib import Path

# Add the tools directory to the path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

from automated_cleanup import AutomatedCleanup

def main():
    """Quick cleanup interface."""
    print("🧹 Personal System Cleanup")
    print("=" * 30)
    
    # Check if config exists
    config_path = tools_dir / "cleanup_config.yaml"
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        print("Please ensure cleanup_config.yaml exists in automation/tools/cleanup/")
        return 1
    
    cleanup = AutomatedCleanup(str(config_path))
    
    # Show menu
    print("\nChoose cleanup mode:")
    print("1. 🔍 Dry run (see what would be cleaned)")
    print("2. 🎯 Interactive cleanup (guided)")
    print("3. 🚀 Auto cleanup (automatic)")
    print("4. 📊 Show cleanup stats")
    print("5. ❌ Exit")
    
    try:
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            print("\n🔍 Running dry run...")
            cleanup.cleanup_files(dry_run=True)
            
        elif choice == "2":
            print("\n🎯 Starting interactive cleanup...")
            cleanup.interactive_cleanup()
            
        elif choice == "3":
            print("\n🚀 Running automatic cleanup...")
            cleanup.cleanup_files(dry_run=False)
            
        elif choice == "4":
            print("\n📊 Scanning for cleanup candidates...")
            results = cleanup.scan_directory()
            print(f"\n📈 Cleanup Statistics:")
            print(f"  🗑️  Files to remove: {len(results['auto_remove'])}")
            print(f"  🏷️  Files to mark: {len(results['mark_for_review'])}")
            print(f"  🔒 Preserved files: {len(results['preserved'])}")
            print(f"  ❓ Unknown files: {len(results['unknown'])}")
            
            if results['auto_remove']:
                print(f"\n🗑️  Files to remove:")
                for file in results['auto_remove'][:10]:  # Show first 10
                    print(f"    - {file}")
                if len(results['auto_remove']) > 10:
                    print(f"    ... and {len(results['auto_remove']) - 10} more")
            
            if results['mark_for_review']:
                print(f"\n🏷️  Files to mark for review:")
                for file in results['mark_for_review'][:10]:  # Show first 10
                    print(f"    - {file}")
                if len(results['mark_for_review']) > 10:
                    print(f"    ... and {len(results['mark_for_review']) - 10} more")
                    
        elif choice == "5":
            print("👋 Goodbye!")
            return 0
            
        else:
            print("❌ Invalid choice. Please enter 1-5.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n👋 Cleanup cancelled by user.")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
