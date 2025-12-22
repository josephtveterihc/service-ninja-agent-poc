import os

from agent_framework import WorkflowBuilder
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential, ManagedIdentityCredential
from src.project_util.file_util import load_agent_instructions
from src.tools.project_tools import get_projects, add_project, update_project, remove_project, get_project_by_name
from src.tools.project_environment_tools import (
    get_project_environments, 
    add_project_environment, 
    update_project_environment_information, 
    remove_project_environment, 
    get_project_environment_by_name, 
    get_environments_for_project
)
from src.tools.service_tools import (
    get_services,
    add_service,
    update_service,
    remove_service,
    get_service_by_name,
    get_services_for_project
)
from src.tools.alive_check_tools import (
    check_service_alive,
    check_service_alive_by_id,
    check_all_services_in_project
)
from src.tools.health_check_tools import (
    check_service_health,
    check_service_health_by_id,
    check_all_services_health_in_project,
    check_environment_health
)

def get_credential():
    """Will use Managed Identity when running in Azure, otherwise falls back to DefaultAzureCredential."""
    return (
        ManagedIdentityCredential()
        if os.getenv("MSI_ENDPOINT")
        else DefaultAzureCredential()
    )

def create_mcp_server_tools():
    """Create tools that call the local MCP server endpoints."""
    import httpx
    import json
    
    def create_mcp_tool(name: str, description: str):
        print(f"🔧 Creating MCP tool: {name}")
        async def mcp_tool(**kwargs):
            """Generic MCP tool that calls the local server."""
            print(f"🔧 Invoking MCP tool: {name} with args: {kwargs}")
            try:
                print(f"🌐 Preparing to call MCP server for tool: {name}")
                # Extract arguments from kwargs if they're wrapped
                if len(kwargs) == 1 and 'kwargs' in kwargs:
                    print("📦 Detected wrapped kwargs")
                    # If arguments are wrapped in a kwargs object, extract them
                    if len(kwargs['kwargs']) and isinstance(kwargs['kwargs'], str):
                        arguments = json.loads(kwargs['kwargs'])
                    else:
                        arguments = kwargs['kwargs']
                else:
                    print("📦 Using direct kwargs")
                    # Use kwargs directly
                    arguments = kwargs
                
                print(f"🔧 MCP Tool Call: {name}")
                print(f"📤 Request Arguments: {json.dumps(arguments, indent=2)}")
                
                # Add timeout and better error handling
                timeout = httpx.Timeout(30.0, connect=10.0)
                
                async with httpx.AsyncClient(timeout=timeout) as client:
                    request_payload = {
                        "name": name,
                        "arguments": arguments
                    }
                    
                    print(f"📡 Making request to: http://localhost:3000/mcp/tool/call")
                    print(f"📦 Payload: {json.dumps(request_payload, indent=2)}")
                    
                    response = await client.post(
                        "http://localhost:3000/mcp/tool/call",
                        json=request_payload,
                        headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        }
                    )
                    
                    print(f"📨 Response Status: {response.status_code}")
                    print(f"📋 Response Headers: {dict(response.headers)}")
                    
                    # Check content length
                    content_length = response.headers.get('content-length', 'unknown')
                    print(f"📏 Content Length: {content_length}")
                    
                    # Get raw response text for debugging
                    response_text = response.text
                    print(f"📄 Raw Response (first 500 chars): {response_text[:500]}")
                    
                    if response.status_code == 200:
                        # Check if response is empty
                        if not response_text or not response_text.strip():
                            error_msg = f"Empty response from MCP server for tool: {name}"
                            print(f"❌ {error_msg}")
                            return {"error": error_msg}
                        
                        # Attempt to parse JSON
                        try:
                            result = response.json()
                            print(f"✅ Parsed JSON successfully: {json.dumps(result, indent=2)[:300]}...")
                        except json.JSONDecodeError as json_err:
                            error_msg = f"Invalid JSON response from MCP server: {json_err}. Response: '{response_text[:200]}'"
                            print(f"❌ {error_msg}")
                            return {"error": error_msg}
                        
                        # Handle MCP server error responses
                        if result.get("isError"):
                            error_content = result.get("content", [])
                            if error_content and isinstance(error_content, list) and len(error_content) > 0:
                                error_msg = error_content[0].get("text", "Unknown error from MCP server")
                            else:
                                error_msg = "Unknown error occurred in MCP server"
                            print(f"🔴 MCP Server Error: {error_msg}")
                            return {"error": error_msg}
                        
                        # Handle successful responses
                        content = result.get("content", [])
                        if content and isinstance(content, list) and len(content) > 0:
                            first_content = content[0]
                            print(f"✅ Tool '{name}' returned content: {first_content}")
                            print(f"📊 Content structure: {list(first_content.keys()) if isinstance(first_content, dict) else type(first_content)}")
                            
                            # Try to get data first, then text as fallback
                            if isinstance(first_content, dict):
                                print(f"🔍 Inspecting content keys: {list(first_content.keys())}")
                                if "data" in first_content:
                                    print(f"📥 Returning 'data' from content")
                                    return first_content["data"]
                                elif "text" in first_content:
                                    print(f"📥 Returning 'text' from content")
                                    return first_content["text"]
                                else:
                                    print(f"📥 Returning full content dictionary")
                                    return first_content
                            else:
                                print(f"📥 Returning first content as is. Not a dict")
                                return first_content

                        else:
                            print("✅ Operation completed successfully (no content returned)")
                            return {"message": "Operation completed successfully", "tool": name}
                            
                    elif response.status_code == 404:
                        error_msg = f"MCP server endpoint not found. Is the server running on port 3000?"
                        print(f"❌ {error_msg}")
                        return {"error": error_msg}
                    
                    elif response.status_code == 500:
                        error_msg = f"MCP server internal error: {response_text}"
                        print(f"❌ {error_msg}")
                        return {"error": error_msg}
                    
                    else:
                        error_msg = f"HTTP {response.status_code}: {response_text}"
                        print(f"❌ {error_msg}")
                        return {"error": error_msg}
                        
            except httpx.TimeoutException:
                error_msg = "Request timeout - MCP server may be unresponsive"
                print(f"⏱️ {error_msg}")
                return {"error": error_msg}
                
            except httpx.ConnectError as conn_err:
                error_msg = f"Cannot connect to MCP server at localhost:3000: {conn_err}. Ensure server is running."
                print(f"🔌 {error_msg}")
                return {"error": error_msg}
                
            except Exception as e:
                error_msg = f"Unexpected error calling MCP server: {type(e).__name__}: {str(e)}"
                print(f"💥 {error_msg}")
                return {"error": error_msg}
        
        # Set function metadata for the agent framework
        mcp_tool.__name__ = name.replace('_', ' ').title().replace(' ', '')
        mcp_tool.__doc__ = description
        return mcp_tool

    # Create MCP tools based on your server's capabilities
    return [
        # Project tools
        create_mcp_tool("create_project", "Create a new Service Ninja project"),
        create_mcp_tool("list_projects", "List all Service Ninja projects"),
        create_mcp_tool("get_project_by_id", "Get project by ID"),
        create_mcp_tool("get_project_by_name", "Get project by name"),
        create_mcp_tool("update_project", "Update an existing project"),
        create_mcp_tool("delete_project", "Delete a project"),
        
        # Environment tools
        create_mcp_tool("create_environment", "Create a new environment for a project"),
        create_mcp_tool("list_environments", "List environments for a project"),
        create_mcp_tool("get_environment_by_id", "Get environment by ID"),
        create_mcp_tool("get_environment_by_name", "Get environment by name"),
        create_mcp_tool("update_environment", "Update an existing environment"),
        create_mcp_tool("delete_environment", "Delete an environment"),
        
        # Resource tools
        create_mcp_tool("create_resource", "Create a new resource"),
        create_mcp_tool("list_resources", "List resources"),
        create_mcp_tool("get_resource_by_id", "Get resource by ID"),
        create_mcp_tool("get_resource_by_name", "Get resource by name"),
        create_mcp_tool("update_resource", "Update an existing resource"),
        create_mcp_tool("delete_resource", "Delete a resource"),
        
        # Resource Monitoring tools
        create_mcp_tool("get_resource_health_status", "Get health status of a specific resource by making a request to its health check URL"),
        create_mcp_tool("get_project_resources_health_status", "Get health status of all resources in a specific project environment"),
        create_mcp_tool("get_resource_alive_status", "Check if a specific resource is alive and responding by making a request to its alive check URL"),
    ]

async def start_workflow(chat_client: AzureAIAgentClient, as_agent: bool = True):
    print("🚀 Starting Service Ninja workflow...")
    # Get MCP server tools
    mcp_tools = create_mcp_server_tools()
    
    # Combine with existing tools
    # all_tools = [
    #     get_projects, add_project, update_project, remove_project, get_project_by_name,
    #     get_project_environments, add_project_environment, update_project_environment_information, 
    #     remove_project_environment, get_project_environment_by_name, get_environments_for_project,
    #     get_services, add_service, update_service, remove_service, get_service_by_name, get_services_for_project,
    #     check_service_alive, check_service_alive_by_id, check_all_services_in_project,
    #     check_service_health, check_service_health_by_id, check_all_services_health_in_project, check_environment_health
    # ] + mcp_tools

    response_agent_instructions = load_agent_instructions("response_agent")
    service_ninja_instructions = load_agent_instructions("service_ninja")
    service_ninja = chat_client.create_agent(
        name="Service Ninja",
        instructions=service_ninja_instructions,
        tools=mcp_tools,
    )

    response_agent = chat_client.create_agent(
        name="Response Agent", 
        instructions=response_agent_instructions,
    )

    # Build the workflow by adding agents directly as edges.
    workflow = (
        WorkflowBuilder()
        .set_start_executor(service_ninja)
        .add_edge(service_ninja, response_agent)
        .build()
    )
    
    # If returning as agent, we can set a display name
    if as_agent:
        workflow_agent = workflow.as_agent()
        # The workflow agent will show as "Service Ninja" since it starts with that agent
        return workflow_agent
    else:
        return workflow
