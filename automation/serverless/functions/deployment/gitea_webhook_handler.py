#!/usr/bin/env python3
"""
Gitea Webhook Handler for CI/CD
Receives webhooks from Gitea and triggers deployments
"""

import json
import os
import hmac
import hashlib
import requests
from typing import Dict, Any, Optional
from cicd_orchestrator import CICDVoiceOrchestrator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GiteaWebhookHandler:
    def __init__(self):
        self.orchestrator = CICDVoiceOrchestrator()
        self.webhook_secret = os.getenv('GITEA_WEBHOOK_SECRET')

    def handle_webhook(self, event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        """Handle incoming webhook from Gitea"""

        # Verify webhook signature if secret is configured
        if self.webhook_secret:
            if not self._verify_signature(event, headers):
                logger.warning("⚠️ Webhook signature verification failed")
                return {'statusCode': 401, 'body': 'Invalid signature'}

        # Extract webhook body
        if isinstance(event.get('body'), str):
            try:
                webhook_data = json.loads(event['body'])
            except json.JSONDecodeError:
                return {'statusCode': 400, 'body': 'Invalid JSON'}
        else:
            webhook_data = event

        # Add source identifier
        webhook_data['source'] = 'gitea'

        # Log webhook details
        event_type = headers.get('X-Gitea-Event', 'unknown')
        logger.info(f"🎣 Received {event_type} webhook from Gitea")

        # Handle different webhook events
        if event_type == 'push':
            return self._handle_push_event(webhook_data)
        elif event_type == 'pull_request':
            return self._handle_pull_request_event(webhook_data)
        else:
            logger.info(f"⏭️ Ignoring {event_type} event")
            return {'statusCode': 200, 'body': 'Event ignored'}

    def _handle_push_event(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle push events (main deployment trigger)"""
        result = self.orchestrator.handle_gitea_webhook(webhook_data)

        if result.get('status') == 'success':
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Deployment triggered successfully',
                    'deployment_id': result.get('version'),
                    'commits': result.get('commits')
                })
            }
        else:
            status_code = 500 if result.get('status') == 'error' else 200
            return {
                'statusCode': status_code,
                'body': json.dumps(result)
            }

    def _handle_pull_request_event(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pull request events (optional staging deployment)"""
        action = webhook_data.get('action')
        merged = webhook_data.get('pull_request', {}).get('merged', False)

        if action == 'closed' and merged:
            logger.info("🔄 Pull request merged, could trigger staging deployment")
            # Optional: Trigger staging deployment
            return {'statusCode': 200, 'body': 'PR merged - staging deployment could be triggered'}

        return {'statusCode': 200, 'body': 'PR event processed'}

    def _verify_signature(self, event: Dict[str, Any], headers: Dict[str, str]) -> bool:
        """Verify webhook signature for security"""
        signature = headers.get('X-Gitea-Signature')

        if not signature:
            return False

        # Get the raw body for signature verification
        if isinstance(event.get('body'), str):
            body = event['body'].encode('utf-8')
        else:
            body = json.dumps(event).encode('utf-8')

        # Calculate expected signature
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()

        # Compare signatures
        return hmac.compare_digest(f"sha256={expected_signature}", signature)

def create_gitea_webhook(gitea_url: str, repo_owner: str, repo_name: str, webhook_url: str, token: str):
    """Create webhook in Gitea repository"""
    url = f"{gitea_url}/api/v1/repos/{repo_owner}/{repo_name}/hooks"

    webhook_config = {
        "type": "gitea",
        "config": {
            "url": webhook_url,
            "content_type": "json"
        },
        "events": ["push", "pull_request"],
        "active": True
    }

    # Add secret if configured
    secret = os.getenv('GITEA_WEBHOOK_SECRET')
    if secret:
        webhook_config["config"]["secret"] = secret

    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=webhook_config, headers=headers)

        if response.status_code == 201:
            webhook_data = response.json()
            print(f"✅ Webhook created successfully: {webhook_data['url']}")
            return webhook_data
        else:
            print(f"❌ Failed to create webhook: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error creating webhook: {e}")
        return None

def lambda_handler(event, context):
    """AWS Lambda handler for Gitea webhooks"""
    handler = GiteaWebhookHandler()

    # Get headers from the event
    headers = event.get('headers', {})

    # Handle the webhook
    result = handler.handle_webhook(event, headers)

    return result

if __name__ == "__main__":
    # Local testing
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'create-webhook':
        # Create webhook in Gitea
        gitea_url = os.getenv('GITEA_URL', 'https://git.yourdomain.com')
        repo_owner = input("Repository owner: ")
        repo_name = input("Repository name: ")
        webhook_url = input("Webhook URL (Lambda URL): ")
        token = os.getenv('GITEA_TOKEN')

        if not token:
            print("❌ GITEA_TOKEN environment variable not set")
            sys.exit(1)

        create_gitea_webhook(gitea_url, repo_owner, repo_name, webhook_url, token)

    else:
        # Test webhook handling
        handler = GiteaWebhookHandler()

        # Test push event
        test_event = {
            "ref": "refs/heads/main",
            "repository": {"name": "personal-system", "owner": {"login": "yourusername"}},
            "commits": [
                {
                    "message": "Add voice notifications to CI/CD",
                    "author": {"name": "Developer"},
                    "added": ["cicd_orchestrator.py"],
                    "modified": ["README.md"]
                }
            ],
            "pusher": {"name": "John Doe"}
        }

        test_headers = {"X-Gitea-Event": "push"}

        result = handler.handle_webhook(test_event, test_headers)
        print(f"Webhook result: {result}")
