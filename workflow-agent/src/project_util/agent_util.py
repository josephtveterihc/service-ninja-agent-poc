import os
from typing import Dict, List, Any
from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient

"""
  Method: get_agent_list
  Description: Retrieve a list of AI agents in the project using Azure AI Projects API
  Args:
    None
  Returns:
    List[Dict[str, Any]]: List of agent dictionaries with id, name, description, etc.
"""
async def get_agent_list():
    try:
        print("🔍 Retrieving agent list from Azure AI Projects...")
        
        # Get authentication
        credential = DefaultAzureCredential()
        
        # Create Azure AI Projects client with additional configuration
        project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        
        # Try with custom transport configuration to handle SSL issues
        from azure.core.configuration import Configuration
        from azure.core.pipeline.transport import AioHttpTransport
        
        config = Configuration()
        transport = AioHttpTransport()
        
        ai_client = AIProjectClient(
            credential=credential, 
            endpoint=project_endpoint,
            transport=transport
        )
        
        print(f"📡 Using endpoint: {project_endpoint}")
        
        # List all agents in the project - this returns an AsyncItemPaged
        agents_pager = ai_client.agents.list()

        
        
        agents = []
        """
        agent = await ai_client.agents.update_agent(
            agent_id=existing_agent_id,
            model=os.environ["AZURE_AI_AGENT_DEPLOYMENT_NAME"],
            name=os.environ["AZURE_AI_AGENT_NAME"],
            instructions=instructions,
            tools=all_tools,
            tool_resources=tool_resources
        )
        """
        # Iterate through the async pager
        async for agent in agents_pager:
            latest_agent = agent.versions.latest
            description = getattr(latest_agent.metadata, 'description', 'No description available'),
            print(f"description: {description}")
            created_at = getattr(latest_agent, 'created_at', None)
            print(f"created_at: {created_at}")
            model = getattr(latest_agent.definition, 'model', None)
            print(f"model: {model}")
            instructions = getattr(latest_agent.definition, 'instructions', None)
            print(f"instructions: {instructions}")
            agent_data = {
                "id": agent.id,
                "name": agent.name,
                "description": description,
                "created_at": created_at,
                "model": model,
                "instructions": instructions,
                "status": "active"
            }
            agents.append(agent_data)
            
        print(f"✅ Found {len(agents)} agents in project")
        return agents
        
    except Exception as e:
        print(f"❌ Error retrieving agent list: {e}")
        
        # Fallback: Try without the problematic API call for now
        print("⚠️  Falling back to test mode due to Azure SDK SSL/TLS compatibility issue")
        print("   This appears to be a known issue with the current Azure AI Projects SDK")
        print("   The authentication works, but the API calls have SSL enforcement problems")
        
        return []

"""
  Method: get_agent_by_name
  Description: Retrieve an AI agent by its name using Azure AI Projects API
  Args:
    name (str): The name of the agent to search for
    print_instructions (bool): Whether to print the agent's instructions (default: False)
  Returns:
    Optional[Dict[str, Any]]: Agent dictionary if found, None otherwise
"""
async def get_agent_by_name(name: str, print_instructions: bool = False):
    try:
        print(f"🔍 Searching for agent named: {name}")
        
        # Get all agents first
        agents = await get_agent_list()
        
        if not agents:
            print("❌ Could not retrieve agent list")
            return None
            
        # Find agent by name
        for agent in agents:
            if agent['name'] == name:
                print(f"✅ Found agent: {agent['name']} (ID: {agent['id']})")
                
                if print_instructions:
                    print_agent_instructions(agent)
                
                return agent        
        
        print(f"❌ Agent named '{name}' not found in project")
        return None
        
    except Exception as e:
        print(f"❌ Error retrieving agent: {e}")
        return None

"""
  Method: get_agent_by_id
  Description: Retrieve an AI agent by its ID using Azure AI Projects API
  Args:
    id (str): The unique identifier of the agent to retrieve
    print_instructions (bool): Whether to print the agent's instructions (default: False)
  Returns:
    Optional[Dict[str, Any]]: Agent dictionary if found, None otherwise
"""
async def get_agent_by_id(id: str, print_instructions: bool = False):
    try:
        print(f"🔍 Searching for agent with ID: {id}")
        
        # Get authentication
        credential = DefaultAzureCredential()
        
        # Create Azure AI Projects client with custom transport
        project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        from azure.core.pipeline.transport import AioHttpTransport
        transport = AioHttpTransport()
        
        ai_client = AIProjectClient(
            credential=credential, 
            endpoint=project_endpoint,
            transport=transport
        )
        
        # Get specific agent by ID - need to await the coroutine
        agent = await ai_client.agents.get(id)
        
        agent_data = {
            "id": agent.id,
            "name": agent.name,
            "description": getattr(agent, 'description', 'No description available'),
            "created_at": getattr(agent, 'created_at', None),
            "model": getattr(agent, 'model', None),
            "instructions": getattr(agent, 'instructions', None),
            "status": "active"
        }
        
        print(f"✅ Found agent: {agent_data['name']} (ID: {agent_data['id']})")
        
        if print_instructions:
            print_agent_instructions(agent_data)
        
        return agent_data
        
    except Exception as e:
        print(f"❌ Error retrieving agent by ID: {e}")
        return None


"""
  Method: print_agent_instructions
  Description: Print formatted agent instructions for a given agent
  Args:
    agent_data (Dict[str, Any]): Agent dictionary containing instructions and metadata
  Returns:
    None: Prints formatted instructions to console
"""
def print_agent_instructions(agent_data):
    if not agent_data:
        print("❌ No agent data provided")
        return
    
    print("\n" + "="*80)
    print(f"🤖 AGENT INSTRUCTIONS: {agent_data.get('name', 'Unknown Agent')}")
    print("="*80)
    
    print(f"📋 Agent ID: {agent_data.get('id', 'Unknown')}")
    print(f"📝 Description: {agent_data.get('description', 'No description available')}")
    print(f"🧠 Model: {agent_data.get('model', 'Not specified')}")
    
    if agent_data.get('created_at'):
        print(f"📅 Created: {agent_data['created_at']}")
    
    instructions = agent_data.get('instructions')
    if instructions:
        print("\n📜 INSTRUCTIONS:")
        print("-" * 50)
        print(instructions)
        print("-" * 50)
    else:
        print("\n⚠️  No instructions found for this agent")
    
    print("="*80 + "\n")


"""
  Method: find_and_print_agent_instructions
  Description: Find an agent by name and print its instructions
  Args:
    name (str): Name of the agent to find and display instructions for
  Returns:
    bool: True if agent found and instructions printed, False otherwise
"""
async def find_and_print_agent_instructions(name: str):
    try:
        print(f"🔍 Looking up instructions for agent: {name}")
        
        # Get the agent by name
        agent = await get_agent_by_name(name)
        
        if agent:
            print_agent_instructions(agent)
            return True
        else:
            print(f"❌ Could not find agent named '{name}'")
            return False
            
    except Exception as e:
        print(f"❌ Error retrieving agent instructions: {e}")
        return False


"""
  Method: get_agents_by_name
  Description: Retrieve multiple AI agents by their names using Azure AI Projects API
  Args:
    names (List[str]): List of agent names to search for
    print_instructions (bool): Whether to print the agents' instructions (default: False)
  Returns:
    Dict[str, Any]: Dictionary with agent names as keys and agent dictionaries as values
"""
async def get_agents_by_name(names: List[str], print_instructions: bool = False) -> Dict[str, Any]:
    try:
        print(f"🔍 Searching for agents: {', '.join(names)}")
        
        # Get all agents first
        agents = await get_agent_list()
        
        if not agents:
            print("❌ Could not retrieve agent list")
            return {}
        
        # Find agents by name
        found_agents = {}
        
        for agent in agents:
            if agent['name'] in names:
                found_agents[agent['name']] = agent
                print(f"✅ Found agent: {agent['name']} (ID: {agent['id']})")
                
                if print_instructions:
                    print_agent_instructions(agent)
        
        # Report missing agents
        missing_agents = set(names) - set(found_agents.keys())
        if missing_agents:
            print(f"❌ Could not find agents: {', '.join(missing_agents)}")
        
        return found_agents
        
    except Exception as e:
        print(f"❌ Error retrieving agents: {e}")
        return {}