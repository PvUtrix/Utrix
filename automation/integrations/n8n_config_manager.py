"""
n8n Configuration Manager
Manages n8n integration configurations across the personal system
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import logging


@dataclass
class N8nConfig:
    """n8n configuration data class"""
    base_url: str
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    timeout: int = 30
    webhook_base_path: str = "webhook"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    openai_temperature: float = 0.3
    openai_max_tokens: int = 1000


class N8nConfigManager:
    """Manager for n8n configurations across the system"""
    
    def __init__(self, config_dir: str = "automation/integrations/configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Default configuration file
        self.default_config_file = self.config_dir / "n8n_default.yaml"
        self.configs_file = self.config_dir / "n8n_configs.yaml"
        
        # Load configurations
        self.configs = self._load_configs()
    
    def _load_configs(self) -> Dict[str, N8nConfig]:
        """Load all n8n configurations"""
        configs = {}
        
        # Load default configuration
        if self.default_config_file.exists():
            with open(self.default_config_file, 'r') as f:
                default_data = yaml.safe_load(f)
                configs['default'] = N8nConfig(**default_data)
        
        # Load additional configurations
        if self.configs_file.exists():
            with open(self.configs_file, 'r') as f:
                configs_data = yaml.safe_load(f)
                for name, config_data in configs_data.items():
                    configs[name] = N8nConfig(**config_data)
        
        return configs
    
    def save_config(self, name: str, config: N8nConfig) -> None:
        """Save a configuration"""
        self.configs[name] = config
        self._save_configs()
        self.logger.info(f"Saved n8n configuration: {name}")
    
    def get_config(self, name: str = "default") -> Optional[N8nConfig]:
        """Get a configuration by name"""
        return self.configs.get(name)
    
    def list_configs(self) -> List[str]:
        """List all available configurations"""
        return list(self.configs.keys())
    
    def delete_config(self, name: str) -> bool:
        """Delete a configuration"""
        if name in self.configs:
            del self.configs[name]
            self._save_configs()
            self.logger.info(f"Deleted n8n configuration: {name}")
            return True
        return False
    
    def _save_configs(self) -> None:
        """Save all configurations to file"""
        # Save default configuration
        if 'default' in self.configs:
            with open(self.default_config_file, 'w') as f:
                yaml.dump(asdict(self.configs['default']), f, default_flow_style=False)
        
        # Save other configurations
        other_configs = {k: v for k, v in self.configs.items() if k != 'default'}
        if other_configs:
            with open(self.configs_file, 'w') as f:
                configs_data = {name: asdict(config) for name, config in other_configs.items()}
                yaml.dump(configs_data, f, default_flow_style=False)
    
    def create_default_config(self) -> N8nConfig:
        """Create a default configuration"""
        default_config = N8nConfig(
            base_url="http://localhost:5678",
            timeout=30,
            webhook_base_path="webhook"
        )
        self.save_config("default", default_config)
        return default_config
    
    def validate_config(self, config: N8nConfig) -> List[str]:
        """Validate a configuration and return any errors"""
        errors = []
        
        if not config.base_url:
            errors.append("base_url is required")
        
        if not config.api_key and not (config.username and config.password):
            errors.append("Either api_key or username/password must be provided")
        
        if config.timeout <= 0:
            errors.append("timeout must be positive")
        
        if config.openai_temperature < 0 or config.openai_temperature > 2:
            errors.append("openai_temperature must be between 0 and 2")
        
        if config.openai_max_tokens <= 0:
            errors.append("openai_max_tokens must be positive")
        
        return errors
    
    def get_config_for_service(self, service_name: str) -> Optional[N8nConfig]:
        """Get configuration for a specific service"""
        # Try service-specific config first
        service_config = self.get_config(service_name)
        if service_config:
            return service_config
        
        # Fall back to default
        return self.get_config("default")
    
    def create_service_config(self, service_name: str, base_url: str, 
                            api_key: Optional[str] = None,
                            username: Optional[str] = None,
                            password: Optional[str] = None) -> N8nConfig:
        """Create a configuration for a specific service"""
        config = N8nConfig(
            base_url=base_url,
            api_key=api_key,
            username=username,
            password=password
        )
        
        # Validate configuration
        errors = self.validate_config(config)
        if errors:
            raise ValueError(f"Invalid configuration: {', '.join(errors)}")
        
        self.save_config(service_name, config)
        return config


class N8nWorkflowRegistry:
    """Registry for managing n8n workflows across the system"""
    
    def __init__(self, registry_file: str = "automation/integrations/n8n_workflow_registry.json"):
        self.registry_file = Path(registry_file)
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load workflow registry"""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_registry(self) -> None:
        """Save workflow registry"""
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def register_workflow(self, name: str, workflow_id: str, 
                         webhook_path: str, description: str = "") -> None:
        """Register a workflow in the registry"""
        self.registry[name] = {
            "workflow_id": workflow_id,
            "webhook_path": webhook_path,
            "description": description,
            "registered_at": str(Path().cwd()),
            "status": "active"
        }
        self._save_registry()
        self.logger.info(f"Registered workflow: {name} -> {workflow_id}")
    
    def get_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """Get workflow information by name"""
        return self.registry.get(name)
    
    def list_workflows(self) -> List[str]:
        """List all registered workflows"""
        return list(self.registry.keys())
    
    def unregister_workflow(self, name: str) -> bool:
        """Unregister a workflow"""
        if name in self.registry:
            del self.registry[name]
            self._save_registry()
            self.logger.info(f"Unregistered workflow: {name}")
            return True
        return False
    
    def get_webhook_url(self, name: str, base_url: str) -> Optional[str]:
        """Get the webhook URL for a workflow"""
        workflow = self.get_workflow(name)
        if workflow:
            return f"{base_url.rstrip('/')}/{workflow['webhook_path']}"
        return None


class N8nIntegrationManager:
    """Main manager for n8n integrations across the personal system"""
    
    def __init__(self, config_dir: str = "automation/integrations/configs"):
        self.config_manager = N8nConfigManager(config_dir)
        self.workflow_registry = N8nWorkflowRegistry()
        self.logger = logging.getLogger(__name__)
    
    def setup_integration(self, service_name: str, base_url: str,
                         api_key: Optional[str] = None,
                         username: Optional[str] = None,
                         password: Optional[str] = None) -> N8nConfig:
        """Setup n8n integration for a service"""
        config = self.config_manager.create_service_config(
            service_name, base_url, api_key, username, password
        )
        self.logger.info(f"Setup n8n integration for service: {service_name}")
        return config
    
    def get_integration_config(self, service_name: str) -> Optional[N8nConfig]:
        """Get integration configuration for a service"""
        return self.config_manager.get_config_for_service(service_name)
    
    def register_workflow(self, name: str, workflow_id: str, 
                         webhook_path: str, description: str = "") -> None:
        """Register a workflow"""
        self.workflow_registry.register_workflow(name, workflow_id, webhook_path, description)
    
    def get_workflow_url(self, service_name: str, workflow_name: str) -> Optional[str]:
        """Get webhook URL for a workflow"""
        config = self.get_integration_config(service_name)
        if config:
            return self.workflow_registry.get_webhook_url(workflow_name, config.base_url)
        return None
    
    def list_integrations(self) -> Dict[str, Any]:
        """List all integrations and workflows"""
        return {
            "configurations": self.config_manager.list_configs(),
            "workflows": self.workflow_registry.list_workflows()
        }
