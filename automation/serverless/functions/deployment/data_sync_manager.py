#!/usr/bin/env python3
"""
Multi-Tier Data Sync Manager
Manages data movement between Core (Free Tier), Main (Self-hosted), and Archive (Home Server)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import boto3
from supabase import create_client, Client
import requests
import logging
import yaml
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseTier:
    """Represents a database tier configuration"""
    name: str
    supabase_url: str
    supabase_key: str
    priority: int  # 1 = highest priority (Core)
    capacity_mb: int
    retention_days: int

    @property
    def client(self) -> Client:
        return create_client(self.supabase_url, self.supabase_key)

class DataSyncManager:
    def __init__(self):
        self.tiers = self._load_tier_config()
        self.sync_log_table = "data_sync_log"

    def _load_tier_config(self) -> Dict[str, DatabaseTier]:
        """Load database tier configurations from YAML config file"""
        config_path = os.path.join(os.path.dirname(__file__), 'multi_tier_config.yaml')
        if not os.path.exists(config_path):
            # Try local config first
            local_config = os.path.join(os.path.dirname(__file__), 'multi_tier_config.local.yaml')
            if os.path.exists(local_config):
                config_path = local_config

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            tiers = {}
            for tier_name, tier_config in config['database_tiers'].items():
                tiers[tier_name] = DatabaseTier(
                    name=tier_config['name'],
                    supabase_url=os.getenv(tier_config['url_env']),
                    supabase_key=os.getenv(tier_config['key_env']),
                    priority=tier_config['priority'],
                    capacity_mb=tier_config['capacity_mb'],
                    retention_days=int(tier_config['retention_policy'].replace(' days', ''))
                )
            return tiers
        else:
            # Fallback to environment variables if config file doesn't exist
            return {
                'core': DatabaseTier(
                    name='core',
                    supabase_url=os.getenv('CORE_SUPABASE_URL'),
                    supabase_key=os.getenv('CORE_SUPABASE_ANON_KEY'),
                    priority=1,
                    capacity_mb=500,
                    retention_days=90
                ),
                'main': DatabaseTier(
                    name='main',
                    supabase_url=os.getenv('MAIN_SUPABASE_URL'),
                    supabase_key=os.getenv('MAIN_SUPABASE_ANON_KEY'),
                    priority=2,
                    capacity_mb=10000,
                    retention_days=365
                ),
                'archive': DatabaseTier(
                    name='archive',
                    supabase_url=os.getenv('ARCHIVE_SUPABASE_URL', ''),
                    supabase_key=os.getenv('ARCHIVE_SUPABASE_ANON_KEY', ''),
                    priority=3,
                    capacity_mb=50000,
                    retention_days=-1
                )
            }

    def classify_data_for_tier(self, data_type: str, data_size_kb: int, last_accessed: datetime) -> str:
        """Classify which tier data should belong to based on access patterns"""

        # Core tier: Frequently accessed, small data
        if data_type in ['daily_summary', 'shadow_work_current', 'recent_journal', 'active_tasks']:
            return 'core'

        # Main tier: Historical data, moderate access
        days_since_access = (datetime.now() - last_accessed).days
        if days_since_access <= 90:
            return 'main'

        # Archive tier: Old data, rarely accessed
        if days_since_access > 365 or data_size_kb > 100:  # Large files
            return 'archive'

        return 'main'  # Default

    def move_data_between_tiers(self, data_id: str, from_tier: str, to_tier: str, data_type: str):
        """Move data between database tiers"""
        try:
            # Get data from source tier
            source_client = self.tiers[from_tier].client
            dest_client = self.tiers[to_tier].client

            # Query data from source
            source_data = self._get_data_from_tier(source_client, data_id, data_type)
            if not source_data:
                logger.warning(f"No data found for {data_id} in {from_tier}")
                return False

            # Insert into destination
            success = self._insert_data_to_tier(dest_client, source_data, data_type)

            if success:
                # Delete from source (if not archive tier)
                if from_tier != 'archive':
                    self._delete_data_from_tier(source_client, data_id, data_type)

                # Log the sync
                self._log_sync_operation(data_id, from_tier, to_tier, data_type, 'move')
                logger.info(f"✅ Moved {data_id} from {from_tier} to {to_tier}")

                return True
            else:
                logger.error(f"Failed to move {data_id} to {to_tier}")
                return False

        except Exception as e:
            logger.error(f"Error moving data {data_id}: {e}")
            return False

    def sync_data_across_tiers(self):
        """Synchronize data across all tiers based on policies"""
        logger.info("🔄 Starting data synchronization across tiers")

        # Check each tier for data that needs to be moved
        for tier_name, tier in self.tiers.items():
            if not tier.supabase_url:  # Skip if not configured
                continue

            self._process_tier_data_movement(tier_name, tier)

        logger.info("✅ Data synchronization complete")

    def _process_tier_data_movement(self, tier_name: str, tier: DatabaseTier):
        """Process data movement for a specific tier"""
        client = tier.client

        # Check data size vs capacity
        current_size = self._get_tier_size_mb(client)
        if current_size > tier.capacity_mb * 0.8:  # 80% threshold
            logger.warning(f"⚠️ {tier_name} tier at {current_size}/{tier.capacity_mb}MB")
            self._move_old_data_to_next_tier(tier_name)

        # Move old data based on retention policy
        self._enforce_retention_policy(tier_name, tier)

    def _move_old_data_to_next_tier(self, current_tier: str):
        """Move oldest data to the next tier when capacity is reached"""
        next_tier = self._get_next_tier(current_tier)
        if not next_tier:
            logger.warning(f"No next tier available for {current_tier}")
            return

        # Get oldest data from current tier
        current_client = self.tiers[current_tier].client
        old_data = self._get_oldest_data(current_client, limit=10)  # Move 10 items at a time

        for data_item in old_data:
            self.move_data_between_tiers(
                data_item['id'],
                current_tier,
                next_tier,
                data_item['data_type']
            )

    def _enforce_retention_policy(self, tier_name: str, tier: DatabaseTier):
        """Enforce data retention policies"""
        if tier.retention_days == -1:  # Keep forever
            return

        client = tier.client
        cutoff_date = datetime.now() - timedelta(days=tier.retention_days)

        # Find data older than retention period
        old_data = self._get_data_older_than(client, cutoff_date)

        next_tier = self._get_next_tier(tier_name)
        if not next_tier:
            logger.warning(f"No next tier for retention enforcement in {tier_name}")
            return

        for data_item in old_data:
            self.move_data_between_tiers(
                data_item['id'],
                tier_name,
                next_tier,
                data_item['data_type']
            )

    def _get_next_tier(self, current_tier: str) -> Optional[str]:
        """Get the next tier in the hierarchy"""
        tier_order = ['core', 'main', 'archive']
        try:
            current_index = tier_order.index(current_tier)
            if current_index < len(tier_order) - 1:
                return tier_order[current_index + 1]
        except ValueError:
            pass
        return None

    def _get_tier_size_mb(self, client: Client) -> float:
        """Get approximate size of data in a tier"""
        try:
            # This is a simplified estimation - in production you'd query actual sizes
            response = client.table('data_inventory').select('size_kb').execute()
            total_kb = sum(item['size_kb'] for item in response.data)
            return total_kb / 1024
        except:
            return 0.0

    def _get_oldest_data(self, client: Client, limit: int = 10) -> List[Dict]:
        """Get oldest data items from a tier"""
        try:
            response = client.table('data_inventory') \
                .select('*') \
                .order('last_accessed', desc=False) \
                .limit(limit) \
                .execute()
            return response.data
        except:
            return []

    def _get_data_older_than(self, client: Client, cutoff_date: datetime) -> List[Dict]:
        """Get data older than specified date"""
        try:
            response = client.table('data_inventory') \
                .select('*') \
                .lt('created_at', cutoff_date.isoformat()) \
                .execute()
            return response.data
        except:
            return []

    def _get_data_from_tier(self, client: Client, data_id: str, data_type: str) -> Optional[Dict]:
        """Retrieve data from a specific tier"""
        try:
            table_name = self._get_table_for_data_type(data_type)
            response = client.table(table_name).select('*').eq('id', data_id).execute()
            return response.data[0] if response.data else None
        except:
            return None

    def _insert_data_to_tier(self, client: Client, data: Dict, data_type: str) -> bool:
        """Insert data into a specific tier"""
        try:
            table_name = self._get_table_for_data_type(data_type)
            # Remove id to avoid conflicts
            insert_data = {k: v for k, v in data.items() if k != 'id'}
            response = client.table(table_name).insert(insert_data).execute()
            return len(response.data) > 0
        except:
            return False

    def _delete_data_from_tier(self, client: Client, data_id: str, data_type: str) -> bool:
        """Delete data from a specific tier"""
        try:
            table_name = self._get_table_for_data_type(data_type)
            response = client.table(table_name).delete().eq('id', data_id).execute()
            return True
        except:
            return False

    def _get_table_for_data_type(self, data_type: str) -> str:
        """Map data type to table name"""
        table_mapping = {
            'daily_summary': 'daily_summaries',
            'shadow_work': 'shadow_work_data',
            'journal': 'journal_entries',
            'projects': 'projects',
            'research': 'research_notes',
            'contacts': 'contacts',
            'templates': 'templates'
        }
        return table_mapping.get(data_type, 'misc_data')

    def _log_sync_operation(self, data_id: str, from_tier: str, to_tier: str,
                           data_type: str, operation: str):
        """Log data synchronization operations"""
        try:
            core_client = self.tiers['core'].client
            log_entry = {
                'data_id': data_id,
                'from_tier': from_tier,
                'to_tier': to_tier,
                'data_type': data_type,
                'operation': operation,
                'timestamp': datetime.now().isoformat()
            }
            core_client.table(self.sync_log_table).insert(log_entry).execute()
        except Exception as e:
            logger.error(f"Failed to log sync operation: {e}")

    def get_sync_status(self) -> Dict[str, Any]:
        """Get synchronization status across all tiers"""
        status = {}

        for tier_name, tier in self.tiers.items():
            if not tier.supabase_url:
                status[tier_name] = {'configured': False}
                continue

            try:
                size_mb = self._get_tier_size_mb(tier.client)
                status[tier_name] = {
                    'configured': True,
                    'size_mb': size_mb,
                    'capacity_mb': tier.capacity_mb,
                    'usage_percent': (size_mb / tier.capacity_mb) * 100,
                    'retention_days': tier.retention_days
                }
            except Exception as e:
                status[tier_name] = {
                    'configured': True,
                    'error': str(e)
                }

        return status

def lambda_handler(event, context):
    """AWS Lambda handler for data synchronization"""
    sync_manager = DataSyncManager()

    if event.get('action') == 'sync':
        sync_manager.sync_data_across_tiers()
        return {'statusCode': 200, 'body': 'Sync completed'}

    elif event.get('action') == 'status':
        status = sync_manager.get_sync_status()
        return {'statusCode': 200, 'body': json.dumps(status)}

    elif event.get('action') == 'move':
        data_id = event.get('data_id')
        from_tier = event.get('from_tier')
        to_tier = event.get('to_tier')
        data_type = event.get('data_type')

        success = sync_manager.move_data_between_tiers(data_id, from_tier, to_tier, data_type)
        return {
            'statusCode': 200 if success else 500,
            'body': json.dumps({'success': success})
        }

    return {'statusCode': 400, 'body': 'Invalid action'}

if __name__ == "__main__":
    # Local testing
    sync_manager = DataSyncManager()

    # Run sync
    sync_manager.sync_data_across_tiers()

    # Print status
    status = sync_manager.get_sync_status()
    print(json.dumps(status, indent=2))
