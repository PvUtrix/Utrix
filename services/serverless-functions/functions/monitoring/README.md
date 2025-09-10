# 📊 Monitoring Functions

System monitoring and health functions for your personal system.

## 📁 Contents

- `comprehensive_monitor.py` - Overall system health monitoring
- `cost_monitor.py` - Track and alert on costs
- `data_monitor.py` - Monitor data usage and health
- `data_lifecycle_manager.py` - Manage data retention and archiving

## 🎯 Purpose

These functions provide comprehensive monitoring capabilities:

- **System Health**: Monitor overall system performance
- **Cost Tracking**: Track usage and costs across services
- **Data Health**: Monitor data integrity and usage
- **Lifecycle Management**: Manage data retention and archiving

## ⏰ Schedule

- **Comprehensive Monitor**: Runs every 6 hours
- **Cost Monitor**: Runs daily at 2 AM UTC
- **Data Monitor**: Runs every 4 hours
- **Lifecycle Manager**: Runs weekly on Sunday at 3 AM UTC

## 🔧 Configuration

```bash
# AWS Configuration
AWS_REGION=eu-central-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Database Configuration
CORE_SUPABASE_URL=your_supabase_url
CORE_SUPABASE_ANON_KEY=your_supabase_key

# Alert Configuration
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 🚀 Usage

### Local Testing

```bash
# Test comprehensive monitoring
serverless invoke local --function comprehensive-monitor

# Test cost monitoring
serverless invoke local --function cost-monitor

# Test data monitoring
serverless invoke local --function data-monitor

# Test lifecycle management
serverless invoke local --function data-lifecycle-manager
```

### Deployment

```bash
# Deploy all monitoring functions
serverless deploy --function comprehensive-monitor
serverless deploy --function cost-monitor
serverless deploy --function data-monitor
serverless deploy --function data-lifecycle-manager
```

## 📊 Monitoring Metrics

### System Health
- Function execution times
- Error rates
- Memory usage
- Database connectivity

### Cost Tracking
- AWS Lambda costs
- Vercel usage
- Supabase storage
- Total monthly costs

### Data Health
- Database size
- Data integrity
- Backup status
- Sync status

## 🚨 Alerts

- **Cost Threshold**: Alert if costs exceed $0.01/month
- **Error Rate**: Alert if error rate > 5%
- **Storage Limit**: Alert when approaching storage limits
- **System Health**: Alert on system issues

## 🔒 Privacy

- No personal data in monitoring logs
- Aggregated metrics only
- Secure credential handling
