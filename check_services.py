#!/usr/bin/env python3
"""
Quick service status checker for deployed services
"""

import requests
import json
from datetime import datetime

def check_service(name, url, timeout=5):
    """Check if a service is responding."""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return {
                "name": name,
                "status": "✅ UP",
                "url": url,
                "response_time": f"{response.elapsed.total_seconds():.2f}s",
                "data": data
            }
        else:
            return {
                "name": name,
                "status": f"❌ DOWN (HTTP {response.status_code})",
                "url": url,
                "response_time": f"{response.elapsed.total_seconds():.2f}s"
            }
    except requests.exceptions.RequestException as e:
        return {
            "name": name,
            "status": f"❌ DOWN ({str(e)[:50]}...)",
            "url": url,
            "response_time": "N/A"
        }

def main():
    """Check all deployed services."""
    print("🔍 Personal System Service Status Check")
    print("=" * 50)
    print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define your services - update these URLs with your actual Coolify domains
    services = [
        ("Telegram Bot", "http://your-telegram-bot-domain:8000/health"),
        ("Personal API", "http://your-personal-api-domain:8000/health"),
        ("Health Dashboard", "http://your-health-dashboard-domain:8000/health"),
    ]
    
    # For now, let's check local services if they're running
    local_services = [
        ("Telegram Bot (Local)", "http://localhost:8000/health"),
        ("Personal API (Local)", "http://localhost:8001/health"),
        ("Health Dashboard (Local)", "http://localhost:8002/health"),
    ]
    
    print("🌐 Checking Local Services:")
    print("-" * 30)
    
    for name, url in local_services:
        result = check_service(name, url)
        print(f"{result['status']} {result['name']}")
        print(f"   URL: {result['url']}")
        print(f"   Response Time: {result['response_time']}")
        if 'data' in result:
            print(f"   Data: {json.dumps(result['data'], indent=2)}")
        print()
    
    print("📊 Service Summary:")
    print("-" * 20)
    
    # Count up/down services
    up_count = 0
    total_count = len(local_services)
    
    for name, url in local_services:
        result = check_service(name, url)
        if "✅" in result['status']:
            up_count += 1
    
    print(f"Services UP: {up_count}/{total_count}")
    print(f"Uptime: {(up_count/total_count)*100:.1f}%")
    
    if up_count == total_count:
        print("🎉 All services are running!")
    elif up_count > 0:
        print("⚠️  Some services are down")
    else:
        print("🚨 All services are down!")

if __name__ == "__main__":
    main()
