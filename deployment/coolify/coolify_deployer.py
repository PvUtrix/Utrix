#!/usr/bin/env python3
"""
Coolify Deployment Integration
Handles automated deployments to Coolify with status tracking
"""

import json
import os
import time
import requests
from typing import Dict, Any, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoolifyDeployer:
    def __init__(self):
        self.coolify_url = os.getenv('COOLIFY_URL', 'https://coolify.yourdomain.com')
        self.api_token = os.getenv('COOLIFY_API_TOKEN')
        self.project_uuid = os.getenv('COOLIFY_PROJECT_UUID')
        self.application_uuid = os.getenv('COOLIFY_APPLICATION_UUID')

        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def deploy_application(self, repo_name: str, version: str, commit_info: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application to Coolify"""
        logger.info(f"🚀 Starting deployment of {repo_name} version {version}")

        if not self._validate_config():
            return {'success': False, 'error': 'Coolify configuration incomplete'}

        try:
            # Step 1: Get application info
            app_info = self._get_application_info()
            if not app_info:
                return {'success': False, 'error': 'Could not retrieve application information'}

            # Step 2: Trigger deployment
            deployment_result = self._trigger_deployment(version, commit_info)
            if not deployment_result['success']:
                return deployment_result

            # Step 3: Monitor deployment progress
            final_status = self._monitor_deployment(deployment_result['deployment_id'])

            return {
                'success': final_status['success'],
                'deployment_id': deployment_result['deployment_id'],
                'status': final_status['status'],
                'logs_url': final_status.get('logs_url'),
                'duration_seconds': final_status.get('duration', 0)
            }

        except Exception as e:
            logger.error(f"Deployment error: {e}")
            return {'success': False, 'error': str(e)}

    def _validate_config(self) -> bool:
        """Validate Coolify configuration"""
        required = [self.coolify_url, self.api_token, self.project_uuid, self.application_uuid]
        return all(required)

    def _get_application_info(self) -> Optional[Dict[str, Any]]:
        """Get application information from Coolify"""
        try:
            url = f"{self.coolify_url}/api/v1/applications/{self.application_uuid}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get app info: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting application info: {e}")
            return None

    def _trigger_deployment(self, version: str, commit_info: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger deployment in Coolify"""
        try:
            url = f"{self.coolify_url}/api/v1/applications/{self.application_uuid}/deploy"

            # Prepare deployment data
            deploy_data = {
                "version": version,
                "commit_message": commit_info.get('messages', [''])[0] if commit_info.get('messages') else '',
                "commit_count": commit_info.get('count', 1),
                "branch": commit_info.get('branch', 'main'),
                "triggered_by": "ci_cd_pipeline"
            }

            response = requests.post(url, json=deploy_data, headers=self.headers, timeout=30)

            if response.status_code in [200, 201]:
                result = response.json()
                deployment_id = result.get('deployment_id') or result.get('id')
                logger.info(f"✅ Deployment triggered: {deployment_id}")
                return {
                    'success': True,
                    'deployment_id': deployment_id
                }
            else:
                error_msg = f"Deployment trigger failed: {response.status_code}"
                logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg,
                    'response': response.text
                }

        except Exception as e:
            error_msg = f"Error triggering deployment: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}

    def _monitor_deployment(self, deployment_id: str, timeout_minutes: int = 10) -> Dict[str, Any]:
        """Monitor deployment progress"""
        logger.info(f"📊 Monitoring deployment: {deployment_id}")

        start_time = time.time()
        max_time = timeout_minutes * 60

        while time.time() - start_time < max_time:
            try:
                status = self._get_deployment_status(deployment_id)

                if status['status'] in ['completed', 'failed', 'cancelled']:
                    duration = time.time() - start_time
                    status['duration'] = duration
                    return status

                # Wait before checking again
                time.sleep(10)

            except Exception as e:
                logger.error(f"Error monitoring deployment: {e}")
                time.sleep(10)

        # Timeout reached
        return {
            'success': False,
            'status': 'timeout',
            'error': f'Deployment monitoring timed out after {timeout_minutes} minutes'
        }

    def _get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get current deployment status"""
        try:
            url = f"{self.coolify_url}/api/v1/deployments/{deployment_id}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()

                status = data.get('status', 'unknown')
                logs_url = data.get('logs_url')

                return {
                    'success': status == 'completed',
                    'status': status,
                    'logs_url': logs_url,
                    'progress': data.get('progress', 0)
                }
            else:
                return {
                    'success': False,
                    'status': 'error',
                    'error': f'API call failed: {response.status_code}'
                }

        except Exception as e:
            return {
                'success': False,
                'status': 'error',
                'error': str(e)
            }

    def get_deployment_logs(self, deployment_id: str) -> Optional[str]:
        """Get deployment logs"""
        try:
            status = self._get_deployment_status(deployment_id)
            logs_url = status.get('logs_url')

            if logs_url:
                response = requests.get(logs_url, headers=self.headers, timeout=30)
                if response.status_code == 200:
                    return response.text

            return None

        except Exception as e:
            logger.error(f"Error getting deployment logs: {e}")
            return None

    def rollback_deployment(self, deployment_id: str, target_version: str = None) -> Dict[str, Any]:
        """Rollback to previous deployment"""
        logger.info(f"🔄 Rolling back deployment: {deployment_id}")

        try:
            url = f"{self.coolify_url}/api/v1/applications/{self.application_uuid}/rollback"

            rollback_data = {
                "deployment_id": deployment_id,
                "target_version": target_version
            }

            response = requests.post(url, json=rollback_data, headers=self.headers, timeout=60)

            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    'success': True,
                    'rollback_id': result.get('id'),
                    'message': 'Rollback initiated'
                }
            else:
                return {
                    'success': False,
                    'error': f'Rollback failed: {response.status_code}'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def list_deployments(self, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """List recent deployments"""
        try:
            url = f"{self.coolify_url}/api/v1/applications/{self.application_uuid}/deployments"
            params = {'limit': limit}

            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if response.status_code == 200:
                return response.json().get('deployments', [])
            else:
                logger.error(f"Failed to list deployments: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error listing deployments: {e}")
            return None

def lambda_handler(event, context):
    """AWS Lambda handler for Coolify deployment"""
    deployer = CoolifyDeployer()

    action = event.get('action')

    if action == 'deploy':
        repo_name = event.get('repo_name', 'unknown')
        version = event.get('version', 'latest')
        commit_info = event.get('commit_info', {})

        result = deployer.deploy_application(repo_name, version, commit_info)
        return {
            'statusCode': 200 if result['success'] else 500,
            'body': json.dumps(result)
        }

    elif action == 'status':
        deployment_id = event.get('deployment_id')
        if deployment_id:
            status = deployer._get_deployment_status(deployment_id)
            return {
                'statusCode': 200,
                'body': json.dumps(status)
            }
        else:
            return {'statusCode': 400, 'body': 'Missing deployment_id'}

    elif action == 'logs':
        deployment_id = event.get('deployment_id')
        if deployment_id:
            logs = deployer.get_deployment_logs(deployment_id)
            return {
                'statusCode': 200,
                'body': json.dumps({'logs': logs})
            }
        else:
            return {'statusCode': 400, 'body': 'Missing deployment_id'}

    elif action == 'rollback':
        deployment_id = event.get('deployment_id')
        target_version = event.get('target_version')

        result = deployer.rollback_deployment(deployment_id, target_version)
        return {
            'statusCode': 200 if result['success'] else 500,
            'body': json.dumps(result)
        }

    elif action == 'list':
        limit = event.get('limit', 10)
        deployments = deployer.list_deployments(limit)
        return {
            'statusCode': 200,
            'body': json.dumps({'deployments': deployments})
        }

    return {'statusCode': 400, 'body': 'Invalid action'}

if __name__ == "__main__":
    # Local testing
    import sys

    if len(sys.argv) > 1:
        action = sys.argv[1]
        deployer = CoolifyDeployer()

        if action == 'list':
            deployments = deployer.list_deployments(5)
            if deployments:
                print("Recent deployments:")
                for deployment in deployments:
                    print(f"  {deployment.get('id')}: {deployment.get('status')} ({deployment.get('version')})")
            else:
                print("No deployments found")

        elif action == 'status':
            if len(sys.argv) > 2:
                deployment_id = sys.argv[2]
                status = deployer._get_deployment_status(deployment_id)
                print(f"Deployment {deployment_id} status: {status}")
            else:
                print("Usage: python coolify_deployer.py status <deployment_id>")

        else:
            print("Usage: python coolify_deployer.py [list|status <id>]")

    else:
        print("Coolify Deployer")
        print("Usage: python coolify_deployer.py [list|status <id>]")
