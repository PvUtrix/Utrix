"""
Google Drive Integration for Personal System

A general-purpose Google Drive connector that respects privacy markers
and integrates with the personal knowledge management system.
"""

import os
import logging
import json
from typing import List, Dict, Optional, Union
from datetime import datetime
from pathlib import Path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# Scopes for different access levels
SCOPES = {
    'readonly': [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.metadata.readonly'
    ],
    'full': [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]
}

class GoogleDriveIntegration:
    """General-purpose Google Drive integration for personal system"""
    
    def __init__(self, 
                 credentials_path: str,
                 scope_level: str = 'readonly',
                 workspace_root: str = None):
        """
        Initialize Google Drive integration
        
        Args:
            credentials_path: Path to credentials.json file
            scope_level: 'readonly' or 'full' access
            workspace_root: Root path of personal system workspace
        """
        self.credentials_path = credentials_path
        self.scope_level = scope_level
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        token_path = self.workspace_root / 'config' / 'local' / 'google_drive_token.json'
        
        # Load existing token if available
        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES[self.scope_level])
            except Exception as e:
                logger.warning(f"Could not load existing token: {e}")
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.warning(f"Could not refresh token: {e}")
                    creds = None
            
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES[self.scope_level])
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next use
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Successfully connected to Google Drive API")
        except Exception as e:
            logger.error(f"Error connecting to Google Drive API: {e}")
            raise
    
    def list_files(self, 
                   folder_id: str = None, 
                   query: str = None,
                   file_types: List[str] = None) -> List[Dict]:
        """
        List files from Google Drive
        
        Args:
            folder_id: Specific folder ID to list from
            query: Custom query string for filtering
            file_types: List of MIME types to filter by
            
        Returns:
            List of file metadata dictionaries
        """
        try:
            # Build query
            query_parts = []
            
            if folder_id:
                query_parts.append(f"'{folder_id}' in parents")
            
            if file_types:
                type_query = " or ".join([f"mimeType='{ft}'" for ft in file_types])
                query_parts.append(f"({type_query})")
            
            if query:
                query_parts.append(query)
            
            # Add trashed=false to exclude deleted files
            query_parts.append("trashed=false")
            
            final_query = " and ".join(query_parts) if query_parts else "trashed=false"
            
            # Execute query
            results = self.service.files().list(
                q=final_query,
                pageSize=1000,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime, parents, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            # Handle pagination
            while 'nextPageToken' in results:
                results = self.service.files().list(
                    q=final_query,
                    pageSize=1000,
                    pageToken=results['nextPageToken'],
                    fields="nextPageToken, files(id, name, mimeType, size, modifiedTime, parents, webViewLink)"
                ).execute()
                files.extend(results.get('files', []))
            
            logger.info(f"Found {len(files)} files in Google Drive")
            return files
            
        except HttpError as e:
            logger.error(f"Error listing files: {e}")
            raise
    
    def download_file(self, 
                     file_id: str, 
                     destination_path: Union[str, Path],
                     create_dirs: bool = True) -> bool:
        """
        Download a file from Google Drive
        
        Args:
            file_id: Google Drive file ID
            destination_path: Local path to save file
            create_dirs: Whether to create parent directories
            
        Returns:
            True if successful, False otherwise
        """
        try:
            destination_path = Path(destination_path)
            
            if create_dirs:
                destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get file metadata
            file_metadata = self.service.files().get(fileId=file_id).execute()
            file_name = file_metadata.get('name', 'unknown_file')
            
            # Download file
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.info(f"Downloading {file_name}: {int(status.progress() * 100)}%")
            
            # Save to destination
            with open(destination_path, 'wb') as f:
                f.write(fh.getvalue())
            
            logger.info(f"Successfully downloaded {file_name} to {destination_path}")
            return True
            
        except HttpError as e:
            logger.error(f"Error downloading file {file_id}: {e}")
            return False
    
    def sync_folder(self, 
                   folder_id: str, 
                   local_path: Union[str, Path],
                   file_types: List[str] = None,
                   respect_privacy: bool = True) -> Dict:
        """
        Sync a Google Drive folder to local storage
        
        Args:
            folder_id: Google Drive folder ID
            local_path: Local directory to sync to
            file_types: List of MIME types to sync
            respect_privacy: Whether to check for privacy markers
            
        Returns:
            Dictionary with sync results
        """
        local_path = Path(local_path)
        local_path.mkdir(parents=True, exist_ok=True)
        
        # Get files from Google Drive
        files = self.list_files(folder_id=folder_id, file_types=file_types)
        
        results = {
            'total_files': len(files),
            'downloaded': 0,
            'skipped': 0,
            'errors': 0,
            'details': []
        }
        
        for file_info in files:
            file_name = file_info['name']
            file_id = file_info['id']
            
            # Check privacy markers if enabled
            if respect_privacy:
                if self._has_privacy_markers(file_name):
                    results['skipped'] += 1
                    results['details'].append({
                        'file': file_name,
                        'status': 'skipped',
                        'reason': 'privacy_marker'
                    })
                    continue
            
            # Download file
            destination = local_path / file_name
            if self.download_file(file_id, destination):
                results['downloaded'] += 1
                results['details'].append({
                    'file': file_name,
                    'status': 'downloaded',
                    'path': str(destination)
                })
            else:
                results['errors'] += 1
                results['details'].append({
                    'file': file_name,
                    'status': 'error'
                })
        
        logger.info(f"Sync completed: {results['downloaded']} downloaded, "
                   f"{results['skipped']} skipped, {results['errors']} errors")
        return results
    
    def _has_privacy_markers(self, file_name: str) -> bool:
        """Check if file has privacy markers"""
        privacy_markers = ['.private', '.share', 'confidential', 'internal']
        file_lower = file_name.lower()
        return any(marker in file_lower for marker in privacy_markers)
    
    def search_files(self, 
                    query: str, 
                    file_types: List[str] = None) -> List[Dict]:
        """
        Search for files in Google Drive
        
        Args:
            query: Search query string
            file_types: List of MIME types to filter by
            
        Returns:
            List of matching files
        """
        search_query = f"fullText contains '{query}'"
        return self.list_files(query=search_query, file_types=file_types)
    
    def get_file_info(self, file_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific file
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            File metadata dictionary or None if not found
        """
        try:
            file_info = self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, modifiedTime, createdTime, parents, webViewLink, description"
            ).execute()
            return file_info
        except HttpError as e:
            logger.error(f"Error getting file info for {file_id}: {e}")
            return None
