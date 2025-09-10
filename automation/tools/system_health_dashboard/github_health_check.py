#!/usr/bin/env python3
"""
GitHub Environment Variables Health Check
Specialized health checker for GitHub Actions environment
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class GitHubSecretStatus:
    name: str
    is_set: bool
    is_valid: bool = False
    error_message: Optional[str] = None
    service_status: Optional[str] = None

@dataclass
class GitHubHealthReport:
    total_secrets: int
    configured_secrets: int
    valid_secrets: int
    failed_secrets: int
    overall_score: int
    last_updated: datetime
    recommendations: List[str]
    secret_details: List[GitHubSecretStatus]

class GitHubHealthChecker:
    """Health checker specifically for GitHub environment variables."""
    
    def __init__(self):
        self.secrets = self._get_required_secrets()
        self.report = None
    
    def _get_required_secrets(self) -> Dict[str, Dict[str, Any]]:
        """Get all required secrets with their validation info."""
        return {
            # Core Required Secrets
            "TELEGRAM_BOT_TOKEN": {
                "required": True,
                "description": "Telegram bot token for notifications",
                "validation_url": "https://api.telegram.org/bot{token}/getMe",
                "category": "core"
            },
            "TELEGRAM_CHAT_ID": {
                "required": True,
                "description": "Telegram chat ID for notifications",
                "validation_url": None,
                "category": "core"
            },
            "CORE_SUPABASE_URL": {
                "required": True,
                "description": "Supabase project URL",
                "validation_url": "{url}/rest/v1/",
                "category": "core"
            },
            "CORE_SUPABASE_ANON_KEY": {
                "required": True,
                "description": "Supabase anonymous key",
                "validation_url": None,
                "category": "core"
            },
            
            # Voice & AI Services (Optional)
            "ELEVENLABS_API_KEY": {
                "required": False,
                "description": "ElevenLabs voice synthesis API key",
                "validation_url": "https://api.elevenlabs.io/v1/voices",
                "category": "voice"
            },
            "OPENAI_API_KEY": {
                "required": False,
                "description": "OpenAI API key for AI features",
                "validation_url": "https://api.openai.com/v1/models",
                "category": "ai"
            },
            "ELEVENLABS_VOICE_ID": {
                "required": False,
                "description": "ElevenLabs voice ID",
                "validation_url": None,
                "category": "voice",
                "default": "21m00Tcm4TlvDq8ikWAM"
            },
            
            # AWS & Serverless (Optional)
            "AWS_ACCESS_KEY_ID": {
                "required": False,
                "description": "AWS access key for serverless functions",
                "validation_url": None,
                "category": "aws"
            },
            "AWS_SECRET_ACCESS_KEY": {
                "required": False,
                "description": "AWS secret key for serverless functions",
                "validation_url": None,
                "category": "aws"
            },
            "AWS_REGION": {
                "required": False,
                "description": "AWS region",
                "validation_url": None,
                "category": "aws",
                "default": "eu-central-1"
            },
            
            # Deployment (Optional)
            "COOLIFY_URL": {
                "required": False,
                "description": "Coolify instance URL",
                "validation_url": None,
                "category": "deployment"
            },
            "COOLIFY_API_TOKEN": {
                "required": False,
                "description": "Coolify API token",
                "validation_url": None,
                "category": "deployment"
            },
            "COOLIFY_PROJECT_UUID": {
                "required": False,
                "description": "Coolify project UUID",
                "validation_url": None,
                "category": "deployment"
            },
            "COOLIFY_APPLICATION_UUID": {
                "required": False,
                "description": "Coolify application UUID",
                "validation_url": None,
                "category": "deployment"
            },
            
            # Development (Optional)
            "GITEA_URL": {
                "required": False,
                "description": "Gitea instance URL",
                "validation_url": None,
                "category": "development"
            },
            "GITEA_TOKEN": {
                "required": False,
                "description": "Gitea API token",
                "validation_url": None,
                "category": "development"
            },
            "GITEA_WEBHOOK_SECRET": {
                "required": False,
                "description": "Gitea webhook secret",
                "validation_url": None,
                "category": "development"
            }
        }
    
    def check_secret_status(self, secret_name: str) -> GitHubSecretStatus:
        """Check the status of a single secret."""
        secret_info = self.secrets.get(secret_name, {})
        
        # Check if secret is set
        secret_value = os.getenv(secret_name)
        is_set = secret_value is not None
        
        status = GitHubSecretStatus(
            name=secret_name,
            is_set=is_set
        )
        
        if not is_set:
            if secret_info.get("required", False):
                status.error_message = "Required secret not set"
            else:
                status.error_message = "Optional secret not set"
            return status
        
        # Validate the secret if validation URL is provided
        validation_url = secret_info.get("validation_url")
        if validation_url:
            try:
                is_valid = self._validate_secret(secret_name, secret_value, validation_url)
                status.is_valid = is_valid
                if not is_valid:
                    status.error_message = "Secret validation failed"
                else:
                    status.service_status = "Connected"
            except Exception as e:
                status.is_valid = False
                status.error_message = f"Validation error: {str(e)}"
        else:
            # No validation URL, assume valid if set
            status.is_valid = True
            status.service_status = "Configured"
        
        return status
    
    def _validate_secret(self, secret_name: str, secret_value: str, validation_url: str) -> bool:
        """Validate a secret by making an API call."""
        import requests
        
        # Replace placeholders in validation URL
        if secret_name == "TELEGRAM_BOT_TOKEN":
            url = validation_url.format(token=secret_value)
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        
        elif secret_name == "CORE_SUPABASE_URL":
            url = validation_url.format(url=secret_value)
            headers = {
                'apikey': os.getenv('CORE_SUPABASE_ANON_KEY', ''),
                'Authorization': f'Bearer {os.getenv("CORE_SUPABASE_ANON_KEY", "")}'
            }
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        
        elif secret_name == "ELEVENLABS_API_KEY":
            headers = {'xi-api-key': secret_value}
            response = requests.get(validation_url, headers=headers, timeout=10)
            return response.status_code == 200
        
        elif secret_name == "OPENAI_API_KEY":
            headers = {'Authorization': f'Bearer {secret_value}'}
            response = requests.get(validation_url, headers=headers, timeout=10)
            return response.status_code == 200
        
        return True
    
    def generate_health_report(self) -> GitHubHealthReport:
        """Generate comprehensive health report for GitHub environment."""
        secret_statuses = []
        
        # Check all secrets
        for secret_name in self.secrets:
            status = self.check_secret_status(secret_name)
            secret_statuses.append(status)
        
        # Calculate metrics
        total_secrets = len(secret_statuses)
        configured_secrets = len([s for s in secret_statuses if s.is_set])
        valid_secrets = len([s for s in secret_statuses if s.is_set and s.is_valid])
        failed_secrets = len([s for s in secret_statuses if s.is_set and not s.is_valid])
        
        # Calculate overall score
        required_secrets = [s for s in secret_statuses if self.secrets[s.name].get("required", False)]
        required_configured = len([s for s in required_secrets if s.is_set and s.is_valid])
        required_total = len(required_secrets)
        
        if required_total == 0:
            overall_score = 100
        else:
            overall_score = int((required_configured / required_total) * 100)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(secret_statuses)
        
        self.report = GitHubHealthReport(
            total_secrets=total_secrets,
            configured_secrets=configured_secrets,
            valid_secrets=valid_secrets,
            failed_secrets=failed_secrets,
            overall_score=overall_score,
            last_updated=datetime.now(),
            recommendations=recommendations,
            secret_details=secret_statuses
        )
        
        return self.report
    
    def _generate_recommendations(self, secret_statuses: List[GitHubSecretStatus]) -> List[str]:
        """Generate recommendations based on secret status."""
        recommendations = []
        
        # Check required secrets
        required_failed = [s for s in secret_statuses 
                          if self.secrets[s.name].get("required", False) and not s.is_set]
        
        if required_failed:
            recommendations.append(f"🔴 {len(required_failed)} required secrets are missing")
            for secret in required_failed:
                recommendations.append(f"   - Set {secret.name}: {self.secrets[secret.name]['description']}")
        
        # Check failed validations
        validation_failed = [s for s in secret_statuses if s.is_set and not s.is_valid]
        if validation_failed:
            recommendations.append(f"⚠️  {len(validation_failed)} secrets failed validation")
            for secret in validation_failed:
                recommendations.append(f"   - Fix {secret.name}: {secret.error_message}")
        
        # Check optional services
        optional_services = {
            "voice": ["ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"],
            "ai": ["OPENAI_API_KEY"],
            "aws": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
            "deployment": ["COOLIFY_URL", "COOLIFY_API_TOKEN"]
        }
        
        for service, secrets in optional_services.items():
            service_secrets = [s for s in secret_statuses if s.name in secrets]
            configured_count = len([s for s in service_secrets if s.is_set])
            
            if configured_count == 0:
                recommendations.append(f"💡 Consider setting up {service} services for enhanced functionality")
            elif configured_count < len(secrets):
                recommendations.append(f"⚠️  {service} service partially configured")
        
        if not recommendations:
            recommendations.append("🎉 All secrets are properly configured!")
        
        return recommendations
    
    def print_report(self):
        """Print a formatted health report."""
        if not self.report:
            self.generate_health_report()
        
        report = self.report
        
        print(f"""
🔐 GITHUB ENVIRONMENT VARIABLES HEALTH CHECK
{'='*60}
📊 Overview
{'='*60}
🕐 Last Updated: {report.last_updated.strftime('%Y-%m-%d %H:%M:%S')}
📈 Overall Health Score: {report.overall_score}/100

📊 Secret Status Summary
{'='*60}
Total Secrets: {report.total_secrets}
✅ Configured: {report.configured_secrets}
✅ Valid: {report.valid_secrets}
❌ Failed: {report.failed_secrets}

🔧 Secret Details
{'='*60}
""")
        
        # Group secrets by category
        categories = {}
        for secret in report.secret_details:
            category = self.secrets[secret.name].get("category", "other")
            if category not in categories:
                categories[category] = []
            categories[category].append(secret)
        
        for category, secrets in categories.items():
            print(f"\n📁 {category.title()} Secrets:")
            print("-" * 40)
            
            for secret in secrets:
                if secret.is_set and secret.is_valid:
                    icon = "✅"
                    status = secret.service_status or "Configured"
                elif secret.is_set and not secret.is_valid:
                    icon = "❌"
                    status = "Validation Failed"
                elif not secret.is_set and self.secrets[secret.name].get("required", False):
                    icon = "🔴"
                    status = "Required - Not Set"
                else:
                    icon = "⚪"
                    status = "Optional - Not Set"
                
                print(f"{icon} {secret.name:<25} {status}")
                if secret.error_message:
                    print(f"    ⚠️  {secret.error_message}")
        
        print(f"\n💡 Recommendations\n{'='*60}")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"{i}. {rec}")
    
    def save_json_report(self, filename: str = None):
        """Save report as JSON file."""
        if not self.report:
            self.generate_health_report()
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"github_health_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(asdict(self.report), f, indent=2, default=str)
        
        print(f"📄 JSON report saved to: {filename}")

def main():
    """Main entry point for GitHub health checker."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitHub Environment Variables Health Check")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--save", help="Save report to file")
    parser.add_argument("--check", help="Check specific secret")
    
    args = parser.parse_args()
    
    checker = GitHubHealthChecker()
    
    if args.check:
        # Check specific secret
        status = checker.check_secret_status(args.check)
        print(f"Secret: {status.name}")
        print(f"Set: {status.is_set}")
        print(f"Valid: {status.is_valid}")
        if status.error_message:
            print(f"Error: {status.error_message}")
        if status.service_status:
            print(f"Status: {status.service_status}")
    elif args.json:
        # Output JSON
        report = checker.generate_health_report()
        print(json.dumps(asdict(report), indent=2, default=str))
    elif args.save:
        # Save report
        checker.generate_health_report()
        checker.save_json_report(args.save)
    else:
        # Print formatted report
        checker.print_report()

if __name__ == "__main__":
    main()

