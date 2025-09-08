#!/usr/bin/env python3
"""
Multi-Tier Serverless Quota Manager
Intelligently manages and monitors free tier quotas across AWS Lambda, Google Cloud Functions, and Azure Functions.
Provides load balancing, projection calculations, and automatic scaling adjustments.
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import requests
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProviderType(Enum):
    AWS_LAMBDA = "aws_lambda"
    GOOGLE_CLOUD_FUNCTIONS = "google_cloud_functions"
    AZURE_FUNCTIONS = "azure_functions"

@dataclass
class QuotaLimits:
    """Free tier quota limits for each provider"""
    provider: ProviderType
    monthly_executions: int
    monthly_compute_time_gb_seconds: int
    monthly_requests: int
    concurrent_executions: int
    memory_mb: int
    timeout_seconds: int
    storage_gb: float

@dataclass
class QuotaUsage:
    """Current usage statistics for a provider"""
    provider: ProviderType
    executions_this_month: int
    compute_time_gb_seconds: int
    requests_this_month: int
    current_concurrent: int
    storage_used_gb: float
    last_updated: datetime
    cost_this_month: float = 0.0

@dataclass
class ExecutionProjection:
    """Projected execution statistics"""
    provider: ProviderType
    projected_monthly_executions: int
    projected_monthly_cost: float
    confidence_level: float  # 0.0 to 1.0
    based_on_days: int
    last_calculated: datetime

@dataclass
class LoadBalancingDecision:
    """Decision made by the load balancer"""
    selected_provider: ProviderType
    reason: str
    confidence: float
    alternative_providers: List[ProviderType]
    estimated_cost: float

class ProviderAdapter(ABC):
    """Abstract base class for provider adapters"""
    
    @abstractmethod
    def get_usage_stats(self) -> QuotaUsage:
        """Get current usage statistics from the provider"""
        pass
    
    @abstractmethod
    def deploy_function(self, function_config: Dict[str, Any]) -> bool:
        """Deploy a function to this provider"""
        pass
    
    @abstractmethod
    def invoke_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a function on this provider"""
        pass
    
    @abstractmethod
    def get_cost_estimate(self, executions: int, duration_ms: int, memory_mb: int) -> float:
        """Get cost estimate for given parameters"""
        pass

class AWSAdapter(ProviderAdapter):
    """AWS Lambda adapter"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = None  # boto3 session would be initialized here
        
    def get_usage_stats(self) -> QuotaUsage:
        """Get AWS Lambda usage statistics"""
        # In a real implementation, this would use boto3 to get CloudWatch metrics
        # For now, we'll simulate the data structure
        return QuotaUsage(
            provider=ProviderType.AWS_LAMBDA,
            executions_this_month=0,  # Would be fetched from CloudWatch
            compute_time_gb_seconds=0,
            requests_this_month=0,
            current_concurrent=0,
            storage_used_gb=0.0,
            last_updated=datetime.now(),
            cost_this_month=0.0
        )
    
    def deploy_function(self, function_config: Dict[str, Any]) -> bool:
        """Deploy function to AWS Lambda"""
        # Implementation would use boto3 lambda client
        logger.info(f"Deploying function {function_config.get('name')} to AWS Lambda")
        return True
    
    def invoke_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke AWS Lambda function"""
        # Implementation would use boto3 lambda client
        logger.info(f"Invoking AWS Lambda function: {function_name}")
        return {"statusCode": 200, "body": "Success"}
    
    def get_cost_estimate(self, executions: int, duration_ms: int, memory_mb: int) -> float:
        """Calculate AWS Lambda cost estimate"""
        # AWS Lambda pricing: $0.0000166667 per GB-second
        gb_seconds = (executions * duration_ms * memory_mb) / (1000 * 1024)
        return gb_seconds * 0.0000166667

class GoogleCloudAdapter(ProviderAdapter):
    """Google Cloud Functions adapter"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def get_usage_stats(self) -> QuotaUsage:
        """Get Google Cloud Functions usage statistics"""
        return QuotaUsage(
            provider=ProviderType.GOOGLE_CLOUD_FUNCTIONS,
            executions_this_month=0,
            compute_time_gb_seconds=0,
            requests_this_month=0,
            current_concurrent=0,
            storage_used_gb=0.0,
            last_updated=datetime.now(),
            cost_this_month=0.0
        )
    
    def deploy_function(self, function_config: Dict[str, Any]) -> bool:
        """Deploy function to Google Cloud Functions"""
        logger.info(f"Deploying function {function_config.get('name')} to Google Cloud Functions")
        return True
    
    def invoke_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke Google Cloud Function"""
        logger.info(f"Invoking Google Cloud Function: {function_name}")
        return {"statusCode": 200, "body": "Success"}
    
    def get_cost_estimate(self, executions: int, duration_ms: int, memory_mb: int) -> float:
        """Calculate Google Cloud Functions cost estimate"""
        # GCP pricing: $0.0000025 per GB-second
        gb_seconds = (executions * duration_ms * memory_mb) / (1000 * 1024)
        return gb_seconds * 0.0000025

class AzureAdapter(ProviderAdapter):
    """Azure Functions adapter"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def get_usage_stats(self) -> QuotaUsage:
        """Get Azure Functions usage statistics"""
        return QuotaUsage(
            provider=ProviderType.AZURE_FUNCTIONS,
            executions_this_month=0,
            compute_time_gb_seconds=0,
            requests_this_month=0,
            current_concurrent=0,
            storage_used_gb=0.0,
            last_updated=datetime.now(),
            cost_this_month=0.0
        )
    
    def deploy_function(self, function_config: Dict[str, Any]) -> bool:
        """Deploy function to Azure Functions"""
        logger.info(f"Deploying function {function_config.get('name')} to Azure Functions")
        return True
    
    def invoke_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke Azure Function"""
        logger.info(f"Invoking Azure Function: {function_name}")
        return {"statusCode": 200, "body": "Success"}
    
    def get_cost_estimate(self, executions: int, duration_ms: int, memory_mb: int) -> float:
        """Calculate Azure Functions cost estimate"""
        # Azure pricing: $0.000016 per GB-second
        gb_seconds = (executions * duration_ms * memory_mb) / (1000 * 1024)
        return gb_seconds * 0.000016

class MultiTierQuotaManager:
    """Main quota management and load balancing system"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.quota_limits = self._initialize_quota_limits()
        self.providers = self._initialize_providers()
        self.usage_history = []
        self.projections = {}
        
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), 'multi_tier_quota_config.yaml')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'providers': {
                'aws_lambda': {
                    'enabled': True,
                    'region': 'us-east-1',
                    'access_key_env': 'AWS_ACCESS_KEY_ID',
                    'secret_key_env': 'AWS_SECRET_ACCESS_KEY'
                },
                'google_cloud_functions': {
                    'enabled': True,
                    'project_id_env': 'GCP_PROJECT_ID',
                    'credentials_path_env': 'GOOGLE_APPLICATION_CREDENTIALS'
                },
                'azure_functions': {
                    'enabled': True,
                    'subscription_id_env': 'AZURE_SUBSCRIPTION_ID',
                    'resource_group_env': 'AZURE_RESOURCE_GROUP',
                    'function_app_env': 'AZURE_FUNCTION_APP'
                }
            },
            'quota_management': {
                'warning_threshold_percent': 80,
                'critical_threshold_percent': 95,
                'auto_scaling_enabled': True,
                'projection_recalculation_hours': 24
            },
            'load_balancing': {
                'strategy': 'cost_optimized',  # cost_optimized, performance, balanced
                'fallback_enabled': True,
                'health_check_interval_minutes': 15
            }
        }
    
    def _initialize_quota_limits(self) -> Dict[ProviderType, QuotaLimits]:
        """Initialize quota limits for each provider"""
        return {
            ProviderType.AWS_LAMBDA: QuotaLimits(
                provider=ProviderType.AWS_LAMBDA,
                monthly_executions=1_000_000,
                monthly_compute_time_gb_seconds=400_000,
                monthly_requests=1_000_000,
                concurrent_executions=1000,
                memory_mb=1024,
                timeout_seconds=900,
                storage_gb=0.5
            ),
            ProviderType.GOOGLE_CLOUD_FUNCTIONS: QuotaLimits(
                provider=ProviderType.GOOGLE_CLOUD_FUNCTIONS,
                monthly_executions=2_000_000,
                monthly_compute_time_gb_seconds=400_000,
                monthly_requests=2_000_000,
                concurrent_executions=1000,
                memory_mb=1024,
                timeout_seconds=540,
                storage_gb=5.0
            ),
            ProviderType.AZURE_FUNCTIONS: QuotaLimits(
                provider=ProviderType.AZURE_FUNCTIONS,
                monthly_executions=1_000_000,
                monthly_compute_time_gb_seconds=400_000,
                monthly_requests=1_000_000,
                concurrent_executions=200,
                memory_mb=1536,
                timeout_seconds=600,
                storage_gb=1.0
            )
        }
    
    def _initialize_providers(self) -> Dict[ProviderType, ProviderAdapter]:
        """Initialize provider adapters"""
        providers = {}
        
        if self.config['providers']['aws_lambda']['enabled']:
            providers[ProviderType.AWS_LAMBDA] = AWSAdapter(
                self.config['providers']['aws_lambda']
            )
        
        if self.config['providers']['google_cloud_functions']['enabled']:
            providers[ProviderType.GOOGLE_CLOUD_FUNCTIONS] = GoogleCloudAdapter(
                self.config['providers']['google_cloud_functions']
            )
        
        if self.config['providers']['azure_functions']['enabled']:
            providers[ProviderType.AZURE_FUNCTIONS] = AzureAdapter(
                self.config['providers']['azure_functions']
            )
        
        return providers
    
    def get_current_usage(self) -> Dict[ProviderType, QuotaUsage]:
        """Get current usage statistics for all providers"""
        usage = {}
        for provider_type, adapter in self.providers.items():
            try:
                usage[provider_type] = adapter.get_usage_stats()
            except Exception as e:
                logger.error(f"Failed to get usage stats for {provider_type}: {e}")
                # Use cached data if available
                usage[provider_type] = self._get_cached_usage(provider_type)
        
        # Store in history
        self.usage_history.append({
            'timestamp': datetime.now(),
            'usage': usage
        })
        
        # Keep only last 30 days of history
        cutoff_date = datetime.now() - timedelta(days=30)
        self.usage_history = [
            entry for entry in self.usage_history 
            if entry['timestamp'] > cutoff_date
        ]
        
        return usage
    
    def _get_cached_usage(self, provider_type: ProviderType) -> QuotaUsage:
        """Get cached usage data when live data is unavailable"""
        if self.usage_history:
            latest_entry = self.usage_history[-1]
            return latest_entry['usage'].get(provider_type, QuotaUsage(
                provider=provider_type,
                executions_this_month=0,
                compute_time_gb_seconds=0,
                requests_this_month=0,
                current_concurrent=0,
                storage_used_gb=0.0,
                last_updated=datetime.now()
            ))
        else:
            return QuotaUsage(
                provider=provider_type,
                executions_this_month=0,
                compute_time_gb_seconds=0,
                requests_this_month=0,
                current_concurrent=0,
                storage_used_gb=0.0,
                last_updated=datetime.now()
            )
    
    def calculate_projections(self) -> Dict[ProviderType, ExecutionProjection]:
        """Calculate execution projections for all providers"""
        projections = {}
        current_usage = self.get_current_usage()
        
        for provider_type, usage in current_usage.items():
            projection = self._calculate_provider_projection(provider_type, usage)
            projections[provider_type] = projection
        
        self.projections = projections
        return projections
    
    def _calculate_provider_projection(self, provider_type: ProviderType, usage: QuotaUsage) -> ExecutionProjection:
        """Calculate projection for a specific provider"""
        # Get historical data for this provider
        provider_history = []
        for entry in self.usage_history:
            if provider_type in entry['usage']:
                provider_history.append(entry['usage'][provider_type])
        
        if not provider_history:
            # No history, use current usage as baseline
            daily_avg = usage.executions_this_month / 30 if usage.executions_this_month > 0 else 1
        else:
            # Calculate daily average from history
            total_executions = sum(h.executions_this_month for h in provider_history)
            total_days = len(provider_history)
            daily_avg = total_executions / total_days if total_days > 0 else 1
        
        # Project monthly executions
        days_in_month = 30
        projected_monthly = int(daily_avg * days_in_month)
        
        # Calculate confidence based on data availability
        confidence = min(1.0, len(provider_history) / 7)  # Full confidence after 7 days
        
        # Estimate cost
        estimated_cost = self.providers[provider_type].get_cost_estimate(
            projected_monthly, 1000, 256  # Assume 1s duration, 256MB memory
        )
        
        return ExecutionProjection(
            provider=provider_type,
            projected_monthly_executions=projected_monthly,
            projected_monthly_cost=estimated_cost,
            confidence_level=confidence,
            based_on_days=len(provider_history),
            last_calculated=datetime.now()
        )
    
    def select_optimal_provider(self, function_config: Dict[str, Any]) -> LoadBalancingDecision:
        """Select the optimal provider for a function execution"""
        current_usage = self.get_current_usage()
        projections = self.calculate_projections()
        
        # Get function requirements
        estimated_duration_ms = function_config.get('estimated_duration_ms', 1000)
        memory_mb = function_config.get('memory_mb', 256)
        priority = function_config.get('priority', 'normal')  # high, normal, low
        
        available_providers = []
        
        for provider_type, usage in current_usage.items():
            limits = self.quota_limits[provider_type]
            projection = projections[provider_type]
            
            # Check if provider has capacity
            if self._has_capacity(provider_type, usage, limits, projection):
                cost_estimate = self.providers[provider_type].get_cost_estimate(
                    1, estimated_duration_ms, memory_mb
                )
                
                available_providers.append({
                    'provider': provider_type,
                    'usage_percent': (usage.executions_this_month / limits.monthly_executions) * 100,
                    'projected_usage_percent': (projection.projected_monthly_executions / limits.monthly_executions) * 100,
                    'cost_estimate': cost_estimate,
                    'confidence': projection.confidence_level
                })
        
        if not available_providers:
            # No providers available, select least used
            least_used = min(current_usage.items(), key=lambda x: x[1].executions_this_month)
            return LoadBalancingDecision(
                selected_provider=least_used[0],
                reason="No providers with capacity, using least used",
                confidence=0.1,
                alternative_providers=list(current_usage.keys()),
                estimated_cost=0.0
            )
        
        # Select based on strategy
        strategy = self.config['load_balancing']['strategy']
        
        if strategy == 'cost_optimized':
            selected = min(available_providers, key=lambda x: x['cost_estimate'])
            reason = "Cost-optimized selection"
        elif strategy == 'performance':
            selected = max(available_providers, key=lambda x: x['confidence'])
            reason = "Performance-optimized selection"
        else:  # balanced
            # Balance between cost and usage
            selected = min(available_providers, key=lambda x: 
                x['projected_usage_percent'] * 0.7 + x['cost_estimate'] * 1000)
            reason = "Balanced selection"
        
        return LoadBalancingDecision(
            selected_provider=selected['provider'],
            reason=reason,
            confidence=selected['confidence'],
            alternative_providers=[p['provider'] for p in available_providers if p['provider'] != selected['provider']],
            estimated_cost=selected['cost_estimate']
        )
    
    def _has_capacity(self, provider_type: ProviderType, usage: QuotaUsage, 
                     limits: QuotaLimits, projection: ExecutionProjection) -> bool:
        """Check if provider has capacity for additional executions"""
        warning_threshold = self.config['quota_management']['warning_threshold_percent']
        critical_threshold = self.config['quota_management']['critical_threshold_percent']
        
        # Check current usage
        current_usage_percent = (usage.executions_this_month / limits.monthly_executions) * 100
        
        # Check projected usage
        projected_usage_percent = (projection.projected_monthly_executions / limits.monthly_executions) * 100
        
        # Provider has capacity if both current and projected usage are below warning threshold
        return (current_usage_percent < warning_threshold and 
                projected_usage_percent < warning_threshold)
    
    def adjust_execution_frequency(self, function_name: str, current_frequency_hours: int) -> int:
        """Adjust execution frequency based on quota usage"""
        current_usage = self.get_current_usage()
        projections = self.calculate_projections()
        
        # Find the most constrained provider
        most_constrained = None
        max_usage_percent = 0
        
        for provider_type, usage in current_usage.items():
            limits = self.quota_limits[provider_type]
            projection = projections[provider_type]
            
            usage_percent = max(
                (usage.executions_this_month / limits.monthly_executions) * 100,
                (projection.projected_monthly_executions / limits.monthly_executions) * 100
            )
            
            if usage_percent > max_usage_percent:
                max_usage_percent = usage_percent
                most_constrained = provider_type
        
        if not most_constrained:
            return current_frequency_hours
        
        # Adjust frequency based on usage
        if max_usage_percent > 80:
            # Reduce frequency by 50%
            return int(current_frequency_hours * 1.5)
        elif max_usage_percent > 60:
            # Reduce frequency by 25%
            return int(current_frequency_hours * 1.25)
        else:
            # Can increase frequency
            return max(1, int(current_frequency_hours * 0.9))
    
    def get_quota_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive quota status report"""
        current_usage = self.get_current_usage()
        projections = self.calculate_projections()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'providers': {},
            'overall_status': 'healthy',
            'recommendations': []
        }
        
        for provider_type in self.providers.keys():
            usage = current_usage[provider_type]
            limits = self.quota_limits[provider_type]
            projection = projections[provider_type]
            
            usage_percent = (usage.executions_this_month / limits.monthly_executions) * 100
            projected_percent = (projection.projected_monthly_executions / limits.monthly_executions) * 100
            
            status = 'healthy'
            if projected_percent > 95:
                status = 'critical'
                report['overall_status'] = 'critical'
            elif projected_percent > 80:
                status = 'warning'
                if report['overall_status'] == 'healthy':
                    report['overall_status'] = 'warning'
            
            report['providers'][provider_type.value] = {
                'status': status,
                'current_usage': {
                    'executions': usage.executions_this_month,
                    'percentage': round(usage_percent, 2),
                    'cost': usage.cost_this_month
                },
                'projected_usage': {
                    'executions': projection.projected_monthly_executions,
                    'percentage': round(projected_percent, 2),
                    'cost': projection.projected_monthly_cost,
                    'confidence': round(projection.confidence_level, 2)
                },
                'limits': {
                    'monthly_executions': limits.monthly_executions,
                    'monthly_compute_time': limits.monthly_compute_time_gb_seconds,
                    'concurrent_executions': limits.concurrent_executions
                }
            }
        
        # Generate recommendations
        if report['overall_status'] == 'critical':
            report['recommendations'].append("Consider reducing function execution frequency")
            report['recommendations'].append("Review and optimize function performance")
        elif report['overall_status'] == 'warning':
            report['recommendations'].append("Monitor usage closely")
            report['recommendations'].append("Consider load balancing to other providers")
        
        return report
    
    def save_quota_config(self, config_path: str = None):
        """Save current configuration to file"""
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), 'multi_tier_quota_config.yaml')
        
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        
        logger.info(f"Quota configuration saved to {config_path}")

def main():
    """Main function for testing and CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Tier Serverless Quota Manager')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--status', action='store_true', help='Show quota status')
    parser.add_argument('--projections', action='store_true', help='Show execution projections')
    parser.add_argument('--select-provider', help='Test provider selection for function')
    parser.add_argument('--adjust-frequency', help='Test frequency adjustment for function')
    
    args = parser.parse_args()
    
    # Initialize quota manager
    manager = MultiTierQuotaManager(args.config)
    
    if args.status:
        report = manager.get_quota_status_report()
        print(json.dumps(report, indent=2))
    
    if args.projections:
        projections = manager.calculate_projections()
        for provider, projection in projections.items():
            print(f"{provider.value}: {projection.projected_monthly_executions} executions/month "
                  f"(confidence: {projection.confidence_level:.2f})")
    
    if args.select_provider:
        function_config = {
            'name': args.select_provider,
            'estimated_duration_ms': 1000,
            'memory_mb': 256,
            'priority': 'normal'
        }
        decision = manager.select_optimal_provider(function_config)
        print(f"Selected: {decision.selected_provider.value}")
        print(f"Reason: {decision.reason}")
        print(f"Confidence: {decision.confidence:.2f}")
        print(f"Estimated cost: ${decision.estimated_cost:.6f}")
    
    if args.adjust_frequency:
        new_frequency = manager.adjust_execution_frequency(args.adjust_frequency, 24)
        print(f"Adjusted frequency for {args.adjust_frequency}: {new_frequency} hours")

if __name__ == "__main__":
    main()
