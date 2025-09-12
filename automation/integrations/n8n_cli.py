#!/usr/bin/env python3
"""
n8n Integration CLI
Command-line tool for managing n8n integrations across the personal system
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json
import yaml

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent.parent))

from automation.integrations.n8n_framework import N8nIntegration, N8nClient, N8nWorkflowManager
from automation.integrations.n8n_config_manager import N8nIntegrationManager


class N8nCLI:
    """Command-line interface for n8n integrations"""
    
    def __init__(self):
        self.integration_manager = N8nIntegrationManager()
        self.logger = None
    
    async def test_connection(self, service_name: str = "default") -> bool:
        """Test connection to n8n instance"""
        config = self.integration_manager.get_integration_config(service_name)
        if not config:
            print(f"❌ No configuration found for service: {service_name}")
            return False
        
        client = N8nClient(
            base_url=config.base_url,
            api_key=config.api_key,
            username=config.username,
            password=config.password
        )
        
        print(f"🔍 Testing connection to {config.base_url}...")
        success = await client.test_connection()
        
        if success:
            print("✅ Connection successful!")
        else:
            print("❌ Connection failed!")
        
        return success
    
    async def setup_integration(self, service_name: str, base_url: str,
                              api_key: Optional[str] = None,
                              username: Optional[str] = None,
                              password: Optional[str] = None) -> bool:
        """Setup n8n integration for a service"""
        try:
            config = self.integration_manager.setup_integration(
                service_name, base_url, api_key, username, password
            )
            print(f"✅ Setup integration for service: {service_name}")
            print(f"   Base URL: {config.base_url}")
            print(f"   Auth: {'API Key' if config.api_key else 'Username/Password'}")
            return True
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
    
    async def deploy_workflow(self, service_name: str, template_name: str, 
                            workflow_name: Optional[str] = None) -> bool:
        """Deploy a workflow template"""
        config = self.integration_manager.get_integration_config(service_name)
        if not config:
            print(f"❌ No configuration found for service: {service_name}")
            return False
        
        client = N8nClient(
            base_url=config.base_url,
            api_key=config.api_key,
            username=config.username,
            password=config.password
        )
        
        manager = N8nWorkflowManager(client)
        
        print(f"🚀 Deploying workflow template: {template_name}")
        workflow_id = await manager.deploy_template(template_name, workflow_name)
        
        if workflow_id:
            print(f"✅ Workflow deployed successfully: {workflow_id}")
            
            # Register the workflow
            webhook_path = template_name.replace("_", "-")
            self.integration_manager.register_workflow(
                template_name, workflow_id, webhook_path, f"Deployed from template {template_name}"
            )
            return True
        else:
            print("❌ Workflow deployment failed!")
            return False
    
    async def list_workflows(self, service_name: str = "default") -> None:
        """List workflows in n8n instance"""
        config = self.integration_manager.get_integration_config(service_name)
        if not config:
            print(f"❌ No configuration found for service: {service_name}")
            return
        
        client = N8nClient(
            base_url=config.base_url,
            api_key=config.api_key,
            username=config.username,
            password=config.password
        )
        
        print(f"📋 Workflows in {config.base_url}:")
        workflows = await client.get_workflows()
        
        if workflows:
            for workflow in workflows:
                status = "🟢 Active" if workflow.get('active') else "🔴 Inactive"
                print(f"  {workflow['name']} ({workflow['id']}) - {status}")
        else:
            print("  No workflows found")
    
    async def test_webhook(self, service_name: str, workflow_name: str, 
                          test_data: Dict[str, Any]) -> bool:
        """Test a webhook endpoint"""
        webhook_url = self.integration_manager.get_workflow_url(service_name, workflow_name)
        if not webhook_url:
            print(f"❌ No webhook URL found for workflow: {workflow_name}")
            return False
        
        config = self.integration_manager.get_integration_config(service_name)
        client = N8nClient(
            base_url=config.base_url,
            api_key=config.api_key,
            username=config.username,
            password=config.password
        )
        
        print(f"🧪 Testing webhook: {webhook_url}")
        result = await client.call_webhook(workflow_name, test_data)
        
        if result:
            print("✅ Webhook test successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print("❌ Webhook test failed!")
            return False
    
    def list_configs(self) -> None:
        """List all configurations"""
        configs = self.integration_manager.list_integrations()
        
        print("📋 n8n Integration Configurations:")
        for config_name in configs["configurations"]:
            config = self.integration_manager.get_integration_config(config_name)
            if config:
                print(f"  {config_name}: {config.base_url}")
        
        print("\n📋 Registered Workflows:")
        for workflow_name in configs["workflows"]:
            workflow = self.integration_manager.workflow_registry.get_workflow(workflow_name)
            if workflow:
                print(f"  {workflow_name}: {workflow['webhook_path']}")
    
    def create_template(self, template_name: str, template_type: str) -> bool:
        """Create a new workflow template"""
        from automation.integrations.n8n_framework import N8nWorkflowBuilder
        
        if template_type == "multilingual":
            builder = N8nWorkflowBuilder("Multilingual Intent Detection")
            # Add multilingual intent workflow nodes
            webhook_id = builder.add_webhook_trigger("multilingual-intent")
            # ... add other nodes
            workflow_data = builder.build()
        elif template_type == "data_processor":
            builder = N8nWorkflowBuilder("Data Processor")
            webhook_id = builder.add_webhook_trigger("process-data")
            # ... add other nodes
            workflow_data = builder.build()
        else:
            print(f"❌ Unknown template type: {template_type}")
            return False
        
        # Save template
        template_path = Path("automation/integrations/n8n_templates") / f"{template_name}.json"
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(template_path, 'w') as f:
            json.dump(workflow_data, f, indent=2)
        
        print(f"✅ Created template: {template_path}")
        return True


async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="n8n Integration CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test connection command
    test_parser = subparsers.add_parser("test", help="Test connection to n8n")
    test_parser.add_argument("--service", default="default", help="Service name")
    
    # Setup integration command
    setup_parser = subparsers.add_parser("setup", help="Setup n8n integration")
    setup_parser.add_argument("service", help="Service name")
    setup_parser.add_argument("base_url", help="n8n base URL")
    setup_parser.add_argument("--api-key", help="API key")
    setup_parser.add_argument("--username", help="Username")
    setup_parser.add_argument("--password", help="Password")
    
    # Deploy workflow command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy workflow template")
    deploy_parser.add_argument("--service", default="default", help="Service name")
    deploy_parser.add_argument("template", help="Template name")
    deploy_parser.add_argument("--name", help="Workflow name")
    
    # List workflows command
    list_parser = subparsers.add_parser("list", help="List workflows")
    list_parser.add_argument("--service", default="default", help="Service name")
    
    # Test webhook command
    webhook_parser = subparsers.add_parser("test-webhook", help="Test webhook")
    webhook_parser.add_argument("--service", default="default", help="Service name")
    webhook_parser.add_argument("workflow", help="Workflow name")
    webhook_parser.add_argument("--data", help="Test data JSON file")
    
    # List configs command
    subparsers.add_parser("configs", help="List configurations")
    
    # Create template command
    template_parser = subparsers.add_parser("create-template", help="Create template")
    template_parser.add_argument("name", help="Template name")
    template_parser.add_argument("type", choices=["multilingual", "data_processor"], help="Template type")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = N8nCLI()
    
    if args.command == "test":
        await cli.test_connection(args.service)
    
    elif args.command == "setup":
        await cli.setup_integration(
            args.service, args.base_url, 
            args.api_key, args.username, args.password
        )
    
    elif args.command == "deploy":
        await cli.deploy_workflow(args.service, args.template, args.name)
    
    elif args.command == "list":
        await cli.list_workflows(args.service)
    
    elif args.command == "test-webhook":
        test_data = {}
        if args.data:
            with open(args.data, 'r') as f:
                test_data = json.load(f)
        else:
            test_data = {"test": "data"}
        
        await cli.test_webhook(args.service, args.workflow, test_data)
    
    elif args.command == "configs":
        cli.list_configs()
    
    elif args.command == "create-template":
        cli.create_template(args.name, args.type)


if __name__ == "__main__":
    asyncio.run(main())
