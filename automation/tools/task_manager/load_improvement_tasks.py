#!/usr/bin/env python3
"""
Load Improvement Tasks
Load the recommended improvement tasks from the markdown file into the task manager.
"""

import re
import logging
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from main import TaskManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_markdown_tasks(markdown_file: str) -> list:
    """Parse tasks from the markdown file."""
    tasks = []
    
    try:
        with open(markdown_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"Markdown file not found: {markdown_file}")
        return tasks
    
    # Parse immediate tasks
    immediate_section = re.search(r'## 🚀 Immediate Tasks.*?(?=## 📅|$)', content, re.DOTALL)
    if immediate_section:
        tasks.extend(parse_task_section(immediate_section.group(0), "immediate"))
    
    # Parse short-term tasks
    shortterm_section = re.search(r'## 📅 Short-term Tasks.*?(?=## 🎯|$)', content, re.DOTALL)
    if shortterm_section:
        tasks.extend(parse_task_section(shortterm_section.group(0), "short-term"))
    
    # Parse long-term tasks
    longterm_section = re.search(r'## 🎯 Long-term Tasks.*?(?=## 📊|$)', content, re.DOTALL)
    if longterm_section:
        tasks.extend(parse_task_section(longterm_section.group(0), "long-term"))
    
    return tasks

def parse_task_section(section_content: str, category: str) -> list:
    """Parse tasks from a specific section."""
    tasks = []
    
    # Find all task blocks
    task_pattern = r'### Task (\d+): (.+?)\n- \*\*Priority\*\*: (\w+).*?\n- \*\*Status\*\*: (\w+).*?\n- \*\*Description\*\*: (.+?)(?=\n- \*\*|$)'
    
    matches = re.findall(task_pattern, section_content, re.DOTALL)
    
    for match in matches:
        task_num, title, priority, status, description = match
        
        # Clean up the description
        description = description.strip()
        
        # Map priority to standard format
        priority_map = {
            "High": "high",
            "Medium": "medium", 
            "Low": "low"
        }
        priority = priority_map.get(priority, "medium")
        
        # Only add pending tasks
        if status.lower() == "pending":
            tasks.append({
                "title": f"Task {task_num}: {title}",
                "priority": priority,
                "category": category,
                "description": description,
                "task_id": f"task_{task_num}"
            })
    
    return tasks

def load_tasks_to_manager():
    """Load all improvement tasks into the task manager."""
    # Get the project root directory (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent
    markdown_file = project_root / "automation/outputs/codebase_improvement_tasks.md"
    manager = TaskManager()
    
    # Parse tasks from markdown
    tasks = parse_markdown_tasks(markdown_file)
    
    if not tasks:
        logger.warning("No tasks found in markdown file")
        return
    
    # Add tasks to manager
    added_count = 0
    for task in tasks:
        # Check if task already exists
        existing_tasks = manager.list_tasks()
        task_exists = any(task["task_id"] in t["title"] for t in existing_tasks)
        
        if not task_exists:
            manager.add_task(
                title=task["title"],
                priority=task["priority"],
                category=task["category"],
                description=task["description"]
            )
            added_count += 1
        else:
            logger.info(f"Task already exists: {task['title']}")
    
    logger.info(f"Added {added_count} new tasks to the task manager")
    
    # Generate and save report
    manager.save_report()
    print(f"\nTask Summary:")
    stats = manager.get_task_stats()
    print(f"- Total Tasks: {stats['total']}")
    print(f"- Completed: {stats['completed']}")
    print(f"- Pending: {stats['pending']}")
    print(f"- Completion Rate: {stats['completion_rate']:.1f}%")

if __name__ == "__main__":
    load_tasks_to_manager()
