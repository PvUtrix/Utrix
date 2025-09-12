"""
n8n Integration Framework
A reusable framework for integrating with n8n workflows across the personal system
"""

import httpx
import json
import asyncio
import yaml
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import logging


class N8nNodeType(Enum):
    """n8n node types for workflow creation"""
    WEBHOOK = "n8n-nodes-base.webhook"
    CODE = "n8n-nodes-base.code"
    OPENAI = "n8n-nodes-base.openAi"
    HTTP_REQUEST = "n8n-nodes-base.httpRequest"
    RESPOND_TO_WEBHOOK = "n8n-nodes-base.respondToWebhook"
    IF = "n8n-nodes-base.if"
    SWITCH = "n8n-nodes-base.switch"
    SET = "n8n-nodes-base.set"
    FUNCTION = "n8n-nodes-base.function"


@dataclass
class N8nNode:
    """Represents an n8n workflow node"""
    id: str
    name: str
    type: N8nNodeType
    parameters: Dict[str, Any]
    position: List[int]
    type_version: int = 1


@dataclass
class N8nConnection:
    """Represents a connection between n8n nodes"""
    source_node: str
    target_node: str
    source_output: str = "main"
    target_input: str = "main"
    source_output_index: int = 0
    target_input_index: int = 0


class N8nWorkflowBuilder:
    """Builder class for creating n8n workflows programmatically"""
    
    def __init__(self, name: str):
        self.name = name
        self.nodes: List[N8nNode] = []
        self.connections: List[N8nConnection] = []
        self.settings = {"executionOrder": "v1"}
        self.active = True
    
    def add_node(self, node: N8nNode) -> 'N8nWorkflowBuilder':
        """Add a node to the workflow"""
        self.nodes.append(node)
        return self
    
    def add_connection(self, connection: N8nConnection) -> 'N8nWorkflowBuilder':
        """Add a connection between nodes"""
        self.connections.append(connection)
        return self
    
    def add_webhook_trigger(self, path: str, method: str = "POST") -> str:
        """Add a webhook trigger node"""
        node_id = "webhook-trigger"
        node = N8nNode(
            id=node_id,
            name="Webhook Trigger",
            type=N8nNodeType.WEBHOOK,
            parameters={
                "httpMethod": method,
                "path": path,
                "responseMode": "responseNode",
                "options": {}
            },
            position=[240, 300]
        )
        self.add_node(node)
        return node_id
    
    def add_code_node(self, name: str, code: str, position: List[int]) -> str:
        """Add a code execution node"""
        node_id = name.lower().replace(" ", "-")
        node = N8nNode(
            id=node_id,
            name=name,
            type=N8nNodeType.CODE,
            parameters={"jsCode": code},
            position=position,
            type_version=2
        )
        self.add_node(node)
        return node_id
    
    def add_openai_node(self, name: str, system_prompt: str, user_prompt: str, 
                       model: str = "gpt-4o", temperature: float = 0.3, 
                       max_tokens: int = 1000, position: List[int] = [680, 300]) -> str:
        """Add an OpenAI node"""
        node_id = name.lower().replace(" ", "-")
        node = N8nNode(
            id=node_id,
            name=name,
            type=N8nNodeType.OPENAI,
            parameters={
                "model": model,
                "options": {
                    "temperature": temperature,
                    "maxTokens": max_tokens
                },
                "messages": {
                    "values": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                }
            },
            position=position
        )
        self.add_node(node)
        return node_id
    
    def add_http_request_node(self, name: str, url: str, method: str = "GET", 
                            headers: Optional[Dict] = None, position: List[int] = [500, 300]) -> str:
        """Add an HTTP request node"""
        node_id = name.lower().replace(" ", "-")
        node = N8nNode(
            id=node_id,
            name=name,
            type=N8nNodeType.HTTP_REQUEST,
            parameters={
                "url": url,
                "method": method,
                "headers": headers or {},
                "options": {}
            },
            position=position
        )
        self.add_node(node)
        return node_id
    
    def add_webhook_response(self, response_body: str = "={{ $json }}", 
                           response_mode: str = "json", position: List[int] = [1120, 300]) -> str:
        """Add a webhook response node"""
        node_id = "webhook-response"
        node = N8nNode(
            id=node_id,
            name="Webhook Response",
            type=N8nNodeType.RESPOND_TO_WEBHOOK,
            parameters={
                "respondWith": response_mode,
                "responseBody": response_body
            },
            position=position
        )
        self.add_node(node)
        return node_id
    
    def connect_nodes(self, source: str, target: str, 
                     source_output: str = "main", target_input: str = "main") -> 'N8nWorkflowBuilder':
        """Connect two nodes"""
        connection = N8nConnection(
            source_node=source,
            target_node=target,
            source_output=source_output,
            target_input=target_input
        )
        self.add_connection(connection)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build the workflow dictionary"""
        # Convert connections to n8n format
        connections_dict = {}
        for conn in self.connections:
            if conn.source_node not in connections_dict:
                connections_dict[conn.source_node] = {"main": []}
            
            connections_dict[conn.source_node]["main"].append([{
                "node": conn.target_node,
                "type": conn.target_input,
                "index": conn.target_input_index
            }])
        
        # Convert nodes to n8n format
        nodes_dict = []
        for node in self.nodes:
            node_dict = {
                "id": node.id,
                "name": node.name,
                "type": node.type.value,
                "typeVersion": node.type_version,
                "position": node.position,
                "parameters": node.parameters
            }
            nodes_dict.append(node_dict)
        
        return {
            "name": self.name,
            "nodes": nodes_dict,
            "connections": connections_dict,
            "active": self.active,
            "settings": self.settings,
            "versionId": "1",
            "meta": {"templateCredsSetupCompleted": True},
            "tags": []
        }


class N8nClient:
    """Client for interacting with n8n API"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, 
                 username: Optional[str] = None, password: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/v1"
        self.api_key = api_key
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            headers["X-N8N-API-KEY"] = self.api_key
        elif self.username and self.password:
            import base64
            credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            headers["Authorization"] = f"Basic {credentials}"
        
        return headers
    
    async def test_connection(self) -> bool:
        """Test connection to n8n instance"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.api_url}/workflows",
                    headers=self._get_headers()
                )
                return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Optional[str]:
        """Create a new workflow in n8n"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.api_url}/workflows",
                    json=workflow_data,
                    headers=self._get_headers()
                )
                
                if response.status_code in [200, 201]:
                    workflow_id = response.json().get("id")
                    self.logger.info(f"Created workflow: {workflow_id}")
                    return workflow_id
                else:
                    self.logger.error(f"Failed to create workflow: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            self.logger.error(f"Error creating workflow: {e}")
            return None
    
    async def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> bool:
        """Update an existing workflow"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.put(
                    f"{self.api_url}/workflows/{workflow_id}",
                    json=workflow_data,
                    headers=self._get_headers()
                )
                return response.status_code in [200, 201]
        except Exception as e:
            self.logger.error(f"Error updating workflow: {e}")
            return False
    
    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.delete(
                    f"{self.api_url}/workflows/{workflow_id}",
                    headers=self._get_headers()
                )
                return response.status_code in [200, 204]
        except Exception as e:
            self.logger.error(f"Error deleting workflow: {e}")
            return False
    
    async def get_workflows(self) -> List[Dict[str, Any]]:
        """Get all workflows"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(
                    f"{self.api_url}/workflows",
                    headers=self._get_headers()
                )
                if response.status_code == 200:
                    return response.json().get("data", [])
                return []
        except Exception as e:
            self.logger.error(f"Error getting workflows: {e}")
            return []
    
    async def execute_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a workflow with data"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.api_url}/workflows/{workflow_id}/execute",
                    json=data,
                    headers=self._get_headers()
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            self.logger.error(f"Error executing workflow: {e}")
            return None
    
    async def call_webhook(self, webhook_path: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call a webhook endpoint"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.base_url}/webhook/{webhook_path}",
                    json=data
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            self.logger.error(f"Error calling webhook: {e}")
            return None


class N8nWorkflowManager:
    """Manager for n8n workflows with templates and utilities"""
    
    def __init__(self, client: N8nClient, templates_dir: str = "automation/integrations/n8n_templates"):
        self.client = client
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def save_workflow_template(self, name: str, workflow_data: Dict[str, Any]) -> str:
        """Save a workflow as a template"""
        template_path = self.templates_dir / f"{name}.json"
        with open(template_path, 'w') as f:
            json.dump(workflow_data, f, indent=2)
        self.logger.info(f"Saved template: {template_path}")
        return str(template_path)
    
    def load_workflow_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a workflow template"""
        template_path = self.templates_dir / f"{name}.json"
        if template_path.exists():
            with open(template_path, 'r') as f:
                return json.load(f)
        return None
    
    def list_templates(self) -> List[str]:
        """List available workflow templates"""
        return [f.stem for f in self.templates_dir.glob("*.json")]
    
    async def deploy_template(self, template_name: str, workflow_name: Optional[str] = None) -> Optional[str]:
        """Deploy a template as a workflow"""
        template_data = self.load_workflow_template(template_name)
        if not template_data:
            self.logger.error(f"Template not found: {template_name}")
            return None
        
        if workflow_name:
            template_data["name"] = workflow_name
        
        return await self.client.create_workflow(template_data)
    
    def create_multilingual_intent_workflow(self) -> Dict[str, Any]:
        """Create a multilingual intent detection workflow"""
        builder = N8nWorkflowBuilder("Multilingual Intent Detection")
        
        # Webhook trigger
        webhook_id = builder.add_webhook_trigger("multilingual-intent")
        
        # Data extractor
        extractor_id = builder.add_code_node(
            "Extract Data",
            """
// Extract data from webhook
const text = $input.first().json.text;
const user_id = $input.first().json.user_id;
const context = $input.first().json.context;
const language_hint = $input.first().json.language_hint;

// Prepare data for AI processing
return {
  text: text,
  user_id: user_id,
  context: context,
  language_hint: language_hint,
  timestamp: new Date().toISOString()
};
            """,
            [460, 300]
        )
        
        # AI intent detection
        ai_id = builder.add_openai_node(
            "AI Intent Detection",
            "You are a multilingual personal assistant that understands user intent in multiple languages. Analyze the user's message and determine their intent.\n\nSupported intents:\n- tasks: Questions about tasks, projects, what to work on today\n- health: Health tracking, fitness, wellness questions\n- learning: Learning progress, courses, education\n- shadow_work: Shadow work, archetypes, personal development\n- journal: Journal entries, patterns, insights\n- goals: Goals, progress, achievements\n- values: Core values, life direction\n- help: General help, what can you do\n- unknown: Unclear or unrecognized intent\n\nRespond with a JSON object containing:\n- intent: The detected intent\n- confidence: Confidence score (0-1)\n- language: Detected language (en, ru, etc.)\n- response: A helpful response in the user's language\n- action: Any specific action to take\n- reasoning: Brief explanation of the intent detection",
            "User message: \"{{ $json.text }}\"\nUser context: {{ JSON.stringify($json.context) }}\nLanguage hint: {{ $json.language_hint }}\n\nDetect the intent and provide a helpful response in the user's language.",
            position=[680, 300]
        )
        
        # Response processor
        processor_id = builder.add_code_node(
            "Process Response",
            """
// Parse AI response and structure the output
const aiResponse = $input.first().json.choices[0].message.content;

let parsedResponse;
try {
  // Try to parse as JSON first
  parsedResponse = JSON.parse(aiResponse);
} catch (e) {
  // If not JSON, create a structured response
  parsedResponse = {
    intent: "unknown",
    confidence: 0.5,
    language: "en",
    response: aiResponse,
    action: {},
    reasoning: "Could not parse AI response as JSON"
  };
}

// Add metadata
parsedResponse.metadata = {
  processed_at: new Date().toISOString(),
  user_id: $('Extract Data').first().json.user_id,
  original_text: $('Extract Data').first().json.text
};

return parsedResponse;
            """,
            [900, 300]
        )
        
        # Webhook response
        response_id = builder.add_webhook_response()
        
        # Connect nodes
        builder.connect_nodes(webhook_id, extractor_id)
        builder.connect_nodes(extractor_id, ai_id)
        builder.connect_nodes(ai_id, processor_id)
        builder.connect_nodes(processor_id, response_id)
        
        return builder.build()
    
    def create_data_processor_workflow(self, name: str, processing_function: str) -> Dict[str, Any]:
        """Create a data processing workflow"""
        builder = N8nWorkflowBuilder(name)
        
        # Webhook trigger
        webhook_id = builder.add_webhook_trigger(f"process-{name.lower().replace(' ', '-')}")
        
        # Data processor
        processor_id = builder.add_code_node(
            "Data Processor",
            processing_function,
            [460, 300]
        )
        
        # Webhook response
        response_id = builder.add_webhook_response()
        
        # Connect nodes
        builder.connect_nodes(webhook_id, processor_id)
        builder.connect_nodes(processor_id, response_id)
        
        return builder.build()
    
    def create_api_integration_workflow(self, name: str, api_url: str, 
                                      headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Create an API integration workflow"""
        builder = N8nWorkflowBuilder(name)
        
        # Webhook trigger
        webhook_id = builder.add_webhook_trigger(f"api-{name.lower().replace(' ', '-')}")
        
        # Data extractor
        extractor_id = builder.add_code_node(
            "Extract Data",
            "return $input.first().json;",
            [460, 300]
        )
        
        # HTTP request
        http_id = builder.add_http_request_node(
            "API Call",
            api_url,
            "POST",
            headers,
            [680, 300]
        )
        
        # Response processor
        processor_id = builder.add_code_node(
            "Process Response",
            "return $input.first().json;",
            [900, 300]
        )
        
        # Webhook response
        response_id = builder.add_webhook_response()
        
        # Connect nodes
        builder.connect_nodes(webhook_id, extractor_id)
        builder.connect_nodes(extractor_id, http_id)
        builder.connect_nodes(http_id, processor_id)
        builder.connect_nodes(processor_id, response_id)
        
        return builder.build()


class N8nIntegration:
    """Main integration class for n8n workflows"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = N8nClient(
            base_url=config.get('base_url', 'http://localhost:5678'),
            api_key=config.get('api_key'),
            username=config.get('username'),
            password=config.get('password')
        )
        self.manager = N8nWorkflowManager(self.client)
        self.logger = logging.getLogger(__name__)
    
    async def setup_multilingual_intent(self) -> bool:
        """Setup the multilingual intent detection workflow"""
        try:
            workflow_data = self.manager.create_multilingual_intent_workflow()
            
            # Save as template
            self.manager.save_workflow_template("multilingual-intent", workflow_data)
            
            # Deploy to n8n
            workflow_id = await self.manager.deploy_template("multilingual-intent")
            
            if workflow_id:
                self.logger.info(f"Multilingual intent workflow deployed: {workflow_id}")
                return True
            else:
                self.logger.error("Failed to deploy multilingual intent workflow")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting up multilingual intent: {e}")
            return False
    
    async def call_workflow(self, workflow_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call a specific workflow by name"""
        workflows = await self.client.get_workflows()
        workflow = next((w for w in workflows if w['name'] == workflow_name), None)
        
        if workflow:
            return await self.client.execute_workflow(workflow['id'], data)
        else:
            self.logger.error(f"Workflow not found: {workflow_name}")
            return None
    
    async def call_webhook(self, webhook_path: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call a webhook endpoint"""
        return await self.client.call_webhook(webhook_path, data)
    
    async def test_connection(self) -> bool:
        """Test connection to n8n"""
        return await self.client.test_connection()
