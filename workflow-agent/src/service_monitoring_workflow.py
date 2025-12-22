from agent_framework import (
    ChatAgent,
    ChatMessage,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowOutputEvent,
    handler,
    executor,
)
from src.project_util.file_util import load_agent_instructions
from agent_framework_azure_ai import AzureAIAgentClient
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.core.credentials import AzureKeyCredential
import asyncio
from typing_extensions import Never
import json
import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load .env file from the parent directory (workflow-agent/)
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass

# Add the src directory to Python path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .tools.monitoring_tools import (
        get_system_status, 
        check_service_health, 
        analyze_metrics,
        get_service_logs,
        MONITORING_TOOLS
    )
    from .tools.document_tools import (
        search_monitoring_documents,
        list_available_documents,
        get_document_excerpt,
        DOCUMENT_TOOLS
    )
except ImportError:
    # If relative imports fail (when running as script), use absolute imports
    from tools.monitoring_tools import (
        get_system_status, 
        check_service_health, 
        analyze_metrics,
        get_service_logs,
        MONITORING_TOOLS
    )
    from tools.document_tools import (
        search_monitoring_documents,
        list_available_documents,
        get_document_excerpt,
        DOCUMENT_TOOLS
    )

# Configuration - can be set via environment variables or updated here
ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_NAME", "gpt-4.1-mini")



class InfoAgent(Executor):
    """Agent that answers general monitoring questions without triggering investigation workflows."""
    
    def __init__(self, agent: ChatAgent, id="info"):
        self.agent = agent
        super().__init__(id=id)

    @handler
    async def answer_question(self, message: str, ctx: WorkflowContext[Never, str]) -> None:
        """Answer monitoring-related questions directly."""
        # Remove the routing prefix if present
        clean_message = message.replace("INFO:", "").strip()
        messages = [ChatMessage(role="user", text=clean_message)]
        response = await self.agent.run(messages)
        
        # Don't print here - let the main loop handle output
        # Yield the answer directly as workflow output
        await ctx.yield_output(response.messages[-1].contents[-1].text)

@executor(id="routing_executor")
async def route_request(message: str, ctx: WorkflowContext[str]) -> None:
    """Route the request to either info agent or monitoring workflow."""
    
    # Simple routing logic based on keywords
    question_keywords = [
        "what is", "how does", "explain", "tell me about", "status of", "health of",
        "metrics", "logs", "configuration", "documentation", "runbook", "procedure",
        "policy", "info", "information", "overview", "summary", "dashboard"
    ]
    
    investigation_keywords = [
        "investigate", "analyze", "troubleshoot", "diagnose", "alert", "issue", 
        "problem", "error", "failure", "outage", "incident", "check health",
        "monitor", "escalate", "urgent", "critical", "down", "slow"
    ]
    
    message_lower = message.lower()
    
    # Check if this is a question about monitoring info
    is_question = any(keyword in message_lower for keyword in question_keywords)
    is_investigation = any(keyword in message_lower for keyword in investigation_keywords)
    
    if is_question and not is_investigation:
        # Route to info agent - don't print routing info
        await ctx.send_message(f"INFO:{message}")
    else:
        # Route to monitoring workflow - don't print routing info  
        await ctx.send_message(f"INVESTIGATE:{message}")

class DetectorAgentExecutor(Executor):
    """Agent responsible for detecting and categorizing service issues."""

    def __init__(self, agent: ChatAgent, id="detector"):
        self.agent = agent
        super().__init__(id=id)

    @handler
    async def process_detection_request(self, message: str, ctx: WorkflowContext[Never, str]) -> None:
        """Process and categorize incoming monitoring requests."""
        
        # Remove routing prefix if present
        clean_message = message.replace("INVESTIGATE:", "").strip()
        
        print(f"\n🔍 Detector Agent: Analyzing issue...")
        
        # Create system prompt with current context
        system_message = ChatMessage(role="system", text="You are a service monitoring detector agent. Analyze the issue and provide initial categorization.")
        user_message = ChatMessage(role="user", text=clean_message)
        
        response = await self.agent.run([system_message, user_message])
        detection_result = response.messages[-1].contents[-1].text
        
        print(f"🔍 Detection Result: {detection_result}")
        
        # Pass to analyzer for detailed investigation
        await ctx.send_message(f"ANALYZE:{clean_message}\n\nDetection Result: {detection_result}")

class AnalyzerAgentExecutor(Executor):
    """Agent responsible for analyzing detected issues and determining solutions."""

    def __init__(self, agent: ChatAgent, id="analyzer"):
        self.agent = agent
        super().__init__(id=id)

    @handler
    async def process_analysis_request(self, message: str, ctx: WorkflowContext[Never, str]) -> None:
        """Perform detailed analysis of the detected issue."""
        
        print(f"\n🔬 Analyzer Agent: Performing detailed analysis...")
        
        # Create system prompt for analysis
        system_message = ChatMessage(role="system", text="You are a service monitoring analyzer agent. Perform detailed investigation and recommend actions.")
        user_message = ChatMessage(role="user", text=message.replace("ANALYZE:", ""))
        
        response = await self.agent.run([system_message, user_message])
        analysis_result = response.messages[-1].contents[-1].text
        
        print(f"🔬 Analysis Result: {analysis_result}")
        
        # Pass to alerting agent for notification/escalation
        await ctx.send_message(f"ALERT:{message}\n\nAnalysis Result: {analysis_result}")

class AlertingAgentExecutor(Executor):
    """Agent responsible for sending alerts and managing escalations."""

    def __init__(self, agent: ChatAgent, id="alerting"):
        self.agent = agent
        super().__init__(id=id)

    @handler
    async def process_alert_request(self, message: str, ctx: WorkflowContext[Never, str]) -> None:
        """Process alert requests and manage notifications."""
        
        print(f"\n📢 Alerting Agent: Processing alert and notifications...")
        
        # Create system prompt for alerting
        system_message = ChatMessage(role="system", text="You are a service monitoring alerting agent. Create appropriate alerts and escalation plans.")
        user_message = ChatMessage(role="user", text=message.replace("ALERT:", ""))
        
        response = await self.agent.run([user_message])
        final_result = response.messages[-1].contents[-1].text
        
        print(f"📢 Alert Processing Complete: {final_result}")
        
        # Yield final output
        await ctx.yield_output(final_result)

"""
  Method: create_monitoring_workflow
  Description: Create and configure the monitoring workflow with all agents
  Args:
    None
  Returns:
    WorkflowBuilder: Configured monitoring workflow ready for execution
"""
async def create_monitoring_workflow():
    
    try:
        # Determine credential type based on available environment variables
        api_key = os.getenv("AZURE_PROJECT_APIKEY")
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET") 
        tenant_id = os.getenv("AZURE_TENANT_ID")
        
        if api_key:
            # Try API key credential first
            credential = AzureKeyCredential(api_key)
            print(f"✅ Using API key authentication")
        elif client_id and client_secret and tenant_id and client_id != "your-client-id":
            # Use service principal credential
            credential = ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id, 
                client_secret=client_secret
            )
            print(f"✅ Using Service Principal authentication")
        else:
            # Use default Azure credential (requires az login)
            credential = DefaultAzureCredential()
            print(f"✅ Using DefaultAzureCredential authentication")
        
        # Create Azure AI agent client
        if api_key:
            agent_client = AzureAIAgentClient(
                endpoint=ENDPOINT,
                credential=AzureKeyCredential(api_key)
            )
        else:
            # Use DefaultAzureCredential
            agent_client = AzureAIAgentClient(
                endpoint=ENDPOINT,
                credential=credential
            )
        
        print(f"✅ Connected to Azure AI endpoint: {ENDPOINT}")
        
        # Load agent instructions
        info_instructions = load_agent_instructions("info")
        detector_instructions = load_agent_instructions("detector")
        analyzer_instructions = load_agent_instructions("analyzer") 
        alerting_instructions = load_agent_instructions("alerting")
        
        # Create agents with monitoring tools
        info_agent = agent_client.create_agent(
            model=MODEL_DEPLOYMENT_NAME,
            instructions=info_instructions,
            tools=MONITORING_TOOLS + DOCUMENT_TOOLS
        )
        
        detector_agent = agent_client.create_agent(
            model=MODEL_DEPLOYMENT_NAME,
            instructions=detector_instructions,
            tools=MONITORING_TOOLS + DOCUMENT_TOOLS
        )
        
        analyzer_agent = agent_client.create_agent(
            model=MODEL_DEPLOYMENT_NAME,
            instructions=analyzer_instructions,
            tools=MONITORING_TOOLS + DOCUMENT_TOOLS
        )
        
        alerting_agent = agent_client.create_agent(
            model=MODEL_DEPLOYMENT_NAME,
            instructions=alerting_instructions,
            tools=MONITORING_TOOLS + DOCUMENT_TOOLS
        )
        
        print("✅ All agents created successfully with monitoring tools")
        
        # Create executors
        info_executor = InfoAgent(info_agent)
        detector_executor = DetectorAgentExecutor(detector_agent)
        analyzer_executor = AnalyzerAgentExecutor(analyzer_agent)
        alerting_executor = AlertingAgentExecutor(alerting_agent)
        
        # Build workflow
        workflow = (
            WorkflowBuilder("monitoring_workflow")
            .add_executor(route_request)
            .add_executor(info_executor)
            .add_executor(detector_executor)
            .add_executor(analyzer_executor)
            .add_executor(alerting_executor)
            .add_dependency("routing_executor", "info")
            .add_dependency("routing_executor", "detector")
            .add_dependency("detector", "analyzer")
            .add_dependency("analyzer", "alerting")
            .build()
        )
        
        print("✅ Monitoring workflow created successfully")
        return workflow
        
    except Exception as e:
        print(f"❌ Error creating monitoring workflow: {str(e)}")
        print(f"💡 Make sure your Azure credentials are set up and the endpoint is correct")
        raise

async def run_monitoring_session():
    """Run an interactive monitoring session."""
    
    workflow = await create_monitoring_workflow()
    
    print("\n" + "="*60)
    print("🔍 SERVICE MONITORING AGENT")
    print("="*60)
    print("I can help you monitor services, investigate issues, and manage alerts.")
    print("Examples:")
    print("• 'Check the health of our payment service'")
    print("• 'Investigate high CPU usage on web servers'") 
    print("• 'What's the status of our database cluster?'")
    print("• 'Analyze recent error logs for authentication service'")
    print("• 'Tell me about our monitoring policies'")
    print("\nType 'exit' to quit")
    print("="*60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye! Thanks for using Service Monitoring Agent.")
                break
                
            if not user_input:
                continue
            
            print(f"\n🤖 Processing your request...")
            
            # Run workflow with user input
            async for output in workflow.run(user_input):
                if isinstance(output, WorkflowOutputEvent):
                    print(f"\n📋 Final Result:\n{output.data}")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Service Monitoring Agent.")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again with a different request.")

def main():
    """Main entry point for the monitoring workflow."""
    try:
        asyncio.run(run_monitoring_session())
    except KeyboardInterrupt:
        print("\n👋 Monitoring session ended.")
    except Exception as e:
        print(f"❌ Failed to start monitoring workflow: {str(e)}")

if __name__ == "__main__":
    main()