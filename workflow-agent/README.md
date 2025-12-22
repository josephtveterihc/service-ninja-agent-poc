# Service Ninja Agent

An AI-powered service management system using Microsoft Agent Framework for managing projects, environments, services, and monitoring service health across different environments.

## Project Structure

```
service-ninja-agent/
├── workflow-agent/
│   ├── src/                               # Source code
│   │   ├── __init__.py                   # Package initialization
│   │   ├── workflow_core.py              # Main workflow with Service Ninja agent
│   │   ├── project_util/                 # Project utilities
│   │   │   └── file_util.py             # File handling utilities
│   │   ├── tools/                        # Agent tools
│   │   │   ├── project_tools.py         # Project management tools
│   │   │   ├── project_environment_tools.py # Environment management
│   │   │   ├── service_tools.py         # Service management tools
│   │   │   ├── alive_check_tools.py     # Service availability checks
│   │   │   └── health_check_tools.py    # Service health monitoring
│   │   └── agent_instructions/           # Agent behavior definitions
│   │       ├── service_ninja.md         # Main Service Ninja agent
│   │       └── response_agent.md        # Response formatting agent
│   ├── requirements.txt                  # Dependencies
│   └── README.md                        # This documentation
├── mcp-server/                          # MCP integration server
└── client/                              # Frontend client
```

## Features

The Service Ninja agent provides comprehensive service management capabilities:

### **Core Management Operations:**
- **Project Management**: Create, update, list, and delete Service Ninja projects
- **Environment Management**: Manage project environments (dev, staging, prod, etc.)
- **Service Management**: Register and manage services within projects
- **Health Monitoring**: Check service availability and health status
- **Cross-Environment Tracking**: Monitor services across multiple environments

### **Available Tools:**
- `get_projects()` / `list_projects()` - List all projects
- `add_project()` / `create_project()` - Create new projects
- `update_project()` - Modify existing projects
- `remove_project()` / `delete_project()` - Delete projects
- `get_project_by_name()` - Find projects by name
- `get_project_environments()` / `list_environments()` - List environments
- `add_project_environment()` / `create_environment()` - Create environments
- `update_project_environment_information()` / `update_environment()` - Update environments
- `remove_project_environment()` / `delete_environment()` - Delete environments
- `get_services()` / `list_resources()` - List services/resources
- `add_service()` / `create_resource()` - Add new services
- `update_service()` / `update_resource()` - Modify services
- `remove_service()` / `delete_resource()` - Remove services
- `check_service_alive()` - Check if service is responding
- `check_service_health()` / `get_service_health()` - Comprehensive health checks
- `check_all_services_in_project()` / `get_project_status()` - Project-wide health status

### **Smart Management Features:**
- ✅ Multi-environment service tracking
- ✅ Real-time health status monitoring
- ✅ Project-based service organization
- ✅ Automated service discovery and registration
- ✅ Cross-environment health correlation
- ✅ Comprehensive service lifecycle management

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **MCP Server Integration**
   The agent integrates with a local MCP server at `http://localhost:3000` for database operations. Ensure your MCP server is running before using the agent.

3. **Authentication Setup**
   - Ensure you're logged into Azure: `az login`
   - Or set up service principal credentials via environment variables

4. **Configure Microsoft Foundry Endpoint**
   ```bash
   # Set your Microsoft Foundry project endpoint
   export AZURE_AI_PROJECT_ENDPOINT="https://your-project-name.ai.azure.com"
   
   # Optionally set your model deployment name (defaults to gpt-4.1-mini)
   export AZURE_AI_MODEL_NAME="gpt-4"
   ```

## How It Works

The system consists of two AI agents working in a workflow:

1. **Service Ninja Agent**: Main agent that handles all service management operations
2. **Response Agent**: Formats and presents responses to users

### Workflow Flow:
```
User Request → Service Ninja (Tools + MCP Server) → Response Agent → User
```

### **Dual Tool Architecture:**
- **Local Tools**: Direct Python functions for immediate operations
- **MCP Server Tools**: Database-backed operations via HTTP calls to local MCP server

## Running the Agent

### **Basic Usage:**
```python
from workflow_core import start_workflow, get_credential
from agent_framework.azure import AzureAIAgentClient

# Create Azure AI client
credential = get_credential()
chat_client = AzureAIAgentClient(credential=credential)

# Start the Service Ninja workflow
workflow_agent = await start_workflow(chat_client, as_agent=True)

# Use the agent
response = await workflow_agent.run("List all my projects")
print(response.messages[-1].content)
```

### **MCP Server Integration:**
The agent automatically connects to your local MCP server for persistent storage operations. Make sure your MCP server is running at `http://localhost:3000` with the following endpoints:
- `POST /mcp/tool/call` - Tool execution endpoint
- `GET /mcp/capabilities` - Server capabilities
- `GET /mcp/tools` - Available tools

## Example Usage

**User Input**: "Create a new project called 'E-commerce Platform'"
**Agent Response**: "I've created the 'E-commerce Platform' project. You can now add environments and services to it."

**User Input**: "Add a production environment to the E-commerce Platform"
**Agent Response**: "Production environment has been added to the E-commerce Platform project."

**User Input**: "Check the health of all services in the E-commerce Platform"
**Agent Response**: "Checking health across all environments... Payment service: Healthy (150ms response), User service: Warning (high CPU), Order service: Healthy."

**User Input**: "List all my projects and their status"
**Agent Response**: "Here are your projects:
- E-commerce Platform: 3 environments, 8 services, 1 warning
- Internal Tools: 2 environments, 4 services, all healthy
- Mobile App Backend: 1 environment, 6 services, all healthy"

## Package Dependencies

- `azure-ai-agentserver-agentframework==1.0.0b7` - Microsoft Agent Framework
- `azure-identity` - Azure authentication
- `httpx` - HTTP client for MCP server communication
- Additional dependencies as listed in `requirements.txt`

## Security Best Practices

This project follows Snyk security guidelines:
- All generated code is scanned for security vulnerabilities
- Dependencies are regularly updated for security patches
- Security issues are automatically detected and fixed during development

## MCP Server Configuration

The agent expects your MCP server to provide these tools:
- Project management: `create_project`, `list_projects`, `get_project_by_name`, `update_project`, `delete_project`
- Environment management: `create_environment`, `list_environments`, `get_environment_by_name`, `update_environment`, `delete_environment`
- Resource/Service management: `create_resource`, `list_resources`, `get_resource_by_name`, `update_resource`, `delete_resource`
- Monitoring: `create_service_monitor`, `get_service_health`, `get_project_status`

## Troubleshooting

### MCP Server Connection Issues
If you see MCP server connection errors:
- Ensure your MCP server is running at `http://localhost:3000`
- Check that the `/mcp/tool/call` endpoint is available
- Verify your MCP server implements the expected tool interface

### Azure Authentication Issues
If you encounter authentication errors:
- Run `az login` to authenticate with Azure
- Ensure your Azure AI project endpoint is correctly configured
- Check that your service principal has proper permissions

### Package Conflicts
If you encounter version conflicts:
1. Uninstall conflicting packages: `pip uninstall agent-framework agent-framework-core agent-framework-azure-ai -y`
2. Reinstall from requirements: `pip install -r requirements.txt`

### Running locally
There are 2 ways to run locally.
1. python test_with_vscode.py
   VSCODE -> View -> Command Palette (cmd + shift + p)
      Microsoft Foundry: Open ContainerAgent Playground Locally
      select where to run the agent

2. python test_with_command_line.py