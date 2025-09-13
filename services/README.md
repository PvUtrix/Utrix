# 🚀 Personal System Services

This directory contains all deployable services for your personal system, organized for optimal deployment and management.

## 📁 Services Overview

### 🤖 **Telegram Bot** (`telegram-bot/`)
- **Purpose**: Primary user interface for your personal system
- **Port**: 8000
- **Features**: Voice commands, LLM-powered intent parsing, daily operations, automation integration
- **Deployment**: Coolify-ready with Docker Compose
- **Latest Features**: Configurable LLM models, Russian/English support, complex command parsing

### 🔌 **Personal API** (`personal-api/`)
- **Purpose**: Unified API interface for all personal data and services
- **Port**: 8001
- **Features**: Data access, automation triggers, analytics
- **Deployment**: FastAPI-based service

### 📊 **Health Dashboard** (`health-dashboard/`)
- **Purpose**: System health monitoring and analytics
- **Port**: 8002
- **Features**: Real-time monitoring, alerts, system metrics
- **Deployment**: Monitoring service

### ⚡ **Serverless Functions** (`serverless-functions/`)
- **Purpose**: AWS Lambda functions for automation
- **Features**: Daily summaries, voice processing, data sync
- **Deployment**: Serverless framework

## 🎯 **Deployment Strategy**

### **Option 1: Individual Service Deployment (Recommended)**
Deploy each service separately in Coolify:

```yaml
# Telegram Bot
Build Path: services/telegram-bot
Docker Compose: docker-compose.yaml
Port: 8000

# Personal API
Build Path: services/personal-api
Docker Compose: docker-compose.yaml
Port: 8001

# Health Dashboard
Build Path: services/health-dashboard
Docker Compose: docker-compose.yaml
Port: 8002
```

### **Option 2: Full System Deployment**
Deploy all services together using the main docker-compose.yaml:

```yaml
Build Path: . (root directory)
Docker Compose: docker-compose.yaml
Ports: 8000, 8001, 8002
```

## 🔧 **Environment Variables**

### **Required for All Services:**
```bash
# Core Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO

# API Keys
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

### **Telegram Bot Specific:**
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_USER_ID=your_user_id_here
HEALTH_CHECK_PORT=8000
```

### **Personal API Specific:**
```bash
DATABASE_URL=your_database_url_here
REDIS_URL=your_redis_url_here
JWT_SECRET_KEY=your_jwt_secret_here
API_KEY=your_api_key_here
```

### **Health Dashboard Specific:**
```bash
MONITORING_INTERVAL=300
ALERT_THRESHOLD=80
TELEGRAM_BOT_URL=http://telegram-bot:8000
PERSONAL_API_URL=http://personal-api:8000
```

## 🚀 **Quick Start**

### **1. Deploy Telegram Bot:**
```bash
# In Coolify:
# - Create new application
# - Set build path: services/telegram-bot
# - Use docker-compose.yaml
# - Set environment variables
# - Deploy!
```

### **2. Deploy Personal API:**
```bash
# In Coolify:
# - Create new application
# - Set build path: services/personal-api
# - Use docker-compose.yaml
# - Set environment variables
# - Deploy!
```

### **3. Deploy Health Dashboard:**
```bash
# In Coolify:
# - Create new application
# - Set build path: services/health-dashboard
# - Use docker-compose.yaml
# - Set environment variables
# - Deploy!
```

## 🔍 **Service Communication**

### **Internal Communication:**
- Services communicate via HTTP APIs
- Health dashboard monitors all services
- Telegram bot triggers API endpoints
- Shared data through volume mounts

### **External Communication:**
- Telegram bot: Telegram API
- Personal API: External service APIs
- Health dashboard: Monitoring endpoints
- Serverless functions: AWS services

## 📊 **Monitoring & Health Checks**

### **Health Endpoints:**
- Telegram Bot: `http://localhost:8000/health`
- Personal API: `http://localhost:8001/health`
- Health Dashboard: `http://localhost:8002/health`

### **Monitoring Features:**
- Automatic health checks every 30s
- Resource usage monitoring
- Service status tracking
- Alert notifications

## 🔒 **Security**

### **Container Security:**
- Non-root users for all services
- Minimal base images
- Resource limits
- Health checks

### **Network Security:**
- Internal service communication
- External API access only
- Environment variable secrets
- Volume isolation

## 📈 **Scaling**

### **Resource Limits:**
- Telegram Bot: 512MB RAM, 0.5 CPU
- Personal API: 512MB RAM, 0.5 CPU
- Health Dashboard: 256MB RAM, 0.25 CPU

### **Scaling Strategy:**
- Horizontal scaling per service
- Load balancing for high traffic
- Auto-scaling based on metrics
- Resource monitoring

## 🛠️ **Development**

### **Local Development:**
```bash
# Run individual service
cd services/telegram-bot
docker-compose up

# Run all services
docker-compose up
```

### **Testing:**
```bash
# Test health endpoints
curl http://localhost:8000/health  # Telegram Bot
curl http://localhost:8001/health  # Personal API
curl http://localhost:8002/health  # Health Dashboard
```

## 📝 **Maintenance**

### **Updates:**
- Git-based deployments
- Zero-downtime updates
- Rollback capability
- Health check validation

### **Backups:**
- Volume data backups
- Configuration backups
- Database backups
- Log retention

## 🎉 **Benefits of This Structure**

✅ **Modular**: Each service can be deployed independently
✅ **Scalable**: Services can be scaled individually
✅ **Maintainable**: Clear separation of concerns
✅ **Deployable**: Ready for Coolify deployment
✅ **Monitorable**: Built-in health checks and monitoring
✅ **Secure**: Production-ready security measures

---

**Your personal system is now organized for optimal deployment and management!** 🚀
