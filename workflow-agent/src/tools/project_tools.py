import os
import json
import uuid
from typing import List, Union
from agent_framework import ai_function
from src.models.project_model import ProjectModel

@ai_function
def get_projects() -> list:
    """Load projects from the projects.json file."""
    projects_file_path = os.path.join(os.path.dirname(__file__), '../../store/projects.json')
    if not os.path.exists(projects_file_path):
        return []

    with open(projects_file_path, 'r') as f:
        projects = json.load(f)
    
    return projects

@ai_function
def update_project(project_name: str, updates: dict) -> dict:
    """Update specific fields of an existing project by name.
    
    Args:
        project_name: The name of the project to update
        updates: Dictionary containing fields to update (e.g., {"description": "new desc"})
        
    Returns:
        dict: Success status and operation message
    """
    try:
        # Load existing projects
        existing_projects_data = get_projects()
        existing_projects = [ProjectModel.from_dict(proj) for proj in existing_projects_data]
        
        # Find and update the project
        updated_projects = []
        project_found = False
        
        for existing_project in existing_projects:
            if existing_project.name.lower() == project_name.lower():
                # Found the project - create updated version
                # Start with existing values
                updated_data = {
                    "id": existing_project.id,
                    "name": existing_project.name,
                    "description": existing_project.description
                }
                
                # Apply updates from the provided dictionary
                for field, value in updates.items():
                    if field in updated_data:
                        updated_data[field] = value
                
                # Create updated project model
                updated_project = ProjectModel(
                    id=updated_data["id"],
                    name=updated_data["name"],
                    description=updated_data["description"]
                )
                updated_projects.append(updated_project)
                project_found = True
            else:
                # Keep the existing project unchanged
                updated_projects.append(existing_project)
        
        # If no matching project was found, return error
        if not project_found:
            return {
                "success": False,
                "message": f"Project with name '{project_name}' not found"
            }
        
        # Convert updated ProjectModel objects to dictionaries
        projects_data = [proj.to_dict() for proj in updated_projects]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to projects.json file
        projects_file_path = os.path.join(store_dir, 'projects.json')
        with open(projects_file_path, 'w') as f:
            json.dump(projects_data, f, indent=2)
        
        # Create detailed success message
        updated_fields = list(updates.keys())
        fields_str = ", ".join(updated_fields)
        
        return {
            "success": True,
            "message": f"Project '{project_name}' updated successfully. Updated fields: {fields_str}",
            "updated_fields": updated_fields
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating project: {str(e)}"
        }

@ai_function
def add_project(name: str, description: str) -> dict:
    """Add a new project with a randomly generated UUID.
    
    Args:
        name: The name of the project
        description: The description of the project
        
    Returns:
        dict: Success status and project information
    """
    try:
        # Generate a random UUID for the project ID
        project_id = str(uuid.uuid4())
        
        # Create the new ProjectModel
        new_project = ProjectModel(
            id=project_id,
            name=name,
            description=description
        )
        
        # Load existing projects
        existing_projects_data = get_projects()
        
        # Convert existing project data to ProjectModel objects
        existing_projects = [ProjectModel.from_dict(proj) for proj in existing_projects_data]
        
        # Check if a project with the same name already exists
        for existing_project in existing_projects:
            if existing_project.name.lower() == name.lower():
                return {
                    "success": False,
                    "message": f"Project with name '{name}' already exists"
                }
        
        # Add the new project to the list
        existing_projects.append(new_project)
        
        # Convert updated ProjectModel objects to dictionaries
        projects_data = [project.to_dict() for project in existing_projects]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to projects.json file
        projects_file_path = os.path.join(store_dir, 'projects.json')
        with open(projects_file_path, 'w') as f:
            json.dump(projects_data, f, indent=2)
        
        return {
            "success": True,
            "message": f"Project '{name}' added successfully",
            "project": new_project.to_dict()
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error adding project: {str(e)}"
        }

@ai_function
def remove_project(name: str) -> dict:
    """Remove a project from the projects.json file by name.
    Also removes all environments associated with the project (cascade delete).
    
    Args:
        name: The name of the project to remove
        
    Returns:
        dict: Success status and operation message
    """
    try:
        # Load existing projects
        existing_projects_data = get_projects()
        existing_projects = [ProjectModel.from_dict(proj) for proj in existing_projects_data]
        
        # Filter out the project to remove and get its ID
        updated_projects = []
        project_found = False
        project_id_to_remove = None
        
        for existing_project in existing_projects:
            if existing_project.name.lower() == name.lower():
                # Found the project to remove - don't add it to updated list
                project_found = True
                project_id_to_remove = existing_project.id
            else:
                # Keep this project
                updated_projects.append(existing_project)
        
        # If no matching project was found, return error
        if not project_found:
            return {
                "success": False,
                "message": f"Project with name '{name}' not found"
            }
        
        # Remove all environments associated with this project
        environments_removed = 0
        services_removed = 0
        if project_id_to_remove:
            # Remove environments
            environments_file_path = os.path.join(os.path.dirname(__file__), '../../store/project_environments.json')
            if os.path.exists(environments_file_path):
                with open(environments_file_path, 'r') as f:
                    existing_environments = json.load(f)
                
                # Filter out environments belonging to the project being removed
                updated_environments = []
                for env in existing_environments:
                    if env.get('project_id') != project_id_to_remove:
                        updated_environments.append(env)
                    else:
                        environments_removed += 1
                
                # Write updated environments back to file
                with open(environments_file_path, 'w') as f:
                    json.dump(updated_environments, f, indent=2)
            
            # Remove services
            services_file_path = os.path.join(os.path.dirname(__file__), '../../store/services.json')
            if os.path.exists(services_file_path):
                with open(services_file_path, 'r') as f:
                    existing_services = json.load(f)
                
                # Filter out services belonging to the project being removed
                updated_services = []
                for svc in existing_services:
                    if svc.get('project_id') != project_id_to_remove:
                        updated_services.append(svc)
                    else:
                        services_removed += 1
                
                # Write updated services back to file
                with open(services_file_path, 'w') as f:
                    json.dump(updated_services, f, indent=2)
        
        # Convert updated ProjectModel objects to dictionaries
        projects_data = [project.to_dict() for project in updated_projects]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to projects.json file
        projects_file_path = os.path.join(store_dir, 'projects.json')
        with open(projects_file_path, 'w') as f:
            json.dump(projects_data, f, indent=2)
        
        # Create detailed success message
        message = f"Project '{name}' removed successfully"
        details = []
        if environments_removed > 0:
            details.append(f"{environments_removed} environment(s)")
        if services_removed > 0:
            details.append(f"{services_removed} service(s)")
        if details:
            message += f" along with {', '.join(details)}"
        
        return {
            "success": True,
            "message": message,
            "environments_removed": environments_removed,
            "services_removed": services_removed
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error removing project: {str(e)}"
        }

@ai_function
def get_project_by_name(name: str) -> dict:
    """Get a specific project by name from the projects.json file.
    
    Args:
        name: The name of the project to find
        
    Returns:
        dict: Success status and project information if found
    """
    try:
        # Load existing projects
        existing_projects_data = get_projects()
        
        # Search for the project by name (case-insensitive)
        for project_data in existing_projects_data:
            project = ProjectModel.from_dict(project_data)
            if project.name.lower() == name.lower():
                return {
                    "success": True,
                    "message": f"Project '{name}' found",
                    "project": project.to_dict()
                }
        
        # Project not found
        return {
            "success": False,
            "message": f"Project with name '{name}' not found"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error searching for project: {str(e)}"
        }