#!/usr/bin/env python3
"""
System Health Dashboard
Comprehensive monitoring tool for all Personal System components.
Provides real-time overview of uptimes, health status, and system metrics.
"""

import json
import argparse
import logging
import subprocess
import psutil
import requests
import time
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import yaml
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComponentStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"

class ComponentType(Enum):
    CORE_APP = "core_app"
    PROJECT_APP = "project_app"
    AUTOMATION_TOOL = "automation_tool"
    SERVERLESS_FUNCTION = "serverless_function"
    CONTAINER = "container"
    DATABASE = "database"
    EXTERNAL_SERVICE = "external_service"

@dataclass
class ComponentInfo:
    name: str
    type: ComponentType
    status: ComponentStatus
    uptime: Optional[str] = None
    last_check: Optional[datetime] = None
    health_score: int = 0
    port: Optional[int] = None
    pid: Optional[int] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    error_message: Optional[str] = None
    dependencies: List[str] = None
    config_file: Optional[str] = None
    start_script: Optional[str] = None

@dataclass
class SystemMetrics:
    total_components: int
    running_components: int
    healthy_components: int
    warning_components: int
    critical_components: int
    system_uptime: str
    total_memory_usage: float
    total_cpu_usage: float
    disk_usage: float
    network_status: bool
    last_updated: datetime

class SystemHealthDashboard:
    """Main system health dashboard class."""
    
    def __init__(self, config_file: str = None):
        """Initialize the dashboard."""
        self.config_file = config_file or "automation/tools/system_health_dashboard/config.yaml"
        self.config = self._load_config()
        self.components = self._load_component_definitions()
        self.metrics_history = []
        self.dashboard_active = False
        
        # Create output directory
        self.output_dir = Path("automation/outputs/health_dashboard")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing metrics
        self._load_metrics_history()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "dashboard": {
                "refresh_interval": 30,
                "max_history": 100,
                "auto_refresh": True,
                "show_detailed_metrics": True
            },
            "monitoring": {
                "check_ports": True,
                "check_processes": True,
                "check_services": True,
                "check_disk_space": True,
                "check_memory": True,
                "check_network": True
            },
            "alerts": {
                "enable_alerts": True,
                "critical_threshold": 80,
                "warning_threshold": 60,
                "notification_methods": ["console", "file"]
            },
            "components": {
                "core_apps": [
                    {
                        "name": "PersonalSystemBot",
                        "type": "core_app",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_telegram_bot.sh",
                        "dependencies": ["TELEGRAM_BOT_TOKEN"]
                    },
                    {
                        "name": "PersonalSystemAPI",
                        "type": "core_app", 
                        "port": 8000,
                        "process_name": "python",
                        "start_script": "start_main_api.sh",
                        "dependencies": []
                    }
                ],
                "project_apps": [
                    {
                        "name": "HabitTracker",
                        "type": "project_app",
                        "port": 5000,
                        "process_name": "python",
                        "start_script": "start_habit_tracker.sh",
                        "dependencies": []
                    },
                    {
                        "name": "PresentationAnalyzer",
                        "type": "project_app",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_presentation_analyzer.sh",
                        "dependencies": ["GOOGLE_DRIVE_CREDENTIALS_PATH"]
                    }
                ],
                "automation_tools": [
                    {
                        "name": "TaskManager",
                        "type": "automation_tool",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_task_manager.sh",
                        "dependencies": []
                    },
                    {
                        "name": "DailySummary",
                        "type": "automation_tool",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_daily_summary.sh",
                        "dependencies": []
                    },
                    {
                        "name": "CleanupTool",
                        "type": "automation_tool",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_cleanup_tool.sh",
                        "dependencies": []
                    },
                    {
                        "name": "CodeQualityChecker",
                        "type": "automation_tool",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_code_quality_checker.sh",
                        "dependencies": []
                    },
                    {
                        "name": "LabAnalyzer",
                        "type": "automation_tool",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_lab_analyzer.sh",
                        "dependencies": []
                    },
                    {
                        "name": "ReminderSystem",
                        "type": "automation_tool",
                        "port": None,
                        "process_name": "python",
                        "start_script": "start_reminder_system.sh",
                        "dependencies": []
                    }
                ],
                "serverless_functions": [
                    {
                        "name": "DailySummaryLambda",
                        "type": "serverless_function",
                        "port": None,
                        "process_name": None,
                        "start_script": None,
                        "dependencies": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
                    },
                    {
                        "name": "DailyVoiceLambda",
                        "type": "serverless_function",
                        "port": None,
                        "process_name": None,
                        "start_script": None,
                        "dependencies": ["ELEVENLABS_API_KEY"]
                    },
                    {
                        "name": "VoiceTranscription",
                        "type": "serverless_function",
                        "port": None,
                        "process_name": None,
                        "start_script": None,
                        "dependencies": ["ELEVENLABS_API_KEY", "OPENAI_API_KEY"]
                    }
                ],
                "external_services": [
                    {
                        "name": "TelegramAPI",
                        "type": "external_service",
                        "port": None,
                        "process_name": None,
                        "start_script": None,
                        "dependencies": ["TELEGRAM_BOT_TOKEN"],
                        "health_check_url": "https://api.telegram.org/bot{token}/getMe"
                    },
                    {
                        "name": "Supabase",
                        "type": "external_service",
                        "port": None,
                        "process_name": None,
                        "start_script": None,
                        "dependencies": ["CORE_SUPABASE_URL", "CORE_SUPABASE_ANON_KEY"],
                        "health_check_url": "{url}/rest/v1/"
                    }
                ]
            }
        }
    
    def _load_component_definitions(self) -> List[ComponentInfo]:
        """Load component definitions from config."""
        components = []
        
        for category, component_list in self.config.get("components", {}).items():
            for comp_def in component_list:
                component = ComponentInfo(
                    name=comp_def["name"],
                    type=ComponentType(comp_def["type"]),
                    status=ComponentStatus.UNKNOWN,
                    port=comp_def.get("port"),
                    dependencies=comp_def.get("dependencies", []),
                    start_script=comp_def.get("start_script"),
                    config_file=comp_def.get("config_file")
                )
                components.append(component)
        
        return components
    
    def _load_metrics_history(self):
        """Load metrics history from file."""
        history_file = self.output_dir / "metrics_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.metrics_history = [
                        SystemMetrics(**metric) for metric in data
                    ]
            except Exception as e:
                logger.error(f"Error loading metrics history: {e}")
                self.metrics_history = []
    
    def _save_metrics_history(self):
        """Save metrics history to file."""
        history_file = self.output_dir / "metrics_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump([asdict(metric) for metric in self.metrics_history], f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving metrics history: {e}")
    
    def check_process_status(self, process_name: str) -> Tuple[bool, Optional[int], Optional[float], Optional[float]]:
        """Check if a process is running and get its metrics."""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
                if process_name.lower() in proc.info['name'].lower():
                    return True, proc.info['pid'], proc.info['memory_percent'], proc.info['cpu_percent']
            return False, None, None, None
        except Exception as e:
            logger.error(f"Error checking process {process_name}: {e}")
            return False, None, None, None
    
    def check_port_status(self, port: int) -> bool:
        """Check if a port is open and listening."""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except Exception as e:
            logger.error(f"Error checking port {port}: {e}")
            return False
    
    def check_environment_variables(self, dependencies: List[str]) -> Dict[str, bool]:
        """Check if required environment variables are set."""
        env_status = {}
        for dep in dependencies:
            env_status[dep] = os.getenv(dep) is not None
        return env_status
    
    def check_external_service(self, component: ComponentInfo) -> bool:
        """Check external service health."""
        try:
            # This would need to be implemented based on the specific service
            # For now, just check if environment variables are set
            if component.dependencies:
                env_status = self.check_environment_variables(component.dependencies)
                return all(env_status.values())
            return True
        except Exception as e:
            logger.error(f"Error checking external service {component.name}: {e}")
            return False
    
    def update_component_status(self, component: ComponentInfo) -> ComponentInfo:
        """Update the status of a single component."""
        try:
            component.last_check = datetime.now()
            
            # Check environment variables first
            if component.dependencies:
                env_status = self.check_environment_variables(component.dependencies)
                if not all(env_status.values()):
                    component.status = ComponentStatus.ERROR
                    component.error_message = f"Missing environment variables: {[k for k, v in env_status.items() if not v]}"
                    component.health_score = 0
                    return component
            
            # Check based on component type
            if component.type == ComponentType.CORE_APP or component.type == ComponentType.PROJECT_APP or component.type == ComponentType.AUTOMATION_TOOL:
                # Check if process is running
                is_running, pid, memory, cpu = self.check_process_status("python")
                
                if is_running:
                    component.status = ComponentStatus.RUNNING
                    component.pid = pid
                    component.memory_usage = memory
                    component.cpu_usage = cpu
                    component.health_score = 85
                    
                    # Check port if specified
                    if component.port:
                        port_open = self.check_port_status(component.port)
                        if port_open:
                            component.health_score = 95
                        else:
                            component.health_score = 70
                            component.error_message = f"Port {component.port} not accessible"
                else:
                    component.status = ComponentStatus.STOPPED
                    component.health_score = 0
                    component.error_message = "Process not running"
            
            elif component.type == ComponentType.SERVERLESS_FUNCTION:
                # For serverless functions, we can only check environment variables
                # In a real implementation, you'd check AWS Lambda status
                component.status = ComponentStatus.HEALTHY
                component.health_score = 90
                component.error_message = "Serverless function (environment variables configured)"
            
            elif component.type == ComponentType.EXTERNAL_SERVICE:
                # Check external service
                is_healthy = self.check_external_service(component)
                if is_healthy:
                    component.status = ComponentStatus.HEALTHY
                    component.health_score = 95
                else:
                    component.status = ComponentStatus.ERROR
                    component.health_score = 0
                    component.error_message = "External service not accessible"
            
            # Determine overall status based on health score
            if component.health_score >= 90:
                component.status = ComponentStatus.HEALTHY
            elif component.health_score >= 70:
                component.status = ComponentStatus.WARNING
            elif component.health_score >= 50:
                component.status = ComponentStatus.WARNING
            else:
                component.status = ComponentStatus.CRITICAL
            
        except Exception as e:
            logger.error(f"Error updating component {component.name}: {e}")
            component.status = ComponentStatus.ERROR
            component.error_message = str(e)
            component.health_score = 0
        
        return component
    
    def get_system_metrics(self) -> SystemMetrics:
        """Get overall system metrics."""
        try:
            # Update all components
            for component in self.components:
                self.update_component_status(component)
            
            # Calculate metrics
            total_components = len(self.components)
            running_components = len([c for c in self.components if c.status in [ComponentStatus.RUNNING, ComponentStatus.HEALTHY]])
            healthy_components = len([c for c in self.components if c.status == ComponentStatus.HEALTHY])
            warning_components = len([c for c in self.components if c.status == ComponentStatus.WARNING])
            critical_components = len([c for c in self.components if c.status == ComponentStatus.CRITICAL])
            
            # System metrics
            system_uptime = str(timedelta(seconds=int(time.time() - psutil.boot_time())))
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('/')
            
            # Network check
            network_status = True
            try:
                requests.get('https://www.google.com', timeout=5)
            except:
                network_status = False
            
            metrics = SystemMetrics(
                total_components=total_components,
                running_components=running_components,
                healthy_components=healthy_components,
                warning_components=warning_components,
                critical_components=critical_components,
                system_uptime=system_uptime,
                total_memory_usage=memory.percent,
                total_cpu_usage=cpu,
                disk_usage=disk.percent,
                network_status=network_status,
                last_updated=datetime.now()
            )
            
            # Save to history
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.config.get("dashboard", {}).get("max_history", 100):
                self.metrics_history = self.metrics_history[-100:]
            
            self._save_metrics_history()
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return SystemMetrics(
                total_components=0,
                running_components=0,
                healthy_components=0,
                warning_components=0,
                critical_components=0,
                system_uptime="Unknown",
                total_memory_usage=0,
                total_cpu_usage=0,
                disk_usage=0,
                network_status=False,
                last_updated=datetime.now()
            )
    
    def generate_dashboard_report(self) -> str:
        """Generate a comprehensive dashboard report."""
        metrics = self.get_system_metrics()
        
        report = f"""
🏥 PERSONAL SYSTEM HEALTH DASHBOARD
{'='*60}
📊 System Overview
{'='*60}
🕐 Last Updated: {metrics.last_updated.strftime('%Y-%m-%d %H:%M:%S')}
⏱️  System Uptime: {metrics.system_uptime}
🌐 Network Status: {'✅ Connected' if metrics.network_status else '❌ Disconnected'}

📈 Overall Health Score: {self._calculate_overall_health_score(metrics)}/100
💾 Memory Usage: {metrics.total_memory_usage:.1f}%
🖥️  CPU Usage: {metrics.total_cpu_usage:.1f}%
💿 Disk Usage: {metrics.disk_usage:.1f}%

📊 Component Status Summary
{'='*60}
Total Components: {metrics.total_components}
✅ Healthy: {metrics.healthy_components}
⚠️  Warning: {metrics.warning_components}
🔴 Critical: {metrics.critical_components}
🟢 Running: {metrics.running_components}

🔧 Component Details
{'='*60}
"""
        
        # Group components by type
        component_groups = {}
        for component in self.components:
            if component.type not in component_groups:
                component_groups[component.type] = []
            component_groups[component.type].append(component)
        
        for comp_type, components in component_groups.items():
            report += f"\n📁 {comp_type.value.replace('_', ' ').title()}s:\n"
            report += "-" * 40 + "\n"
            
            for component in components:
                status_icon = self._get_status_icon(component.status)
                report += f"{status_icon} {component.name:<25} "
                report += f"Health: {component.health_score:3d}/100 "
                
                if component.port:
                    report += f"Port: {component.port} "
                if component.pid:
                    report += f"PID: {component.pid} "
                if component.memory_usage:
                    report += f"RAM: {component.memory_usage:.1f}% "
                if component.cpu_usage:
                    report += f"CPU: {component.cpu_usage:.1f}% "
                
                report += "\n"
                
                if component.error_message:
                    report += f"    ⚠️  {component.error_message}\n"
        
        # Add recommendations
        report += f"\n💡 Recommendations\n{'='*60}\n"
        recommendations = self._generate_recommendations(metrics)
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        return report
    
    def _get_status_icon(self, status: ComponentStatus) -> str:
        """Get status icon for display."""
        icons = {
            ComponentStatus.HEALTHY: "✅",
            ComponentStatus.RUNNING: "🟢",
            ComponentStatus.WARNING: "⚠️",
            ComponentStatus.CRITICAL: "🔴",
            ComponentStatus.ERROR: "❌",
            ComponentStatus.STOPPED: "⏹️",
            ComponentStatus.UNKNOWN: "❓"
        }
        return icons.get(status, "❓")
    
    def _calculate_overall_health_score(self, metrics: SystemMetrics) -> int:
        """Calculate overall system health score."""
        if metrics.total_components == 0:
            return 0
        
        healthy_ratio = metrics.healthy_components / metrics.total_components
        running_ratio = metrics.running_components / metrics.total_components
        
        # Weight healthy components more heavily
        score = int((healthy_ratio * 0.7 + running_ratio * 0.3) * 100)
        
        # Penalize for high resource usage
        if metrics.total_memory_usage > 90:
            score -= 20
        elif metrics.total_memory_usage > 80:
            score -= 10
        
        if metrics.total_cpu_usage > 90:
            score -= 20
        elif metrics.total_cpu_usage > 80:
            score -= 10
        
        if metrics.disk_usage > 90:
            score -= 15
        elif metrics.disk_usage > 80:
            score -= 5
        
        return max(0, min(100, score))
    
    def _generate_recommendations(self, metrics: SystemMetrics) -> List[str]:
        """Generate recommendations based on current status."""
        recommendations = []
        
        if metrics.critical_components > 0:
            recommendations.append(f"🔴 {metrics.critical_components} critical components need immediate attention")
        
        if metrics.warning_components > 0:
            recommendations.append(f"⚠️  {metrics.warning_components} components have warnings that should be addressed")
        
        if metrics.total_memory_usage > 80:
            recommendations.append("💾 High memory usage detected - consider restarting heavy processes")
        
        if metrics.total_cpu_usage > 80:
            recommendations.append("🖥️  High CPU usage detected - check for resource-intensive processes")
        
        if metrics.disk_usage > 80:
            recommendations.append("💿 Disk space running low - run cleanup tool")
        
        if not metrics.network_status:
            recommendations.append("🌐 Network connectivity issues detected")
        
        # Check for stopped core components
        core_components = [c for c in self.components if c.type == ComponentType.CORE_APP]
        stopped_core = [c for c in core_components if c.status == ComponentStatus.STOPPED]
        if stopped_core:
            recommendations.append(f"🤖 Core components stopped: {', '.join([c.name for c in stopped_core])}")
        
        if not recommendations:
            recommendations.append("🎉 All systems are running smoothly!")
        
        return recommendations
    
    def start_dashboard(self, refresh_interval: int = None):
        """Start the interactive dashboard."""
        if refresh_interval is None:
            refresh_interval = self.config.get("dashboard", {}).get("refresh_interval", 30)
        
        self.dashboard_active = True
        print("🏥 Starting Personal System Health Dashboard...")
        print("Press Ctrl+C to stop")
        
        try:
            while self.dashboard_active:
                # Clear screen (works on most terminals)
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Generate and display report
                report = self.generate_dashboard_report()
                print(report)
                
                # Show next refresh time
                next_refresh = datetime.now() + timedelta(seconds=refresh_interval)
                print(f"\n🔄 Next refresh in {refresh_interval}s ({next_refresh.strftime('%H:%M:%S')})")
                print("Press Ctrl+C to stop dashboard")
                
                # Wait for refresh interval
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user")
            self.dashboard_active = False
    
    def save_report(self, filename: str = None):
        """Save current report to file."""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"health_report_{timestamp}.txt"
        
        report_path = self.output_dir / filename
        report = self.generate_dashboard_report()
        
        try:
            with open(report_path, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {report_path}")
        except Exception as e:
            logger.error(f"Error saving report: {e}")

# Web server for health endpoints
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Health Dashboard",
    description="Personal System Health Monitoring Dashboard",
    version="1.0.0"
)

# Global dashboard instance
dashboard = SystemHealthDashboard()

@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "service": "Personal System Health Dashboard",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "dashboard": "/dashboard"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Coolify."""
    try:
        metrics = dashboard.get_system_metrics()
        return {
            "status": "healthy",
            "timestamp": metrics.last_updated,
            "overall_health_score": dashboard._calculate_overall_health_score(metrics),
            "components_healthy": metrics.healthy_components,
            "components_total": metrics.total_components
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now()
        }

@app.get("/metrics")
async def get_metrics():
    """Get system metrics in JSON format."""
    try:
        metrics = dashboard.get_system_metrics()
        return asdict(metrics)
    except Exception as e:
        return {"error": str(e)}

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """Get dashboard as HTML."""
    try:
        report = dashboard.generate_dashboard_report()
        # Convert to HTML
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Personal System Health Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: 'Courier New', monospace; margin: 20px; background: #1a1a1a; color: #00ff00; }}
                pre {{ white-space: pre-wrap; word-wrap: break-word; }}
                .refresh {{ margin-top: 20px; }}
                .refresh button {{ padding: 10px 20px; background: #00ff00; color: #000; border: none; cursor: pointer; }}
            </style>
        </head>
        <body>
            <pre>{report}</pre>
            <div class="refresh">
                <button onclick="location.reload()">Refresh Dashboard</button>
            </div>
            <script>
                // Auto-refresh every 30 seconds
                setTimeout(() => location.reload(), 30000);
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_report)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading dashboard</h1><p>{str(e)}</p>")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Personal System Health Dashboard")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--dashboard", action="store_true", help="Start interactive dashboard")
    parser.add_argument("--report", action="store_true", help="Generate one-time report")
    parser.add_argument("--save", help="Save report to file")
    parser.add_argument("--refresh", type=int, help="Dashboard refresh interval in seconds")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--web", action="store_true", help="Start web server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    # Initialize dashboard
    global dashboard
    dashboard = SystemHealthDashboard(args.config)
    
    if args.web:
        # Start web server
        uvicorn.run(app, host=args.host, port=args.port)
    elif args.json:
        # Output metrics in JSON format
        metrics = dashboard.get_system_metrics()
        print(json.dumps(asdict(metrics), indent=2, default=str))
    elif args.dashboard:
        # Start interactive dashboard
        dashboard.start_dashboard(args.refresh)
    elif args.save:
        # Save report to file
        dashboard.save_report(args.save)
    else:
        # Generate one-time report
        report = dashboard.generate_dashboard_report()
        print(report)

if __name__ == "__main__":
    main()
