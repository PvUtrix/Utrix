# 🚀 Personal System Deployment Guide

Complete guide for deploying your reorganized personal system services to Coolify.

## 📁 **New Repository Structure**

```
personal-system/
├── 📁 services/                    # Deployable services
│   ├── 📁 telegram-bot/           # Telegram bot service
│   ├── 📁 personal-api/           # Personal API service
│   ├── 📁 health-dashboard/       # Health monitoring service
│   └── 📁 serverless-functions/   # AWS Lambda functions
├── 📁 core/                       # Core data & knowledge
├── 📁 domains/                    # Life domains
├── 📁 projects/                   # Active projects
├── 📁 automation/                 # Automation scripts
├── 📁 config/                     # Configuration files
├── 📁 deployment/                 # Deployment configs
└── 📁 docs/                       # Documentation
```

## 🎯 **Deployment Options**

### **Option 1: Individual Service Deployment (Recommended)**

Deploy each service separately for better control and scaling.

#### **1. Telegram Bot Service**
```yaml
# Coolify Configuration:
Application Name: personal-telegram-bot
Build Path: services/telegram-bot
Docker Compose: docker-compose.yaml
Port: 8000
Health Check: http://localhost:8000/health

# Environment Variables:
TELEGRAM_BOT_TOKEN=8433928834:AAEVArfPyUMqh4z_mYLP3NMxkBQVmH3Up_4
TELEGRAM_USER_ID=71597815
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=sk_9382e4b7a49fa13e8334898360f9e3bd75ee67cfb27492fc
HEALTH_CHECK_PORT=8000
```

#### **2. Personal API Service**
```yaml
# Coolify Configuration:
Application Name: personal-api
Build Path: services/personal-api
Docker Compose: docker-compose.yaml
Port: 8001
Health Check: http://localhost:8000/health

# Environment Variables:
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
DATABASE_URL=your_database_url_here
REDIS_URL=your_redis_url_here
JWT_SECRET_KEY=your_jwt_secret_here
API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

#### **3. Health Dashboard Service**
```yaml
# Coolify Configuration:
Application Name: health-dashboard
Build Path: services/health-dashboard
Docker Compose: docker-compose.yaml
Port: 8002
Health Check: http://localhost:8000/health

# Environment Variables:
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8000
ENVIRONMENT=production
MONITORING_INTERVAL=300
ALERT_THRESHOLD=80
TELEGRAM_BOT_URL=http://your-telegram-bot-domain:8000
PERSONAL_API_URL=http://your-api-domain:8000
```

### **Option 2: Full System Deployment**

Deploy all services together using the main docker-compose.yaml.

```yaml
# Coolify Configuration:
Application Name: personal-system
Build Path: . (root directory)
Docker Compose: docker-compose.yaml
Ports: 8000, 8001, 8002

# Environment Variables: (All variables from above)
```

## 🔧 **Step-by-Step Deployment**

### **Step 1: Prepare Repository**
```bash
# Ensure all changes are committed and pushed
git add .
git commit -m "🚀 Reorganize into services structure"
git push origin main
```

### **Step 2: Deploy Telegram Bot**
1. **Create New Application** in Coolify
2. **Choose "Docker Compose"**
3. **Set Repository URL** to your Git repository
4. **Set Build Path** to: `services/telegram-bot`
5. **Add Environment Variables** (see above)
6. **Deploy**

### **Step 3: Deploy Personal API**
1. **Create New Application** in Coolify
2. **Choose "Docker Compose"**
3. **Set Repository URL** to your Git repository
4. **Set Build Path** to: `services/personal-api`
5. **Add Environment Variables** (see above)
6. **Deploy**

### **Step 4: Deploy Health Dashboard**
1. **Create New Application** in Coolify
2. **Choose "Docker Compose"**
3. **Set Repository URL** to your Git repository
4. **Set Build Path** to: `services/health-dashboard`
5. **Add Environment Variables** (see above)
6. **Deploy**

### **Step 5: Configure Service Communication**
1. **Update service URLs** in environment variables
2. **Test inter-service communication**
3. **Verify health checks**

## 🔍 **Verification & Testing**

### **Health Check Endpoints:**
```bash
# Test each service
curl http://your-telegram-bot-domain:8000/health
curl http://your-api-domain:8001/health
curl http://your-dashboard-domain:8002/health
```

### **Service Integration:**
1. **Test Telegram Bot** - Send `/start` command
2. **Test API Endpoints** - Check API documentation
3. **Test Dashboard** - Verify monitoring data
4. **Test Inter-service Communication** - Check logs

## 📊 **Monitoring & Maintenance**

### **Health Monitoring:**
- **Automatic Health Checks**: Every 30 seconds
- **Resource Monitoring**: CPU, memory, disk usage
- **Service Status**: Real-time status tracking
- **Alert System**: Failure notifications

### **Log Management:**
- **Centralized Logs**: Access through Coolify dashboard
- **Log Rotation**: Automatic log management
- **Error Tracking**: Monitor for issues
- **Performance Metrics**: Track service performance

### **Updates & Maintenance:**
- **Git-based Deployments**: Automatic on push
- **Zero-downtime Updates**: Rolling updates
- **Rollback Capability**: Quick rollback if needed
- **Backup Strategy**: Regular data backups

## 🔒 **Security Considerations**

### **Environment Variables:**
- Store all secrets in Coolify environment variables
- Never commit API keys to Git
- Use strong, unique secrets
- Rotate secrets regularly

### **Network Security:**
- Services communicate internally
- External access only through defined ports
- Health checks for security monitoring
- Resource limits to prevent abuse

### **Data Protection:**
- Encrypted data storage
- Secure volume mounts
- Regular backups
- Access control

## 🚀 **Benefits of New Structure**

### ✅ **Modular Deployment:**
- Deploy services independently
- Scale services individually
- Update services separately
- Isolate failures

### ✅ **Better Organization:**
- Clear service boundaries
- Easier maintenance
- Better testing
- Simplified debugging

### ✅ **Production Ready:**
- Health checks
- Resource limits
- Security measures
- Monitoring capabilities

### ✅ **Coolify Optimized:**
- Proper build paths
- Environment variables
- Volume mounts
- Health endpoints

## 🎯 **Next Steps**

1. **Deploy Telegram Bot** first (most critical)
2. **Test bot functionality** thoroughly
3. **Deploy Personal API** for data access
4. **Deploy Health Dashboard** for monitoring
5. **Configure inter-service communication**
6. **Set up monitoring and alerts**
7. **Test full system integration**

## 🆘 **Troubleshooting**

### **Common Issues:**
- **Build Failures**: Check Dockerfile and requirements
- **Health Check Failures**: Verify health endpoints
- **Service Communication**: Check environment variables
- **Resource Issues**: Monitor resource usage

### **Debug Commands:**
```bash
# Check service logs
docker logs personal-telegram-bot
docker logs personal-api
docker logs health-dashboard

# Test health endpoints
curl -v http://localhost:8000/health
curl -v http://localhost:8001/health
curl -v http://localhost:8002/health
```

---

**Your personal system is now ready for production deployment with optimal organization and scalability!** 🎉
