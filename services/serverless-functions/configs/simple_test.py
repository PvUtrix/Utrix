#!/usr/bin/env python3
"""
Simple test function for serverless deployment
"""

import json
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    Simple Lambda handler for testing deployment
    """
    try:
        # Get environment variables
        supabase_url = os.getenv('CORE_SUPABASE_URL', 'Not set')
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', 'Not set')
        
        # Create response
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Hello from refactored serverless function!',
                'timestamp': datetime.utcnow().isoformat(),
                'environment': {
                    'supabase_url_configured': bool(supabase_url and supabase_url != 'Not set'),
                    'telegram_token_configured': bool(telegram_token and telegram_token != 'Not set'),
                    'function_name': context.function_name,
                    'aws_request_id': context.aws_request_id
                },
                'deployment_status': 'SUCCESS - Refactored structure working!'
            })
        }
        
        return response
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Function execution failed'
            })
        }
