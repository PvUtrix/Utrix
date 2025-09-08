# 🛠️ Utility Functions

Utility and helper functions for your personal system.

## 📁 Contents

- `home_server_archiver.py` - Archive data to home server
- `intelligent_load_balancer.py` - Smart load balancing
- `multi_tier_quota_manager.py` - Manage multi-tier database quotas
- `multi_tier_setup.py` - Setup multi-tier database architecture

## 🎯 Purpose

These functions provide utility services and system management:

- **Data Archiving**: Archive old data to home server
- **Load Balancing**: Intelligent load distribution
- **Quota Management**: Manage database quotas across tiers
- **System Setup**: Automated system configuration

## ⏰ Schedule

- **Home Server Archiver**: Runs weekly on Sunday at 4 AM UTC
- **Load Balancer**: Runs continuously (event-driven)
- **Quota Manager**: Runs daily at 3 AM UTC
- **Multi-Tier Setup**: Runs on-demand or during initial setup

## 🔧 Configuration

```bash
# Home Server Configuration
HOME_SERVER_URL=your_home_server_url
HOME_SERVER_TOKEN=your_home_server_token
ARCHIVE_PATH=/path/to/archive

# Load Balancer Configuration
LOAD_BALANCER_ALGORITHM=round_robin
HEALTH_CHECK_INTERVAL=30
MAX_RETRIES=3

# Database Configuration
CORE_SUPABASE_URL=your_core_supabase_url
MAIN_SUPABASE_URL=your_main_supabase_url
ARCHIVE_SUPABASE_URL=your_archive_supabase_url

# Quota Configuration
CORE_QUOTA_LIMIT=500MB
MAIN_QUOTA_LIMIT=10GB
ARCHIVE_QUOTA_LIMIT=100GB
```

## 🚀 Usage

### Local Testing

```bash
# Test home server archiver
serverless invoke local --function home-server-archiver

# Test load balancer
serverless invoke local --function intelligent-load-balancer

# Test quota manager
serverless invoke local --function multi-tier-quota-manager

# Test multi-tier setup
serverless invoke local --function multi-tier-setup
```

### Deployment

```bash
# Deploy utility functions
serverless deploy --function home-server-archiver
serverless deploy --function intelligent-load-balancer
serverless deploy --function multi-tier-quota-manager
serverless deploy --function multi-tier-setup
```

## 🏗️ Multi-Tier Architecture

### Tier Structure
1. **Core Tier** (Free Supabase): Active data, fast access
2. **Main Tier** (Self-hosted): Historical data, medium access
3. **Archive Tier** (Home Server): Long-term storage, slow access

### Data Flow
```
Active Data → Core Tier → Main Tier → Archive Tier
     ↑           ↑           ↑           ↑
  Fast Access  Free Tier  Historical  Long-term
```

## 📊 Features

### Home Server Archiver
- **Automated Archiving**: Move old data to home server
- **Compression**: Compress archived data
- **Integrity Checks**: Verify archived data integrity
- **Restore Capability**: Restore archived data when needed

### Intelligent Load Balancer
- **Health Monitoring**: Monitor service health
- **Traffic Distribution**: Distribute traffic intelligently
- **Failover**: Automatic failover to healthy services
- **Performance Optimization**: Optimize based on performance metrics

### Quota Manager
- **Usage Monitoring**: Monitor quota usage across tiers
- **Automatic Migration**: Move data when quotas are reached
- **Cost Optimization**: Optimize costs by tier usage
- **Alert System**: Alert when approaching limits

### Multi-Tier Setup
- **Automated Configuration**: Set up multi-tier architecture
- **Database Migration**: Migrate data between tiers
- **Index Optimization**: Optimize database indexes
- **Performance Tuning**: Tune performance for each tier

## 🔒 Security

- **Encrypted Storage**: All data encrypted at rest
- **Secure Transfer**: Encrypted data transfer
- **Access Control**: Role-based access control
- **Audit Logging**: Complete audit trail

## 📈 Performance

### Optimization Strategies
- **Caching**: Intelligent caching at each tier
- **Indexing**: Optimized database indexes
- **Compression**: Data compression for storage
- **Batch Processing**: Batch operations for efficiency

### Monitoring
- **Performance Metrics**: Track performance across tiers
- **Usage Statistics**: Monitor usage patterns
- **Cost Tracking**: Track costs per tier
- **Health Status**: Monitor system health

## 🛠️ Development

### Testing Multi-Tier Setup

```bash
# Test tier configuration
python3 -c "
from multi_tier_setup import MultiTierSetup
setup = MultiTierSetup()
setup.validate_configuration()
"
```

### Testing Load Balancer

```bash
# Test load balancing
python3 -c "
from intelligent_load_balancer import IntelligentLoadBalancer
lb = IntelligentLoadBalancer()
lb.test_health_checks()
"
```
