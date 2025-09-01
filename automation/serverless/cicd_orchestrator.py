#!/usr/bin/env python3
"""
CI/CD Orchestrator with Voice Notifications
Manages automated deployments with spoken feedback
"""

import json
import os
import subprocess
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from voice_content_generator import VoiceContentGenerator
from elevenlabs_tts import ElevenLabsTTS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CICDVoiceOrchestrator:
    def __init__(self):
        self.voice_generator = VoiceContentGenerator()
        self.tts = ElevenLabsTTS()
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.gitea_token = os.getenv('GITEA_TOKEN')
        self.gitea_url = os.getenv('GITEA_URL', 'https://git.yourdomain.com')
        self.coolify_token = os.getenv('COOLIFY_TOKEN')
        self.coolify_url = os.getenv('COOLIFY_URL', 'https://coolify.yourdomain.com')

    def handle_gitea_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming Gitea webhook and trigger CI/CD pipeline"""
        logger.info("🎣 Received Gitea webhook")

        # Extract webhook information
        repository = webhook_data.get('repository', {})
        commits = webhook_data.get('commits', [])
        ref = webhook_data.get('ref', '')
        pusher = webhook_data.get('pusher', {})

        # Check if this is a push to main/master branch
        if not self._is_main_branch_push(ref):
            logger.info("⏭️ Not a main branch push, skipping deployment")
            return {'status': 'skipped', 'reason': 'not_main_branch'}

        # Extract commit information
        commit_info = self._extract_commit_info(commits)

        # Start voice-enabled deployment process
        return self._run_voice_deployment_pipeline(commit_info, repository, pusher)

    def _run_voice_deployment_pipeline(self, commit_info: Dict[str, Any],
                                     repository: Dict[str, Any], pusher: Dict[str, Any]) -> Dict[str, Any]:
        """Run the complete deployment pipeline with a single voice notification"""

        repo_name = repository.get('name', 'unknown')
        branch = commit_info.get('branch', 'main')
        commit_count = commit_info.get('count', 0)

        try:
            # Run all steps silently (no intermediate voice notifications)
            validation_result = self._validate_changes(commit_info)
            if not validation_result['success']:
                self._speak_simple_notification(f"❌ Deployment failed for {repo_name}: validation error")
                return {'status': 'failed', 'stage': 'validation', 'error': validation_result['error']}

            build_result = self._build_application(repo_name)
            if not build_result['success']:
                self._speak_simple_notification(f"❌ Deployment failed for {repo_name}: build error")
                return {'status': 'failed', 'stage': 'build', 'error': build_result['error']}

            version = self._generate_version_number(commit_info)
            deploy_result = self._deploy_to_coolify(repo_name, version, commit_info)
            if not deploy_result['success']:
                self._speak_simple_notification(f"❌ Deployment failed for {repo_name}: deployment error")
                return {'status': 'failed', 'stage': 'deploy', 'error': deploy_result['error']}

            verification_result = self._verify_deployment(repo_name, version)

            # Single success notification with all details
            self._speak_simple_notification(
                f"✅ {repo_name} version {version} deployed successfully with {commit_count} commits"
            )

            # Log deployment
            self._log_deployment(version, commit_info, deploy_result)

            return {
                'status': 'success',
                'version': version,
                'commits': commit_count,
                'deployment_time_minutes': self._calculate_deployment_time()
            }

        except Exception as e:
            error_msg = f"Deployment error for {repo_name}: {str(e)}"
            self._speak_simple_notification(f"💥 {error_msg}")
            logger.error(error_msg)
            return {'status': 'error', 'error': error_msg}

    def _speak_notification(self, message: str):
        """Send voice notification via Telegram"""
        logger.info(f"🎤 Speaking: {message}")

        try:
            # Generate speech
            audio_data = self.tts.generate_speech(message)

            if audio_data:
                # Send via Telegram
                self._send_voice_message(audio_data, message[:100])  # Caption limited to 100 chars

                # Also send as text for backup
                self._send_text_message(message)

        except Exception as e:
            logger.error(f"Failed to send voice notification: {e}")
            # Fallback to text-only notification
            self._send_text_message(f"🔊 {message}")

    def _speak_simple_notification(self, message: str):
        """Send a simple, concise voice notification"""
        logger.info(f"🎤 Simple notification: {message}")

        try:
            # Generate speech with shorter text for faster processing
            audio_data = self.tts.generate_speech(message)

            if audio_data:
                # Send via Telegram with minimal caption
                self._send_voice_message(audio_data, message[:50])
                # Skip text backup for simplicity
            else:
                # Fallback to text-only
                self._send_text_message(message)

        except Exception as e:
            logger.error(f"Failed to send simple voice notification: {e}")
            self._send_text_message(message)

    def _send_voice_message(self, audio_data: bytes, caption: str = None):
        """Send voice message via Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            return

        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendVoice"
            files = {'voice': ('notification.mp3', audio_data, 'audio/mpeg')}
            data = {'chat_id': self.telegram_chat_id}

            if caption:
                data['caption'] = caption

            response = requests.post(url, data=data, files=files, timeout=30)

            if response.status_code == 200:
                logger.info("✅ Voice notification sent")
            else:
                logger.error(f"Failed to send voice: {response.status_code}")

        except Exception as e:
            logger.error(f"Error sending voice message: {e}")

    def _send_text_message(self, message: str):
        """Send text message via Telegram as backup"""
        if not self.telegram_token or not self.telegram_chat_id:
            return

        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }

            response = requests.post(url, json=data, timeout=10)

            if response.status_code == 200:
                logger.info("✅ Text notification sent")
            else:
                logger.error(f"Failed to send text: {response.status_code}")

        except Exception as e:
            logger.error(f"Error sending text message: {e}")

    def _is_main_branch_push(self, ref: str) -> bool:
        """Check if this is a push to main/master branch"""
        return ref in ['refs/heads/main', 'refs/heads/master']

    def _extract_commit_info(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract relevant information from commits"""
        if not commits:
            return {'count': 0, 'messages': [], 'affected_files': []}

        commit_messages = []
        affected_files = set()

        for commit in commits:
            # Extract commit message
            message = commit.get('message', '').split('\n')[0]  # First line only
            commit_messages.append(message)

            # Extract affected files
            for file_info in commit.get('added', []) + commit.get('modified', []) + commit.get('removed', []):
                affected_files.add(file_info)

        # Extract branch from ref if available
        branch = 'main'  # Default
        if commits and 'url' in commits[0]:
            # Try to extract branch from commit URL
            pass

        return {
            'count': len(commits),
            'messages': commit_messages,
            'affected_files': list(affected_files)[:10],  # Limit to 10 files
            'branch': branch,
            'authors': list(set(commit.get('author', {}).get('name', 'unknown') for commit in commits))
        }

    def _validate_changes(self, commit_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate code changes (placeholder for actual validation)"""
        # In a real implementation, you might:
        # - Run tests
        # - Check code quality
        # - Validate configuration
        # - Security scanning

        logger.info("🔍 Running validation checks...")

        # Simulate validation
        return {'success': True}

    def _build_application(self, repo_name: str) -> Dict[str, Any]:
        """Build application (placeholder for actual build)"""
        # In a real implementation, you might:
        # - Run Docker builds
        # - Compile assets
        # - Run build scripts
        # - Package application

        logger.info(f"🔨 Building {repo_name}...")

        # Simulate build process
        return {'success': True}

    def _deploy_to_coolify(self, repo_name: str, version: str, commit_info: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to Coolify"""
        logger.info(f"📦 Deploying {repo_name} version {version} to Coolify")

        if not self.coolify_token or not self.coolify_url:
            return {'success': False, 'error': 'Coolify credentials not configured'}

        try:
            # Coolify API deployment
            # This is a simplified example - adjust based on your Coolify setup
            headers = {
                'Authorization': f'Bearer {self.coolify_token}',
                'Content-Type': 'application/json'
            }

            # Trigger deployment
            deploy_data = {
                'repository': repo_name,
                'version': version,
                'commit_info': commit_info
            }

            response = requests.post(
                f"{self.coolify_url}/api/deploy",
                json=deploy_data,
                headers=headers,
                timeout=300  # 5 minutes for deployment
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'deployment_id': result.get('id'),
                    'status_url': result.get('status_url')
                }
            else:
                return {
                    'success': False,
                    'error': f'Coolify API error: {response.status_code}'
                }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _verify_deployment(self, repo_name: str, version: str) -> Dict[str, Any]:
        """Verify deployment health"""
        logger.info(f"✅ Verifying deployment of {repo_name} {version}")

        # In a real implementation, you might:
        # - Health checks
        # - Smoke tests
        # - Performance monitoring
        # - Error log checking

        return {'success': True}

    def _generate_version_number(self, commit_info: Dict[str, Any]) -> str:
        """Generate version number based on commits"""
        # Simple versioning: date + commit count
        today = datetime.now().strftime('%Y%m%d')
        commit_count = commit_info.get('count', 1)

        return f"{today}.{commit_count}"

    def _calculate_deployment_time(self) -> float:
        """Calculate deployment duration (placeholder)"""
        # In a real implementation, track start/end times
        return 2.5  # minutes

    def _log_deployment(self, version: str, commit_info: Dict[str, Any], deploy_result: Dict[str, Any]):
        """Log deployment details"""
        logger.info(f"📊 Deployment logged: {version}")

        # In a real implementation, save to database
        # You could integrate with your existing multi-tier database system

def lambda_handler(event, context):
    """AWS Lambda handler for CI/CD webhooks"""
    orchestrator = CICDVoiceOrchestrator()

    # Handle Gitea webhook
    if event.get('source') == 'gitea':
        result = orchestrator.handle_gitea_webhook(event)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    return {'statusCode': 400, 'body': 'Invalid event source'}

if __name__ == "__main__":
    # Local testing
    orchestrator = CICDVoiceOrchestrator()

    # Test webhook data
    test_webhook = {
        'source': 'gitea',
        'ref': 'refs/heads/main',
        'repository': {'name': 'personal-system'},
        'commits': [
            {
                'message': 'Add simplified voice notifications',
                'author': {'name': 'Developer'},
                'added': ['voice_system.py'],
                'modified': ['README.md']
            }
        ],
        'pusher': {'name': 'John Doe'}
    }

    print("Testing simplified CI/CD pipeline...")
    print("Expected: Single voice notification on success/failure")
    result = orchestrator.handle_gitea_webhook(test_webhook)
    print(f"Deployment result: {result}")
