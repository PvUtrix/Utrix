#!/usr/bin/env python3
"""
Intelligent Load Balancer for Multi-Tier Serverless Architecture
Distributes function executions across AWS Lambda, Google Cloud Functions, and Azure Functions
based on quota availability, cost optimization, and performance metrics.
"""

import json
import os
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

from multi_tier_quota_manager import (
    MultiTierQuotaManager, 
    ProviderType, 
    LoadBalancingDecision,
    QuotaUsage,
    ExecutionProjection
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoadBalancingStrategy(Enum):
    COST_OPTIMIZED = "cost_optimized"
    PERFORMANCE = "performance"
    BALANCED = "balanced"
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"

class FunctionType(Enum):
    DAILY_SUMMARY = "daily_summary"
    SHADOW_WORK_TRACKER = "shadow_work_tracker"
    GOOGLE_DRIVE_SYNC = "google_drive_sync"
    VOICE_GENERATION = "voice_generation"
    DATA_PROCESSING = "data_processing"
    HEALTH_CHECK = "health_check"
    NOTIFICATION = "notification"

@dataclass
class FunctionRequest:
    """Request to execute a function"""
    function_name: str
    function_type: FunctionType
    payload: Dict[str, Any]
    priority: str = "normal"  # high, normal, low
    timeout_seconds: int = 30
    retry_count: int = 3
    expected_duration_ms: int = 1000
    memory_mb: int = 256
    tags: List[str] = None

@dataclass
class ExecutionResult:
    """Result of function execution"""
    success: bool
    provider: ProviderType
    execution_time_ms: int
    response_data: Dict[str, Any]
    error_message: str = None
    cost_estimate: float = 0.0
    retry_count: int = 0

@dataclass
class ProviderHealth:
    """Health status of a provider"""
    provider: ProviderType
    is_healthy: bool
    response_time_ms: float
    error_rate: float
    last_check: datetime
    consecutive_failures: int = 0

class IntelligentLoadBalancer:
    """Main load balancer class"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.quota_manager = MultiTierQuotaManager(config_path)
        self.provider_health = {}
        self.execution_history = []
        self.function_routing_table = self._build_routing_table()
        self.strategy = LoadBalancingStrategy(self.config.get('strategy', 'cost_optimized'))
        
        # Initialize provider health tracking
        self._initialize_provider_health()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration"""
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), 'load_balancer_config.yaml')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'strategy': 'cost_optimized',
            'health_check_interval_seconds': 300,  # 5 minutes
            'execution_timeout_seconds': 30,
            'max_retries': 3,
            'retry_delay_seconds': 1,
            'circuit_breaker_threshold': 5,
            'circuit_breaker_timeout_seconds': 300,
            'performance_window_minutes': 60,
            'cost_optimization_weight': 0.4,
            'performance_weight': 0.3,
            'quota_utilization_weight': 0.3
        }
    
    def _build_routing_table(self) -> Dict[FunctionType, Dict[str, Any]]:
        """Build function routing table based on configuration"""
        routing_table = {}
        
        # Default routing for each function type
        default_routing = {
            FunctionType.DAILY_SUMMARY: {
                'preferred_providers': [ProviderType.AWS_LAMBDA, ProviderType.GOOGLE_CLOUD_FUNCTIONS],
                'estimated_duration_ms': 5000,
                'memory_mb': 256,
                'priority': 'high'
            },
            FunctionType.SHADOW_WORK_TRACKER: {
                'preferred_providers': [ProviderType.GOOGLE_CLOUD_FUNCTIONS, ProviderType.AZURE_FUNCTIONS],
                'estimated_duration_ms': 2000,
                'memory_mb': 128,
                'priority': 'normal'
            },
            FunctionType.GOOGLE_DRIVE_SYNC: {
                'preferred_providers': [ProviderType.AWS_LAMBDA],
                'estimated_duration_ms': 45000,
                'memory_mb': 512,
                'priority': 'low'
            },
            FunctionType.VOICE_GENERATION: {
                'preferred_providers': [ProviderType.AZURE_FUNCTIONS, ProviderType.AWS_LAMBDA],
                'estimated_duration_ms': 10000,
                'memory_mb': 1024,
                'priority': 'normal'
            },
            FunctionType.DATA_PROCESSING: {
                'preferred_providers': [ProviderType.GOOGLE_CLOUD_FUNCTIONS, ProviderType.AWS_LAMBDA],
                'estimated_duration_ms': 15000,
                'memory_mb': 1024,
                'priority': 'normal'
            },
            FunctionType.HEALTH_CHECK: {
                'preferred_providers': [ProviderType.AWS_LAMBDA, ProviderType.GOOGLE_CLOUD_FUNCTIONS],
                'estimated_duration_ms': 1000,
                'memory_mb': 128,
                'priority': 'high'
            },
            FunctionType.NOTIFICATION: {
                'preferred_providers': [ProviderType.GOOGLE_CLOUD_FUNCTIONS, ProviderType.AZURE_FUNCTIONS],
                'estimated_duration_ms': 2000,
                'memory_mb': 128,
                'priority': 'high'
            }
        }
        
        # Load from config if available
        if 'function_routing' in self.config:
            for func_type_str, routing in self.config['function_routing'].items():
                try:
                    func_type = FunctionType(func_type_str)
                    routing_table[func_type] = routing
                except ValueError:
                    logger.warning(f"Unknown function type: {func_type_str}")
        
        # Use defaults for missing entries
        for func_type, default in default_routing.items():
            if func_type not in routing_table:
                routing_table[func_type] = default
        
        return routing_table
    
    def _initialize_provider_health(self):
        """Initialize provider health tracking"""
        for provider_type in ProviderType:
            self.provider_health[provider_type] = ProviderHealth(
                provider=provider_type,
                is_healthy=True,
                response_time_ms=0.0,
                error_rate=0.0,
                last_check=datetime.now(),
                consecutive_failures=0
            )
    
    def _start_background_tasks(self):
        """Start background monitoring tasks"""
        # In a real implementation, this would start async tasks
        # For now, we'll simulate with periodic checks
        logger.info("Background monitoring tasks started")
    
    async def execute_function(self, request: FunctionRequest) -> ExecutionResult:
        """Execute a function using the load balancer"""
        start_time = time.time()
        
        # Get routing information for this function type
        routing_info = self.function_routing_table.get(request.function_type, {})
        
        # Select optimal provider
        provider_decision = await self._select_provider(request, routing_info)
        
        if not provider_decision:
            return ExecutionResult(
                success=False,
                provider=ProviderType.AWS_LAMBDA,  # Default
                execution_time_ms=0,
                response_data={},
                error_message="No available providers"
            )
        
        # Execute function with retries
        result = await self._execute_with_retries(request, provider_decision)
        
        # Update execution history and provider health
        execution_time_ms = int((time.time() - start_time) * 1000)
        result.execution_time_ms = execution_time_ms
        
        self._update_execution_history(request, result)
        self._update_provider_health(provider_decision.selected_provider, result)
        
        return result
    
    async def _select_provider(self, request: FunctionRequest, routing_info: Dict[str, Any]) -> Optional[LoadBalancingDecision]:
        """Select the optimal provider for function execution"""
        # Get current quota status
        current_usage = self.quota_manager.get_current_usage()
        projections = self.quota_manager.calculate_projections()
        
        # Filter healthy providers
        healthy_providers = [
            provider for provider, health in self.provider_health.items()
            if health.is_healthy and provider in self.quota_manager.providers
        ]
        
        if not healthy_providers:
            logger.error("No healthy providers available")
            return None
        
        # Apply load balancing strategy
        if self.strategy == LoadBalancingStrategy.COST_OPTIMIZED:
            return self._select_cost_optimized(request, healthy_providers, current_usage, projections)
        elif self.strategy == LoadBalancingStrategy.PERFORMANCE:
            return self._select_performance_optimized(request, healthy_providers, current_usage, projections)
        elif self.strategy == LoadBalancingStrategy.BALANCED:
            return self._select_balanced(request, healthy_providers, current_usage, projections)
        elif self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._select_round_robin(request, healthy_providers)
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._select_least_connections(request, healthy_providers, current_usage)
        else:
            # Default to cost optimized
            return self._select_cost_optimized(request, healthy_providers, current_usage, projections)
    
    def _select_cost_optimized(self, request: FunctionRequest, healthy_providers: List[ProviderType], 
                              current_usage: Dict[ProviderType, QuotaUsage], 
                              projections: Dict[ProviderType, ExecutionProjection]) -> LoadBalancingDecision:
        """Select provider based on cost optimization"""
        provider_costs = []
        
        for provider in healthy_providers:
            if provider in self.quota_manager.providers:
                adapter = self.quota_manager.providers[provider]
                cost_estimate = adapter.get_cost_estimate(
                    1, request.expected_duration_ms, request.memory_mb
                )
                
                # Check quota availability
                usage = current_usage.get(provider)
                projection = projections.get(provider)
                
                if usage and projection:
                    quota_available = self._check_quota_availability(provider, usage, projection)
                    if quota_available:
                        provider_costs.append({
                            'provider': provider,
                            'cost': cost_estimate,
                            'quota_usage_percent': (usage.executions_this_month / self.quota_manager.quota_limits[provider].monthly_executions) * 100
                        })
        
        if not provider_costs:
            # Fallback to least used provider
            least_used = min(healthy_providers, key=lambda p: current_usage.get(p, QuotaUsage(
                provider=p, executions_this_month=0, compute_time_gb_seconds=0,
                requests_this_month=0, current_concurrent=0, storage_used_gb=0.0,
                last_updated=datetime.now()
            )).executions_this_month)
            
            return LoadBalancingDecision(
                selected_provider=least_used,
                reason="Fallback to least used provider",
                confidence=0.1,
                alternative_providers=healthy_providers,
                estimated_cost=0.0
            )
        
        # Select lowest cost provider
        selected = min(provider_costs, key=lambda x: x['cost'])
        
        return LoadBalancingDecision(
            selected_provider=selected['provider'],
            reason=f"Cost optimized selection (${selected['cost']:.6f})",
            confidence=0.8,
            alternative_providers=[p['provider'] for p in provider_costs if p['provider'] != selected['provider']],
            estimated_cost=selected['cost']
        )
    
    def _select_performance_optimized(self, request: FunctionRequest, healthy_providers: List[ProviderType],
                                     current_usage: Dict[ProviderType, QuotaUsage],
                                     projections: Dict[ProviderType, ExecutionProjection]) -> LoadBalancingDecision:
        """Select provider based on performance metrics"""
        provider_performance = []
        
        for provider in healthy_providers:
            health = self.provider_health[provider]
            
            # Calculate performance score
            response_time_score = max(0, 1 - (health.response_time_ms / 5000))  # Normalize to 5s max
            error_rate_score = max(0, 1 - health.error_rate)
            quota_availability = self._check_quota_availability(provider, current_usage.get(provider), projections.get(provider))
            
            if quota_availability:
                performance_score = (response_time_score * 0.4 + error_rate_score * 0.6)
                provider_performance.append({
                    'provider': provider,
                    'score': performance_score,
                    'response_time': health.response_time_ms,
                    'error_rate': health.error_rate
                })
        
        if not provider_performance:
            # Fallback
            return LoadBalancingDecision(
                selected_provider=healthy_providers[0],
                reason="Fallback to first available provider",
                confidence=0.1,
                alternative_providers=healthy_providers[1:],
                estimated_cost=0.0
            )
        
        # Select highest performance provider
        selected = max(provider_performance, key=lambda x: x['score'])
        
        return LoadBalancingDecision(
            selected_provider=selected['provider'],
            reason=f"Performance optimized selection (score: {selected['score']:.2f})",
            confidence=0.8,
            alternative_providers=[p['provider'] for p in provider_performance if p['provider'] != selected['provider']],
            estimated_cost=0.0
        )
    
    def _select_balanced(self, request: FunctionRequest, healthy_providers: List[ProviderType],
                        current_usage: Dict[ProviderType, QuotaUsage],
                        projections: Dict[ProviderType, ExecutionProjection]) -> LoadBalancingDecision:
        """Select provider using balanced approach (cost + performance + quota)"""
        provider_scores = []
        
        for provider in healthy_providers:
            if provider in self.quota_manager.providers:
                adapter = self.quota_manager.providers[provider]
                health = self.provider_health[provider]
                usage = current_usage.get(provider)
                projection = projections.get(provider)
                
                # Check quota availability
                if not self._check_quota_availability(provider, usage, projection):
                    continue
                
                # Calculate scores
                cost_estimate = adapter.get_cost_estimate(1, request.expected_duration_ms, request.memory_mb)
                cost_score = max(0, 1 - (cost_estimate * 10000))  # Normalize cost
                
                response_time_score = max(0, 1 - (health.response_time_ms / 5000))
                error_rate_score = max(0, 1 - health.error_rate)
                performance_score = (response_time_score * 0.4 + error_rate_score * 0.6)
                
                quota_usage_percent = (usage.executions_this_month / self.quota_manager.quota_limits[provider].monthly_executions) * 100
                quota_score = max(0, 1 - (quota_usage_percent / 100))
                
                # Weighted combined score
                combined_score = (
                    cost_score * self.config.get('cost_optimization_weight', 0.4) +
                    performance_score * self.config.get('performance_weight', 0.3) +
                    quota_score * self.config.get('quota_utilization_weight', 0.3)
                )
                
                provider_scores.append({
                    'provider': provider,
                    'score': combined_score,
                    'cost': cost_estimate,
                    'performance': performance_score,
                    'quota_usage': quota_usage_percent
                })
        
        if not provider_scores:
            # Fallback
            return LoadBalancingDecision(
                selected_provider=healthy_providers[0],
                reason="Fallback to first available provider",
                confidence=0.1,
                alternative_providers=healthy_providers[1:],
                estimated_cost=0.0
            )
        
        # Select highest combined score
        selected = max(provider_scores, key=lambda x: x['score'])
        
        return LoadBalancingDecision(
            selected_provider=selected['provider'],
            reason=f"Balanced selection (score: {selected['score']:.2f})",
            confidence=0.8,
            alternative_providers=[p['provider'] for p in provider_scores if p['provider'] != selected['provider']],
            estimated_cost=selected['cost']
        )
    
    def _select_round_robin(self, request: FunctionRequest, healthy_providers: List[ProviderType]) -> LoadBalancingDecision:
        """Select provider using round-robin strategy"""
        # Simple round-robin based on function name hash
        hash_value = int(hashlib.md5(request.function_name.encode()).hexdigest(), 16)
        selected_index = hash_value % len(healthy_providers)
        selected_provider = healthy_providers[selected_index]
        
        return LoadBalancingDecision(
            selected_provider=selected_provider,
            reason="Round-robin selection",
            confidence=0.5,
            alternative_providers=[p for p in healthy_providers if p != selected_provider],
            estimated_cost=0.0
        )
    
    def _select_least_connections(self, request: FunctionRequest, healthy_providers: List[ProviderType],
                                 current_usage: Dict[ProviderType, QuotaUsage]) -> LoadBalancingDecision:
        """Select provider with least concurrent connections"""
        provider_connections = []
        
        for provider in healthy_providers:
            usage = current_usage.get(provider)
            if usage:
                provider_connections.append({
                    'provider': provider,
                    'concurrent': usage.current_concurrent
                })
        
        if not provider_connections:
            return LoadBalancingDecision(
                selected_provider=healthy_providers[0],
                reason="Fallback to first available provider",
                confidence=0.1,
                alternative_providers=healthy_providers[1:],
                estimated_cost=0.0
            )
        
        # Select provider with least concurrent connections
        selected = min(provider_connections, key=lambda x: x['concurrent'])
        
        return LoadBalancingDecision(
            selected_provider=selected['provider'],
            reason=f"Least connections selection ({selected['concurrent']} concurrent)",
            confidence=0.7,
            alternative_providers=[p['provider'] for p in provider_connections if p['provider'] != selected['provider']],
            estimated_cost=0.0
        )
    
    def _check_quota_availability(self, provider: ProviderType, usage: QuotaUsage, 
                                 projection: ExecutionProjection) -> bool:
        """Check if provider has quota availability"""
        if not usage or not projection:
            return False
        
        limits = self.quota_manager.quota_limits[provider]
        warning_threshold = self.quota_manager.config['quota_management']['warning_threshold_percent']
        
        # Check current usage
        current_usage_percent = (usage.executions_this_month / limits.monthly_executions) * 100
        
        # Check projected usage
        projected_usage_percent = (projection.projected_monthly_executions / limits.monthly_executions) * 100
        
        # Provider has capacity if both are below warning threshold
        return (current_usage_percent < warning_threshold and 
                projected_usage_percent < warning_threshold)
    
    async def _execute_with_retries(self, request: FunctionRequest, 
                                   decision: LoadBalancingDecision) -> ExecutionResult:
        """Execute function with retry logic"""
        last_error = None
        
        for attempt in range(request.retry_count + 1):
            try:
                # Execute function
                result = await self._execute_single_attempt(request, decision.selected_provider)
                
                if result.success:
                    result.retry_count = attempt
                    return result
                else:
                    last_error = result.error_message
                    
            except Exception as e:
                last_error = str(e)
                logger.error(f"Execution attempt {attempt + 1} failed: {e}")
            
            # Wait before retry (exponential backoff)
            if attempt < request.retry_count:
                delay = self.config.get('retry_delay_seconds', 1) * (2 ** attempt)
                await asyncio.sleep(delay)
        
        # All retries failed
        return ExecutionResult(
            success=False,
            provider=decision.selected_provider,
            execution_time_ms=0,
            response_data={},
            error_message=f"All retries failed. Last error: {last_error}",
            retry_count=request.retry_count
        )
    
    async def _execute_single_attempt(self, request: FunctionRequest, 
                                     provider: ProviderType) -> ExecutionResult:
        """Execute a single attempt of the function"""
        start_time = time.time()
        
        try:
            # Get provider adapter
            adapter = self.quota_manager.providers[provider]
            
            # Prepare function configuration
            function_config = {
                'name': request.function_name,
                'payload': request.payload,
                'timeout': request.timeout_seconds,
                'memory_mb': request.memory_mb
            }
            
            # Execute function
            response = adapter.invoke_function(request.function_name, request.payload)
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Calculate cost estimate
            cost_estimate = adapter.get_cost_estimate(1, execution_time_ms, request.memory_mb)
            
            return ExecutionResult(
                success=True,
                provider=provider,
                execution_time_ms=execution_time_ms,
                response_data=response,
                cost_estimate=cost_estimate
            )
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            return ExecutionResult(
                success=False,
                provider=provider,
                execution_time_ms=execution_time_ms,
                response_data={},
                error_message=str(e)
            )
    
    def _update_execution_history(self, request: FunctionRequest, result: ExecutionResult):
        """Update execution history for analytics"""
        history_entry = {
            'timestamp': datetime.now(),
            'function_name': request.function_name,
            'function_type': request.function_type.value,
            'provider': result.provider.value,
            'success': result.success,
            'execution_time_ms': result.execution_time_ms,
            'cost_estimate': result.cost_estimate,
            'retry_count': result.retry_count
        }
        
        self.execution_history.append(history_entry)
        
        # Keep only last 1000 entries
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-1000:]
    
    def _update_provider_health(self, provider: ProviderType, result: ExecutionResult):
        """Update provider health metrics"""
        health = self.provider_health[provider]
        
        # Update response time (exponential moving average)
        alpha = 0.1  # Smoothing factor
        if health.response_time_ms == 0:
            health.response_time_ms = result.execution_time_ms
        else:
            health.response_time_ms = (alpha * result.execution_time_ms + 
                                     (1 - alpha) * health.response_time_ms)
        
        # Update error rate
        window_minutes = self.config.get('performance_window_minutes', 60)
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        
        recent_executions = [
            entry for entry in self.execution_history
            if (entry['provider'] == provider.value and 
                entry['timestamp'] > cutoff_time)
        ]
        
        if recent_executions:
            error_count = sum(1 for entry in recent_executions if not entry['success'])
            health.error_rate = error_count / len(recent_executions)
        
        # Update consecutive failures
        if result.success:
            health.consecutive_failures = 0
            health.is_healthy = True
        else:
            health.consecutive_failures += 1
            
            # Circuit breaker logic
            threshold = self.config.get('circuit_breaker_threshold', 5)
            if health.consecutive_failures >= threshold:
                health.is_healthy = False
                logger.warning(f"Provider {provider.value} marked as unhealthy due to {health.consecutive_failures} consecutive failures")
        
        health.last_check = datetime.now()
    
    async def health_check_all_providers(self) -> Dict[ProviderType, bool]:
        """Perform health check on all providers"""
        health_results = {}
        
        for provider_type, adapter in self.quota_manager.providers.items():
            try:
                # Simple health check - try to get usage stats
                start_time = time.time()
                usage = adapter.get_usage_stats()
                response_time = (time.time() - start_time) * 1000
                
                health = self.provider_health[provider_type]
                health.response_time_ms = response_time
                health.last_check = datetime.now()
                
                # If we got here, provider is healthy
                health_results[provider_type] = True
                
                # Reset circuit breaker if it was open
                if not health.is_healthy and health.consecutive_failures > 0:
                    timeout_seconds = self.config.get('circuit_breaker_timeout_seconds', 300)
                    if (datetime.now() - health.last_check).total_seconds() > timeout_seconds:
                        health.is_healthy = True
                        health.consecutive_failures = 0
                        logger.info(f"Provider {provider_type.value} circuit breaker reset")
                
            except Exception as e:
                logger.error(f"Health check failed for {provider_type.value}: {e}")
                health_results[provider_type] = False
                
                # Update failure count
                health = self.provider_health[provider_type]
                health.consecutive_failures += 1
                health.last_check = datetime.now()
        
        return health_results
    
    def get_load_balancer_status(self) -> Dict[str, Any]:
        """Get comprehensive load balancer status"""
        current_usage = self.quota_manager.get_current_usage()
        projections = self.quota_manager.calculate_projections()
        
        # Calculate recent performance metrics
        recent_executions = self.execution_history[-100:] if self.execution_history else []
        
        total_executions = len(recent_executions)
        successful_executions = sum(1 for e in recent_executions if e['success'])
        avg_execution_time = sum(e['execution_time_ms'] for e in recent_executions) / total_executions if total_executions > 0 else 0
        total_cost = sum(e['cost_estimate'] for e in recent_executions)
        
        # Provider distribution
        provider_distribution = {}
        for execution in recent_executions:
            provider = execution['provider']
            provider_distribution[provider] = provider_distribution.get(provider, 0) + 1
        
        return {
            'timestamp': datetime.now().isoformat(),
            'strategy': self.strategy.value,
            'overall_health': all(health.is_healthy for health in self.provider_health.values()),
            'provider_health': {
                provider.value: {
                    'is_healthy': health.is_healthy,
                    'response_time_ms': round(health.response_time_ms, 2),
                    'error_rate': round(health.error_rate, 3),
                    'consecutive_failures': health.consecutive_failures,
                    'last_check': health.last_check.isoformat()
                }
                for provider, health in self.provider_health.items()
            },
            'recent_performance': {
                'total_executions': total_executions,
                'success_rate': round(successful_executions / total_executions, 3) if total_executions > 0 else 0,
                'average_execution_time_ms': round(avg_execution_time, 2),
                'total_cost_estimate': round(total_cost, 6),
                'provider_distribution': provider_distribution
            },
            'quota_status': {
                provider.value: {
                    'current_usage_percent': round((usage.executions_this_month / self.quota_manager.quota_limits[provider].monthly_executions) * 100, 2),
                    'projected_usage_percent': round((projection.projected_monthly_executions / self.quota_manager.quota_limits[provider].monthly_executions) * 100, 2),
                    'cost_this_month': round(usage.cost_this_month, 6)
                }
                for provider, usage in current_usage.items()
                for projection in [projections.get(provider)]
                if projection
            }
        }

def main():
    """Main function for testing and CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Intelligent Load Balancer')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--status', action='store_true', help='Show load balancer status')
    parser.add_argument('--health-check', action='store_true', help='Perform health check')
    parser.add_argument('--test-execution', help='Test function execution')
    parser.add_argument('--strategy', choices=['cost_optimized', 'performance', 'balanced', 'round_robin', 'least_connections'],
                       help='Set load balancing strategy')
    
    args = parser.parse_args()
    
    # Initialize load balancer
    balancer = IntelligentLoadBalancer(args.config)
    
    if args.strategy:
        balancer.strategy = LoadBalancingStrategy(args.strategy)
        print(f"Load balancing strategy set to: {args.strategy}")
    
    if args.status:
        status = balancer.get_load_balancer_status()
        print(json.dumps(status, indent=2))
    
    if args.health_check:
        async def run_health_check():
            results = await balancer.health_check_all_providers()
            for provider, is_healthy in results.items():
                status_emoji = "✅" if is_healthy else "❌"
                print(f"{status_emoji} {provider.value}: {'Healthy' if is_healthy else 'Unhealthy'}")
        
        asyncio.run(run_health_check())
    
    if args.test_execution:
        async def test_execution():
            request = FunctionRequest(
                function_name=args.test_execution,
                function_type=FunctionType.DAILY_SUMMARY,
                payload={"test": True},
                priority="normal"
            )
            
            result = await balancer.execute_function(request)
            print(f"Execution result: {result.success}")
            print(f"Provider: {result.provider.value}")
            print(f"Execution time: {result.execution_time_ms}ms")
            print(f"Cost estimate: ${result.cost_estimate:.6f}")
            if not result.success:
                print(f"Error: {result.error_message}")
        
        asyncio.run(test_execution())

if __name__ == "__main__":
    main()
