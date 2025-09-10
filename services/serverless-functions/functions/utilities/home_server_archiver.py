#!/usr/bin/env python3
"""
Home Server Archiver
Manages data archiving to home server for long-term storage
"""

import json
import os
import paramiko
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HomeServerArchiver:
    def __init__(self):
        self.home_server_host = os.getenv('HOME_SERVER_HOST')
        self.home_server_user = os.getenv('HOME_SERVER_USER')
        self.home_server_key_path = os.getenv('HOME_SERVER_KEY_PATH', '~/.ssh/id_rsa')
        self.archive_path = os.getenv('HOME_SERVER_ARCHIVE_PATH', '/data/archive')
        self.api_endpoint = os.getenv('HOME_SERVER_API_ENDPOINT')

        # Use API if available, otherwise SSH
        self.use_api = bool(self.api_endpoint)

    def archive_data_batch(self, data_batch: List[Dict[str, Any]], batch_id: str) -> bool:
        """Archive a batch of data to home server"""
        try:
            if self.use_api:
                return self._archive_via_api(data_batch, batch_id)
            else:
                return self._archive_via_ssh(data_batch, batch_id)
        except Exception as e:
            logger.error(f"Error archiving batch {batch_id}: {e}")
            return False

    def _archive_via_api(self, data_batch: List[Dict[str, Any]], batch_id: str) -> bool:
        """Archive data via REST API"""
        try:
            payload = {
                'batch_id': batch_id,
                'data': data_batch,
                'timestamp': datetime.now().isoformat(),
                'source': 'personal_system'
            }

            response = requests.post(
                f"{self.api_endpoint}/archive",
                json=payload,
                headers={'Authorization': f"Bearer {os.getenv('HOME_SERVER_API_KEY')}"},
                timeout=30
            )

            if response.status_code == 200:
                logger.info(f"✅ Archived batch {batch_id} via API")
                return True
            else:
                logger.error(f"API archive failed: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"API archive error: {e}")
            return False

    def _archive_via_ssh(self, data_batch: List[Dict[str, Any]], batch_id: str) -> bool:
        """Archive data via SSH/SCP"""
        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect using key
            ssh.connect(
                self.home_server_host,
                username=self.home_server_user,
                key_filename=os.path.expanduser(self.home_server_key_path)
            )

            # Create archive directory
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            remote_dir = f"{self.archive_path}/{timestamp}_{batch_id}"

            stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {remote_dir}")
            if stdout.channel.recv_exit_status() != 0:
                logger.error(f"Failed to create remote directory: {stderr.read().decode()}")
                return False

            # Save data to temporary file
            local_file = f"/tmp/archive_{batch_id}.json"
            with open(local_file, 'w') as f:
                json.dump({
                    'batch_id': batch_id,
                    'data': data_batch,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'personal_system'
                }, f, indent=2)

            # Upload file via SCP
            with ssh.open_sftp() as sftp:
                remote_file = f"{remote_dir}/data.json"
                sftp.put(local_file, remote_file)

            # Clean up local file
            os.remove(local_file)

            # Create index file
            index_data = {
                'batch_id': batch_id,
                'timestamp': datetime.now().isoformat(),
                'data_types': list(set(item.get('data_type', 'unknown') for item in data_batch)),
                'record_count': len(data_batch),
                'file_path': f"{remote_dir}/data.json"
            }

            index_file = f"/tmp/index_{batch_id}.json"
            with open(index_file, 'w') as f:
                json.dump(index_data, f, indent=2)

            with ssh.open_sftp() as sftp:
                sftp.put(index_file, f"{remote_dir}/index.json")

            os.remove(index_file)

            ssh.close()

            logger.info(f"✅ Archived batch {batch_id} via SSH")
            return True

        except Exception as e:
            logger.error(f"SSH archive error: {e}")
            return False

    def retrieve_archived_data(self, batch_id: str) -> Dict[str, Any]:
        """Retrieve archived data from home server"""
        try:
            if self.use_api:
                return self._retrieve_via_api(batch_id)
            else:
                return self._retrieve_via_ssh(batch_id)
        except Exception as e:
            logger.error(f"Error retrieving batch {batch_id}: {e}")
            return {}

    def _retrieve_via_api(self, batch_id: str) -> Dict[str, Any]:
        """Retrieve data via REST API"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/archive/{batch_id}",
                headers={'Authorization': f"Bearer {os.getenv('HOME_SERVER_API_KEY')}"},
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API retrieve failed: {response.status_code}")
                return {}

        except Exception as e:
            logger.error(f"API retrieve error: {e}")
            return {}

    def _retrieve_via_ssh(self, batch_id: str) -> Dict[str, Any]:
        """Retrieve data via SSH/SCP"""
        try:
            # Find the batch file
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                self.home_server_host,
                username=self.home_server_user,
                key_filename=os.path.expanduser(self.home_server_key_path)
            )

            # Search for batch files
            stdin, stdout, stderr = ssh.exec_command(
                f"find {self.archive_path} -name '*{batch_id}*' -type f"
            )

            files = stdout.read().decode().strip().split('\n')
            if not files or files[0] == '':
                logger.warning(f"No files found for batch {batch_id}")
                return {}

            # Download the data file
            local_file = f"/tmp/retrieve_{batch_id}.json"
            with ssh.open_sftp() as sftp:
                for remote_file in files:
                    if remote_file.endswith('data.json'):
                        sftp.get(remote_file, local_file)
                        break

            ssh.close()

            # Read the data
            with open(local_file, 'r') as f:
                data = json.load(f)

            # Clean up
            os.remove(local_file)

            logger.info(f"✅ Retrieved batch {batch_id}")
            return data

        except Exception as e:
            logger.error(f"SSH retrieve error: {e}")
            return {}

    def list_archived_batches(self) -> List[Dict[str, Any]]:
        """List all archived batches"""
        try:
            if self.use_api:
                return self._list_via_api()
            else:
                return self._list_via_ssh()
        except Exception as e:
            logger.error(f"Error listing archived batches: {e}")
            return []

    def _list_via_api(self) -> List[Dict[str, Any]]:
        """List batches via REST API"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/archive",
                headers={'Authorization': f"Bearer {os.getenv('HOME_SERVER_API_KEY')}"},
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                return []

        except Exception as e:
            return []

    def _list_via_ssh(self) -> List[Dict[str, Any]]:
        """List batches via SSH"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                self.home_server_host,
                username=self.home_server_user,
                key_filename=os.path.expanduser(self.home_server_key_path)
            )

            # Get all index files
            stdin, stdout, stderr = ssh.exec_command(
                f"find {self.archive_path} -name 'index.json' -type f"
            )

            index_files = stdout.read().decode().strip().split('\n')
            batches = []

            with ssh.open_sftp() as sftp:
                for index_file in index_files:
                    if not index_file:
                        continue

                    try:
                        local_index = f"/tmp/index_{os.path.basename(os.path.dirname(index_file))}.json"
                        sftp.get(index_file, local_index)

                        with open(local_index, 'r') as f:
                            batch_info = json.load(f)

                        batches.append(batch_info)
                        os.remove(local_index)

                    except Exception as e:
                        logger.error(f"Error reading index {index_file}: {e}")
                        continue

            ssh.close()
            return batches

        except Exception as e:
            return []

    def cleanup_old_archives(self, retention_days: int = 2555):  # ~7 years
        """Clean up archives older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)

            if self.use_api:
                self._cleanup_via_api(cutoff_date)
            else:
                self._cleanup_via_ssh(cutoff_date)

            logger.info("🧹 Cleaned up old archives")

        except Exception as e:
            logger.error(f"Error cleaning up archives: {e}")

    def _cleanup_via_api(self, cutoff_date: datetime):
        """Clean up via REST API"""
        try:
            response = requests.post(
                f"{self.api_endpoint}/cleanup",
                json={'cutoff_date': cutoff_date.isoformat()},
                headers={'Authorization': f"Bearer {os.getenv('HOME_SERVER_API_KEY')}"},
                timeout=60
            )

            if response.status_code != 200:
                logger.error(f"API cleanup failed: {response.status_code}")

        except Exception as e:
            logger.error(f"API cleanup error: {e}")

    def _cleanup_via_ssh(self, cutoff_date: datetime):
        """Clean up via SSH"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                self.home_server_host,
                username=self.home_server_user,
                key_filename=os.path.expanduser(self.home_server_key_path)
            )

            # Find old directories
            cutoff_str = cutoff_date.strftime('%Y%m%d')
            stdin, stdout, stderr = ssh.exec_command(
                f"find {self.archive_path} -type d -name '{cutoff_str}*' -prune -o -type d -name '20*' -print | head -20"
            )

            old_dirs = stdout.read().decode().strip().split('\n')

            for old_dir in old_dirs:
                if old_dir and old_dir >= f"{self.archive_path}/{cutoff_str}":
                    # Remove old directory
                    stdin, stdout, stderr = ssh.exec_command(f"rm -rf {old_dir}")
                    if stdout.channel.recv_exit_status() == 0:
                        logger.info(f"Removed old archive: {old_dir}")

            ssh.close()

        except Exception as e:
            logger.error(f"SSH cleanup error: {e}")

def lambda_handler(event, context):
    """AWS Lambda handler for home server archiving"""
    archiver = HomeServerArchiver()

    action = event.get('action')

    if action == 'archive':
        data_batch = event.get('data_batch', [])
        batch_id = event.get('batch_id', f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        success = archiver.archive_data_batch(data_batch, batch_id)
        return {'statusCode': 200 if success else 500, 'body': json.dumps({'success': success})}

    elif action == 'retrieve':
        batch_id = event.get('batch_id')
        data = archiver.retrieve_archived_data(batch_id)
        return {'statusCode': 200, 'body': json.dumps(data)}

    elif action == 'list':
        batches = archiver.list_archived_batches()
        return {'statusCode': 200, 'body': json.dumps(batches)}

    elif action == 'cleanup':
        retention_days = event.get('retention_days', 2555)
        archiver.cleanup_old_archives(retention_days)
        return {'statusCode': 200, 'body': 'Cleanup completed'}

    return {'statusCode': 400, 'body': 'Invalid action'}

if __name__ == "__main__":
    # Local testing
    archiver = HomeServerArchiver()

    # Example data batch
    test_batch = [
        {
            'id': 'test_1',
            'data_type': 'journal',
            'content': 'Test journal entry',
            'timestamp': datetime.now().isoformat()
        }
    ]

    # Archive test batch
    success = archiver.archive_data_batch(test_batch, 'test_batch_001')
    print(f"Archive success: {success}")

    # List archived batches
    batches = archiver.list_archived_batches()
    print(f"Archived batches: {len(batches)}")
