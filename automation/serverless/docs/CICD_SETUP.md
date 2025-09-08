# 🚀 Simplified Voice CI/CD Pipeline Setup

A streamlined CI/CD pipeline with single voice notifications for success/failure, keeping deployments fast and efficient.

## 🎯 What You'll Get

### Single Voice Notification
```
🎤 "✅ personal-system version 20241201.3 deployed successfully with 3 commits"
```

**Or on failure:**
```
🎤 "❌ Deployment failed for personal-system: validation error"
```

### Complete CI/CD Pipeline
- **Gitea Integration**: Automatic webhook triggers
- **Voice Feedback**: Every step announced via Telegram
- **Coolify Deployment**: Seamless production deployments
- **Version Tracking**: Automatic version numbering
- **Rollback Support**: Easy rollback on failures

## 📋 Prerequisites

### Required Services
- **Gitea**: Your Git server (already installed on Coolify)
- **Coolify**: Your deployment platform
- **ElevenLabs**: Voice generation (already configured)
- **Telegram**: Voice message delivery (already configured)
- **AWS Lambda**: Serverless functions (already set up)

### Environment Variables
Add these to your environment or `.env` file:

```bash
# Gitea Configuration
GITEA_URL=https://git.yourdomain.com
GITEA_TOKEN=your_gitea_personal_access_token
GITEA_WEBHOOK_SECRET=your_webhook_secret

# Coolify Configuration
COOLIFY_URL=https://coolify.yourdomain.com
COOLIFY_API_TOKEN=your_coolify_api_token
COOLIFY_PROJECT_UUID=your_project_uuid
COOLIFY_APPLICATION_UUID=your_application_uuid
```

## 🚀 Step-by-Step Setup

### Step 1: Deploy Lambda Functions

```bash
cd automation/serverless

# Deploy all functions including CI/CD
./run.sh deploy

# Verify deployment
serverless info --stage prod
```

### Step 2: Get Lambda Webhook URL

After deployment, get the webhook URL:

```bash
# Get the webhook endpoint URL
serverless info --stage prod | grep -A 5 "endpoints:"
```

It should look like:
```
endpoints:
  POST - https://your-lambda-url.amazonaws.com/prod/webhook/gitea
```

### Step 3: Configure Gitea Webhook

#### Option A: Using the Script (Recommended)

```bash
cd automation/serverless

# Run the webhook creation script
python3 gitea_webhook_handler.py create-webhook
```

You'll be prompted for:
- Repository owner
- Repository name
- Webhook URL (from Step 2)

#### Option B: Manual Configuration

1. Go to your Gitea repository
2. Navigate to **Settings** → **Webhooks**
3. Click **Add Webhook** → **Gitea**
4. Configure:
   - **Target URL**: `https://your-lambda-url.amazonaws.com/prod/webhook/gitea`
   - **POST Content Type**: `application/json`
   - **Secret**: `your_webhook_secret` (same as `GITEA_WEBHOOK_SECRET`)
   - **Trigger On**: Check `Push Events`

### Step 4: Configure Coolify

#### Get Required UUIDs

1. **Project UUID**: In Coolify, go to your project and copy the UUID from the URL
2. **Application UUID**: Go to your application and copy its UUID

#### API Token

1. In Coolify, go to **Keys & Tokens**
2. Create a new API token
3. Copy the token value

### Step 5: Test the Pipeline

```bash
cd automation/serverless

# Test webhook handling
./run.sh webhook-test

# Test Coolify connection
./run.sh coolify-list

# Manual deployment test
./run.sh cicd-deploy
```

### Step 6: Make Your First Commit

```bash
# Make a small change
echo "# Test deployment" >> README.md

# Commit and push
git add README.md
git commit -m "Test: Voice-enabled CI/CD deployment"
git push origin main
```

You should receive voice messages throughout the entire deployment process!

## 🎵 Voice Message Flow

### Success Notification
```
🎤 "✅ personal-system version 20241201.1 deployed successfully with 1 commit"
```

### Failure Notifications
```
🎤 "❌ Deployment failed for personal-system: validation error"
🎤 "❌ Deployment failed for personal-system: build error"
🎤 "❌ Deployment failed for personal-system: deployment error"
```

### Silent Operation
- All deployment steps run silently in the background
- Only success or failure notifications are sent
- No intermediate voice updates to avoid spam
- Fast, efficient deployment process

## ⚙️ Configuration Options

### Voice Settings

Customize the voice experience in `cicd_orchestrator.py`:

```python
# Change voice ID for different speakers
ELEVENLABS_VOICE_ID = "29vD33N1CtxCmqQRPOHJ"  # Drew (energetic)
ELEVENLABS_VOICE_ID = "2EiwWnXFnvU5JabPnv8n"  # Clyde (authoritative)
```

### Deployment Settings

Customize deployment behavior in `coolify_deployer.py`:

```python
# Adjust monitoring timeout
max_time = timeout_minutes * 60  # Default: 10 minutes

# Change health check frequency
time.sleep(10)  # Check every 10 seconds
```

### Notification Settings

Control notifications in `cicd_orchestrator.py`:

```python
# Enable/disable specific announcements
self._speak_notification("Starting deployment...")  # ✅ Enabled
# self._speak_notification("Internal step...")     # ❌ Comment out to disable
```

## 📊 Monitoring & Troubleshooting

### Check Deployment Status

```bash
# List recent deployments
./run.sh coolify-list

# Check specific deployment
./run.sh cicd-status <deployment_id>

# Get deployment logs
./run.sh cicd-logs <deployment_id>
```

### Voice Message History

```bash
# View recent voice messages
./run.sh voice-history

# Check system health
./run.sh monitor
```

### Common Issues

#### Webhook Not Triggering
```bash
# Check webhook delivery in Gitea
# Go to Repository Settings → Webhooks → Recent Deliveries

# Test webhook manually
curl -X POST https://your-lambda-url.amazonaws.com/prod/webhook/gitea \
  -H "Content-Type: application/json" \
  -H "X-Gitea-Event: push" \
  -d '{"test": "webhook"}'
```

#### Voice Messages Not Working
```bash
# Test ElevenLabs connection
./run.sh voice-test

# Check API key
echo $ELEVENLABS_API_KEY

# Test voice generation
python3 elevenlabs_tts.py test
```

#### Coolify Deployment Failing
```bash
# Check Coolify API token
curl -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
  $COOLIFY_URL/api/v1/user

# Verify application UUID
./run.sh coolify-list
```

## 🔄 Advanced Features

### Custom Deployment Scripts

Add custom deployment steps in `coolify_deployer.py`:

```python
def _custom_deployment_steps(self):
    """Add custom deployment logic"""
    # Run database migrations
    # Update configuration files
    # Restart dependent services
    # Send notifications to team
    pass
```

### Multi-Environment Support

Deploy to different environments:

```python
def deploy_to_staging(self):
    """Deploy to staging environment"""
    # Use different Coolify application UUID
    # Different configuration
    # Skip some validation steps
    pass
```

### Rollback Automation

Automatic rollback on failures:

```python
def auto_rollback_on_failure(self, deployment_id):
    """Rollback if deployment fails"""
    result = self.rollback_deployment(deployment_id)
    if result['success']:
        self._speak_notification("Rollback completed successfully.")
    else:
        self._speak_notification("Rollback failed. Manual intervention required.")
```

## 📈 Usage Statistics

### Voice Messages Per Deployment
- **Success**: 1 voice message (on successful deployment)
- **Failure**: 1 voice message (on deployment failure)
- **Total**: 1 voice message per deployment

### Cost Estimation
- **ElevenLabs**: ~$0.002 per deployment × 30 = **$0.06/month**
- **AWS Lambda**: ~$0.002 per deployment
- **Total Cost**: ~$0.004 per deployment
- **Monthly Cost**: ~$0.12 (30 deployments/month)

## 🎯 Production Checklist

- [ ] Lambda functions deployed and working
- [ ] Gitea webhook configured and tested
- [ ] Coolify API token and UUIDs configured
- [ ] ElevenLabs voice working
- [ ] Telegram notifications working
- [ ] Test deployment completed successfully
- [ ] Monitoring and logging configured
- [ ] Rollback procedures tested

## 🚨 Emergency Procedures

### Stop Deployments
```bash
# Disable webhook in Gitea
# Repository Settings → Webhooks → Uncheck "Active"

# Or remove webhook entirely
```

### Manual Deployment
```bash
# Deploy directly via Coolify dashboard
# Or use Coolify CLI
```

### Voice Override
```bash
# Disable voice notifications temporarily
# Comment out speak_notification calls in cicd_orchestrator.py
```

## 🎉 Success!

Your voice-enabled CI/CD pipeline is now active! Every time you push code to your main branch, you'll receive spoken updates throughout the entire deployment process.

**Experience**: Human-like voice guidance through your deployment workflow
**Transparency**: Every step explained clearly
**Reliability**: Automated deployment with comprehensive error handling
**Cost**: ~$0.008 per deployment

Your development workflow just became significantly more engaging and informative! 🎤✨
