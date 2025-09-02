# Config

## Purpose
The config directory contains configuration files for various environments, services, and system components. These configurations ensure consistent behavior across different deployment environments and provide centralized management of system settings.

## Contents
- `global/` - System-wide preferences and settings
  - `preferences.yaml` - Global system preferences
- `automation/` - Automation and deployment configurations
  - `coolify-deploy.yaml` - Coolify deployment configuration
  - `gitea-shared-db.yaml` - Gitea shared database configuration
- `domains/` - Domain-specific configuration files
- `environments/` - Environment-specific configurations
- `local/` - Local development and testing configurations

## Usage
Configuration files serve several purposes:

- **Environment Management**: Different settings for development, staging, and production
- **Service Configuration**: API keys, database connections, and external service settings
- **Automation Settings**: Script parameters, scheduling, and execution preferences
- **Domain Preferences**: Specific configurations for different life areas
- **Deployment**: Infrastructure and deployment configurations

## Related
- `automation/` - Scripts that use these configuration files
- `serverless/` - Serverless functions that require configuration
- `domains/` - Domain-specific configuration needs
- `workflows/` - Workflow configurations and preferences
- `privacy/` - Secure storage of sensitive configuration data

## Last Updated
2024-12-19 - Initial README creation
