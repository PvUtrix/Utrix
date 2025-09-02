# Deployment

## Purpose
The deployment directory contains all files and configurations needed for deploying the personal system, including Docker configurations, Coolify deployment scripts, and infrastructure setup.

## Contents
- `docker/` - Docker configuration files
  - `Dockerfile` - Main application container
  - `docker-compose.yml` - Local development setup
  - `docker-compose.shared-db.yml` - Shared database configuration
- `coolify/` - Coolify deployment configurations
  - `coolify.yaml` - Coolify deployment configuration
  - `coolify-deploy.sh` - Automated deployment script
- `scripts/` - Deployment and setup scripts
- `configs/` - Deployment-specific configuration files

## Usage
This directory serves deployment needs:

- **Local Development**: Docker Compose for local testing
- **Production**: Coolify deployment to your own server
- **Infrastructure**: Database and service configurations
- **Automation**: Scripts for automated deployment

## Related
- `../docs/deployment/` - Deployment documentation and guides
- `../config/` - System configuration files
- `../automation/serverless/` - Serverless deployment functions
- `../logs/` - Deployment and system logs

## Last Updated
2024-12-19 - Initial README creation
