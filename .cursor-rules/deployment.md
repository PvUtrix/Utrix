# Deployment & Infrastructure Standards

## Containerization

### Docker Standards
- **Multi-stage builds**: Use multi-stage builds for optimization
- **Base images**: Use official, minimal base images
- **Layer optimization**: Minimize layers and optimize layer caching
- **Security**: Follow security best practices for containers
- **Health checks**: Implement proper health checks

### Dockerfile Template
```dockerfile
# Multi-stage build for Python applications
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Set PATH to include user's local bin
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "main.py"]
```

### Docker Compose Standards
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
    volumes:
      - ./logs:/app/logs
    depends_on:
      - database
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

## Serverless Deployment

### AWS Lambda Standards
- **Function size**: Keep functions under 50MB for optimal performance
- **Memory allocation**: Allocate appropriate memory based on workload
- **Timeout settings**: Set reasonable timeout values
- **Environment variables**: Use environment variables for configuration
- **IAM roles**: Use least privilege IAM roles

### Serverless Framework Configuration
```yaml
service: personal-system-automation

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  stage: ${opt:stage, 'dev'}
  environment:
    DATABASE_URL: ${env:DATABASE_URL}
    API_KEY: ${env:API_KEY}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - logs:CreateLogGroup
            - logs:CreateLogStream
            - logs:PutLogEvents
          Resource: "*"

functions:
  dailySummary:
    handler: daily_summary_lambda.lambda_handler
    timeout: 300
    memorySize: 256
    events:
      - schedule: cron(0 12 * * ? *)
    environment:
      FUNCTION_NAME: dailySummary

  dataSync:
    handler: data_sync_manager.lambda_handler
    timeout: 600
    memorySize: 512
    events:
      - http:
          path: /sync
          method: post
    environment:
      FUNCTION_NAME: dataSync

plugins:
  - serverless-python-requirements
  - serverless-offline

custom:
  pythonRequirements:
    dockerizePip: true
    slim: true
    strip: false
```

## Infrastructure as Code

### Terraform Standards
- **Modular structure**: Use modules for reusable components
- **State management**: Use remote state with locking
- **Variable management**: Use variables for configuration
- **Output values**: Define useful output values
- **Resource tagging**: Tag all resources appropriately

### Terraform Module Structure
```
terraform/
├── main.tf                 # Main configuration
├── variables.tf            # Input variables
├── outputs.tf              # Output values
├── terraform.tfvars        # Variable values
├── modules/
│   ├── database/           # Database module
│   ├── networking/         # Networking module
│   └── compute/            # Compute module
└── environments/
    ├── dev/                # Development environment
    ├── staging/            # Staging environment
    └── prod/               # Production environment
```

### Terraform Configuration Example
```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "personal-system-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "personal-system"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

module "database" {
  source = "./modules/database"
  
  environment = var.environment
  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password
}

module "compute" {
  source = "./modules/compute"
  
  environment = var.environment
  vpc_id      = module.networking.vpc_id
  subnet_ids  = module.networking.private_subnet_ids
}

module "networking" {
  source = "./modules/networking"
  
  environment = var.environment
  vpc_cidr    = var.vpc_cidr
}
```

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: personal-system

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src/ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v2
    
    - name: Build and push Docker image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Deploy to AWS
      run: |
        aws ecs update-service --cluster personal-system --service personal-system-service --force-new-deployment
```

## Environment Management

### Environment Configuration
- **Development**: Local development environment
- **Staging**: Pre-production testing environment
- **Production**: Live production environment
- **Isolation**: Complete isolation between environments
- **Data**: Separate data stores for each environment

### Environment Variables
```bash
# .env.development
NODE_ENV=development
DATABASE_URL=postgresql://localhost:5432/personal_system_dev
API_KEY=dev_api_key
LOG_LEVEL=debug

# .env.staging
NODE_ENV=staging
DATABASE_URL=postgresql://staging-db:5432/personal_system_staging
API_KEY=staging_api_key
LOG_LEVEL=info

# .env.production
NODE_ENV=production
DATABASE_URL=postgresql://prod-db:5432/personal_system_prod
API_KEY=${PROD_API_KEY}
LOG_LEVEL=warn
```

## Monitoring & Observability

### Application Monitoring
- **Health checks**: Implement health check endpoints
- **Metrics collection**: Collect application metrics
- **Log aggregation**: Centralize log collection
- **Alerting**: Set up alerts for critical issues
- **Dashboards**: Create monitoring dashboards

### Infrastructure Monitoring
- **Resource monitoring**: Monitor CPU, memory, disk usage
- **Network monitoring**: Monitor network traffic and latency
- **Database monitoring**: Monitor database performance
- **Cost monitoring**: Monitor cloud costs and usage

### Monitoring Configuration
```yaml
# monitoring.yml
monitoring:
  health_checks:
    - name: "application"
      url: "/health"
      interval: 30s
      timeout: 5s
      retries: 3
    
    - name: "database"
      url: "/health/database"
      interval: 60s
      timeout: 10s
      retries: 2
  
  metrics:
    - name: "response_time"
      type: "histogram"
      labels: ["method", "endpoint", "status_code"]
    
    - name: "request_count"
      type: "counter"
      labels: ["method", "endpoint", "status_code"]
  
  alerts:
    - name: "high_error_rate"
      condition: "error_rate > 0.05"
      duration: "5m"
      severity: "critical"
    
    - name: "high_response_time"
      condition: "response_time_p95 > 1000ms"
      duration: "10m"
      severity: "warning"
```

## Security Standards

### Container Security
- **Base image security**: Use trusted base images
- **Vulnerability scanning**: Scan images for vulnerabilities
- **Non-root user**: Run containers as non-root user
- **Resource limits**: Set resource limits for containers
- **Network policies**: Implement network security policies

### Infrastructure Security
- **IAM roles**: Use least privilege IAM roles
- **VPC configuration**: Use private subnets for sensitive resources
- **Security groups**: Configure security groups properly
- **Encryption**: Encrypt data at rest and in transit
- **Secrets management**: Use proper secrets management

### Security Scanning
```yaml
# security-scan.yml
security:
  container_scanning:
    enabled: true
    tools:
      - trivy
      - snyk
    schedule: "0 2 * * *"  # Daily at 2 AM
  
  dependency_scanning:
    enabled: true
    tools:
      - safety
      - bandit
    schedule: "0 3 * * *"  # Daily at 3 AM
  
  infrastructure_scanning:
    enabled: true
    tools:
      - checkov
      - tfsec
    schedule: "0 4 * * *"  # Daily at 4 AM
```

## Backup & Recovery

### Backup Strategy
- **Automated backups**: Schedule automated backups
- **Multiple locations**: Store backups in multiple locations
- **Retention policies**: Implement backup retention policies
- **Testing**: Regularly test backup restoration
- **Documentation**: Document backup and recovery procedures

### Backup Configuration
```yaml
# backup.yml
backup:
  database:
    enabled: true
    schedule: "0 1 * * *"  # Daily at 1 AM
    retention: 30  # days
    locations:
      - s3://personal-system-backups/database/
      - local://backups/database/
  
  application_data:
    enabled: true
    schedule: "0 2 * * *"  # Daily at 2 AM
    retention: 7  # days
    locations:
      - s3://personal-system-backups/application/
  
  configuration:
    enabled: true
    schedule: "0 3 * * *"  # Daily at 3 AM
    retention: 90  # days
    locations:
      - s3://personal-system-backups/config/
```

## Disaster Recovery

### Recovery Procedures
- **RTO (Recovery Time Objective)**: Target recovery time
- **RPO (Recovery Point Objective)**: Target data loss tolerance
- **Recovery procedures**: Documented recovery procedures
- **Testing**: Regular disaster recovery testing
- **Communication**: Communication plan for incidents

### Recovery Configuration
```yaml
# disaster-recovery.yml
disaster_recovery:
  objectives:
    rto: "4 hours"  # Recovery Time Objective
    rpo: "1 hour"   # Recovery Point Objective
  
  procedures:
    - name: "database_recovery"
      steps:
        - "Stop application services"
        - "Restore database from backup"
        - "Verify data integrity"
        - "Start application services"
        - "Run health checks"
    
    - name: "full_system_recovery"
      steps:
        - "Provision new infrastructure"
        - "Restore all backups"
        - "Configure services"
        - "Start all services"
        - "Run comprehensive tests"
  
  testing:
    schedule: "quarterly"
    procedures:
      - "database_recovery_test"
      - "full_system_recovery_test"
```
