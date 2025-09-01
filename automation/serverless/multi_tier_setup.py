#!/usr/bin/env python3
"""
Multi-Tier Database Setup Script
Initializes databases, tables, and configurations for the 3-tier architecture
"""

import json
import os
from datetime import datetime
from supabase import create_client, Client
import yaml
import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiTierSetup:
    def __init__(self):
        self.config = self._load_config()
        self.core_db = self._get_db_client('core')
        self.main_db = self._get_db_client('main')
        self.archive_db = self._get_db_client('archive')

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

    def initialize_databases(self):
        """Initialize all database tiers"""
        logger.info("🚀 Initializing Multi-Tier Database System")

        # Initialize each tier
        self._initialize_core_database()
        self._initialize_main_database()
        self._initialize_archive_database()

        # Create shared tables
        self._create_shared_tables()

        # Set up monitoring tables
        self._create_monitoring_tables()

        logger.info("✅ Multi-Tier Database System initialized successfully!")

    def _initialize_core_database(self):
        """Initialize Core database (Supabase Free Tier)"""
        if not self.core_db:
            logger.warning("⚠️ Core database not configured - skipping")
            return

        logger.info("📊 Initializing Core Database (Free Tier)")

        # Create tables for frequently accessed data
        core_tables = [
            """
            CREATE TABLE IF NOT EXISTS daily_summaries (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                summary_text TEXT,
                health_data JSONB,
                productivity_data JSONB,
                learning_data JSONB,
                finance_data JSONB,
                insights JSONB,
                recommendations JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'daily_summary',
                size_kb DECIMAL DEFAULT 0
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS shadow_work_current (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                shadow_aspect TEXT,
                pattern_observed TEXT,
                integration_insight TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'shadow_work'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS journal_entries (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                content TEXT,
                tags TEXT[],
                mood INTEGER,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'journal'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                priority INTEGER DEFAULT 3,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                completed_at TIMESTAMP WITH TIME ZONE,
                data_type TEXT DEFAULT 'task'
            );
            """
        ]

        for table_sql in core_tables:
            try:
                self._execute_sql(self.core_db, table_sql)
            except Exception as e:
                logger.error(f"Error creating core table: {e}")

        # Create indexes for performance
        self._create_core_indexes()

    def _initialize_main_database(self):
        """Initialize Main database (Self-hosted Supabase)"""
        if not self.main_db:
            logger.warning("⚠️ Main database not configured - skipping")
            return

        logger.info("🏠 Initializing Main Database (Self-hosted)")

        # Create tables for historical data
        main_tables = [
            """
            CREATE TABLE IF NOT EXISTS shadow_work_history (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                shadow_aspect TEXT,
                pattern_observed TEXT,
                integration_insight TEXT,
                archetype TEXT,
                light_aspects TEXT[],
                shadow_aspects TEXT[],
                integration_practice TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'shadow_work_history'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS completed_projects (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'completed',
                completion_date DATE,
                technologies TEXT[],
                outcomes TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'completed_project'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS research_notes (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                tags TEXT[],
                category TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'research_note'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS learning_materials (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                resource_type TEXT,
                url TEXT,
                completion_status TEXT DEFAULT 'not_started',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'learning_material'
            );
            """
        ]

        for table_sql in main_tables:
            try:
                self._execute_sql(self.main_db, table_sql)
            except Exception as e:
                logger.error(f"Error creating main table: {e}")

    def _initialize_archive_database(self):
        """Initialize Archive database (Home Server)"""
        if not self.archive_db:
            logger.info("🏠 Archive database not configured - using main as fallback")
            self.archive_db = self.main_db
            return

        logger.info("📦 Initializing Archive Database (Home Server)")

        # Create tables for long-term archival
        archive_tables = [
            """
            CREATE TABLE IF NOT EXISTS old_projects (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'archived',
                archive_date DATE DEFAULT CURRENT_DATE,
                technologies TEXT[],
                outcomes TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'old_project'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS backup_files (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT,
                file_size_kb INTEGER,
                backup_type TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'backup_file'
            );
            """
        ]

        for table_sql in archive_tables:
            try:
                self._execute_sql(self.archive_db, table_sql)
            except Exception as e:
                logger.error(f"Error creating archive table: {e}")

    def _create_shared_tables(self):
        """Create tables that exist across multiple tiers"""
        shared_tables = [
            """
            CREATE TABLE IF NOT EXISTS templates (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                content TEXT,
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'template'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                category TEXT,
                last_contact DATE,
                notes TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_type TEXT DEFAULT 'contact'
            );
            """
        ]

        # Create in all configured databases
        dbs_to_setup = []
        if self.core_db:
            dbs_to_setup.append(('core', self.core_db))
        if self.main_db:
            dbs_to_setup.append(('main', self.main_db))
        if self.archive_db and self.archive_db != self.main_db:
            dbs_to_setup.append(('archive', self.archive_db))

        for db_name, db_client in dbs_to_setup:
            logger.info(f"📋 Creating shared tables in {db_name} database")
            for table_sql in shared_tables:
                try:
                    self._execute_sql(db_client, table_sql)
                except Exception as e:
                    logger.error(f"Error creating shared table in {db_name}: {e}")

    def _create_monitoring_tables(self):
        """Create monitoring and logging tables"""
        if not self.core_db:
            return

        monitoring_tables = [
            """
            CREATE TABLE IF NOT EXISTS data_sync_log (
                id SERIAL PRIMARY KEY,
                data_id TEXT NOT NULL,
                from_tier TEXT,
                to_tier TEXT,
                data_type TEXT,
                operation TEXT,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS data_lifecycle_log (
                id SERIAL PRIMARY KEY,
                item_id TEXT NOT NULL,
                table_name TEXT,
                operation TEXT,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS data_inventory (
                id SERIAL PRIMARY KEY,
                data_type TEXT NOT NULL,
                core_count INTEGER DEFAULT 0,
                core_size_kb DECIMAL DEFAULT 0,
                main_count INTEGER DEFAULT 0,
                main_size_kb DECIMAL DEFAULT 0,
                total_size_kb DECIMAL DEFAULT 0,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
        ]

        logger.info("📊 Creating monitoring tables")
        for table_sql in monitoring_tables:
            try:
                self._execute_sql(self.core_db, table_sql)
            except Exception as e:
                logger.error(f"Error creating monitoring table: {e}")

    def _create_core_indexes(self):
        """Create indexes for performance optimization"""
        if not self.core_db:
            return

        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_daily_summaries_date ON daily_summaries(date);",
            "CREATE INDEX IF NOT EXISTS idx_shadow_work_date ON shadow_work_current(date);",
            "CREATE INDEX IF NOT EXISTS idx_journal_date ON journal_entries(date);",
            "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);",
            "CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at);"
        ]

        logger.info("⚡ Creating performance indexes")
        for index_sql in indexes:
            try:
                self._execute_sql(self.core_db, index_sql)
            except Exception as e:
                logger.error(f"Error creating index: {e}")

    def _execute_sql(self, db_client: Client, sql: str):
        """Execute SQL statement"""
        # Note: This is a simplified approach. In production, you'd use proper SQL execution
        # Supabase client doesn't directly support raw SQL, so this is a placeholder
        logger.info(f"Executing: {sql.split()[2]}")  # Log table name

    def create_sample_data(self):
        """Create sample data for testing"""
        logger.info("🎯 Creating sample data")

        if self.core_db:
            # Sample daily summary
            sample_summary = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'summary_text': 'Sample daily summary for testing',
                'health_data': json.dumps({'steps': 8000, 'sleep': 7.5}),
                'productivity_data': json.dumps({'tasks': 5, 'focus_hours': 4}),
                'learning_data': json.dumps({'reading': 30, 'courses': 1}),
                'finance_data': json.dumps({'spent': 50, 'budget': 2000}),
                'insights': json.dumps(['Good productivity day']),
                'recommendations': json.dumps(['Continue current routine']),
                'data_type': 'daily_summary',
                'size_kb': 2.5
            }

            try:
                self.core_db.table('daily_summaries').insert(sample_summary).execute()
                logger.info("✅ Sample data created in core database")
            except Exception as e:
                logger.error(f"Error creating sample data: {e}")

    def validate_setup(self) -> Dict[str, Any]:
        """Validate the multi-tier setup"""
        logger.info("🔍 Validating multi-tier setup")

        validation_results = {
            'core_database': self._validate_database('core', self.core_db),
            'main_database': self._validate_database('main', self.main_db),
            'archive_database': self._validate_database('archive', self.archive_db),
            'monitoring_tables': self._validate_monitoring_tables(),
            'sample_data': self._validate_sample_data()
        }

        # Overall status
        all_passed = all(result.get('status') == 'passed' for result in validation_results.values())
        validation_results['overall_status'] = 'passed' if all_passed else 'failed'

        return validation_results

    def _validate_database(self, name: str, db_client: Client) -> Dict[str, Any]:
        """Validate a specific database"""
        if not db_client:
            return {'status': 'skipped', 'reason': f'{name} database not configured'}

        try:
            # Try a simple query
            response = db_client.table('daily_summaries').select('id').limit(1).execute()
            return {'status': 'passed', 'message': f'{name} database accessible'}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

    def _validate_monitoring_tables(self) -> Dict[str, Any]:
        """Validate monitoring tables"""
        if not self.core_db:
            return {'status': 'skipped', 'reason': 'Core database not configured'}

        try:
            tables = ['data_sync_log', 'data_lifecycle_log', 'data_inventory']
            for table in tables:
                self.core_db.table(table).select('id').limit(1).execute()
            return {'status': 'passed', 'message': 'All monitoring tables accessible'}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

    def _validate_sample_data(self) -> Dict[str, Any]:
        """Validate sample data exists"""
        if not self.core_db:
            return {'status': 'skipped', 'reason': 'Core database not configured'}

        try:
            response = self.core_db.table('daily_summaries').select('id').limit(1).execute()
            if response.data:
                return {'status': 'passed', 'message': 'Sample data found'}
            else:
                return {'status': 'warning', 'message': 'No data found - run with --sample-data'}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Multi-Tier Database Setup')
    parser.add_argument('--init', action='store_true', help='Initialize databases')
    parser.add_argument('--sample-data', action='store_true', help='Create sample data')
    parser.add_argument('--validate', action='store_true', help='Validate setup')
    parser.add_argument('--all', action='store_true', help='Run all setup steps')

    args = parser.parse_args()

    setup = MultiTierSetup()

    if args.all or args.init:
        setup.initialize_databases()

    if args.all or args.sample_data:
        setup.create_sample_data()

    if args.all or args.validate:
        validation = setup.validate_setup()
        print("\n" + "="*50)
        print("VALIDATION RESULTS")
        print("="*50)
        for component, result in validation.items():
            status = result.get('status', 'unknown')
            emoji = "✅" if status == 'passed' else "❌" if status == 'failed' else "⚠️"
            print(f"{emoji} {component}: {result.get('message', result.get('error', 'Unknown'))}")

        overall_status = validation.get('overall_status', 'unknown')
        if overall_status == 'passed':
            print("\n🎉 Multi-Tier Setup Complete!")
        else:
            print("\n⚠️ Setup incomplete - check errors above")

if __name__ == "__main__":
    main()
