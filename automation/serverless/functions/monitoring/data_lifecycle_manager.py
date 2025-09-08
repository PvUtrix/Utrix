#!/usr/bin/env python3
"""
Data Lifecycle Manager
Manages data lifecycle across multiple tiers with automatic archiving
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from supabase import create_client, Client
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLifecycleManager:
    def __init__(self):
        self.core_db = create_client(
            os.getenv('CORE_SUPABASE_URL'),
            os.getenv('CORE_SUPABASE_ANON_KEY')
        )
        self.main_db = create_client(
            os.getenv('MAIN_SUPABASE_URL'),
            os.getenv('MAIN_SUPABASE_ANON_KEY')
        )
        self.archive_db = create_client(
            os.getenv('ARCHIVE_SUPABASE_URL', ''),
            os.getenv('ARCHIVE_SUPABASE_ANON_KEY', '')
        ) if os.getenv('ARCHIVE_SUPABASE_URL') else None

        # Load lifecycle policies from config
        self.policies = self._load_lifecycle_policies()

    def _load_lifecycle_policies(self) -> Dict[str, Dict[str, int]]:
        """Load lifecycle policies from config file"""
        config_path = os.path.join(os.path.dirname(__file__), 'multi_tier_config.yaml')
        if not os.path.exists(config_path):
            # Try local config first
            local_config = os.path.join(os.path.dirname(__file__), 'multi_tier_config.local.yaml')
            if os.path.exists(local_config):
                config_path = local_config

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            policies = {}
            for data_type, policy in config['lifecycle_policies'].items():
                policies[data_type] = {
                    'core_retention': policy['core_retention_days'],
                    'main_retention': policy['main_retention_days'],
                    'archive_after': policy['archive_after_days']
                }
            return policies
        else:
            # Fallback to hardcoded policies
            return {
                'daily_summary': {'core_retention': 30, 'main_retention': 365, 'archive_after': 1095},
                'shadow_work': {'core_retention': 90, 'main_retention': 730, 'archive_after': 1825},
                'journal': {'core_retention': 7, 'main_retention': 365, 'archive_after': 1825},
                'projects': {'core_retention': 90, 'main_retention': 1095, 'archive_after': 3650},
                'research': {'core_retention': 30, 'main_retention': 730, 'archive_after': 1825},
                'contacts': {'core_retention': 365, 'main_retention': 1825, 'archive_after': -1},
                'templates': {'core_retention': 90, 'main_retention': 1825, 'archive_after': -1}
            }

    def process_data_lifecycle(self):
        """Process data lifecycle management across all tiers"""
        logger.info("🔄 Processing data lifecycle management")

        # Process each data type
        for data_type, policy in self.policies.items():
            self._process_data_type_lifecycle(data_type, policy)

        # Clean up old sync logs
        self._cleanup_sync_logs()

        # Update data inventory
        self._update_data_inventory()

        logger.info("✅ Data lifecycle processing complete")

    def _process_data_type_lifecycle(self, data_type: str, policy: Dict[str, int]):
        """Process lifecycle for a specific data type"""
        table_name = self._get_table_name(data_type)
        now = datetime.now()

        # Move from Core to Main
        if policy['core_retention'] > 0:
            core_cutoff = now - timedelta(days=policy['core_retention'])
            self._move_data_between_tiers(
                self.core_db, self.main_db,
                table_name, core_cutoff,
                f"core_to_main_{data_type}"
            )

        # Move from Main to Archive
        if policy['main_retention'] > 0 and self.archive_db:
            main_cutoff = now - timedelta(days=policy['main_retention'])
            self._move_data_between_tiers(
                self.main_db, self.archive_db,
                table_name, main_cutoff,
                f"main_to_archive_{data_type}"
            )

        # Delete from Archive (if retention is set)
        if policy['archive_after'] > 0 and self.archive_db:
            archive_cutoff = now - timedelta(days=policy['archive_after'])
            self._delete_old_data(self.archive_db, table_name, archive_cutoff)

    def _move_data_between_tiers(self, from_db: Client, to_db: Client,
                                table_name: str, cutoff_date: datetime, operation_id: str):
        """Move data between database tiers"""
        try:
            # Get data older than cutoff
            response = from_db.table(table_name) \
                .select('*') \
                .lt('created_at', cutoff_date.isoformat()) \
                .limit(50) \
                .execute()

            if not response.data:
                return

            moved_count = 0
            for item in response.data:
                try:
                    # Insert into destination (without id to avoid conflicts)
                    insert_data = {k: v for k, v in item.items() if k != 'id'}
                    to_db.table(table_name).insert(insert_data).execute()

                    # Delete from source
                    from_db.table(table_name).delete().eq('id', item['id']).execute()

                    moved_count += 1

                    # Log the move
                    self._log_lifecycle_operation(
                        item['id'], table_name, operation_id,
                        from_db, to_db
                    )

                except Exception as e:
                    logger.error(f"Error moving item {item['id']}: {e}")
                    continue

            if moved_count > 0:
                logger.info(f"✅ Moved {moved_count} {table_name} items")

        except Exception as e:
            logger.error(f"Error in _move_data_between_tiers: {e}")

    def _delete_old_data(self, db: Client, table_name: str, cutoff_date: datetime):
        """Delete old data from a tier"""
        try:
            response = db.table(table_name) \
                .delete() \
                .lt('created_at', cutoff_date.isoformat()) \
                .execute()

            deleted_count = len(response.data) if response.data else 0
            if deleted_count > 0:
                logger.info(f"🗑️ Deleted {deleted_count} old {table_name} items")

        except Exception as e:
            logger.error(f"Error deleting old data from {table_name}: {e}")

    def _cleanup_sync_logs(self):
        """Clean up old synchronization logs"""
        try:
            cutoff_date = datetime.now() - timedelta(days=90)
            self.core_db.table('data_sync_log') \
                .delete() \
                .lt('timestamp', cutoff_date.isoformat()) \
                .execute()
            logger.info("🧹 Cleaned up old sync logs")
        except Exception as e:
            logger.error(f"Error cleaning sync logs: {e}")

    def _update_data_inventory(self):
        """Update data inventory with current sizes"""
        try:
            inventory = {}

            # Get sizes for each data type
            for data_type in self.policies.keys():
                table_name = self._get_table_name(data_type)

                # Core database
                core_count = self._get_table_count(self.core_db, table_name)
                core_size = self._estimate_table_size(self.core_db, table_name)

                # Main database
                main_count = self._get_table_count(self.main_db, table_name)
                main_size = self._estimate_table_size(self.main_db, table_name)

                inventory[data_type] = {
                    'core': {'count': core_count, 'size_kb': core_size},
                    'main': {'count': main_count, 'size_kb': main_size},
                    'total_size_kb': core_size + main_size,
                    'updated_at': datetime.now().isoformat()
                }

            # Store inventory in core database
            self.core_db.table('data_inventory').upsert(inventory).execute()
            logger.info("📊 Updated data inventory")

        except Exception as e:
            logger.error(f"Error updating data inventory: {e}")

    def _get_table_count(self, db: Client, table_name: str) -> int:
        """Get row count for a table"""
        try:
            response = db.table(table_name).select('id', count='exact').execute()
            return response.count or 0
        except:
            return 0

    def _estimate_table_size(self, db: Client, table_name: str) -> int:
        """Estimate table size in KB (simplified)"""
        try:
            # This is a rough estimation - in production you'd use database-specific size queries
            count = self._get_table_count(db, table_name)
            # Assume average 1KB per record (adjust based on your data)
            return count * 1
        except:
            return 0

    def _get_table_name(self, data_type: str) -> str:
        """Map data type to table name"""
        mapping = {
            'daily_summary': 'daily_summaries',
            'shadow_work': 'shadow_work_data',
            'journal': 'journal_entries',
            'projects': 'projects',
            'research': 'research_notes',
            'contacts': 'contacts',
            'templates': 'templates'
        }
        return mapping.get(data_type, data_type)

    def _log_lifecycle_operation(self, item_id: str, table_name: str,
                                operation: str, from_db: Client, to_db: Client):
        """Log lifecycle operations"""
        try:
            log_entry = {
                'item_id': item_id,
                'table_name': table_name,
                'operation': operation,
                'timestamp': datetime.now().isoformat()
            }
            self.core_db.table('data_lifecycle_log').insert(log_entry).execute()
        except Exception as e:
            logger.error(f"Error logging lifecycle operation: {e}")

    def get_lifecycle_status(self) -> Dict[str, Any]:
        """Get lifecycle management status"""
        status = {}

        try:
            # Get data inventory
            inventory_response = self.core_db.table('data_inventory').select('*').execute()
            inventory = {item['data_type']: item for item in inventory_response.data}

            # Calculate totals
            total_core_size = sum(item.get('core', {}).get('size_kb', 0) for item in inventory.values())
            total_main_size = sum(item.get('main', {}).get('size_kb', 0) for item in inventory.values())

            status = {
                'inventory': inventory,
                'totals': {
                    'core_size_kb': total_core_size,
                    'main_size_kb': total_main_size,
                    'total_size_kb': total_core_size + total_main_size,
                    'core_usage_percent': (total_core_size / (500 * 1024)) * 100,  # 500MB limit
                },
                'policies': self.policies,
                'last_updated': datetime.now().isoformat()
            }

        except Exception as e:
            status = {'error': str(e)}

        return status

def lambda_handler(event, context):
    """AWS Lambda handler for data lifecycle management"""
    manager = DataLifecycleManager()

    if event.get('action') == 'process':
        manager.process_data_lifecycle()
        return {'statusCode': 200, 'body': 'Lifecycle processing complete'}

    elif event.get('action') == 'status':
        status = manager.get_lifecycle_status()
        return {'statusCode': 200, 'body': json.dumps(status)}

    return {'statusCode': 400, 'body': 'Invalid action'}

if __name__ == "__main__":
    # Local testing
    manager = DataLifecycleManager()
    manager.process_data_lifecycle()

    # Print status
    status = manager.get_lifecycle_status()
    print(json.dumps(status, indent=2))
