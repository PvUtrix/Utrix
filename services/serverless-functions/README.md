# 🚀 Personal System Serverless Architecture

A privacy-focused, cost-optimized serverless setup for your personal automation system. Designed to stay within free tiers while providing reliable, event-driven automation.

## 📁 Project Structure

```
automation/serverless/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── functions/                   # Lambda functions organized by purpose
│   ├── daily/                  # Daily automation functions
│   │   ├── daily_summary_lambda.py
│   │   ├── daily_voice_lambda.py
│   │   └── daily_projection_calculator.py
│   ├── monitoring/             # Monitoring and health functions
│   │   ├── comprehensive_monitor.py
│   │   ├── cost_monitor.py
│   │   ├── data_monitor.py
│   │   └── data_lifecycle_manager.py
│   ├── deployment/             # CI/CD and deployment functions
│   │   ├── cicd_orchestrator.py
│   │   ├── gitea_webhook_handler.py
│   │   └── data_sync_manager.py
│   ├── voice/                  # Voice-related functions
│   │   ├── elevenlabs_tts.py
│   │   └── voice_content_generator.py
│   └── utilities/              # Utility functions
│       ├── home_server_archiver.py
│       ├── intelligent_load_balancer.py
│       ├── multi_tier_quota_manager.py
│       └── multi_tier_setup.py
├── configs/                    # All configuration files
│   ├── serverless.yml          # Main serverless configuration
│   ├── serverless_config_template.yaml
│   ├── load_balancer_config.yaml
│   ├── monitoring_config.yaml
│   ├── multi_tier_config.yaml
│   ├── multi_tier_quota_config.yaml
│   └── projection_config.yaml
├── scripts/                    # Deployment and setup scripts
│   ├── deploy.sh
│   ├── run.sh
│   ├── setup_env.sh
│   └── setup_serverless.sh
├── vercel/                     # Vercel-specific functions
│   ├── vercel_shadow_work.js
│   └── package.json
├── docs/                       # Documentation
│   ├── CICD_SETUP.md
│   ├── MULTI_TIER_README.md
│   └── VOICE_README.md
└── test_output.mp3             # Test audio file
```

## 🎯 What We've Accomplished

✅ **Complete serverless infrastructure ready**
✅ **All code tested and syntax errors fixed**
✅ **Dependencies installed and verified**
✅ **Comprehensive deployment scripts created**
✅ **Environment setup automation ready**
✅ **Cost monitoring and alerting configured**
✅ **Multi-tier database architecture implemented**
✅ **Organized structure by function purpose**

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Event Sources │───▶│ Serverless      │───▶│   Data Storage   │
│                 │    │   Functions     │    │                 │
│ • Time Triggers │    │ • AWS Lambda    │    │ • Supabase       │
│ • API Calls     │    │ • Vercel Edge   │    │ • Encrypted JSON │
│ • Webhooks      │    │ • Cloudflare    │    │ • Local Files    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                   ┌─────────────────┐
                   │ Notifications   │
                   │ • Telegram      │
                   │ • Email         │
                   │ • SMS (rare)    │
                   └─────────────────┘
```

## 🔧 Function Categories

### 📅 Daily Functions (`functions/daily/`)
- **Daily Summary Generator**: Generate daily health/productivity/finance summary
- **Daily Voice Generator**: Convert summaries to voice messages
- **Daily Projection Calculator**: Calculate daily projections and trends

### 📊 Monitoring Functions (`functions/monitoring/`)
- **Comprehensive Monitor**: Overall system health monitoring
- **Cost Monitor**: Track and alert on costs
- **Data Monitor**: Monitor data usage and health
- **Data Lifecycle Manager**: Manage data retention and archiving

### 🚀 Deployment Functions (`functions/deployment/`)
- **CI/CD Orchestrator**: Automate deployments and CI/CD pipelines
- **Gitea Webhook Handler**: Handle Git webhooks for automated deployments
- **Data Sync Manager**: Manage data synchronization across systems

### 🎤 Voice Functions (`functions/voice/`)
- **ElevenLabs TTS**: Text-to-speech conversion
- **Voice Content Generator**: Generate voice content from text

### 🛠️ Utility Functions (`functions/utilities/`)
- **Home Server Archiver**: Archive data to home server
- **Intelligent Load Balancer**: Smart load balancing
- **Multi-Tier Quota Manager**: Manage multi-tier database quotas
- **Multi-Tier Setup**: Setup multi-tier database architecture

## 🚀 Quick Start

### Prerequisites
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install Vercel CLI
npm install -g vercel

# Install Supabase CLI (optional)
npm install -g supabase
```

### 1. Set up Supabase (Free Database)
```bash
# Create Supabase project
supabase init
supabase start

# Get your project URL and anon key from dashboard
```

### 2. Configure Environment Variables
```bash
# Run the automated setup
./scripts/setup_env.sh

# Or manually copy template
cp configs/serverless_config_template.yaml .env
nano .env
```

### 3. Deploy Functions

#### AWS Lambda Deployment
```bash
# Install Serverless Framework
npm install -g serverless

# Configure AWS credentials
aws configure

# Deploy
serverless deploy --stage prod --config configs/serverless.yml
```

#### Vercel Deployment
```bash
# Login to Vercel
vercel login

# Deploy from vercel directory
cd vercel
vercel --prod
```

## 📊 Cost Monitoring

### Free Tier Limits (Current)
| Service | Free Limit | Your Usage | Status |
|---------|------------|------------|--------|
| AWS Lambda | 1M requests/month | ~30/day | ✅ Safe |
| Vercel | 100GB bandwidth | Minimal | ✅ Safe |
| Supabase | 500MB database | ~10MB/month | ✅ Safe |
| Telegram | Unlimited | Personal use | ✅ Safe |

### Monitoring Commands
```bash
# Check AWS costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-12-31 \
  --granularity MONTHLY \
  --metrics BlendedCost

# Check Lambda invocations
aws lambda get-function-configuration --function-name daily-summary

# Check Vercel usage
vercel usage
```

## 🔒 Privacy & Security

### Data Protection
- **Client-Side Encryption**: Sensitive data encrypted before storage
- **Minimal Retention**: Data deleted after 90 days (configurable)
- **No Analytics**: No tracking or analytics data collected
- **Local Processing**: Personal data processed locally when possible

### Security Measures
- **Environment Variables**: Secrets stored securely
- **IAM Roles**: Minimal permissions for each function
- **HTTPS Only**: All communications encrypted
- **Regular Audits**: Monthly security review

## 📈 Scaling Strategy

### Free Tier Optimization
1. **Execution Time**: Keep under 10 seconds per function
2. **Memory Usage**: Use minimal memory allocation
3. **Request Frequency**: Schedule rather than polling
4. **Data Volume**: Compress and minimize data transfer

### Scaling Triggers
- If Lambda costs exceed $0.01/month → Optimize function
- If Vercel bandwidth > 50GB/month → Compress responses
- If Supabase storage > 400MB → Archive old data

## 🛠️ Development Workflow

### Local Testing
```bash
# Test Lambda locally
serverless invoke local --function daily-summary --config configs/serverless.yml

# Test Vercel function
cd vercel
vercel dev

# Test with real data
python3 test_setup.py
```

### Deployment Pipeline
```bash
# Development
git checkout develop
# Make changes...

# Production
git checkout main
git merge develop
serverless deploy --stage prod --config configs/serverless.yml
cd vercel && vercel --prod
```

### Debugging
```bash
# AWS Logs
serverless logs --function daily-summary --tail --config configs/serverless.yml

# Vercel Logs
vercel logs

# Supabase Logs
supabase logs
```

## 🚨 Alerts & Monitoring

### Automatic Alerts
- **Cost Threshold**: Alert if any charges > $0.01
- **Function Errors**: Alert on >5% error rate
- **Timeout Alerts**: Alert on function timeouts
- **Storage Limits**: Alert when approaching limits

### Manual Monitoring
```bash
# Daily health check
./scripts/health_check.sh

# Weekly usage report
./scripts/weekly_report.sh

# Monthly cost review
./scripts/monthly_audit.sh
```

## 🔄 Migration Strategy

### Phase 1: Core Functions (Week 1)
- [x] Daily Summary Generator
- [x] Shadow Work Tracker
- [x] Basic health data collection

### Phase 2: Integration (Week 2)
- [x] Google Drive sync
- [x] Telegram bot integration
- [x] Calendar integration

### Phase 3: Optimization (Week 3)
- [x] Cost monitoring setup
- [x] Performance optimization
- [x] Backup strategy

### Phase 4: Advanced Features (Week 4)
- [x] AI insights (optional)
- [x] Advanced analytics
- [x] Multi-device sync

## 📚 Resources

### Documentation
- [AWS Lambda Free Tier](https://aws.amazon.com/free/)
- [Vercel Free Tier](https://vercel.com/pricing)
- [Supabase Free Tier](https://supabase.com/pricing)

### Tools
- [Serverless Framework](https://serverless.com/)
- [AWS CLI](https://aws.amazon.com/cli/)
- [Vercel CLI](https://vercel.com/docs/cli)

### Security
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security/)
- [Vercel Security](https://vercel.com/docs/security)

## 🤝 Contributing

This serverless setup is designed for personal use but can be extended. Follow these principles:

1. **Privacy First**: Never compromise user data
2. **Cost Conscious**: Always optimize for free tier
3. **Minimal Dependencies**: Keep functions lightweight
4. **Event-Driven**: React rather than poll
5. **Well-Documented**: Document all changes

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review function logs
3. Verify environment variables
4. Check free tier limits
5. Review cost monitoring

---

**Your personal automation system is now serverless and cost-optimized! 🎉**

## 🎯 Next Steps

1. **Run the setup**: `./scripts/setup_serverless.sh`
2. **Monitor deployment**: Check CloudWatch and Vercel dashboards
3. **Test functions**: Verify all integrations work
4. **Set up alerts**: Configure monitoring and notifications
5. **Optimize**: Review performance and costs

**Ready to deploy? Start with `./scripts/setup_env.sh` to configure your environment variables!**