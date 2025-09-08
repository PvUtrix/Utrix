#!/usr/bin/env python3
"""
Daily Projection Calculator for Multi-Tier Serverless Architecture
Recalculates monthly execution projections daily based on historical usage patterns,
trends, and seasonal variations. Provides intelligent forecasting for quota management.
"""

import json
import os
import logging
import sqlite3
from datetime import datetime, timedelta, date
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import numpy as np
from collections import defaultdict, deque
import statistics
import math

from multi_tier_quota_manager import (
    MultiTierQuotaManager, 
    ProviderType, 
    ExecutionProjection,
    QuotaUsage
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectionMethod(Enum):
    SIMPLE_AVERAGE = "simple_average"
    WEIGHTED_AVERAGE = "weighted_average"
    LINEAR_REGRESSION = "linear_regression"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    SEASONAL_DECOMPOSITION = "seasonal_decomposition"
    MACHINE_LEARNING = "machine_learning"

class TrendDirection(Enum):
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"

@dataclass
class HistoricalDataPoint:
    """Single data point in execution history"""
    timestamp: datetime
    provider: ProviderType
    function_type: str
    executions: int
    duration_ms: int
    memory_mb: int
    cost: float
    success_rate: float

@dataclass
class TrendAnalysis:
    """Analysis of execution trends"""
    provider: ProviderType
    trend_direction: TrendDirection
    trend_strength: float  # 0.0 to 1.0
    volatility: float  # Standard deviation of changes
    confidence: float  # 0.0 to 1.0
    period_days: int
    last_updated: datetime

@dataclass
class SeasonalPattern:
    """Seasonal pattern in execution data"""
    provider: ProviderType
    day_of_week_pattern: Dict[int, float]  # 0=Monday, 6=Sunday
    hour_of_day_pattern: Dict[int, float]  # 0-23
    monthly_pattern: Dict[int, float]  # 1-12
    pattern_strength: float  # 0.0 to 1.0
    last_updated: datetime

@dataclass
class ProjectionResult:
    """Result of projection calculation"""
    provider: ProviderType
    method: ProjectionMethod
    projected_monthly_executions: int
    projected_monthly_cost: float
    confidence_level: float
    trend_analysis: TrendAnalysis
    seasonal_adjustment: float
    risk_factors: List[str]
    alternative_projections: Dict[ProjectionMethod, int]
    last_calculated: datetime

class DailyProjectionCalculator:
    """Main projection calculator class"""
    
    def __init__(self, config_path: str = None, db_path: str = None):
        self.config = self._load_config(config_path)
        self.quota_manager = MultiTierQuotaManager(config_path)
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'projection_data.db')
        
        # Initialize database
        self._init_database()
        
        # Historical data cache
        self.historical_data = defaultdict(list)
        self.trend_analyses = {}
        self.seasonal_patterns = {}
        
        # Load existing data
        self._load_historical_data()
        self._load_trend_analyses()
        self._load_seasonal_patterns()
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration"""
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), 'projection_config.yaml')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'projection_methods': {
                'primary': 'weighted_average',
                'fallback': 'simple_average',
                'advanced': ['linear_regression', 'exponential_smoothing']
            },
            'data_retention_days': 365,
            'trend_analysis_window_days': 30,
            'seasonal_analysis_window_days': 90,
            'confidence_threshold': 0.7,
            'volatility_threshold': 0.3,
            'seasonal_adjustment_weight': 0.2,
            'trend_adjustment_weight': 0.3,
            'recalculation_hour': 2,  # 2 AM daily
            'min_data_points': 7,
            'outlier_detection': {
                'enabled': True,
                'z_score_threshold': 2.5,
                'iqr_multiplier': 1.5
            }
        }
    
    def _init_database(self):
        """Initialize SQLite database for storing historical data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS execution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                provider TEXT NOT NULL,
                function_type TEXT NOT NULL,
                executions INTEGER NOT NULL,
                duration_ms INTEGER NOT NULL,
                memory_mb INTEGER NOT NULL,
                cost REAL NOT NULL,
                success_rate REAL NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trend_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                trend_direction TEXT NOT NULL,
                trend_strength REAL NOT NULL,
                volatility REAL NOT NULL,
                confidence REAL NOT NULL,
                period_days INTEGER NOT NULL,
                last_updated DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seasonal_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                day_of_week_pattern TEXT NOT NULL,
                hour_of_day_pattern TEXT NOT NULL,
                monthly_pattern TEXT NOT NULL,
                pattern_strength REAL NOT NULL,
                last_updated DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projection_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                method TEXT NOT NULL,
                projected_monthly_executions INTEGER NOT NULL,
                projected_monthly_cost REAL NOT NULL,
                confidence_level REAL NOT NULL,
                seasonal_adjustment REAL NOT NULL,
                risk_factors TEXT NOT NULL,
                alternative_projections TEXT NOT NULL,
                last_calculated DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_execution_timestamp ON execution_history(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_execution_provider ON execution_history(provider)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_trend_provider ON trend_analyses(provider)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_seasonal_provider ON seasonal_patterns(provider)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_projection_provider ON projection_results(provider)')
        
        conn.commit()
        conn.close()
    
    def _load_historical_data(self):
        """Load historical execution data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Load last 365 days of data
        cutoff_date = datetime.now() - timedelta(days=self.config['data_retention_days'])
        
        cursor.execute('''
            SELECT timestamp, provider, function_type, executions, duration_ms, 
                   memory_mb, cost, success_rate
            FROM execution_history
            WHERE timestamp > ?
            ORDER BY timestamp
        ''', (cutoff_date,))
        
        for row in cursor.fetchall():
            data_point = HistoricalDataPoint(
                timestamp=datetime.fromisoformat(row[0]),
                provider=ProviderType(row[1]),
                function_type=row[2],
                executions=row[3],
                duration_ms=row[4],
                memory_mb=row[5],
                cost=row[6],
                success_rate=row[7]
            )
            
            self.historical_data[data_point.provider].append(data_point)
        
        conn.close()
        
        # Sort data by timestamp
        for provider_data in self.historical_data.values():
            provider_data.sort(key=lambda x: x.timestamp)
    
    def _load_trend_analyses(self):
        """Load trend analyses from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT provider, trend_direction, trend_strength, volatility, 
                   confidence, period_days, last_updated
            FROM trend_analyses
            ORDER BY last_updated DESC
        ''')
        
        for row in cursor.fetchall():
            trend = TrendAnalysis(
                provider=ProviderType(row[0]),
                trend_direction=TrendDirection(row[1]),
                trend_strength=row[2],
                volatility=row[3],
                confidence=row[4],
                period_days=row[5],
                last_updated=datetime.fromisoformat(row[6])
            )
            
            self.trend_analyses[trend.provider] = trend
        
        conn.close()
    
    def _load_seasonal_patterns(self):
        """Load seasonal patterns from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT provider, day_of_week_pattern, hour_of_day_pattern, 
                   monthly_pattern, pattern_strength, last_updated
            FROM seasonal_patterns
            ORDER BY last_updated DESC
        ''')
        
        for row in cursor.fetchall():
            pattern = SeasonalPattern(
                provider=ProviderType(row[0]),
                day_of_week_pattern=json.loads(row[1]),
                hour_of_day_pattern=json.loads(row[2]),
                monthly_pattern=json.loads(row[3]),
                pattern_strength=row[4],
                last_updated=datetime.fromisoformat(row[5])
            )
            
            self.seasonal_patterns[pattern.provider] = pattern
        
        conn.close()
    
    def add_execution_data(self, data_point: HistoricalDataPoint):
        """Add new execution data point"""
        # Add to memory cache
        self.historical_data[data_point.provider].append(data_point)
        
        # Sort by timestamp
        self.historical_data[data_point.provider].sort(key=lambda x: x.timestamp)
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO execution_history 
            (timestamp, provider, function_type, executions, duration_ms, 
             memory_mb, cost, success_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data_point.timestamp.isoformat(),
            data_point.provider.value,
            data_point.function_type,
            data_point.executions,
            data_point.duration_ms,
            data_point.memory_mb,
            data_point.cost,
            data_point.success_rate
        ))
        
        conn.commit()
        conn.close()
        
        # Clean up old data
        self._cleanup_old_data()
    
    def _cleanup_old_data(self):
        """Remove old data beyond retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.config['data_retention_days'])
        
        # Clean memory cache
        for provider_data in self.historical_data.values():
            self.historical_data[provider_data[0].provider] = [
                dp for dp in provider_data if dp.timestamp > cutoff_date
            ]
        
        # Clean database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM execution_history WHERE timestamp < ?', (cutoff_date,))
        
        conn.commit()
        conn.close()
    
    def calculate_trend_analysis(self, provider: ProviderType) -> TrendAnalysis:
        """Calculate trend analysis for a provider"""
        data_points = self.historical_data.get(provider, [])
        
        if len(data_points) < self.config['min_data_points']:
            return TrendAnalysis(
                provider=provider,
                trend_direction=TrendDirection.STABLE,
                trend_strength=0.0,
                volatility=0.0,
                confidence=0.0,
                period_days=len(data_points),
                last_updated=datetime.now()
            )
        
        # Get recent data for trend analysis
        window_days = self.config['trend_analysis_window_days']
        cutoff_date = datetime.now() - timedelta(days=window_days)
        recent_data = [dp for dp in data_points if dp.timestamp > cutoff_date]
        
        if len(recent_data) < 2:
            return TrendAnalysis(
                provider=provider,
                trend_direction=TrendDirection.STABLE,
                trend_strength=0.0,
                volatility=0.0,
                confidence=0.0,
                period_days=len(recent_data),
                last_updated=datetime.now()
            )
        
        # Calculate daily execution counts
        daily_executions = defaultdict(int)
        for dp in recent_data:
            day_key = dp.timestamp.date()
            daily_executions[day_key] += dp.executions
        
        # Sort by date
        sorted_days = sorted(daily_executions.keys())
        execution_values = [daily_executions[day] for day in sorted_days]
        
        # Calculate trend using linear regression
        n = len(execution_values)
        if n < 2:
            trend_direction = TrendDirection.STABLE
            trend_strength = 0.0
        else:
            x = list(range(n))
            y = execution_values
            
            # Simple linear regression
            x_mean = sum(x) / n
            y_mean = sum(y) / n
            
            numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                slope = 0
            else:
                slope = numerator / denominator
            
            # Determine trend direction and strength
            if abs(slope) < 0.1:
                trend_direction = TrendDirection.STABLE
                trend_strength = 0.0
            elif slope > 0:
                trend_direction = TrendDirection.INCREASING
                trend_strength = min(1.0, abs(slope) / (y_mean / n) if y_mean > 0 else 0.0)
            else:
                trend_direction = TrendDirection.DECREASING
                trend_strength = min(1.0, abs(slope) / (y_mean / n) if y_mean > 0 else 0.0)
        
        # Calculate volatility (coefficient of variation)
        if len(execution_values) > 1:
            mean_executions = statistics.mean(execution_values)
            std_executions = statistics.stdev(execution_values)
            volatility = std_executions / mean_executions if mean_executions > 0 else 0.0
        else:
            volatility = 0.0
        
        # Determine if trend is volatile
        if volatility > self.config['volatility_threshold']:
            trend_direction = TrendDirection.VOLATILE
        
        # Calculate confidence based on data quality
        confidence = min(1.0, len(recent_data) / (window_days * 0.8))  # 80% data coverage = full confidence
        
        trend_analysis = TrendAnalysis(
            provider=provider,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            volatility=volatility,
            confidence=confidence,
            period_days=len(recent_data),
            last_updated=datetime.now()
        )
        
        # Save to database
        self._save_trend_analysis(trend_analysis)
        
        return trend_analysis
    
    def _save_trend_analysis(self, trend: TrendAnalysis):
        """Save trend analysis to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO trend_analyses 
            (provider, trend_direction, trend_strength, volatility, 
             confidence, period_days, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            trend.provider.value,
            trend.trend_direction.value,
            trend.trend_strength,
            trend.volatility,
            trend.confidence,
            trend.period_days,
            trend.last_updated.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        # Update cache
        self.trend_analyses[trend.provider] = trend
    
    def calculate_seasonal_patterns(self, provider: ProviderType) -> SeasonalPattern:
        """Calculate seasonal patterns for a provider"""
        data_points = self.historical_data.get(provider, [])
        
        if len(data_points) < self.config['min_data_points']:
            return SeasonalPattern(
                provider=provider,
                day_of_week_pattern={i: 1.0 for i in range(7)},
                hour_of_day_pattern={i: 1.0 for i in range(24)},
                monthly_pattern={i: 1.0 for i in range(1, 13)},
                pattern_strength=0.0,
                last_updated=datetime.now()
            )
        
        # Get data for seasonal analysis
        window_days = self.config['seasonal_analysis_window_days']
        cutoff_date = datetime.now() - timedelta(days=window_days)
        recent_data = [dp for dp in data_points if dp.timestamp > cutoff_date]
        
        # Calculate patterns
        day_of_week_counts = defaultdict(int)
        hour_of_day_counts = defaultdict(int)
        monthly_counts = defaultdict(int)
        total_executions = 0
        
        for dp in recent_data:
            executions = dp.executions
            total_executions += executions
            
            day_of_week_counts[dp.timestamp.weekday()] += executions
            hour_of_day_counts[dp.timestamp.hour] += executions
            monthly_counts[dp.timestamp.month] += executions
        
        # Normalize patterns
        avg_daily = total_executions / 7 if total_executions > 0 else 1
        avg_hourly = total_executions / 24 if total_executions > 0 else 1
        avg_monthly = total_executions / 12 if total_executions > 0 else 1
        
        day_of_week_pattern = {
            i: day_of_week_counts[i] / avg_daily if avg_daily > 0 else 1.0
            for i in range(7)
        }
        
        hour_of_day_pattern = {
            i: hour_of_day_counts[i] / avg_hourly if avg_hourly > 0 else 1.0
            for i in range(24)
        }
        
        monthly_pattern = {
            i: monthly_counts[i] / avg_monthly if avg_monthly > 0 else 1.0
            for i in range(1, 13)
        }
        
        # Calculate pattern strength (how much variation there is)
        day_variance = statistics.variance(day_of_week_pattern.values()) if len(day_of_week_pattern) > 1 else 0
        hour_variance = statistics.variance(hour_of_day_pattern.values()) if len(hour_of_day_pattern) > 1 else 0
        month_variance = statistics.variance(monthly_pattern.values()) if len(monthly_pattern) > 1 else 0
        
        pattern_strength = (day_variance + hour_variance + month_variance) / 3
        
        seasonal_pattern = SeasonalPattern(
            provider=provider,
            day_of_week_pattern=day_of_week_pattern,
            hour_of_day_pattern=hour_of_day_pattern,
            monthly_pattern=monthly_pattern,
            pattern_strength=pattern_strength,
            last_updated=datetime.now()
        )
        
        # Save to database
        self._save_seasonal_pattern(seasonal_pattern)
        
        return seasonal_pattern
    
    def _save_seasonal_pattern(self, pattern: SeasonalPattern):
        """Save seasonal pattern to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO seasonal_patterns 
            (provider, day_of_week_pattern, hour_of_day_pattern, 
             monthly_pattern, pattern_strength, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            pattern.provider.value,
            json.dumps(pattern.day_of_week_pattern),
            json.dumps(pattern.hour_of_day_pattern),
            json.dumps(pattern.monthly_pattern),
            pattern.pattern_strength,
            pattern.last_updated.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        # Update cache
        self.seasonal_patterns[pattern.provider] = pattern
    
    def calculate_projection(self, provider: ProviderType, method: ProjectionMethod = None) -> ProjectionResult:
        """Calculate execution projection for a provider"""
        if method is None:
            method = ProjectionMethod(self.config['projection_methods']['primary'])
        
        data_points = self.historical_data.get(provider, [])
        
        if len(data_points) < self.config['min_data_points']:
            return self._create_fallback_projection(provider, method)
        
        # Get recent data
        window_days = 30  # Use last 30 days for projection
        cutoff_date = datetime.now() - timedelta(days=window_days)
        recent_data = [dp for dp in data_points if dp.timestamp > cutoff_date]
        
        if not recent_data:
            return self._create_fallback_projection(provider, method)
        
        # Calculate base projection using selected method
        base_projection = self._calculate_base_projection(recent_data, method)
        
        # Apply trend adjustment
        trend_analysis = self.calculate_trend_analysis(provider)
        trend_adjustment = self._calculate_trend_adjustment(base_projection, trend_analysis)
        
        # Apply seasonal adjustment
        seasonal_pattern = self.calculate_seasonal_patterns(provider)
        seasonal_adjustment = self._calculate_seasonal_adjustment(base_projection, seasonal_pattern)
        
        # Calculate final projection
        final_projection = int(base_projection * (1 + trend_adjustment + seasonal_adjustment))
        
        # Calculate confidence
        confidence = self._calculate_confidence(recent_data, trend_analysis, seasonal_pattern)
        
        # Calculate cost projection
        avg_cost_per_execution = statistics.mean([dp.cost / dp.executions for dp in recent_data if dp.executions > 0])
        projected_cost = final_projection * avg_cost_per_execution
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(trend_analysis, seasonal_pattern, confidence)
        
        # Calculate alternative projections
        alternative_projections = self._calculate_alternative_projections(recent_data, provider)
        
        result = ProjectionResult(
            provider=provider,
            method=method,
            projected_monthly_executions=final_projection,
            projected_monthly_cost=projected_cost,
            confidence_level=confidence,
            trend_analysis=trend_analysis,
            seasonal_adjustment=seasonal_adjustment,
            risk_factors=risk_factors,
            alternative_projections=alternative_projections,
            last_calculated=datetime.now()
        )
        
        # Save result
        self._save_projection_result(result)
        
        return result
    
    def _calculate_base_projection(self, data_points: List[HistoricalDataPoint], method: ProjectionMethod) -> float:
        """Calculate base projection using specified method"""
        if not data_points:
            return 0.0
        
        # Get daily execution totals
        daily_executions = defaultdict(int)
        for dp in data_points:
            day_key = dp.timestamp.date()
            daily_executions[day_key] += dp.executions
        
        execution_values = list(daily_executions.values())
        
        if method == ProjectionMethod.SIMPLE_AVERAGE:
            return statistics.mean(execution_values) * 30
        
        elif method == ProjectionMethod.WEIGHTED_AVERAGE:
            # Weight recent data more heavily
            weights = [i + 1 for i in range(len(execution_values))]
            weighted_sum = sum(val * weight for val, weight in zip(execution_values, weights))
            total_weight = sum(weights)
            return (weighted_sum / total_weight) * 30
        
        elif method == ProjectionMethod.LINEAR_REGRESSION:
            # Simple linear regression
            n = len(execution_values)
            if n < 2:
                return statistics.mean(execution_values) * 30
            
            x = list(range(n))
            y = execution_values
            
            x_mean = sum(x) / n
            y_mean = sum(y) / n
            
            numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                slope = 0
            else:
                slope = numerator / denominator
            
            # Project 30 days ahead
            future_x = n + 30
            projected_daily = y_mean + slope * (future_x - x_mean)
            return max(0, projected_daily * 30)
        
        elif method == ProjectionMethod.EXPONENTIAL_SMOOTHING:
            # Simple exponential smoothing
            alpha = 0.3  # Smoothing factor
            if not execution_values:
                return 0.0
            
            smoothed = execution_values[0]
            for value in execution_values[1:]:
                smoothed = alpha * value + (1 - alpha) * smoothed
            
            return smoothed * 30
        
        else:
            # Default to simple average
            return statistics.mean(execution_values) * 30
    
    def _calculate_trend_adjustment(self, base_projection: float, trend_analysis: TrendAnalysis) -> float:
        """Calculate trend-based adjustment to projection"""
        if trend_analysis.confidence < 0.5:
            return 0.0
        
        adjustment_weight = self.config['trend_adjustment_weight']
        
        if trend_analysis.trend_direction == TrendDirection.INCREASING:
            return trend_analysis.trend_strength * adjustment_weight
        elif trend_analysis.trend_direction == TrendDirection.DECREASING:
            return -trend_analysis.trend_strength * adjustment_weight
        else:
            return 0.0
    
    def _calculate_seasonal_adjustment(self, base_projection: float, seasonal_pattern: SeasonalPattern) -> float:
        """Calculate seasonal adjustment to projection"""
        if seasonal_pattern.pattern_strength < 0.1:
            return 0.0
        
        adjustment_weight = self.config['seasonal_adjustment_weight']
        
        # Get current month's pattern
        current_month = datetime.now().month
        monthly_factor = seasonal_pattern.monthly_pattern.get(current_month, 1.0)
        
        # Adjust based on how much current month differs from average
        return (monthly_factor - 1.0) * adjustment_weight
    
    def _calculate_confidence(self, data_points: List[HistoricalDataPoint], 
                            trend_analysis: TrendAnalysis, 
                            seasonal_pattern: SeasonalPattern) -> float:
        """Calculate confidence level for projection"""
        # Base confidence from data quality
        data_confidence = min(1.0, len(data_points) / 30)  # 30 days = full confidence
        
        # Adjust for trend confidence
        trend_confidence = trend_analysis.confidence
        
        # Adjust for seasonal pattern strength
        seasonal_confidence = min(1.0, seasonal_pattern.pattern_strength * 2)  # Normalize to 0-1
        
        # Combine confidences
        combined_confidence = (data_confidence * 0.5 + trend_confidence * 0.3 + seasonal_confidence * 0.2)
        
        return min(1.0, combined_confidence)
    
    def _identify_risk_factors(self, trend_analysis: TrendAnalysis, 
                             seasonal_pattern: SeasonalPattern, 
                             confidence: float) -> List[str]:
        """Identify risk factors that could affect projection accuracy"""
        risk_factors = []
        
        if confidence < self.config['confidence_threshold']:
            risk_factors.append("Low confidence due to insufficient data")
        
        if trend_analysis.volatility > self.config['volatility_threshold']:
            risk_factors.append("High volatility in execution patterns")
        
        if trend_analysis.trend_direction == TrendDirection.VOLATILE:
            risk_factors.append("Volatile trend direction")
        
        if seasonal_pattern.pattern_strength > 0.5:
            risk_factors.append("Strong seasonal patterns may affect accuracy")
        
        if trend_analysis.trend_strength > 0.7:
            risk_factors.append("Strong trend may lead to over/under-projection")
        
        return risk_factors
    
    def _calculate_alternative_projections(self, data_points: List[HistoricalDataPoint], 
                                         provider: ProviderType) -> Dict[ProjectionMethod, int]:
        """Calculate alternative projections using different methods"""
        alternatives = {}
        
        for method in ProjectionMethod:
            if method != ProjectionMethod(self.config['projection_methods']['primary']):
                try:
                    base_projection = self._calculate_base_projection(data_points, method)
                    alternatives[method] = int(base_projection)
                except Exception as e:
                    logger.warning(f"Failed to calculate alternative projection with {method.value}: {e}")
                    alternatives[method] = 0
        
        return alternatives
    
    def _create_fallback_projection(self, provider: ProviderType, method: ProjectionMethod) -> ProjectionResult:
        """Create fallback projection when insufficient data"""
        return ProjectionResult(
            provider=provider,
            method=method,
            projected_monthly_executions=1000,  # Conservative estimate
            projected_monthly_cost=0.01,  # Conservative cost estimate
            confidence_level=0.1,
            trend_analysis=TrendAnalysis(
                provider=provider,
                trend_direction=TrendDirection.STABLE,
                trend_strength=0.0,
                volatility=0.0,
                confidence=0.0,
                period_days=0,
                last_updated=datetime.now()
            ),
            seasonal_adjustment=0.0,
            risk_factors=["Insufficient historical data"],
            alternative_projections={},
            last_calculated=datetime.now()
        )
    
    def _save_projection_result(self, result: ProjectionResult):
        """Save projection result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projection_results 
            (provider, method, projected_monthly_executions, projected_monthly_cost,
             confidence_level, seasonal_adjustment, risk_factors, 
             alternative_projections, last_calculated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.provider.value,
            result.method.value,
            result.projected_monthly_executions,
            result.projected_monthly_cost,
            result.confidence_level,
            result.seasonal_adjustment,
            json.dumps(result.risk_factors),
            json.dumps({k.value: v for k, v in result.alternative_projections.items()}),
            result.last_calculated.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def calculate_all_projections(self) -> Dict[ProviderType, ProjectionResult]:
        """Calculate projections for all providers"""
        projections = {}
        
        for provider in ProviderType:
            if provider in self.quota_manager.providers:
                try:
                    projection = self.calculate_projection(provider)
                    projections[provider] = projection
                except Exception as e:
                    logger.error(f"Failed to calculate projection for {provider.value}: {e}")
                    projections[provider] = self._create_fallback_projection(provider, ProjectionMethod.SIMPLE_AVERAGE)
        
        return projections
    
    def get_projection_summary(self) -> Dict[str, Any]:
        """Get summary of all projections"""
        projections = self.calculate_all_projections()
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_providers': len(projections),
            'projections': {},
            'overall_confidence': 0.0,
            'total_projected_executions': 0,
            'total_projected_cost': 0.0,
            'risk_summary': {}
        }
        
        total_confidence = 0.0
        total_executions = 0
        total_cost = 0.0
        all_risk_factors = []
        
        for provider, projection in projections.items():
            summary['projections'][provider.value] = {
                'projected_monthly_executions': projection.projected_monthly_executions,
                'projected_monthly_cost': round(projection.projected_monthly_cost, 6),
                'confidence_level': round(projection.confidence_level, 3),
                'trend_direction': projection.trend_analysis.trend_direction.value,
                'trend_strength': round(projection.trend_analysis.trend_strength, 3),
                'seasonal_adjustment': round(projection.seasonal_adjustment, 3),
                'risk_factors': projection.risk_factors,
                'method': projection.method.value
            }
            
            total_confidence += projection.confidence_level
            total_executions += projection.projected_monthly_executions
            total_cost += projection.projected_monthly_cost
            all_risk_factors.extend(projection.risk_factors)
        
        # Calculate averages
        if projections:
            summary['overall_confidence'] = round(total_confidence / len(projections), 3)
        
        summary['total_projected_executions'] = total_executions
        summary['total_projected_cost'] = round(total_cost, 6)
        
        # Risk factor summary
        risk_counts = {}
        for risk in all_risk_factors:
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        summary['risk_summary'] = risk_counts
        
        return summary

def main():
    """Main function for testing and CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily Projection Calculator')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--db-path', help='Database file path')
    parser.add_argument('--calculate-all', action='store_true', help='Calculate projections for all providers')
    parser.add_argument('--provider', help='Calculate projection for specific provider')
    parser.add_argument('--method', choices=[m.value for m in ProjectionMethod], help='Projection method')
    parser.add_argument('--summary', action='store_true', help='Show projection summary')
    parser.add_argument('--add-test-data', action='store_true', help='Add test data for demonstration')
    
    args = parser.parse_args()
    
    # Initialize calculator
    calculator = DailyProjectionCalculator(args.config, args.db_path)
    
    if args.add_test_data:
        # Add some test data
        from datetime import datetime, timedelta
        import random
        
        for i in range(30):  # 30 days of test data
            for provider in ProviderType:
                data_point = HistoricalDataPoint(
                    timestamp=datetime.now() - timedelta(days=i),
                    provider=provider,
                    function_type="daily_summary",
                    executions=random.randint(10, 100),
                    duration_ms=random.randint(1000, 5000),
                    memory_mb=256,
                    cost=random.uniform(0.001, 0.01),
                    success_rate=random.uniform(0.95, 1.0)
                )
                calculator.add_execution_data(data_point)
        
        print("Test data added successfully")
    
    if args.calculate_all:
        projections = calculator.calculate_all_projections()
        for provider, projection in projections.items():
            print(f"{provider.value}: {projection.projected_monthly_executions} executions/month "
                  f"(confidence: {projection.confidence_level:.2f})")
    
    if args.provider:
        try:
            provider = ProviderType(args.provider)
            method = ProjectionMethod(args.method) if args.method else None
            projection = calculator.calculate_projection(provider, method)
            
            print(f"Provider: {provider.value}")
            print(f"Method: {projection.method.value}")
            print(f"Projected monthly executions: {projection.projected_monthly_executions}")
            print(f"Projected monthly cost: ${projection.projected_monthly_cost:.6f}")
            print(f"Confidence level: {projection.confidence_level:.2f}")
            print(f"Trend direction: {projection.trend_analysis.trend_direction.value}")
            print(f"Risk factors: {', '.join(projection.risk_factors)}")
            
        except ValueError as e:
            print(f"Invalid provider: {e}")
    
    if args.summary:
        summary = calculator.get_projection_summary()
        print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
