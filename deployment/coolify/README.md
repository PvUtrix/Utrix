# 🐳 Coolify Deployment Integration

Coolify deployment automation for containerized applications in your personal system.

## 📁 Contents

- `coolify_deployer.py` - Automated deployment handler for Coolify platform

## 🎯 Purpose

Coolify is a self-hosted alternative to Heroku/Vercel for container deployments. This integration provides:

- **Automated Deployments**: Trigger deployments from CI/CD pipelines
- **Status Tracking**: Monitor deployment progress and health
- **Rollback Support**: Quick rollback capabilities
- **Integration**: Seamless integration with your personal system

## 🚀 Usage

### Prerequisites

1. **Coolify Instance**: Self-hosted Coolify instance running
2. **API Token**: Coolify API token with deployment permissions
3. **Project Setup**: Project and application configured in Coolify

### Environment Variables

```bash
COOLIFY_URL=https://coolify.yourdomain.com
COOLIFY_API_TOKEN=your_api_token_here
COOLIFY_PROJECT_UUID=your_project_uuid
COOLIFY_APPLICATION_UUID=your_application_uuid
```

### Basic Usage

```python
from coolify_deployer import CoolifyDeployer

deployer = CoolifyDeployer()

# Deploy application
result = deployer.deploy_application(
    repo_name="my-app",
    version="v1.2.3",
    commit_info={
        "commit_hash": "abc123",
        "branch": "main",
        "message": "Feature: Add new functionality"
    }
)

if result['success']:
    print(f"✅ Deployment successful: {result['deployment_id']}")
else:
    print(f"❌ Deployment failed: {result['error']}")
```

## 🔧 Integration with Personal System

This Coolify deployer integrates with:

- **CI/CD Orchestrator**: Automated deployment triggers
- **Gitea Webhooks**: Git-based deployment triggers
- **Monitoring System**: Deployment status monitoring
- **Notification System**: Deployment success/failure alerts

## 📊 Features

- ✅ **Automated Deployments**: Trigger from webhooks or CI/CD
- ✅ **Status Monitoring**: Real-time deployment progress tracking
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Rollback Support**: Quick rollback to previous versions
- ✅ **Health Checks**: Post-deployment health verification
- ✅ **Integration Ready**: Works with existing personal system tools

## 🔒 Security

- **API Token Security**: Secure token storage and usage
- **HTTPS Only**: All communications encrypted
- **Minimal Permissions**: Least privilege access patterns
- **Audit Logging**: Complete deployment audit trail

## 📈 Monitoring

The deployer provides comprehensive monitoring:

- **Deployment Status**: Real-time status updates
- **Performance Metrics**: Deployment time and success rates
- **Error Tracking**: Detailed error logging and reporting
- **Health Checks**: Post-deployment verification

## 🛠️ Development

### Local Testing

```bash
# Test deployment locally
python3 coolify_deployer.py

# Test with mock data
python3 -c "
from coolify_deployer import CoolifyDeployer
deployer = CoolifyDeployer()
print(deployer._validate_config())
"
```

### Integration Testing

```bash
# Test with real Coolify instance
export COOLIFY_URL="https://your-coolify-instance.com"
export COOLIFY_API_TOKEN="your_token"
python3 coolify_deployer.py
```

## 📚 Documentation

- [Coolify Documentation](https://coolify.io/docs)
- [Coolify API Reference](https://coolify.io/docs/api)
- [Docker Deployment Guide](https://coolify.io/docs/docker)

## 🤝 Contributing

When extending this integration:

1. **Follow Security Best Practices**: Never expose API tokens
2. **Add Comprehensive Logging**: Log all deployment activities
3. **Handle Errors Gracefully**: Provide meaningful error messages
4. **Test Thoroughly**: Test with real Coolify instances
5. **Document Changes**: Update this README with new features

---

**Note**: This is part of the personal system's deployment automation. Coolify provides container deployment capabilities, complementing the serverless functions in the main automation system.