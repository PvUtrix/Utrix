# Docker Configuration

## Purpose
The docker directory contains all Docker-related configuration files for local development, testing, and containerized deployment of the personal system.

## Contents
- `Dockerfile` - Main application container definition
- `docker-compose.yml` - Local development environment setup
- `docker-compose.shared-db.yml` - Shared database configuration
- `.dockerignore` - Files to exclude from Docker builds

## Usage
These files enable containerized development and deployment:

- **Dockerfile**: Defines the application container image
- **docker-compose.yml**: Sets up local development environment
- **docker-compose.shared-db.yml**: Configures shared database services
- **.dockerignore**: Optimizes build context and security

## Related
- `../coolify/` - Coolify deployment configurations
- `../../config/` - System configuration files
- `../../automation/serverless/` - Serverless functions
- `../../docs/deployment/docker/` - Docker documentation

## Last Updated
2024-12-19 - Initial README creation
