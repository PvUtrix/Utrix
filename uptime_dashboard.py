#!/usr/bin/env python3
"""
Personal System Uptime Dashboard
Monitors deployed services and provides a comprehensive status overview
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse

class ServiceMonitor:
    def __init__(self):
        self.services = {}
        self.uptime_data = {}
        
    def add_service(self, name: str, url: str, health_endpoint: str = "/health"):
        """Add a service to monitor."""
        self.services[name] = {
            "url": url,
            "health_endpoint": health_endpoint,
            "full_url": f"{url.rstrip('/')}{health_endpoint}",
            "status_history": [],
            "last_check": None,
            "uptime_percentage": 0.0
        }
    
    def check_service(self, name: str) -> Dict:
        """Check a single service."""
        if name not in self.services:
            return {"error": f"Service '{name}' not found"}
        
        service = self.services[name]
        start_time = time.time()
        
        try:
            response = requests.get(service["full_url"], timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                status = {
                    "name": name,
                    "status": "✅ HEALTHY",
                    "url": service["url"],
                    "response_time": f"{response_time:.2f}s",
                    "http_status": response.status_code,
                    "data": data,
                    "timestamp": datetime.now(),
                    "uptime": True
                }
            else:
                status = {
                    "name": name,
                    "status": f"❌ UNHEALTHY (HTTP {response.status_code})",
                    "url": service["url"],
                    "response_time": f"{response_time:.2f}s",
                    "http_status": response.status_code,
                    "timestamp": datetime.now(),
                    "uptime": False
                }
        except requests.exceptions.RequestException as e:
            status = {
                "name": name,
                "status": f"❌ DOWN ({str(e)[:50]}...)",
                "url": service["url"],
                "response_time": "N/A",
                "http_status": None,
                "timestamp": datetime.now(),
                "uptime": False
            }
        
        # Update service history
        service["status_history"].append(status)
        service["last_check"] = status["timestamp"]
        
        # Keep only last 100 checks
        if len(service["status_history"]) > 100:
            service["status_history"] = service["status_history"][-100:]
        
        # Calculate uptime percentage
        if service["status_history"]:
            uptime_count = sum(1 for check in service["status_history"] if check["uptime"])
            service["uptime_percentage"] = (uptime_count / len(service["status_history"])) * 100
        
        return status
    
    def check_all_services(self) -> List[Dict]:
        """Check all services."""
        results = []
        for name in self.services:
            result = self.check_service(name)
            results.append(result)
        return results
    
    def get_summary(self) -> Dict:
        """Get overall system summary."""
        if not self.services:
            return {"error": "No services configured"}
        
        total_services = len(self.services)
        healthy_services = 0
        total_uptime = 0.0
        
        for name, service in self.services.items():
            if service["last_check"] and service["last_check"]["uptime"]:
                healthy_services += 1
            total_uptime += service["uptime_percentage"]
        
        avg_uptime = total_uptime / total_services if total_services > 0 else 0
        
        return {
            "total_services": total_services,
            "healthy_services": healthy_services,
            "down_services": total_services - healthy_services,
            "overall_uptime": f"{avg_uptime:.1f}%",
            "last_check": datetime.now(),
            "status": "🟢 ALL HEALTHY" if healthy_services == total_services else "🟡 PARTIAL OUTAGE" if healthy_services > 0 else "🔴 ALL DOWN"
        }
    
    def print_dashboard(self):
        """Print a formatted dashboard."""
        print("🔍 Personal System Uptime Dashboard")
        print("=" * 60)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Check all services
        results = self.check_all_services()
        
        # Print individual service status
        print("📊 Service Status:")
        print("-" * 40)
        for result in results:
            print(f"{result['status']} {result['name']}")
            print(f"   URL: {result['url']}")
            print(f"   Response Time: {result['response_time']}")
            if result.get('http_status'):
                print(f"   HTTP Status: {result['http_status']}")
            if result.get('data'):
                print(f"   Health Data: {json.dumps(result['data'], indent=2)}")
            print()
        
        # Print summary
        summary = self.get_summary()
        print("📈 System Summary:")
        print("-" * 20)
        print(f"Status: {summary['status']}")
        print(f"Healthy Services: {summary['healthy_services']}/{summary['total_services']}")
        print(f"Overall Uptime: {summary['overall_uptime']}")
        print()
        
        # Print uptime percentages
        print("⏱️  Uptime Percentages:")
        print("-" * 25)
        for name, service in self.services.items():
            print(f"{name}: {service['uptime_percentage']:.1f}%")
        print()

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Personal System Uptime Dashboard")
    parser.add_argument("--watch", action="store_true", help="Watch mode - refresh every 30 seconds")
    parser.add_argument("--services", help="JSON file with service configurations")
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = ServiceMonitor()
    
    # Add your Coolify services here - replace with your actual domains
    # Example configuration:
    monitor.add_service("Telegram Bot", "https://your-telegram-bot-domain.com")
    monitor.add_service("Personal API", "https://your-personal-api-domain.com")
    monitor.add_service("Health Dashboard", "https://your-health-dashboard-domain.com")
    
    if args.watch:
        print("🔄 Starting watch mode (Ctrl+C to stop)...")
        try:
            while True:
                monitor.print_dashboard()
                print("⏳ Waiting 30 seconds...")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 Stopping monitor...")
    else:
        monitor.print_dashboard()

if __name__ == "__main__":
    main()
