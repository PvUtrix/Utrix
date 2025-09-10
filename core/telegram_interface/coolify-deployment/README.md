# 🚀 Personal System Telegram Bot - Coolify Deployment

Complete deployment package for hosting your Personal System Telegram Bot on Coolify for 24/7 operation.

## 📁 Contents

This deployment package includes:

- `Dockerfile` - Optimized Docker image for production
- `docker-compose.yml` - Container orchestration configuration
- `config.yaml` - Environment-variable based configuration
- `env.example` - Environment variables template
- `coolify.yaml` - Coolify-specific deployment settings
- `requirements.txt` - Production-optimized Python dependencies
- `deploy-to-coolify.sh` - Automated deployment script
- `README.md` - This comprehensive guide

## 🎯 Quick Start

### Option 1: Automated Deployment (Recommended)

```bash
# Navigate to the deployment directory
cd core/telegram_interface/coolify-deployment

# Run the deployment script
./deploy-to-coolify.sh
```

The script will:
- ✅ Validate your configuration
- ✅ Create necessary deployment files
- ✅ Check Git status and commit changes
- ✅ Display step-by-step Coolify instructions

### Option 2: Manual Setup

1. **Copy deployment files to your bot directory**
2. **Configure environment variables**
3. **Push to Git repository**
4. **Configure Coolify application**

## 🔧 Prerequisites

### Required
- **Coolify Server**: Running Coolify instance
- **Git Repository**: Your code in a Git repository (GitHub, GitLab, Gitea)
- **Telegram Bot Token**: From @BotFather
- **Telegram User ID**: Your Telegram user ID

### Optional (for enhanced features)
- **OpenAI API Key**: For voice transcription
- **ElevenLabs API Key**: For advanced voice features

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Environment

1. **Get your Telegram Bot Token**:
   - Message @BotFather on Telegram
   - Create a new bot or use existing one
   - Copy the bot token

2. **Get your Telegram User ID**:
   - Message @userinfobot on Telegram
   - Copy your user ID

3. **Set up API keys** (optional):
   - OpenAI API key for voice transcription
   - ElevenLabs API key for advanced voice features

### Step 2: Configure Environment Variables

1. **Copy the environment template**:
   ```bash
   cp env.example .env
   ```

2. **Edit the .env file** with your actual values:
   ```bash
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   TELEGRAM_USER_ID=your_actual_user_id_here
   OPENAI_API_KEY=your_openai_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_key_here
   ```

### Step 3: Run Deployment Script

```bash
./deploy-to-coolify.sh
```

This will:
- Validate your configuration
- Create deployment files
- Commit changes to Git
- Display Coolify setup instructions

### Step 4: Configure Coolify Application

1. **Log into Coolify Dashboard**
   - Go to your Coolify instance
   - Click "New Application"

2. **Choose Application Type**
   - Select "Docker Compose" (recommended)
   - Or "Dockerfile" if you prefer

3. **Repository Configuration**
   - **Repository URL**: Your Git repository URL
   - **Branch**: `main`
   - **Build Path**: `core/telegram_interface`

4. **Environment Variables**
   Add these in Coolify environment variables:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_USER_ID=your_user_id_here
   OPENAI_API_KEY=your_openai_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_key_here
   HEALTH_CHECK_PORT=8000
   ```

5. **Build Configuration**
   - **Port**: `8000`
   - **Health Check**: `http://localhost:8000/health`
   - **Volume Mounts**:
     - `/app/data` → `./data`
     - `/app/logs` → `./logs`
     - `/app/config` → `./config`

### Step 5: Deploy and Test

1. **Deploy Application**
   - Click "Deploy" in Coolify
   - Monitor build logs
   - Wait for successful deployment

2. **Verify Deployment**
   - Check container status: `Running`
   - Review logs for any errors
   - Test health endpoint: `http://your-domain:8000/health`

3. **Test Bot Functionality**
   - Send `/start` to your bot
   - Test `/help` command
   - Try voice messages (if configured)
   - Test daily operations commands

## 🔍 Configuration Details

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Your Telegram bot token from @BotFather |
| `TELEGRAM_USER_ID` | ✅ | Your Telegram user ID |
| `OPENAI_API_KEY` | ❌ | OpenAI API key for voice transcription |
| `ELEVENLABS_API_KEY` | ❌ | ElevenLabs API key for voice features |
| `HEALTH_CHECK_PORT` | ❌ | Health check port (default: 8000) |
| `LOG_LEVEL` | ❌ | Logging level (default: INFO) |
| `ENVIRONMENT` | ❌ | Environment (default: production) |

### Volume Mounts

| Container Path | Host Path | Purpose |
|----------------|-----------|---------|
| `/app/data` | `./data` | Persistent bot data |
| `/app/logs` | `./logs` | Application logs |
| `/app/config` | `./config` | Configuration files |

### Health Check

- **Endpoint**: `http://localhost:8000/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3
- **Start Period**: 40 seconds

## 🛠️ Features

### Core Features
- ✅ **24/7 Operation**: Always-on bot availability
- ✅ **Voice Transcription**: OpenAI Whisper integration
- ✅ **Daily Operations**: Health tracking, task management
- ✅ **Shadow Work**: Personal development tracking
- ✅ **Journal Integration**: Knowledge management
- ✅ **System Status**: Health monitoring and alerts

### Production Features
- ✅ **Health Monitoring**: Automatic health checks
- ✅ **Log Management**: Structured logging with rotation
- ✅ **Auto Restart**: Container restart on failure
- ✅ **Resource Limits**: Memory and CPU constraints
- ✅ **Security**: Non-root user, read-only filesystem
- ✅ **Backup**: Automatic data backups

### Deployment Features
- ✅ **Zero Downtime**: Rolling updates
- ✅ **Auto Deploy**: Git-based deployments
- ✅ **Rollback**: Quick rollback capability
- ✅ **Monitoring**: Real-time status monitoring
- ✅ **Scaling**: Horizontal scaling support

## 🔧 Troubleshooting

### Common Issues

#### Bot Not Responding
```bash
# Check container logs
docker logs personal-telegram-bot

# Verify environment variables
docker exec personal-telegram-bot env | grep TELEGRAM

# Test bot connection
docker exec personal-telegram-bot python -c "from telegram import Bot; print('Bot token valid')"
```

#### Build Failures
```bash
# Check Dockerfile syntax
docker build -t test-bot .

# Verify all files are committed
git status

# Check build logs in Coolify
```

#### Permission Issues
```bash
# Fix volume permissions
docker exec personal-telegram-bot chown -R botuser:botuser /app/data

# Check file ownership
docker exec personal-telegram-bot ls -la /app/
```

#### Health Check Failures
```bash
# Test health endpoint manually
curl http://localhost:8000/health

# Check if health check service is running
docker exec personal-telegram-bot ps aux | grep health
```

### Debug Commands

```bash
# Access container shell
docker exec -it personal-telegram-bot /bin/bash

# View real-time logs
docker logs personal-telegram-bot -f

# Check resource usage
docker stats personal-telegram-bot

# Test bot functionality
docker exec personal-telegram-bot python -c "import main; print('Bot loaded successfully')"
```

## 📊 Monitoring and Maintenance

### Health Monitoring
- **Health Checks**: Every 30 seconds
- **Log Monitoring**: Real-time log access
- **Resource Monitoring**: CPU and memory usage
- **Alert System**: Failure notifications

### Log Management
- **Log Location**: `/app/logs/bot.log`
- **Log Rotation**: Automatic (10MB max, 5 backups)
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Access**: Through Coolify dashboard

### Updates and Maintenance
- **Automatic Deployments**: On git push to main
- **Zero Downtime**: Rolling updates
- **Rollback**: Available through Coolify
- **Maintenance Window**: Configurable

## 🔒 Security Considerations

### Data Protection
- **Environment Variables**: All secrets in environment variables
- **Encryption**: Sensitive data encryption enabled
- **No Hardcoded Secrets**: All credentials externalized
- **Secure Storage**: Volume mounts for persistent data

### Access Control
- **User Restrictions**: Bot limited to authorized users
- **Admin Commands**: Protected admin functionality
- **Privacy Markers**: Respect for private data
- **Network Isolation**: Container network isolation

### Container Security
- **Non-root User**: Runs as `botuser`
- **Minimal Image**: Slim Python base image
- **No Unnecessary Packages**: Minimal dependencies
- **Health Checks**: Automatic failure detection

## 💰 Cost Optimization

### Resource Usage
- **Memory Limit**: 512MB (adjustable)
- **CPU Limit**: 0.5 cores (adjustable)
- **Storage**: Efficient volume usage
- **Network**: Minimal bandwidth usage

### Monitoring
- **Resource Tracking**: Monitor usage patterns
- **Alert Thresholds**: Set up usage alerts
- **Optimization**: Adjust limits based on usage
- **Scaling**: Scale based on demand

## 🚀 Advanced Configuration

### Custom Environment Variables
Add custom variables to `coolify.yaml`:
```yaml
environment:
  custom:
    - "CUSTOM_VARIABLE"
    - "ANOTHER_VARIABLE"
```

### Scaling Configuration
```yaml
scaling:
  replicas:
    min: 1
    max: 5
    default: 2
  autoscaling:
    enabled: true
    cpu_threshold: 70
    memory_threshold: 80
```

### Backup Configuration
```yaml
backup:
  enabled: true
  schedule: "0 2 * * *"
  retention:
    daily: 7
    weekly: 4
    monthly: 12
```

## 📞 Support

### Getting Help
1. **Check Logs**: Review container and application logs
2. **Verify Configuration**: Ensure all environment variables are set
3. **Test Locally**: Run the bot locally to isolate issues
4. **Check Documentation**: Review this guide and Coolify docs

### Common Solutions
- **Restart Container**: Often resolves temporary issues
- **Check Environment Variables**: Ensure all required variables are set
- **Verify Git Repository**: Ensure all files are committed and pushed
- **Review Build Logs**: Check for build or deployment errors

## 🎉 Success!

Once deployed, your Personal System Telegram Bot will be:
- ✅ **Always Available**: 24/7 operation
- ✅ **Automatically Updated**: Git-based deployments
- ✅ **Monitored**: Health checks and logging
- ✅ **Scalable**: Ready for growth
- ✅ **Secure**: Production-ready security

Your bot is now ready to help you manage your personal system from anywhere, anytime! 🚀

---

**Need help?** Check the troubleshooting section or review the logs in your Coolify dashboard.
