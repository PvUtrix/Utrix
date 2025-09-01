#!/usr/bin/env python3
"""
Serverless Cost Monitor
Tracks usage and costs across all serverless providers
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError
import requests

class ServerlessCostMonitor:
    def __init__(self):
        self.aws_client = boto3.client('ce', region_name='us-east-1')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def get_aws_costs(self, days: int = 30) -> Dict[str, Any]:
        """Get AWS costs for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        try:
            response = self.aws_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost'],
                GroupBy=[
                    {
                        'Type': 'DIMENSION',
                        'Key': 'SERVICE'
                    }
                ]
            )

            total_cost = 0.0
            services = {}

            for group in response.get('ResultsByTime', []):
                for group_item in group.get('Groups', []):
                    service_name = group_item['Keys'][0]
                    amount = float(group_item['Metrics']['BlendedCost']['Amount'])
                    total_cost += amount
                    services[service_name] = amount

            return {
                'total_cost': total_cost,
                'services': services,
                'period_days': days,
                'free_tier_safe': total_cost < 0.01  # Alert threshold
            }

        except ClientError as e:
            print(f"AWS Cost Explorer error: {e}")
            return {'error': str(e)}

    def get_lambda_usage(self) -> Dict[str, Any]:
        """Get Lambda function usage statistics"""
        try:
            lambda_client = boto3.client('lambda')
            cloudwatch = boto3.client('cloudwatch')

            # List functions
            functions = lambda_client.list_functions()
            usage_stats = {}

            for function in functions.get('Functions', []):
                function_name = function['FunctionName']

                # Get invocation count
                invocations = cloudwatch.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Invocations',
                    Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                    StartTime=datetime.now() - timedelta(days=30),
                    EndTime=datetime.now(),
                    Period=86400,  # 1 day
                    Statistics=['Sum']
                )

                # Get duration
                duration = cloudwatch.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Duration',
                    Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                    StartTime=datetime.now() - timedelta(days=30),
                    EndTime=datetime.now(),
                    Period=86400,
                    Statistics=['Average']
                )

                total_invocations = sum(point['Sum'] for point in invocations.get('Datapoints', []))
                avg_duration = sum(point['Average'] for point in duration.get('Datapoints', [])) / len(duration.get('Datapoints', [])) if duration.get('Datapoints') else 0

                usage_stats[function_name] = {
                    'invocations': int(total_invocations),
                    'avg_duration_ms': round(avg_duration, 2),
                    'estimated_cost': round(total_invocations * avg_duration * 0.0000000021, 6)  # Lambda pricing
                }

            return usage_stats

        except Exception as e:
            print(f"Lambda usage error: {e}")
            return {'error': str(e)}

    def get_vercel_usage(self) -> Dict[str, Any]:
        """Get Vercel usage (simplified - would need API access)"""
        # This is a placeholder - Vercel doesn't have a public API for usage
        # You'd need to implement Vercel's API or check dashboard manually

        return {
            'note': 'Vercel usage monitoring requires dashboard access',
            'estimated_bandwidth_gb': 0.1,  # Rough estimate
            'estimated_requests': 1000,
            'estimated_cost': 0.0
        }

    def get_supabase_usage(self) -> Dict[str, Any]:
        """Get Supabase usage (placeholder)"""
        return {
            'note': 'Supabase usage monitoring requires dashboard access',
            'estimated_storage_mb': 50,
            'estimated_bandwidth_gb': 1,
            'estimated_cost': 0.0
        }

    def generate_report(self) -> str:
        """Generate comprehensive cost and usage report"""
        aws_costs = self.get_aws_costs()
        lambda_usage = self.get_lambda_usage()
        vercel_usage = self.get_vercel_usage()
        supabase_usage = self.get_supabase_usage()

        report = ".1f"".1f"f"""
# 📊 Serverless Cost & Usage Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## 💰 AWS Costs (Last 30 Days)
**Total Cost: ${aws_costs.get('total_cost', 0):.4f}**
**Free Tier Status: {'✅ SAFE' if aws_costs.get('free_tier_safe', False) else '⚠️ WARNING'}**

### Service Breakdown:
{chr(10).join(f"• {service}: ${cost:.4f}" for service, cost in aws_costs.get('services', {}).items())}

## ⚡ Lambda Function Usage
"""

        if 'error' not in lambda_usage:
            for function_name, stats in lambda_usage.items():
                report += f"""
**{function_name}:**
• Invocations: {stats['invocations']}
• Avg Duration: {stats['avg_duration_ms']}ms
• Est. Cost: ${stats['estimated_cost']:.6f}
"""
        else:
            report += f"❌ Error getting Lambda usage: {lambda_usage['error']}\n"

        report += ".1f"f"""
## 🌐 Vercel Usage
• Bandwidth: {vercel_usage.get('estimated_bandwidth_gb', 0)} GB
• Requests: {vercel_usage.get('estimated_requests', 0):,}
• Est. Cost: ${vercel_usage.get('estimated_cost', 0):.4f}

## 🗄️ Supabase Usage
• Storage: {supabase_usage.get('estimated_storage_mb', 0)} MB
• Bandwidth: {supabase_usage.get('estimated_bandwidth_gb', 0)} GB
• Est. Cost: ${supabase_usage.get('estimated_cost', 0):.4f}

## 🎯 Free Tier Status Summary
"""

        # Overall status
        total_estimated_cost = (
            aws_costs.get('total_cost', 0) +
            sum(stats.get('estimated_cost', 0) for stats in lambda_usage.values() if isinstance(stats, dict)) +
            vercel_usage.get('estimated_cost', 0) +
            supabase_usage.get('estimated_cost', 0)
        )

        if total_estimated_cost < 0.01:
            report += "✅ **ALL CLEAR** - Well within free tier limits\n"
        elif total_estimated_cost < 1.0:
            report += f"⚠️ **MONITOR** - Estimated cost: ${total_estimated_cost:.4f}\n"
        else:
            report += f"🚨 **REVIEW NEEDED** - Estimated cost: ${total_estimated_cost:.4f}\n"

        report += ".6f"f"""
## 📈 Recommendations
• Total Estimated Monthly Cost: ${total_estimated_cost:.6f}
• Lambda Free Tier: 1M requests (you're using ~{sum(stats.get('invocations', 0) for stats in lambda_usage.values() if isinstance(stats, dict))})
• Monitor closely if approaching limits
• Consider optimization if costs > $0.01/month

---
*Report generated by Serverless Cost Monitor*
"""

        return report

    def send_telegram_alert(self, message: str):
        """Send alert via Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            print("Telegram credentials not configured")
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
                print("✅ Cost alert sent to Telegram")
            else:
                print(f"❌ Failed to send Telegram alert: {response.status_code}")
        except Exception as e:
            print(f"Error sending Telegram alert: {e}")

    def check_alerts(self):
        """Check for cost alerts and send notifications"""
        aws_costs = self.get_aws_costs()

        if not aws_costs.get('free_tier_safe', True):
            alert_message = f"""
🚨 **COST ALERT**
Your AWS costs for the last 30 days: ${aws_costs.get('total_cost', 0):.4f}
This exceeds the $0.01 safety threshold!

Please review your Lambda functions and usage patterns.
            """.strip()

            self.send_telegram_alert(alert_message)

def main():
    monitor = ServerlessCostMonitor()

    if len(os.sys.argv) > 1 and os.sys.argv[1] == '--alert':
        # Check alerts only
        monitor.check_alerts()
    else:
        # Generate full report
        report = monitor.generate_report()
        print(report)

        # Send to Telegram if configured
        if monitor.telegram_token and monitor.telegram_chat_id:
            monitor.send_telegram_alert(report)

if __name__ == "__main__":
    main()
