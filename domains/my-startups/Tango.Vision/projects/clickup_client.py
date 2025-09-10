#!/usr/bin/env python3
"""
ClickUp API Client for Tango.Vision Project Management
Handles authentication, project creation, task management, and document uploads.
"""

import requests
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClickUpConfig:
    """ClickUp API configuration"""
    api_token: str
    team_id: Optional[str] = None
    space_id: Optional[str] = None
    base_url: str = "https://api.clickup.com/api/v2"
    rate_limit_delay: float = 0.1  # Delay between requests to respect rate limits
    custom_fields: Optional[Dict] = None
    list_mappings: Optional[Dict] = None
    priority_mappings: Optional[Dict] = None

class ClickUpClient:
    """ClickUp API client for Tango.Vision integration"""
    
    def __init__(self, config: ClickUpConfig):
        """Initialize the ClickUp client."""
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': config.api_token,
            'Content-Type': 'application/json'
        })
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting to respect API limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.config.rate_limit_delay:
            time.sleep(self.config.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict:
        """Make an authenticated request to ClickUp API."""
        self._rate_limit()
        
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"ClickUp API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            raise
    
    def get_teams(self) -> List[Dict]:
        """Get all teams for the authenticated user."""
        response = self._make_request('GET', '/team')
        return response.get('teams', [])
    
    def get_spaces(self, team_id: Optional[str] = None) -> List[Dict]:
        """Get all spaces for a team."""
        team_id = team_id or self.config.team_id
        if not team_id:
            raise ValueError("Team ID is required")
        
        response = self._make_request('GET', f'/team/{team_id}/space')
        return response.get('spaces', [])
    
    def create_space(self, team_id: str, name: str, private: bool = True) -> Dict:
        """Create a new space in ClickUp."""
        data = {
            'name': name,
            'private': private
        }
        return self._make_request('POST', f'/team/{team_id}/space', data=data)
    
    def create_folder(self, space_id: str, name: str) -> Dict:
        """Create a new folder in a space."""
        data = {'name': name}
        return self._make_request('POST', f'/space/{space_id}/folder', data=data)
    
    def create_list(self, folder_id: str, name: str, content: str = "", 
                   due_date: Optional[str] = None, priority: int = 3) -> Dict:
        """Create a new list in a folder."""
        data = {
            'name': name,
            'content': content,
            'due_date': due_date,
            'priority': priority
        }
        return self._make_request('POST', f'/folder/{folder_id}/list', data=data)
    
    def create_task(self, list_id: str, name: str, description: str = "", 
                   priority: int = 3, due_date: Optional[str] = None,
                   assignees: Optional[List[str]] = None, 
                   tags: Optional[List[str]] = None,
                   custom_fields: Optional[List[Dict]] = None) -> Dict:
        """Create a new task in a list."""
        data = {
            'name': name,
            'description': description,
            'priority': priority,
            'due_date': due_date,
            'assignees': assignees or [],
            'tags': tags or [],
            'custom_fields': custom_fields or []
        }
        return self._make_request('POST', f'/list/{list_id}/task', data=data)
    
    def update_task(self, task_id: str, **kwargs) -> Dict:
        """Update an existing task."""
        return self._make_request('PUT', f'/task/{task_id}', data=kwargs)
    
    def get_task(self, task_id: str) -> Dict:
        """Get task details."""
        return self._make_request('GET', f'/task/{task_id}')
    
    def add_task_comment(self, task_id: str, comment_text: str, 
                        notify_all: bool = False) -> Dict:
        """Add a comment to a task."""
        data = {
            'comment_text': comment_text,
            'notify_all': notify_all
        }
        return self._make_request('POST', f'/task/{task_id}/comment', data=data)
    
    def upload_attachment(self, task_id: str, file_path: Union[str, Path], 
                         filename: Optional[str] = None) -> Dict:
        """Upload a file attachment to a task."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        filename = filename or file_path.name
        
        # Prepare multipart form data
        files = {
            'attachment': (filename, open(file_path, 'rb'), 'application/octet-stream')
        }
        
        # Remove Content-Type header for multipart request
        headers = {'Authorization': self.config.api_token}
        
        self._rate_limit()
        url = f"{self.config.base_url}/task/{task_id}/attachment"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'attachment': (filename, f, 'application/octet-stream')}
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"File upload failed: {e}")
            raise
    
    def create_custom_field(self, list_id: str, name: str, field_type: str, 
                           options: Optional[List[str]] = None) -> Dict:
        """Create a custom field for a list."""
        data = {
            'name': name,
            'type': field_type,
            'type_config': {
                'options': options or []
            }
        }
        return self._make_request('POST', f'/list/{list_id}/field', data=data)
    
    def get_custom_fields(self, list_id: str) -> List[Dict]:
        """Get custom fields for a list."""
        response = self._make_request('GET', f'/list/{list_id}/field')
        return response.get('fields', [])
    
    def set_custom_field_value(self, task_id: str, field_id: str, value: Any) -> Dict:
        """Set a custom field value for a task."""
        data = {'value': value}
        return self._make_request('POST', f'/task/{task_id}/field/{field_id}', data=data)
    
    def get_lists_in_folder(self, folder_id: str) -> List[Dict]:
        """Get all lists in a folder."""
        response = self._make_request('GET', f'/folder/{folder_id}/list')
        return response.get('lists', [])
    
    def get_tasks_in_list(self, list_id: str, archived: bool = False) -> List[Dict]:
        """Get all tasks in a list."""
        params = {'archived': str(archived).lower()}
        response = self._make_request('GET', f'/list/{list_id}/task', params=params)
        return response.get('tasks', [])
    
    def search_tasks(self, query: str, team_id: Optional[str] = None) -> List[Dict]:
        """Search for tasks across the team."""
        team_id = team_id or self.config.team_id
        if not team_id:
            raise ValueError("Team ID is required for search")
        
        params = {'query': query}
        response = self._make_request('GET', f'/team/{team_id}/task', params=params)
        return response.get('tasks', [])

class ClickUpProjectManager:
    """High-level project management interface for ClickUp integration"""
    
    def __init__(self, client: ClickUpClient):
        """Initialize the project manager."""
        self.client = client
        self.project_mappings = {}  # Maps local project IDs to ClickUp folder IDs
    
    def create_project_in_clickup(self, project_name: str, project_description: str = "",
                                 space_id: Optional[str] = None) -> Dict:
        """Create a new project (list) in ClickUp."""
        space_id = space_id or self.client.config.space_id
        if not space_id:
            raise ValueError("Space ID is required")
        
        # Create a single list for the project (instead of folder with multiple lists)
        project_list = self.client.create_list(
            space_id=space_id,
            name=project_name,
            content=project_description or f"Project: {project_name}"
        )
        
        # Create initial project setup tasks
        setup_tasks = [
            {
                "name": "📋 Project Planning",
                "description": "Initial project planning and requirements gathering",
                "priority": 2,
                "tags": ["planning", "setup"]
            },
            {
                "name": "📝 Project Documentation",
                "description": "Create and maintain project documentation",
                "priority": 3,
                "tags": ["documentation", "setup"]
            },
            {
                "name": "💰 Financial Tracking",
                "description": "Track budget, spending, and revenue for this project",
                "priority": 3,
                "tags": ["financial", "tracking"]
            }
        ]
        
        created_tasks = []
        for task_data in setup_tasks:
            task = self.client.create_task(
                list_id=project_list['id'],
                name=task_data['name'],
                description=task_data['description'],
                priority=task_data['priority'],
                tags=task_data['tags']
            )
            created_tasks.append(task)
        
        return {
            'list': project_list,
            'setup_tasks': created_tasks
        }
    
    def sync_task_to_clickup(self, project_id: str, task_data: Dict, 
                            dependencies: Optional[List[str]] = None) -> Dict:
        """Sync a local task to ClickUp."""
        if project_id not in self.project_mappings:
            raise ValueError(f"Project {project_id} not found in ClickUp mappings")
        
        list_id = self.project_mappings[project_id]
        
        # Map priority
        priority_map = {
            'critical': 1,
            'high': 2,
            'medium': 3,
            'low': 4
        }
        priority = priority_map.get(task_data.get('priority', 'medium'), 3)
        
        # Prepare task data
        task_kwargs = {
            'list_id': list_id,
            'name': task_data['title'],
            'description': task_data.get('description', ''),
            'priority': priority,
            'due_date': task_data.get('due_date'),
            'tags': task_data.get('tags', [])
        }
        
        # Add custom fields for financial tracking if available
        custom_fields = []
        if task_data.get('estimated_hours', 0) > 0:
            custom_fields.append({
                'id': 'estimated_hours',
                'value': task_data['estimated_hours']
            })
        
        if custom_fields:
            task_kwargs['custom_fields'] = custom_fields
        
        # Create task in ClickUp
        clickup_task = self.client.create_task(**task_kwargs)
        
        # Handle dependencies if provided
        if dependencies:
            self._add_task_dependencies(clickup_task['id'], dependencies)
        
        return clickup_task
    
    def _add_task_dependencies(self, task_id: str, dependencies: List[str]) -> None:
        """Add dependencies to a task."""
        # Note: ClickUp API doesn't have direct dependency support in task creation
        # Dependencies would need to be handled through custom fields or comments
        for dep_task_id in dependencies:
            # Add dependency as a comment for now
            self.client.add_task_comment(
                task_id=task_id,
                comment_text=f"Depends on: {dep_task_id}"
            )
    
    def upload_project_document(self, project_id: str, file_path: Union[str, Path],
                               task_name: str = "Document Upload") -> Dict:
        """Upload a document to a project in ClickUp."""
        if project_id not in self.project_mappings:
            raise ValueError(f"Project {project_id} not found in ClickUp mappings")
        
        list_id = self.project_mappings[project_id]
        
        # Create a task for the document
        task = self.client.create_task(
            list_id=list_id,
            name=task_name,
            description=f"Document: {Path(file_path).name}",
            tags=["document", "upload"]
        )
        
        # Upload the file as an attachment
        attachment = self.client.upload_attachment(task['id'], file_path)
        
        return {
            'task': task,
            'attachment': attachment
        }
    
    def add_project_comment(self, project_id: str, comment: str, 
                           task_name: str = "Project Comment") -> Dict:
        """Add a comment to a project in ClickUp."""
        if project_id not in self.project_mappings:
            raise ValueError(f"Project {project_id} not found in ClickUp mappings")
        
        list_id = self.project_mappings[project_id]
        
        # Create a task for the comment
        task = self.client.create_task(
            list_id=list_id,
            name=task_name,
            description=comment,
            tags=["comment", "update"]
        )
        
        return task
    
    def get_project_status(self, project_id: str) -> Dict:
        """Get the current status of a project in ClickUp."""
        if project_id not in self.project_mappings:
            raise ValueError(f"Project {project_id} not found in ClickUp mappings")
        
        list_id = self.project_mappings[project_id]
        tasks = self.client.get_tasks_in_list(list_id)
        
        status = {
            'project_id': project_id,
            'list_id': list_id,
            'total_tasks': len(tasks),
            'completed_tasks': len([t for t in tasks if t.get('status', {}).get('status') == 'complete']),
            'pending_tasks': len([t for t in tasks if t.get('status', {}).get('status') != 'complete']),
            'tasks_by_priority': {
                'critical': len([t for t in tasks if t.get('priority', {}).get('priority') == '1']),
                'high': len([t for t in tasks if t.get('priority', {}).get('priority') == '2']),
                'medium': len([t for t in tasks if t.get('priority', {}).get('priority') == '3']),
                'low': len([t for t in tasks if t.get('priority', {}).get('priority') == '4'])
            }
        }
        
        if status['total_tasks'] > 0:
            status['completion_rate'] = (status['completed_tasks'] / status['total_tasks']) * 100
        else:
            status['completion_rate'] = 0
        
        return status

def load_clickup_config(config_file: Union[str, Path] = None) -> ClickUpConfig:
    """Load ClickUp configuration from file."""
    if config_file is None:
        config_file = Path(__file__).parent / "clickup_config.json"
    
    config_file = Path(config_file)
    
    if not config_file.exists():
        # Create a sample configuration file
        sample_config = {
            "api_token": "YOUR_CLICKUP_API_TOKEN_HERE",
            "team_id": "YOUR_TEAM_ID_HERE",
            "space_id": "YOUR_SPACE_ID_HERE",
            "rate_limit_delay": 0.1
        }
        
        with open(config_file, 'w') as f:
            json.dump(sample_config, f, indent=2)
        
        logger.warning(f"Created sample configuration file: {config_file}")
        logger.warning("Please update the configuration with your ClickUp API credentials")
        raise ValueError(f"Please configure ClickUp API credentials in {config_file}")
    
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    
    return ClickUpConfig(**config_data)

def main():
    """Test the ClickUp client functionality."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ClickUp API Client Test")
    parser.add_argument("--config", help="Path to ClickUp configuration file")
    parser.add_argument("--test-connection", action="store_true", help="Test API connection")
    parser.add_argument("--list-teams", action="store_true", help="List available teams")
    parser.add_argument("--list-spaces", action="store_true", help="List available spaces")
    
    args = parser.parse_args()
    
    try:
        config = load_clickup_config(args.config)
        client = ClickUpClient(config)
        
        if args.test_connection:
            print("Testing ClickUp API connection...")
            teams = client.get_teams()
            print(f"✅ Connection successful! Found {len(teams)} teams.")
        
        if args.list_teams:
            teams = client.get_teams()
            print(f"\nAvailable teams ({len(teams)}):")
            for team in teams:
                print(f"- {team['name']} (ID: {team['id']})")
        
        if args.list_spaces:
            if not config.team_id:
                print("❌ Team ID not configured. Please set team_id in config file.")
                return
            
            spaces = client.get_spaces()
            print(f"\nAvailable spaces ({len(spaces)}):")
            for space in spaces:
                print(f"- {space['name']} (ID: {space['id']})")
    
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
