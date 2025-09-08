#!/usr/bin/env python3
"""
Comprehensive Monitoring and Alerting System for Multi-Tier Serverless Architecture
Monitors quota usage, costs, performance, and system health across all providers.
Provides intelligent alerting, reporting, and automated responses.
"""

import json
import os
import logging
import asyncio
import aiohttp
import smtplib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import time
import sqlite3
from collections import defaultdict, deque
import statistics
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utilities'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'daily'))

from multi_tier_quota_manager import MultiTierQuotaManager, ProviderType, QuotaUsage
from daily_projection_calculator import DailyProjectionCalculator, ProjectionResult
from intelligent_load_balancer import IntelligentLoadBalancer, ExecutionResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertType(Enum):
    QUOTA_USAGE = "quota_usage"
    COST_THRESHOLD = "cost_threshold"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    PROVIDER_UNHEALTHY = "provider_unhealthy"
    PROJECTION_ACCURACY = "projection_accuracy"
    SYSTEM_ERROR = "system_error"
    SECURITY_ISSUE = "security_issue"

class NotificationChannel(Enum):
    TELEGRAM = "telegram"
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    LOG = "log"

@dataclass
class Alert:
    """Alert data structure"""
    id: str
    type: AlertType
    level: AlertLevel
    title: str
    message: str
    provider: Optional[ProviderType] = None
    metric_name: Optional[str] = None
    current_value: Optional[float] = None
    threshold_value: Optional[float] = None
    timestamp: datetime = None
    acknowledged: bool = False
    resolved: bool = False
    resolution_notes: str = ""

@dataclass
class MetricData:
    """Metric data point"""
    name: str
    value: float
    unit: str
    provider: Optional[ProviderType] = None
    timestamp: datetime = None
    tags: Dict[str, str] = None

@dataclass
class HealthStatus:
    """System health status"""
    overall_health: str  # healthy, degraded, critical
    provider_health: Dict[ProviderType, str]
    quota_health: Dict[ProviderType, str]
    cost_health: str
    performance_health: str
    last_updated: datetime
    issues: List[str]

class ComprehensiveMonitor:
    """Main monitoring system class"""
    
    def __init__(self, config_path: str = None, db_path: str = None):
        self.config = self._load_config(config_path)
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'monitoring_data.db')
        
        # Initialize components
        self.quota_manager = MultiTierQuotaManager(config_path)
        self.projection_calculator = DailyProjectionCalculator(config_path)
        self.load_balancer = IntelligentLoadBalancer(config_path)
        
        # Initialize database
        self._init_database()
        
        # Monitoring state
        self.metrics_history = defaultdict(list)
        self.active_alerts = {}
        self.alert_history = []
        self.health_status = None
        
        # Background monitoring
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Load existing data
        self._load_alert_history()
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration"""
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), 'monitoring_config.yaml')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'monitoring': {
                'enabled': True,
                'interval_seconds': 300,  # 5 minutes
                'metrics_retention_days': 30,
                'alert_retention_days': 90
            },
            'alerts': {
                'quota_usage': {
                    'warning_threshold': 80,
                    'critical_threshold': 95,
                    'enabled': True
                },
                'cost_threshold': {
                    'warning_threshold': 0.01,
                    'critical_threshold': 0.05,
                    'enabled': True
                },
                'performance': {
                    'slow_response_threshold_ms': 10000,
                    'high_error_rate_threshold': 0.1,
                    'enabled': True
                },
                'provider_health': {
                    'unhealthy_threshold_minutes': 5,
                    'enabled': True
                }
            },
            'notifications': {
                'telegram': {
                    'enabled': True,
                    'bot_token_env': 'TELEGRAM_BOT_TOKEN',
                    'chat_id_env': 'TELEGRAM_CHAT_ID'
                },
                'email': {
                    'enabled': False,
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'username_env': 'EMAIL_USERNAME',
                    'password_env': 'EMAIL_PASSWORD',
                    'to_addresses': []
                }
            },
            'reporting': {
                'daily_reports': True,
                'weekly_reports': True,
                'monthly_reports': True,
                'report_retention_days': 365
            }
        }
    
    def _init_database(self):
        """Initialize SQLite database for monitoring data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                provider TEXT,
                timestamp DATETIME NOT NULL,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                level TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                provider TEXT,
                metric_name TEXT,
                current_value REAL,
                threshold_value REAL,
                timestamp DATETIME NOT NULL,
                acknowledged BOOLEAN DEFAULT FALSE,
                resolved BOOLEAN DEFAULT FALSE,
                resolution_notes TEXT DEFAULT '',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                overall_health TEXT NOT NULL,
                provider_health TEXT NOT NULL,
                quota_health TEXT NOT NULL,
                cost_health TEXT NOT NULL,
                performance_health TEXT NOT NULL,
                issues TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL,
                report_data TEXT NOT NULL,
                period_start DATETIME NOT NULL,
                period_end DATETIME NOT NULL,
                generated_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_health_timestamp ON health_status(timestamp)')
        
        conn.commit()
        conn.close()
    
    def _load_alert_history(self):
        """Load alert history from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Load active alerts
        cursor.execute('''
            SELECT id, type, level, title, message, provider, metric_name,
                   current_value, threshold_value, timestamp, acknowledged, resolved, resolution_notes
            FROM alerts
            WHERE resolved = FALSE
        ''')
        
        for row in cursor.fetchall():
            alert = Alert(
                id=row[0],
                type=AlertType(row[1]),
                level=AlertLevel(row[2]),
                title=row[3],
                message=row[4],
                provider=ProviderType(row[5]) if row[5] else None,
                metric_name=row[6],
                current_value=row[7],
                threshold_value=row[8],
                timestamp=datetime.fromisoformat(row[9]),
                acknowledged=bool(row[10]),
                resolved=bool(row[11]),
                resolution_notes=row[12]
            )
            self.active_alerts[alert.id] = alert
        
        conn.close()
    
    def start_monitoring(self):
        """Start background monitoring"""
        if self.monitoring_active:
            logger.warning("Monitoring is already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("Comprehensive monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10)
        logger.info("Comprehensive monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect metrics
                self._collect_metrics()
                
                # Check for alerts
                self._check_alerts()
                
                # Update health status
                self._update_health_status()
                
                # Clean up old data
                self._cleanup_old_data()
                
                # Wait for next interval
                time.sleep(self.config['monitoring']['interval_seconds'])
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _collect_metrics(self):
        """Collect metrics from all components"""
        timestamp = datetime.now()
        
        try:
            # Collect quota metrics
            current_usage = self.quota_manager.get_current_usage()
            for provider, usage in current_usage.items():
                # Quota usage percentage
                limits = self.quota_manager.quota_limits[provider]
                usage_percent = (usage.executions_this_month / limits.monthly_executions) * 100
                
                self._record_metric(
                    name="quota_usage_percent",
                    value=usage_percent,
                    unit="percent",
                    provider=provider,
                    timestamp=timestamp,
                    tags={"metric_type": "quota"}
                )
                
                # Cost metrics
                self._record_metric(
                    name="monthly_cost",
                    value=usage.cost_this_month,
                    unit="USD",
                    provider=provider,
                    timestamp=timestamp,
                    tags={"metric_type": "cost"}
                )
                
                # Execution metrics
                self._record_metric(
                    name="monthly_executions",
                    value=usage.executions_this_month,
                    unit="count",
                    provider=provider,
                    timestamp=timestamp,
                    tags={"metric_type": "execution"}
                )
            
            # Collect projection metrics
            projections = self.projection_calculator.calculate_all_projections()
            for provider, projection in projections.items():
                self._record_metric(
                    name="projected_monthly_executions",
                    value=projection.projected_monthly_executions,
                    unit="count",
                    provider=provider,
                    timestamp=timestamp,
                    tags={"metric_type": "projection"}
                )
                
                self._record_metric(
                    name="projection_confidence",
                    value=projection.confidence_level,
                    unit="ratio",
                    provider=provider,
                    timestamp=timestamp,
                    tags={"metric_type": "projection"}
                )
            
            # Collect load balancer metrics
            lb_status = self.load_balancer.get_load_balancer_status()
            
            self._record_metric(
                name="overall_success_rate",
                value=lb_status['recent_performance']['success_rate'],
                unit="ratio",
                timestamp=timestamp,
                tags={"metric_type": "performance"}
            )
            
            self._record_metric(
                name="average_execution_time",
                value=lb_status['recent_performance']['average_execution_time_ms'],
                unit="milliseconds",
                timestamp=timestamp,
                tags={"metric_type": "performance"}
            )
            
            self._record_metric(
                name="total_cost_estimate",
                value=lb_status['recent_performance']['total_cost_estimate'],
                unit="USD",
                timestamp=timestamp,
                tags={"metric_type": "cost"}
            )
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
    
    def _record_metric(self, name: str, value: float, unit: str, 
                      provider: ProviderType = None, timestamp: datetime = None,
                      tags: Dict[str, str] = None):
        """Record a metric data point"""
        if timestamp is None:
            timestamp = datetime.now()
        
        metric = MetricData(
            name=name,
            value=value,
            unit=unit,
            provider=provider,
            timestamp=timestamp,
            tags=tags or {}
        )
        
        # Add to memory cache
        self.metrics_history[name].append(metric)
        
        # Keep only recent data in memory
        retention_days = self.config['monitoring']['metrics_retention_days']
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        self.metrics_history[name] = [
            m for m in self.metrics_history[name] if m.timestamp > cutoff_date
        ]
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metrics (name, value, unit, provider, timestamp, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            name, value, unit, 
            provider.value if provider else None,
            timestamp.isoformat(),
            json.dumps(tags) if tags else None
        ))
        
        conn.commit()
        conn.close()
    
    def _check_alerts(self):
        """Check for alert conditions"""
        try:
            # Check quota usage alerts
            self._check_quota_alerts()
            
            # Check cost alerts
            self._check_cost_alerts()
            
            # Check performance alerts
            self._check_performance_alerts()
            
            # Check provider health alerts
            self._check_provider_health_alerts()
            
            # Check projection accuracy alerts
            self._check_projection_alerts()
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    def _check_quota_alerts(self):
        """Check quota usage alerts"""
        if not self.config['alerts']['quota_usage']['enabled']:
            return
        
        current_usage = self.quota_manager.get_current_usage()
        warning_threshold = self.config['alerts']['quota_usage']['warning_threshold']
        critical_threshold = self.config['alerts']['quota_usage']['critical_threshold']
        
        for provider, usage in current_usage.items():
            limits = self.quota_manager.quota_limits[provider]
            usage_percent = (usage.executions_this_month / limits.monthly_executions) * 100
            
            alert_id = f"quota_usage_{provider.value}"
            
            if usage_percent >= critical_threshold:
                if alert_id not in self.active_alerts or self.active_alerts[alert_id].level != AlertLevel.CRITICAL:
                    self._create_alert(
                        alert_id=alert_id,
                        alert_type=AlertType.QUOTA_USAGE,
                        level=AlertLevel.CRITICAL,
                        title=f"Critical Quota Usage - {provider.value}",
                        message=f"Quota usage is at {usage_percent:.1f}% (critical threshold: {critical_threshold}%)",
                        provider=provider,
                        metric_name="quota_usage_percent",
                        current_value=usage_percent,
                        threshold_value=critical_threshold
                    )
            elif usage_percent >= warning_threshold:
                if alert_id not in self.active_alerts or self.active_alerts[alert_id].level != AlertLevel.WARNING:
                    self._create_alert(
                        alert_id=alert_id,
                        alert_type=AlertType.QUOTA_USAGE,
                        level=AlertLevel.WARNING,
                        title=f"High Quota Usage - {provider.value}",
                        message=f"Quota usage is at {usage_percent:.1f}% (warning threshold: {warning_threshold}%)",
                        provider=provider,
                        metric_name="quota_usage_percent",
                        current_value=usage_percent,
                        threshold_value=warning_threshold
                    )
            else:
                # Resolve existing alert if usage is below threshold
                if alert_id in self.active_alerts:
                    self._resolve_alert(alert_id, "Quota usage returned to normal levels")
    
    def _check_cost_alerts(self):
        """Check cost threshold alerts"""
        if not self.config['alerts']['cost_threshold']['enabled']:
            return
        
        current_usage = self.quota_manager.get_current_usage()
        warning_threshold = self.config['alerts']['cost_threshold']['warning_threshold']
        critical_threshold = self.config['alerts']['cost_threshold']['critical_threshold']
        
        total_cost = sum(usage.cost_this_month for usage in current_usage.values())
        
        alert_id = "cost_threshold_total"
        
        if total_cost >= critical_threshold:
            if alert_id not in self.active_alerts or self.active_alerts[alert_id].level != AlertLevel.CRITICAL:
                self._create_alert(
                    alert_id=alert_id,
                    alert_type=AlertType.COST_THRESHOLD,
                    level=AlertLevel.CRITICAL,
                    title="Critical Cost Threshold Exceeded",
                    message=f"Total monthly cost is ${total_cost:.4f} (critical threshold: ${critical_threshold:.4f})",
                    metric_name="total_monthly_cost",
                    current_value=total_cost,
                    threshold_value=critical_threshold
                )
        elif total_cost >= warning_threshold:
            if alert_id not in self.active_alerts or self.active_alerts[alert_id].level != AlertLevel.WARNING:
                self._create_alert(
                    alert_id=alert_id,
                    alert_type=AlertType.COST_THRESHOLD,
                    level=AlertLevel.WARNING,
                    title="Cost Warning Threshold Exceeded",
                    message=f"Total monthly cost is ${total_cost:.4f} (warning threshold: ${warning_threshold:.4f})",
                    metric_name="total_monthly_cost",
                    current_value=total_cost,
                    threshold_value=warning_threshold
                )
        else:
            if alert_id in self.active_alerts:
                self._resolve_alert(alert_id, "Cost returned to normal levels")
    
    def _check_performance_alerts(self):
        """Check performance degradation alerts"""
        if not self.config['alerts']['performance']['enabled']:
            return
        
        lb_status = self.load_balancer.get_load_balancer_status()
        recent_performance = lb_status['recent_performance']
        
        # Check response time
        avg_response_time = recent_performance['average_execution_time_ms']
        slow_threshold = self.config['alerts']['performance']['slow_response_threshold_ms']
        
        if avg_response_time > slow_threshold:
            alert_id = "performance_slow_response"
            if alert_id not in self.active_alerts:
                self._create_alert(
                    alert_id=alert_id,
                    alert_type=AlertType.PERFORMANCE_DEGRADATION,
                    level=AlertLevel.WARNING,
                    title="Slow Response Times Detected",
                    message=f"Average response time is {avg_response_time:.0f}ms (threshold: {slow_threshold}ms)",
                    metric_name="average_execution_time",
                    current_value=avg_response_time,
                    threshold_value=slow_threshold
                )
        else:
            if "performance_slow_response" in self.active_alerts:
                self._resolve_alert("performance_slow_response", "Response times returned to normal")
        
        # Check error rate
        success_rate = recent_performance['success_rate']
        error_rate = 1 - success_rate
        error_threshold = self.config['alerts']['performance']['high_error_rate_threshold']
        
        if error_rate > error_threshold:
            alert_id = "performance_high_error_rate"
            if alert_id not in self.active_alerts:
                self._create_alert(
                    alert_id=alert_id,
                    alert_type=AlertType.PERFORMANCE_DEGRADATION,
                    level=AlertLevel.WARNING,
                    title="High Error Rate Detected",
                    message=f"Error rate is {error_rate:.1%} (threshold: {error_threshold:.1%})",
                    metric_name="error_rate",
                    current_value=error_rate,
                    threshold_value=error_threshold
                )
        else:
            if "performance_high_error_rate" in self.active_alerts:
                self._resolve_alert("performance_high_error_rate", "Error rate returned to normal")
    
    def _check_provider_health_alerts(self):
        """Check provider health alerts"""
        if not self.config['alerts']['provider_health']['enabled']:
            return
        
        lb_status = self.load_balancer.get_load_balancer_status()
        provider_health = lb_status['provider_health']
        
        for provider_name, health in provider_health.items():
            if not health['is_healthy']:
                alert_id = f"provider_unhealthy_{provider_name}"
                if alert_id not in self.active_alerts:
                    self._create_alert(
                        alert_id=alert_id,
                        alert_type=AlertType.PROVIDER_UNHEALTHY,
                        level=AlertLevel.CRITICAL,
                        title=f"Provider Unhealthy - {provider_name}",
                        message=f"Provider {provider_name} is marked as unhealthy with {health['consecutive_failures']} consecutive failures",
                        provider=ProviderType(provider_name),
                        metric_name="provider_health",
                        current_value=0,  # 0 = unhealthy
                        threshold_value=1  # 1 = healthy
                    )
            else:
                alert_id = f"provider_unhealthy_{provider_name}"
                if alert_id in self.active_alerts:
                    self._resolve_alert(alert_id, f"Provider {provider_name} is healthy again")
    
    def _check_projection_alerts(self):
        """Check projection accuracy alerts"""
        projections = self.projection_calculator.calculate_all_projections()
        
        for provider, projection in projections.items():
            if projection.confidence_level < 0.5:
                alert_id = f"projection_low_confidence_{provider.value}"
                if alert_id not in self.active_alerts:
                    self._create_alert(
                        alert_id=alert_id,
                        alert_type=AlertType.PROJECTION_ACCURACY,
                        level=AlertLevel.WARNING,
                        title=f"Low Projection Confidence - {provider.value}",
                        message=f"Projection confidence is {projection.confidence_level:.2f} (threshold: 0.5)",
                        provider=provider,
                        metric_name="projection_confidence",
                        current_value=projection.confidence_level,
                        threshold_value=0.5
                    )
            else:
                alert_id = f"projection_low_confidence_{provider.value}"
                if alert_id in self.active_alerts:
                    self._resolve_alert(alert_id, f"Projection confidence improved to {projection.confidence_level:.2f}")
    
    def _create_alert(self, alert_id: str, alert_type: AlertType, level: AlertLevel,
                     title: str, message: str, provider: ProviderType = None,
                     metric_name: str = None, current_value: float = None,
                     threshold_value: float = None):
        """Create a new alert"""
        alert = Alert(
            id=alert_id,
            type=alert_type,
            level=level,
            title=title,
            message=message,
            provider=provider,
            metric_name=metric_name,
            current_value=current_value,
            threshold_value=threshold_value,
            timestamp=datetime.now()
        )
        
        # Add to active alerts
        self.active_alerts[alert_id] = alert
        
        # Save to database
        self._save_alert(alert)
        
        # Send notifications
        self._send_alert_notifications(alert)
        
        logger.warning(f"Alert created: {alert.title} - {alert.message}")
    
    def _resolve_alert(self, alert_id: str, resolution_notes: str):
        """Resolve an existing alert"""
        if alert_id not in self.active_alerts:
            return
        
        alert = self.active_alerts[alert_id]
        alert.resolved = True
        alert.resolution_notes = resolution_notes
        
        # Remove from active alerts
        del self.active_alerts[alert_id]
        
        # Update in database
        self._update_alert(alert)
        
        # Send resolution notification
        self._send_alert_notifications(alert, is_resolution=True)
        
        logger.info(f"Alert resolved: {alert.title} - {resolution_notes}")
    
    def _save_alert(self, alert: Alert):
        """Save alert to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO alerts 
            (id, type, level, title, message, provider, metric_name,
             current_value, threshold_value, timestamp, acknowledged, resolved, resolution_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert.id, alert.type.value, alert.level.value, alert.title, alert.message,
            alert.provider.value if alert.provider else None,
            alert.metric_name, alert.current_value, alert.threshold_value,
            alert.timestamp.isoformat(), alert.acknowledged, alert.resolved, alert.resolution_notes
        ))
        
        conn.commit()
        conn.close()
    
    def _update_alert(self, alert: Alert):
        """Update alert in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alerts 
            SET acknowledged = ?, resolved = ?, resolution_notes = ?
            WHERE id = ?
        ''', (alert.acknowledged, alert.resolved, alert.resolution_notes, alert.id))
        
        conn.commit()
        conn.close()
    
    def _send_alert_notifications(self, alert: Alert, is_resolution: bool = False):
        """Send alert notifications through configured channels"""
        try:
            # Prepare notification message
            if is_resolution:
                message = f"✅ RESOLVED: {alert.title}\n{alert.resolution_notes}"
            else:
                message = f"🚨 {alert.level.value.upper()}: {alert.title}\n{alert.message}"
                if alert.provider:
                    message += f"\nProvider: {alert.provider.value}"
                if alert.current_value is not None:
                    message += f"\nCurrent Value: {alert.current_value}"
                if alert.threshold_value is not None:
                    message += f"\nThreshold: {alert.threshold_value}"
            
            # Send Telegram notification
            if self.config['notifications']['telegram']['enabled']:
                self._send_telegram_notification(message)
            
            # Send Email notification
            if self.config['notifications']['email']['enabled']:
                self._send_email_notification(alert.title, message)
            
        except Exception as e:
            logger.error(f"Error sending alert notifications: {e}")
    
    def _send_telegram_notification(self, message: str):
        """Send Telegram notification"""
        try:
            bot_token = os.getenv(self.config['notifications']['telegram']['bot_token_env'])
            chat_id = os.getenv(self.config['notifications']['telegram']['chat_id_env'])
            
            if not bot_token or not chat_id:
                logger.warning("Telegram credentials not configured")
                return
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            import requests
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
    
    def _send_email_notification(self, subject: str, message: str):
        """Send email notification"""
        try:
            smtp_server = self.config['notifications']['email']['smtp_server']
            smtp_port = self.config['notifications']['email']['smtp_port']
            username = os.getenv(self.config['notifications']['email']['username_env'])
            password = os.getenv(self.config['notifications']['email']['password_env'])
            to_addresses = self.config['notifications']['email']['to_addresses']
            
            if not username or not password or not to_addresses:
                logger.warning("Email credentials not configured")
                return
            
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = f"Serverless Monitor Alert: {subject}"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
    
    def _update_health_status(self):
        """Update overall system health status"""
        try:
            # Get current status from all components
            current_usage = self.quota_manager.get_current_usage()
            lb_status = self.load_balancer.get_load_balancer_status()
            
            # Determine provider health
            provider_health = {}
            for provider in ProviderType:
                if provider in self.quota_manager.providers:
                    usage = current_usage.get(provider)
                    if usage:
                        usage_percent = (usage.executions_this_month / self.quota_manager.quota_limits[provider].monthly_executions) * 100
                        if usage_percent > 95:
                            provider_health[provider] = "critical"
                        elif usage_percent > 80:
                            provider_health[provider] = "warning"
                        else:
                            provider_health[provider] = "healthy"
                    else:
                        provider_health[provider] = "unknown"
                else:
                    provider_health[provider] = "disabled"
            
            # Determine quota health
            quota_health = {}
            for provider, health in provider_health.items():
                quota_health[provider] = health
            
            # Determine cost health
            total_cost = sum(usage.cost_this_month for usage in current_usage.values())
            if total_cost > 0.05:
                cost_health = "critical"
            elif total_cost > 0.01:
                cost_health = "warning"
            else:
                cost_health = "healthy"
            
            # Determine performance health
            success_rate = lb_status['recent_performance']['success_rate']
            avg_response_time = lb_status['recent_performance']['average_execution_time_ms']
            
            if success_rate < 0.9 or avg_response_time > 10000:
                performance_health = "critical"
            elif success_rate < 0.95 or avg_response_time > 5000:
                performance_health = "warning"
            else:
                performance_health = "healthy"
            
            # Determine overall health
            all_healths = list(provider_health.values()) + [cost_health, performance_health]
            if "critical" in all_healths:
                overall_health = "critical"
            elif "warning" in all_healths:
                overall_health = "degraded"
            else:
                overall_health = "healthy"
            
            # Collect issues
            issues = []
            for provider, health in provider_health.items():
                if health in ["warning", "critical"]:
                    issues.append(f"Provider {provider.value} is {health}")
            
            if cost_health in ["warning", "critical"]:
                issues.append(f"Cost is {cost_health}")
            
            if performance_health in ["warning", "critical"]:
                issues.append(f"Performance is {performance_health}")
            
            # Create health status
            self.health_status = HealthStatus(
                overall_health=overall_health,
                provider_health=provider_health,
                quota_health=quota_health,
                cost_health=cost_health,
                performance_health=performance_health,
                last_updated=datetime.now(),
                issues=issues
            )
            
            # Save to database
            self._save_health_status()
            
        except Exception as e:
            logger.error(f"Error updating health status: {e}")
    
    def _save_health_status(self):
        """Save health status to database"""
        if not self.health_status:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO health_status 
            (overall_health, provider_health, quota_health, cost_health, 
             performance_health, issues, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.health_status.overall_health,
            json.dumps({k.value: v for k, v in self.health_status.provider_health.items()}),
            json.dumps({k.value: v for k, v in self.health_status.quota_health.items()}),
            self.health_status.cost_health,
            self.health_status.performance_health,
            json.dumps(self.health_status.issues),
            self.health_status.last_updated.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _cleanup_old_data(self):
        """Clean up old data beyond retention period"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clean up old metrics
            metrics_retention_days = self.config['monitoring']['metrics_retention_days']
            metrics_cutoff = datetime.now() - timedelta(days=metrics_retention_days)
            cursor.execute('DELETE FROM metrics WHERE timestamp < ?', (metrics_cutoff,))
            
            # Clean up old alerts
            alert_retention_days = self.config['monitoring']['alert_retention_days']
            alert_cutoff = datetime.now() - timedelta(days=alert_retention_days)
            cursor.execute('DELETE FROM alerts WHERE timestamp < ?', (alert_cutoff,))
            
            # Clean up old health status
            health_cutoff = datetime.now() - timedelta(days=30)  # Keep 30 days of health data
            cursor.execute('DELETE FROM health_status WHERE timestamp < ?', (health_cutoff,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive monitoring dashboard data"""
        try:
            # Get current status
            current_usage = self.quota_manager.get_current_usage()
            projections = self.projection_calculator.calculate_all_projections()
            lb_status = self.load_balancer.get_load_balancer_status()
            
            # Get recent metrics
            recent_metrics = {}
            for metric_name, metrics in self.metrics_history.items():
                if metrics:
                    recent_metrics[metric_name] = {
                        'latest_value': metrics[-1].value,
                        'unit': metrics[-1].unit,
                        'timestamp': metrics[-1].timestamp.isoformat(),
                        'trend': self._calculate_metric_trend(metrics)
                    }
            
            # Get active alerts summary
            active_alerts_summary = {
                'total': len(self.active_alerts),
                'by_level': defaultdict(int),
                'by_type': defaultdict(int)
            }
            
            for alert in self.active_alerts.values():
                active_alerts_summary['by_level'][alert.level.value] += 1
                active_alerts_summary['by_type'][alert.type.value] += 1
            
            return {
                'timestamp': datetime.now().isoformat(),
                'overall_health': self.health_status.overall_health if self.health_status else 'unknown',
                'monitoring_active': self.monitoring_active,
                'quota_status': {
                    provider.value: {
                        'current_usage_percent': round((usage.executions_this_month / self.quota_manager.quota_limits[provider].monthly_executions) * 100, 2),
                        'current_cost': round(usage.cost_this_month, 6),
                        'projected_executions': projections.get(provider, {}).projected_monthly_executions if projections.get(provider) else 0,
                        'projected_cost': round(projections.get(provider, {}).projected_monthly_cost, 6) if projections.get(provider) else 0
                    }
                    for provider, usage in current_usage.items()
                },
                'performance_metrics': {
                    'success_rate': lb_status['recent_performance']['success_rate'],
                    'average_execution_time_ms': lb_status['recent_performance']['average_execution_time_ms'],
                    'total_executions': lb_status['recent_performance']['total_executions'],
                    'total_cost_estimate': lb_status['recent_performance']['total_cost_estimate']
                },
                'recent_metrics': recent_metrics,
                'active_alerts': active_alerts_summary,
                'provider_health': lb_status['provider_health'],
                'issues': self.health_status.issues if self.health_status else []
            }
            
        except Exception as e:
            logger.error(f"Error generating monitoring dashboard: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'overall_health': 'error'
            }

def main():
    """Main function for testing and CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive Monitor')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--db-path', help='Database file path')
    parser.add_argument('--start', action='store_true', help='Start monitoring')
    parser.add_argument('--stop', action='store_true', help='Stop monitoring')
    parser.add_argument('--dashboard', action='store_true', help='Show monitoring dashboard')
    parser.add_argument('--alerts', action='store_true', help='Show active alerts')
    parser.add_argument('--health', action='store_true', help='Show health status')
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = ComprehensiveMonitor(args.config, args.db_path)
    
    if args.start:
        monitor.start_monitoring()
        print("Monitoring started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            print("\nMonitoring stopped.")
    
    if args.stop:
        monitor.stop_monitoring()
        print("Monitoring stopped.")
    
    if args.dashboard:
        dashboard = monitor.get_monitoring_dashboard()
        print(json.dumps(dashboard, indent=2))
    
    if args.alerts:
        if monitor.active_alerts:
            for alert in monitor.active_alerts.values():
                print(f"[{alert.level.value.upper()}] {alert.title}")
                print(f"  {alert.message}")
                print(f"  Time: {alert.timestamp}")
                print()
        else:
            print("No active alerts.")
    
    if args.health:
        if monitor.health_status:
            print(f"Overall Health: {monitor.health_status.overall_health}")
            print(f"Last Updated: {monitor.health_status.last_updated}")
            print("\nProvider Health:")
            for provider, health in monitor.health_status.provider_health.items():
                print(f"  {provider.value}: {health}")
            print(f"\nCost Health: {monitor.health_status.cost_health}")
            print(f"Performance Health: {monitor.health_status.performance_health}")
            if monitor.health_status.issues:
                print("\nIssues:")
                for issue in monitor.health_status.issues:
                    print(f"  - {issue}")
        else:
            print("Health status not available.")

if __name__ == "__main__":
    main()
