# 🚀 Deployment Functions

CI/CD and deployment automation functions for your personal system.

## 📁 Contents

- `cicd_orchestrator.py` - Automate deployments and CI/CD pipelines
- `gitea_webhook_handler.py` - Handle Git webhooks for automated deployments
- `data_sync_manager.py` - Manage data synchronization across systems

## 🎯 Purpose

These functions handle deployment and CI/CD automation:

- **CI/CD Orchestration**: Coordinate deployment pipelines
- **Webhook Handling**: Process Git webhooks for automated deployments
- **Data Synchronization**: Manage data sync across different systems

## ⏰ Triggers

- **CI/CD Orchestrator**: Triggered by webhooks or manual calls
- **Gitea Webhook Handler**: Triggered by Git push events
- **Data Sync Manager**: Runs on schedule or manual trigger

## 🔧 Configuration

```bash
# Git Configuration
GITEA_URL=your_gitea_url
GITEA_TOKEN=your_gitea_token
GITEA_WEBHOOK_SECRET=your_webhook_secret

# Deployment Configuration
COOLIFY_URL=your_coolify_url
COOLIFY_API_TOKEN=your_coolify_token
COOLIFY_PROJECT_UUID=your_project_uuid
COOLIFY_APPLICATION_UUID=your_app_uuid

# Database Configuration
CORE_SUPABASE_URL=your_supabase_url
CORE_SUPABASE_ANON_KEY=your_supabase_key
MAIN_SUPABASE_URL=your_main_supabase_url
MAIN_SUPABASE_ANON_KEY=your_main_supabase_key
```

## 🚀 Usage

### Local Testing

```bash
# Test CI/CD orchestrator
serverless invoke local --function cicd-orchestrator

# Test webhook handler
serverless invoke local --function gitea-webhook-handler

# Test data sync manager
serverless invoke local --function data-sync-manager
```

### Deployment

```bash
# Deploy all deployment functions
serverless deploy --function cicd-orchestrator
serverless deploy --function gitea-webhook-handler
serverless deploy --function data-sync-manager
```

## 🔄 Deployment Pipeline

1. **Git Push** → Triggers webhook
2. **Webhook Handler** → Validates and processes
3. **CI/CD Orchestrator** → Coordinates deployment
4. **Data Sync Manager** → Syncs data if needed
5. **Status Update** → Reports deployment status

## 📊 Features

### CI/CD Orchestrator
- Multi-stage deployment pipeline
- Rollback capabilities
- Health checks
- Status reporting

### Webhook Handler
- Git event processing
- Security validation
- Deployment triggering
- Error handling

### Data Sync Manager
- Cross-system synchronization
- Conflict resolution
- Backup management
- Integrity checks

## 🔒 Security

- Webhook signature validation
- Secure credential handling
- Minimal permissions
- Audit logging

## 🚨 Monitoring

- Deployment success/failure rates
- Execution times
- Error tracking
- Resource usage
