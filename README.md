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

### Prerequisites
- **Node.js/Bun**: For the MCP server
- **Python 3.11+**: For the workflow agent
- **Azure CLI**: For authentication

### 1. Clone and Setup Project
```bash
git clone <repository-url>
cd service-ninja-agent-poc
```

### 2. Setup MCP Server (Node.js/TypeScript)
```bash
# Navigate to MCP server directory
cd mcp-server

# Install dependencies using bun (recommended) or npm
bun i
# or
npm install

# Start the MCP server
bun start:dev
# or 
npm run start:dev
```

The MCP server will start on `http://localhost:3000` and provides:
- `POST /mcp/tool/call` - Tool execution endpoint
- `GET /mcp/capabilities` - Server capabilities  
- `GET /mcp/tools` - Available tools

### 3. Setup Workflow Agent (Python)
```bash
# Navigate to workflow agent directory (from project root)
cd workflow-agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Authentication Setup
```bash
# Ensure you're logged into Azure
az login

# Or set up service principal credentials via environment variables
# export AZURE_CLIENT_ID="your-client-id"
# export AZURE_CLIENT_SECRET="your-client-secret" 
# export AZURE_TENANT_ID="your-tenant-id"
```

### 5. Configure Microsoft Foundry Endpoint
```bash
# Set your Microsoft Foundry project endpoint
export AZURE_AI_PROJECT_ENDPOINT="https://your-project-name.ai.azure.com"

# Optionally set your model deployment name (defaults to gpt-4.1-mini)
export AZURE_AI_MODEL_NAME="gpt-4"
```

### 6. Environment Variables
Create `.env` files as needed:

**mcp-server/.env** (optional):
```env
PORT=3000
NODE_ENV=development
```

**workflow-agent/.env** (optional):
```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project-name.ai.azure.com
AZURE_AI_MODEL_NAME=gpt-4
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

## Running the Application

### 1. Start the MCP Server
```bash
# From project root
cd mcp-server
bun run dev
# or
npm run dev
```
The server should start on `http://localhost:3000`

### 2. Run the Workflow Agent

**Option A: VS Code Integration**
```bash
# From project root  
cd workflow-agent
python test_with_vscode.py
```
Then in VS Code:
- View → Command Palette (Cmd + Shift + P)
- Select "Microsoft Foundry: Open ContainerAgent Playground Locally"
- Choose where to run the agent

**Option B: Command Line**
```bash
# From project root
cd workflow-agent
python test_with_command_line.py
```

### 3. Basic Usage Example
```python
# From workflow-agent directory
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

### MCP Server Issues
If you see MCP server connection errors:
- Ensure the MCP server is running: `cd mcp-server && bun run dev`
- Verify it's accessible at `http://localhost:3000`
- Check that the required endpoints are available:
  - `POST /mcp/tool/call` - Tool execution endpoint
  - `GET /mcp/capabilities` - Server capabilities
  - `GET /mcp/tools` - Available tools

### Azure Authentication Issues
If you encounter authentication errors:
- Run `az login` to authenticate with Azure
- Ensure your Azure AI project endpoint is correctly configured
- Check that your service principal has proper permissions
- Verify environment variables are set correctly

### Python Environment Issues
If you encounter Python package conflicts:
1. Create a fresh virtual environment:
   ```bash
   cd workflow-agent
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Uninstall conflicting packages: 
   ```bash
   pip uninstall agent-framework agent-framework-core agent-framework-azure-ai -y
   ```
3. Reinstall from requirements: 
   ```bash
   pip install -r requirements.txt
   ```

### Node.js/Bun Issues
If you have issues with the MCP server:
- Ensure you have Node.js 18+ or Bun installed
- Try clearing node_modules and reinstalling:
  ```bash
  cd mcp-server
  rm -rf node_modules
  bun install  # or npm install
  ```
- Check TypeScript compilation: `bun run build` or `npm run build`

### Development Mode
For development, you can run both components with auto-reload:
```bash
# Terminal 1: MCP Server with auto-reload
cd mcp-server
bun run dev

# Terminal 2: Python agent development
cd workflow-agent  
# Your development commands here
```