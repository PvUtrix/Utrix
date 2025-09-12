#!/usr/bin/env python3
"""
Example: Multilingual Intent Detection using n8n Framework
Demonstrates how to use the n8n framework for multilingual processing
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent.parent))

from automation.integrations.n8n_framework import N8nIntegration, N8nWorkflowBuilder
from automation.integrations.n8n_config_manager import N8nIntegrationManager


async def main():
    """Main example function"""
    print("🚀 n8n Multilingual Integration Example")
    print("=" * 50)
    
    # Configuration
    config = {
        "base_url": "http://localhost:5678",
        "api_key": "your_api_key_here",  # Replace with your actual API key
        "fallback_enabled": True
    }
    
    # Initialize integration
    integration = N8nIntegration(config)
    
    # Test connection
    print("🔍 Testing connection to n8n...")
    if await integration.test_connection():
        print("✅ Connected successfully!")
    else:
        print("❌ Connection failed! Make sure n8n is running and configured.")
        return
    
    # Setup multilingual intent workflow
    print("\n🚀 Setting up multilingual intent workflow...")
    if await integration.setup_multilingual_intent():
        print("✅ Workflow setup complete!")
    else:
        print("❌ Workflow setup failed!")
        return
    
    # Test with different languages
    test_cases = [
        {
            "text": "Какие у меня задачи на сегодня?",
            "language": "Russian",
            "expected_intent": "tasks"
        },
        {
            "text": "What tasks do I have for today?",
            "language": "English",
            "expected_intent": "tasks"
        },
        {
            "text": "Как дела с моим здоровьем?",
            "language": "Russian",
            "expected_intent": "health"
        },
        {
            "text": "What are my shadow archetypes?",
            "language": "English",
            "expected_intent": "shadow_work"
        }
    ]
    
    print("\n🧪 Testing multilingual processing...")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['language']} - '{test_case['text']}'")
        print("-" * 40)
        
        try:
            # Call the webhook
            result = await integration.call_webhook("multilingual-intent", {
                "text": test_case['text'],
                "user_id": 12345,
                "message_type": "text",
                "context": {
                    "user_id": 12345,
                    "preferred_language": "auto",
                    "current_projects": ["Test Project 1", "Test Project 2"]
                },
                "language_hint": "auto"
            })
            
            if result:
                print(f"✅ Intent: {result.get('intent', 'unknown')}")
                print(f"📊 Confidence: {result.get('confidence', 0):.2f}")
                print(f"🌐 Language: {result.get('language', 'unknown')}")
                print(f"💬 Response: {result.get('response', '')[:100]}...")
                
                if result.get('intent') == test_case['expected_intent']:
                    print("✅ Intent detection correct!")
                else:
                    print(f"⚠️ Expected '{test_case['expected_intent']}', got '{result.get('intent')}'")
            else:
                print("❌ No response received")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Example completed!")
    print("\n💡 Next steps:")
    print("1. Configure your n8n instance with OpenAI API key")
    print("2. Test with your actual voice messages")
    print("3. Customize the workflow in n8n UI as needed")


async def create_custom_workflow_example():
    """Example of creating a custom workflow using the framework"""
    print("\n🔧 Creating Custom Workflow Example")
    print("=" * 40)
    
    # Create a custom workflow
    builder = N8nWorkflowBuilder("Custom Data Processor")
    
    # Add webhook trigger
    webhook_id = builder.add_webhook_trigger("custom-processor")
    
    # Add data processor
    processor_id = builder.add_code_node(
        "Data Processor",
        """
// Custom data processing logic
const inputData = $input.first().json;

// Process the data
const processedData = {
    ...inputData,
    processed_at: new Date().toISOString(),
    status: 'processed',
    custom_field: 'added_by_workflow'
};

return processedData;
        """,
        [460, 300]
    )
    
    # Add webhook response
    response_id = builder.add_webhook_response()
    
    # Connect nodes
    builder.connect_nodes(webhook_id, processor_id)
    builder.connect_nodes(processor_id, response_id)
    
    # Build workflow
    workflow_data = builder.build()
    
    print("✅ Custom workflow created!")
    print(f"📋 Workflow name: {workflow_data['name']}")
    print(f"🔗 Webhook path: custom-processor")
    print(f"📊 Nodes: {len(workflow_data['nodes'])}")
    
    # Save as template
    from automation.integrations.n8n_framework import N8nWorkflowManager
    from automation.integrations.n8n_framework import N8nClient
    
    client = N8nClient("http://localhost:5678", "your_api_key")
    manager = N8nWorkflowManager(client)
    
    # Save template
    manager.save_workflow_template("custom-processor", workflow_data)
    print("💾 Template saved!")


if __name__ == "__main__":
    print("Choose an example:")
    print("1. Multilingual Intent Detection")
    print("2. Custom Workflow Creation")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(main())
    elif choice == "2":
        asyncio.run(create_custom_workflow_example())
    else:
        print("Invalid choice!")
