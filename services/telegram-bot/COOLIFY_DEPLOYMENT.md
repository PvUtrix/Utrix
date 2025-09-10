# 🚀 Coolify Deployment Guide for Personal Telegram Bot

## Overview
This guide will help you deploy your Personal System Telegram Bot on Coolify for 24/7 operation.

## Prerequisites

### 1. Coolify Server Setup
- Coolify instance running and accessible
- Docker enabled on your Coolify server
- Git repository access (GitHub/GitLab)

### 2. Telegram Bot Setup
- Bot token from @BotFather
- Your Telegram user ID
- OpenAI API key (optional, for voice transcription)

## Deployment Steps

### Step 1: Prepare Your Repository

1. **Push to Git Repository**
   ```bash
   cd projects/personal_telegram_bot
   git add .
   git commit -m "Add Docker configuration for Coolify deployment"
   git push origin main
   ```

2. **Verify Files**
   Ensure these files are in your repository:
   - `Dockerfile`
   - `docker-compose.yml`
   - `requirements.txt`
   - `config/config.yaml.sample`

### Step 2: Coolify Configuration

1. **Create New Application**
   - Log into your Coolify dashboard
   - Click "New Application"
   - Select "Docker Compose" or "Dockerfile"

2. **Repository Setup**
   - Connect your Git repository
   - Set branch to `main`
   - Set build path to `projects/personal_telegram_bot`

3. **Environment Variables**
   Add these environment variables in Coolify:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_USER_ID=your_user_id_here
   OPENAI_API_KEY=your_openai_key_here (optional)
   ```

### Step 3: Build Configuration

1. **Dockerfile Settings**
   - Build context: `projects/personal_telegram_bot`
   - Dockerfile path: `Dockerfile`
   - Port: `8000`

2. **Volume Mounts**
   Configure these persistent volumes:
   ```
   /app/config -> ./config
   /app/data -> ./data
   /app/logs -> ./logs
   ```

### Step 4: Deploy

1. **Initial Deployment**
   - Click "Deploy" in Coolify
   - Monitor the build logs
   - Wait for successful deployment

2. **Verify Deployment**
   - Check container status
   - Review logs for any errors
   - Test bot functionality

## Configuration Management

### Environment-Based Configuration

Create a `config/config.yaml` that uses environment variables:

```yaml
telegram:
  bot_token: "${TELEGRAM_BOT_TOKEN}"
  allowed_users: [${TELEGRAM_USER_ID}]
  admin_users: [${TELEGRAM_USER_ID}]

openai:
  api_key: "${OPENAI_API_KEY}"
```

### Secrets Management

Store sensitive data in Coolify secrets:
- Bot tokens
- API keys
- Encryption keys

## Monitoring & Maintenance

### Health Checks
- Bot responds to `/status` command
- Container health check every 30s
- Automatic restart on failure

### Logs
- Access logs through Coolify dashboard
- Log files stored in `/app/logs/`
- Rotate logs automatically

### Updates
- Automatic deployments on git push
- Zero-downtime updates
- Rollback capability

## Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check bot token in environment variables
   - Verify user ID is correct
   - Check container logs

2. **Build Failures**
   - Verify all files are committed
   - Check Dockerfile syntax
   - Review build logs

3. **Permission Issues**
   - Ensure volume mounts have correct permissions
   - Check file ownership in container

### Debug Commands

```bash
# Check container status
docker ps

# View logs
docker logs personal-telegram-bot

# Access container shell
docker exec -it personal-telegram-bot /bin/bash

# Test bot manually
docker exec -it personal-telegram-bot python -c "import main; print('Bot loaded successfully')"
```

## Security Considerations

### Data Protection
- All sensitive data encrypted
- Environment variables for secrets
- No hardcoded credentials

### Access Control
- Bot restricted to authorized users
- Admin commands protected
- Privacy markers respected

### Network Security
- Container isolated in network
- Only necessary ports exposed
- Health check endpoint secured

## Backup Strategy

### Data Backup
- Volume mounts preserve data
- Regular backups of config and data
- Export functionality available

### Configuration Backup
- Git repository for version control
- Environment variables in Coolify
- Configuration files in volumes

## Scaling Considerations

### Resource Allocation
- Start with 512MB RAM, 0.5 CPU
- Monitor usage and adjust
- Consider auto-scaling for high load

### Performance Optimization
- Python async/await for efficiency
- Connection pooling for APIs
- Caching for frequently accessed data

## Cost Optimization

### Resource Usage
- Minimal resource footprint
- Efficient Python runtime
- Optimized Docker image

### Monitoring
- Track resource usage
- Set up alerts for high usage
- Optimize based on patterns

## Next Steps

1. **Deploy to Coolify** following this guide
2. **Test all bot commands** thoroughly
3. **Set up monitoring** and alerts
4. **Configure backups** for data safety
5. **Document any customizations** made

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review Coolify documentation
3. Check bot logs for errors
4. Verify configuration settings

---

**Your Personal System Telegram Bot is now ready for 24/7 operation on Coolify!** 🎉
