import os
import json
import uuid
from typing import List, Union
from agent_framework import ai_function
from src.models.project_environment_model import ProjectEnvironmentModel

@ai_function
def get_project_environments() -> list:
    """Load project environments from the project_environments.json file."""
    environments_file_path = os.path.join(os.path.dirname(__file__), '../../store/project_environments.json')
    if not os.path.exists(environments_file_path):
        return []

    with open(environments_file_path, 'r') as f:
        environments = json.load(f)
    
    return environments

@ai_function
def update_project_environment_information(environment: ProjectEnvironmentModel) -> bool:
    """Update an existing project environment in the project_environments.json file by name.
    Only updates an environment that already exists - does not add new ones.
    
    Args:
        environment: A ProjectEnvironmentModel object to update
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load existing environments
        existing_environments_data = get_project_environments()
        existing_environments = [ProjectEnvironmentModel.from_dict(env) for env in existing_environments_data]
        
        # Update existing environment by finding match by name
        updated_environments = []
        environment_found = False
        
        for existing_environment in existing_environments:
            if existing_environment.name.lower() == environment.name.lower():
                # Found a match - use the updated environment
                updated_environments.append(environment)
                environment_found = True
            else:
                # Keep the existing environment unchanged
                updated_environments.append(existing_environment)
        
        # If no matching environment was found, return False
        if not environment_found:
            print(f"Project environment with name '{environment.name}' not found")
            return False
        
        # Convert updated ProjectEnvironmentModel objects to dictionaries
        environments_data = [env.to_dict() for env in updated_environments]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to project_environments.json file
        environments_file_path = os.path.join(store_dir, 'project_environments.json')
        with open(environments_file_path, 'w') as f:
            json.dump(environments_data, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error saving project environment: {e}")
        return False

@ai_function
def add_project_environment(name: str, description: str, project_id: str) -> dict:
    """Add a new project environment with a randomly generated UUID.
    
    Args:
        name: The name of the environment
        description: The description of the environment
        project_id: The ID of the project this environment belongs to
        
    Returns:
        dict: Success status and environment information
    """
    try:
        # Generate a random UUID for the environment ID
        environment_id = str(uuid.uuid4())
        
        # Create the new ProjectEnvironmentModel
        new_environment = ProjectEnvironmentModel(
            id=environment_id,
            name=name,
            description=description,
            project_id=project_id
        )
        
        # Load existing environments
        existing_environments_data = get_project_environments()
        
        # Convert existing environment data to ProjectEnvironmentModel objects
        existing_environments = [ProjectEnvironmentModel.from_dict(env) for env in existing_environments_data]
        
        # Check if an environment with the same name already exists for this project
        for existing_environment in existing_environments:
            if (existing_environment.name.lower() == name.lower() and 
                existing_environment.project_id == project_id):
                return {
                    "success": False,
                    "message": f"Environment with name '{name}' already exists for this project"
                }
        
        # Add the new environment to the list
        existing_environments.append(new_environment)
        
        # Convert updated ProjectEnvironmentModel objects to dictionaries
        environments_data = [environment.to_dict() for environment in existing_environments]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to project_environments.json file
        environments_file_path = os.path.join(store_dir, 'project_environments.json')
        with open(environments_file_path, 'w') as f:
            json.dump(environments_data, f, indent=2)
        
        return {
            "success": True,
            "message": f"Environment '{name}' added successfully to project",
            "environment": new_environment.to_dict()
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error adding environment: {str(e)}"
        }

@ai_function
def remove_project_environment(name: str, project_id: str) -> dict:
    """Remove a project environment from the project_environments.json file by name and project ID.
    
    Args:
        name: The name of the environment to remove
        project_id: The ID of the project the environment belongs to
        
    Returns:
        dict: Success status and operation message
    """
    try:
        # Load existing environments
        existing_environments_data = get_project_environments()
        existing_environments = [ProjectEnvironmentModel.from_dict(env) for env in existing_environments_data]
        
        # Filter out the environment to remove
        updated_environments = []
        environment_found = False
        
        for existing_environment in existing_environments:
            if (existing_environment.name.lower() == name.lower() and 
                existing_environment.project_id == project_id):
                # Found the environment to remove - don't add it to updated list
                environment_found = True
            else:
                # Keep this environment
                updated_environments.append(existing_environment)
        
        # If no matching environment was found, return error
        if not environment_found:
            return {
                "success": False,
                "message": f"Environment with name '{name}' not found for the specified project"
            }
        
        # Convert updated ProjectEnvironmentModel objects to dictionaries
        environments_data = [environment.to_dict() for environment in updated_environments]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to project_environments.json file
        environments_file_path = os.path.join(store_dir, 'project_environments.json')
        with open(environments_file_path, 'w') as f:
            json.dump(environments_data, f, indent=2)
        
        return {
            "success": True,
            "message": f"Environment '{name}' removed successfully from project"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error removing environment: {str(e)}"
        }

@ai_function
def get_project_environment_by_name(name: str, project_id: str) -> dict:
    """Get a specific project environment by name and project ID from the project_environments.json file.
    
    Args:
        name: The name of the environment to find
        project_id: The ID of the project the environment belongs to
        
    Returns:
        dict: Success status and environment information if found
    """
    try:
        # Load existing environments
        existing_environments_data = get_project_environments()
        
        # Search for the environment by name and project ID (case-insensitive)
        for environment_data in existing_environments_data:
            environment = ProjectEnvironmentModel.from_dict(environment_data)
            if (environment.name.lower() == name.lower() and 
                environment.project_id == project_id):
                return {
                    "success": True,
                    "message": f"Environment '{name}' found",
                    "environment": environment.to_dict()
                }
        
        # Environment not found
        return {
            "success": False,
            "message": f"Environment with name '{name}' not found for the specified project"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error searching for environment: {str(e)}"
        }

@ai_function
def get_environments_for_project(project_id: str) -> dict:
    """Get all environments for a specific project.
    
    Args:
        project_id: The ID of the project to get environments for
        
    Returns:
        dict: Success status and list of environments for the project
    """
    try:
        # Load existing environments
        existing_environments_data = get_project_environments()
        
        # Filter environments for the specified project
        project_environments = []
        for environment_data in existing_environments_data:
            environment = ProjectEnvironmentModel.from_dict(environment_data)
            if environment.project_id == project_id:
                project_environments.append(environment.to_dict())
        
        return {
            "success": True,
            "message": f"Found {len(project_environments)} environments for project",
            "environments": project_environments
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting environments for project: {str(e)}"
        }