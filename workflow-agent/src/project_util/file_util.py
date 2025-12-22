import os

"""
  Method: load_agent_instructions
  Description: Load agent instructions from external file
  Args:
    agent_name (str): Name of the agent to load instructions for
  Returns:
    str: Agent instructions text content or default instruction if file not found
"""
def load_agent_instructions(agent_name: str) -> str:
    # Get the directory containing this file (src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # agent_instructions is now in the same src directory
    instructions_dir = os.path.join(current_dir, "agent_instructions")
    instructions_file = os.path.join(instructions_dir, f"{agent_name}_agent_instructions.md")
    
    try:
        with open(instructions_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  Warning: Could not find instructions file {instructions_file}")
        return f"You are a {agent_name} agent in a service monitoring system."