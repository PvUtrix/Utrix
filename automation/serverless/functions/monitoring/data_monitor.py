#!/usr/bin/env python3
"""
Multi-Tier Data Monitor
Monitors data sizes, usage patterns, and triggers automated actions
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from supabase import create_client, Client
import requests
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataMonitor:
    def __init__(self):
        self.config = self._load_config()
        self.core_db = self._get_db_client('core')
        self.main_db = self._get_db_client('main')
        self.archive_db = self._get_db_client('archive')

        # Telegram alerting
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), 'multi_tier_config.yaml')
        if not os.path.exists(config_path):
            # Try local config first
            local_config = os.path.join(os.path.dirname(__file__), 'multi_tier_config.local.yaml')
            if os.path.exists(local_config):
                config_path = local_config
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _get_db_client(self, tier: str) -> Client:
        """Get database client for specified tier"""
        tier_config = self.config['database_tiers'][tier]
        url = os.getenv(tier_config['url_env'])
        key = os.getenv(tier_config['key_env'])

        if url and key:
            return create_client(url, key)
        return None

    def monitor_data_sizes(self) -> Dict[str, Any]:
        """Monitor data sizes across all tiers"""
        logger.info("📊 Monitoring data sizes across tiers")

        sizes = {}

        # Monitor each tier
        for tier_name, tier_config in self.config['database_tiers'].items():
            db_client = getattr(self, f"{tier_name}_db")
            if db_client:
                sizes[tier_name] = self._get_tier_sizes(db_client, tier_name)
            else:
                sizes[tier_name] = {'configured': False}

        # Check thresholds and send alerts
        self._check_size_thresholds(sizes)

        return sizes

    def _get_tier_sizes(self, db_client: Client, tier_name: str) -> Dict[str, Any]:
        """Get data sizes for a specific tier"""
        try:
            # Get table sizes (simplified - in production use database-specific queries)
            tables = self._get_tier_tables(tier_name)
            total_size_kb = 0
            table_sizes = {}

            for table in tables:
                try:
                    # Estimate table size
                    count = self._get_table_count(db_client, table)
                    avg_size_kb = 1  # Rough estimate per record
                    table_size_kb = count * avg_size_kb
                    table_sizes[table] = {
                        'count': count,
                        'size_kb': table_size_kb
                    }
                    total_size_kb += table_size_kb
                except Exception as e:
                    logger.error(f"Error getting size for {table}: {e}")
                    table_sizes[table] = {'error': str(e)}

            capacity_mb = self.config['database_tiers'][tier_name]['capacity_mb']
            usage_percent = (total_size_kb / (capacity_mb * 1024)) * 100

            return {
                'configured': True,
                'total_size_kb': total_size_kb,
                'capacity_mb': capacity_mb,
                'usage_percent': round(usage_percent, 2),
                'table_sizes': table_sizes,
                'last_checked': datetime.now().isoformat()
            }

        except Exception as e:
            return {'error': str(e)}

    def _get_tier_tables(self, tier_name: str) -> List[str]:
        """Get tables for a specific tier"""
        data_types = self.config['data_classification'][f"{tier_name}_data_types"]
        table_mapping = {
            'daily_summary': 'daily_summaries',
            'shadow_work_current': 'shadow_work_current',
            'recent_journal': 'journal_entries',
            'active_tasks': 'tasks',
            'current_projects': 'projects',
            'journal_entries': 'journal_entries',
            'shadow_work_history': 'shadow_work_history',
            'completed_projects': 'completed_projects',
            'research_notes': 'research_notes',
            'learning_materials': 'learning_materials',
            'old_projects': 'old_projects',
            'backup_files': 'backup_files',
            'templates': 'templates',
            'contacts': 'contacts'
        }

        return [table_mapping.get(dt, dt) for dt in data_types]

    def _get_table_count(self, db_client: Client, table_name: str) -> int:
        """Get row count for a table"""
        try:
            response = db_client.table(table_name).select('id', count='exact').execute()
            return response.count or 0
        except:
            return 0

    def _check_size_thresholds(self, sizes: Dict[str, Any]):
        """Check size thresholds and send alerts"""
        alerts = []

        for tier_name, size_data in sizes.items():
            if not size_data.get('configured', False):
                continue

            usage_percent = size_data.get('usage_percent', 0)
            capacity_mb = size_data.get('capacity_mb', 0)

            tier_config = self.config['database_tiers'][tier_name]
            warning_threshold = self.config['capacity_management'][f"{tier_name}_tier"]['warning_threshold_percent']
            critical_threshold = self.config['capacity_management'][f"{tier_name}_tier"]['critical_threshold_percent']

            if usage_percent >= critical_threshold:
                alerts.append(f"🚨 CRITICAL: {tier_name} tier at {usage_percent:.1f}% capacity ({capacity_mb}MB)")
            elif usage_percent >= warning_threshold:
                alerts.append(f"⚠️ WARNING: {tier_name} tier at {usage_percent:.1f}% capacity")

        # Send alerts
        for alert in alerts:
            self._send_telegram_alert(alert)
            logger.warning(alert)

    def monitor_sync_status(self) -> Dict[str, Any]:
        """Monitor data synchronization status"""
        logger.info("🔄 Monitoring sync status")

        try:
            # Get sync logs from core database
            response = self.core_db.table('data_sync_log') \
                .select('*') \
                .gte('timestamp', (datetime.now() - timedelta(hours=24)).isoformat()) \
                .execute()

            sync_logs = response.data or []

            # Analyze sync status
            total_syncs = len(sync_logs)
            successful_syncs = len([log for log in sync_logs if 'error' not in log])
            failed_syncs = total_syncs - successful_syncs

            # Group by operation type
            operations = {}
            for log in sync_logs:
                op = log.get('operation', 'unknown')
                operations[op] = operations.get(op, 0) + 1

            status = {
                'total_syncs_24h': total_syncs,
                'successful_syncs': successful_syncs,
                'failed_syncs': failed_syncs,
                'operations': operations,
                'last_sync': sync_logs[0]['timestamp'] if sync_logs else None
            }

            # Check for sync issues
            if failed_syncs > 5:
                self._send_telegram_alert(f"🚨 HIGH SYNC FAILURE RATE: {failed_syncs}/{total_syncs} syncs failed in last 24h")

            return status

        except Exception as e:
            logger.error(f"Error monitoring sync status: {e}")
            return {'error': str(e)}

    def monitor_data_lifecycle(self) -> Dict[str, Any]:
        """Monitor data lifecycle operations"""
        logger.info("🔄 Monitoring data lifecycle")

        try:
            # Get lifecycle logs
            response = self.core_db.table('data_lifecycle_log') \
                .select('*') \
                .gte('timestamp', (datetime.now() - timedelta(hours=24)).isoformat()) \
                .execute()

            lifecycle_logs = response.data or []

            # Analyze lifecycle operations
            operations = {}
            for log in lifecycle_logs:
                op = log.get('operation', 'unknown')
                operations[op] = operations.get(op, 0) + 1

            return {
                'lifecycle_operations_24h': len(lifecycle_logs),
                'operations': operations,
                'last_operation': lifecycle_logs[0]['timestamp'] if lifecycle_logs else None
            }

        except Exception as e:
            logger.error(f"Error monitoring lifecycle: {e}")
            return {'error': str(e)}

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive monitoring report"""
        sizes = self.monitor_data_sizes()
        sync_status = self.monitor_sync_status()
        lifecycle_status = self.monitor_data_lifecycle()

        report = f"""
# 📊 Multi-Tier Database Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## 💾 Database Sizes

"""

        for tier_name, size_data in sizes.items():
            if not size_data.get('configured', False):
                report += f"### {tier_name.upper()} Tier\n❌ Not configured\n"
                continue

            usage_percent = size_data.get('usage_percent', 0)
            total_size_kb = size_data.get('total_size_kb', 0)
            capacity_mb = size_data.get('capacity_mb', 0)

            status_emoji = "🟢" if usage_percent < 70 else "🟡" if usage_percent < 85 else "🔴"

            report += f"""### {tier_name.upper()} Tier {status_emoji}
- **Usage**: {usage_percent:.1f}% ({total_size_kb/1024:.1f}MB / {capacity_mb}MB)
- **Status**: {'Healthy' if usage_percent < 70 else 'Warning' if usage_percent < 85 else 'Critical'}
"""

            # Table breakdown
            table_sizes = size_data.get('table_sizes', {})
            if table_sizes:
                report += "- **Tables**:\n"
                for table, info in table_sizes.items():
                    if 'error' not in info:
                        report += f"  - {table}: {info.get('count', 0)} records ({info.get('size_kb', 0)}KB)\n"
                    else:
                        report += f"  - {table}: Error - {info['error']}\n"

        report += f"""
## 🔄 Sync Status (Last 24h)
- **Total Syncs**: {sync_status.get('total_syncs_24h', 0)}
- **Successful**: {sync_status.get('successful_syncs', 0)}
- **Failed**: {sync_status.get('failed_syncs', 0)}
- **Last Sync**: {sync_status.get('last_sync', 'Never') or 'Never'}
"""

        # Operations breakdown
        operations = sync_status.get('operations', {})
        if operations:
            report += "\n**Operations**:\n"
            for op, count in operations.items():
                report += f"- {op}: {count}\n"

        report += f"""
## 🔄 Lifecycle Operations (Last 24h)
- **Total Operations**: {lifecycle_status.get('lifecycle_operations_24h', 0)}
- **Last Operation**: {lifecycle_status.get('last_operation', 'Never') or 'Never'}
"""

        # Lifecycle operations breakdown
        lc_operations = lifecycle_status.get('operations', {})
        if lc_operations:
            report += "\n**Operations**:\n"
            for op, count in lc_operations.items():
                report += f"- {op}: {count}\n"

        # Recommendations
        report += f"""
## 💡 Recommendations

"""

        # Size-based recommendations
        for tier_name, size_data in sizes.items():
            if size_data.get('configured', False):
                usage_percent = size_data.get('usage_percent', 0)
                if usage_percent > 85:
                    report += f"- ⚠️ **URGENT**: {tier_name} tier is {usage_percent:.1f}% full - consider data migration\n"
                elif usage_percent > 70:
                    report += f"- 📈 **Monitor**: {tier_name} tier at {usage_percent:.1f}% - plan for expansion\n"

        # Sync recommendations
        failed_syncs = sync_status.get('failed_syncs', 0)
        if failed_syncs > 0:
            report += f"- 🔧 **Fix Sync Issues**: {failed_syncs} sync operations failed\n"

        report += f"""
---
*Multi-Tier Data Monitor*
*Free Tier Usage: Keep core database < 500MB*
"""

        return report

    def _send_telegram_alert(self, message: str):
        """Send alert via Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            return

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_notification": False
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Alert sent to Telegram")
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")

def main():
    monitor = DataMonitor()

    import sys
    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == '--sizes':
            sizes = monitor.monitor_data_sizes()
            print(json.dumps(sizes, indent=2))

        elif action == '--sync':
            sync_status = monitor.monitor_sync_status()
            print(json.dumps(sync_status, indent=2))

        elif action == '--lifecycle':
            lifecycle_status = monitor.monitor_data_lifecycle()
            print(json.dumps(lifecycle_status, indent=2))

        elif action == '--alert':
            # Send comprehensive alert
            report = monitor.generate_comprehensive_report()
            monitor._send_telegram_alert(report)
            print("Alert sent!")

        else:
            print("Usage: python3 data_monitor.py [--sizes|--sync|--lifecycle|--alert]")

    else:
        # Generate full report
        report = monitor.generate_comprehensive_report()
        print(report)

        # Send to Telegram if configured
        if monitor.telegram_token and monitor.telegram_chat_id:
            monitor._send_telegram_alert(report)

if __name__ == "__main__":
    main()
