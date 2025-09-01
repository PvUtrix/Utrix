# 🚀 Personal System Serverless Architecture

A privacy-focused, cost-optimized serverless setup for your personal automation system. Designed to stay within free tiers while providing reliable, event-driven automation.

## 🎯 Design Philosophy

- **Privacy First**: All data encrypted, minimal retention, no tracking
- **Free Tier Optimized**: Designed to never exceed free tier limits
- **Event-Driven**: React to events rather than constant polling
- **Minimal Execution**: Keep functions fast and lightweight
- **Cost Transparent**: Clear monitoring and alerts for any charges

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

## 🔧 Current Functions

### 1. Daily Summary Generator (AWS Lambda)
- **Trigger**: Daily at 12 PM UTC
- **Runtime**: ~5 seconds
- **Memory**: 128MB
- **Cost**: Free (within Lambda free tier)
- **Purpose**: Generate daily health/productivity/finance summary

### 2. Shadow Work Tracker (Vercel Edge)
- **Trigger**: API calls from Telegram bot
- **Runtime**: ~2 seconds
- **Memory**: Minimal (Edge runtime)
- **Cost**: Free (within Vercel free tier)
- **Purpose**: Track shadow work insights and practices

### 3. Google Drive Sync (AWS Lambda)
- **Trigger**: Weekly on Monday at 2 AM UTC
- **Runtime**: ~45 seconds
- **Memory**: 256MB
- **Cost**: Free (within Lambda free tier)
- **Purpose**: Sync Google Drive files to local storage

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
# Copy template
cp serverless_config_template.yaml serverless_config.yaml

# Edit with your values
nano serverless_config.yaml
```

### 3. Deploy Functions

#### AWS Lambda Deployment
```bash
# Install Serverless Framework
npm install -g serverless

# Configure AWS credentials
aws configure

# Deploy
serverless deploy --stage prod
```

#### Vercel Deployment
```bash
# Login to Vercel
vercel login

# Deploy
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
serverless invoke local --function daily-summary

# Test Vercel function
vercel dev

# Test with real data
python test_serverless_functions.py
```

### Deployment Pipeline
```bash
# Development
git checkout develop
# Make changes...

# Production
git checkout main
git merge develop
serverless deploy --stage prod
vercel --prod
```

### Debugging
```bash
# AWS Logs
serverless logs --function daily-summary --tail

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
- [ ] Basic health data collection

### Phase 2: Integration (Week 2)
- [ ] Google Drive sync
- [ ] Telegram bot integration
- [ ] Calendar integration

### Phase 3: Optimization (Week 3)
- [ ] Cost monitoring setup
- [ ] Performance optimization
- [ ] Backup strategy

### Phase 4: Advanced Features (Week 4)
- [ ] AI insights (optional)
- [ ] Advanced analytics
- [ ] Multi-device sync

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
