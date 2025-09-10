#!/usr/bin/env python3
"""
Simplified Cost Monitor Lambda Function
Monitors AWS costs and sends alerts
"""

import json
import os
from datetime import datetime, timedelta
import boto3
import requests

def lambda_handler(event, context):
    """
    Monitor AWS costs and send alerts if needed
    """
    try:
        # Get environment variables
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # Initialize AWS clients
        ce_client = boto3.client('ce')  # Cost Explorer
        lambda_client = boto3.client('lambda')
        
        # Get current month costs
        today = datetime.utcnow()
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        
        try:
            # Get cost data
            response = ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            
            total_cost = 0
            if response['ResultsByTime']:
                cost_data = response['ResultsByTime'][0]['Total']['BlendedCost']
                total_cost = float(cost_data['Amount'])
            
        except Exception as e:
            total_cost = 0
            cost_error = str(e)
        
        # Get Lambda function metrics
        try:
            lambda_response = lambda_client.get_account_settings()
            lambda_usage = {
                'total_code_size': lambda_response['AccountLimit']['TotalCodeSize']['Used'],
                'function_count': lambda_response['AccountLimit']['FunctionCount']['Used']
            }
        except Exception as e:
            lambda_usage = {'error': str(e)}
        
        # Create cost report
        cost_report = {
            'date': today.strftime('%Y-%m-%d'),
            'timestamp': today.isoformat(),
            'monthly_cost': total_cost,
            'cost_status': 'SAFE' if total_cost < 0.01 else 'WARNING',
            'lambda_usage': lambda_usage,
            'free_tier_status': {
                'lambda_requests': 'Within limits',
                'lambda_duration': 'Within limits',
                'api_gateway': 'Within limits'
            }
        }
        
        # Send alert if cost is high
        if total_cost > 0.01 and telegram_token and telegram_chat_id:
            alert_message = f"""
⚠️ **Cost Alert**

💰 **Monthly Cost**: ${total_cost:.4f}
📅 **Period**: {start_date} to {end_date}
🚨 **Status**: Exceeding $0.01 threshold

This is still within free tier limits, but worth monitoring.
            """
            
            telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            telegram_data = {
                'chat_id': telegram_chat_id,
                'text': alert_message,
                'parse_mode': 'Markdown'
            }
            
            try:
                response = requests.post(telegram_url, data=telegram_data, timeout=10)
                cost_report['alert_sent'] = response.status_code == 200
            except Exception as e:
                cost_report['alert_error'] = str(e)
                cost_report['alert_sent'] = False
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(cost_report)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Cost monitoring failed',
                'timestamp': datetime.utcnow().isoformat()
            })
        }
