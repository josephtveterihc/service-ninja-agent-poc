import os
import json
import uuid
from typing import List, Union
from agent_framework import ai_function
from src.models.service_model import ServiceModel

@ai_function
def get_services() -> list:
    """Load services from the services.json file."""
    services_file_path = os.path.join(os.path.dirname(__file__), '../../store/services.json')
    if not os.path.exists(services_file_path):
        return []

    with open(services_file_path, 'r') as f:
        services = json.load(f)
    
    return services

@ai_function
def update_service(service_name: str, project_id: str, env_id: str, updates: dict) -> dict:
    """Update specific fields of an existing service by name and project ID.
    
    Args:
        service_name: The name of the service to update
        project_id: The ID of the project the service belongs to
        updates: Dictionary containing fields to update (e.g., {"description": "new desc"})
        
    Returns:
        dict: Success status and operation message
    """
    print('Updating service with the following changes:', updates)
    try:
        # Load existing services
        existing_services_data = get_services()
        existing_services = [ServiceModel.from_dict(svc) for svc in existing_services_data]
        
        # Find and update the service
        updated_services = []
        service_found = False
        
        for existing_service in existing_services:
            if (existing_service.name.lower() == service_name.lower() and 
                existing_service.project_id == project_id and existing_service.env_id == env_id):
                # Found the service - create updated version
                # Start with existing values
                updated_data = {
                    "id": existing_service.id,
                    "name": existing_service.name,
                    "description": existing_service.description,
                    "project_id": existing_service.project_id,
                    "env_id": existing_service.env_id,
                    "health_check_url": existing_service.health_check_url,
                    "alive_check_url": existing_service.alive_check_url,
                    "apikey": existing_service.apikey
                }
                
                # Apply updates from the provided dictionary
                for field, value in updates.items():
                    if field in updated_data:
                        updated_data[field] = value
                
                # Create updated service model
                updated_service = ServiceModel(
                    id=updated_data["id"],
                    name=updated_data["name"],
                    description=updated_data["description"],
                    project_id=updated_data["project_id"],
                    env_id=updated_data["env_id"],
                    health_check_url=updated_data.get("health_check_url"),
                    alive_check_url=updated_data.get("alive_check_url"),
                    apikey=updated_data.get("apikey")
                )
                updated_services.append(updated_service)
                service_found = True
            else:
                # Keep the existing service unchanged
                updated_services.append(existing_service)
        
        # If no matching service was found, return error
        if not service_found:
            return {
                "success": False,
                "message": f"Service with name '{service_name}' not found for the specified project"
            }
        
        # Convert updated ServiceModel objects to dictionaries
        services_data = [svc.to_dict() for svc in updated_services]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to services.json file
        services_file_path = os.path.join(store_dir, 'services.json')
        with open(services_file_path, 'w') as f:
            json.dump(services_data, f, indent=2)
        
        # Create detailed success message
        updated_fields = list(updates.keys())
        fields_str = ", ".join(updated_fields)
        
        return {
            "success": True,
            "message": f"Service '{service_name}' updated successfully. Updated fields: {fields_str}",
            "updated_fields": updated_fields
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating service: {str(e)}"
        }

@ai_function
def add_service(name: str, description: str, project_id: str) -> dict:
    """Add a new service with instances for each environment in the project.
    Creates one service instance for each environment that exists for the project.
    
    Args:
        name: The name of the service
        description: The description of the service
        project_id: The ID of the project this service belongs to
        
    Returns:
        dict: Success status and service information
    """
    try:
        # Load existing environments for the project
        environments_file_path = os.path.join(os.path.dirname(__file__), '../../store/project_environments.json')
        project_environments = []
        
        if os.path.exists(environments_file_path):
            with open(environments_file_path, 'r') as f:
                all_environments = json.load(f)
                # Filter environments for this project
                project_environments = [env for env in all_environments if env.get('project_id') == project_id]
        
        # If no environments exist for the project, return error
        if not project_environments:
            return {
                "success": False,
                "message": f"No environments found for project. Please create environments first before adding services."
            }
        
        # Load existing services
        existing_services_data = get_services()
        existing_services = [ServiceModel.from_dict(svc) for svc in existing_services_data]
        
        # Check if services with the same name already exist for any environment in this project
        for existing_service in existing_services:
            if (existing_service.name.lower() == name.lower() and 
                existing_service.project_id == project_id):
                return {
                    "success": False,
                    "message": f"Service with name '{name}' already exists for this project"
                }
        
        # Create service instances for each environment
        new_services = []
        for environment in project_environments:
            service_id = str(uuid.uuid4())
            new_service = ServiceModel(
                id=service_id,
                name=name,
                description=description,
                project_id=project_id,
                env_id=environment.get('id')
            )
            new_services.append(new_service)
            existing_services.append(new_service)
        
        # Convert updated ServiceModel objects to dictionaries
        services_data = [service.to_dict() for service in existing_services]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to services.json file
        services_file_path = os.path.join(store_dir, 'services.json')
        with open(services_file_path, 'w') as f:
            json.dump(services_data, f, indent=2)
        
        return {
            "success": True,
            "message": f"Service '{name}' added successfully to project with {len(new_services)} instances (one per environment)",
            "services_created": len(new_services),
            "services": [service.to_dict() for service in new_services]
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error adding service: {str(e)}"
        }

@ai_function
def remove_service(name: str, project_id: str) -> dict:
    """Remove a service from the services.json file by name and project ID.
    
    Args:
        name: The name of the service to remove
        project_id: The ID of the project the service belongs to
        
    Returns:
        dict: Success status and operation message
    """
    try:
        # Load existing services
        existing_services_data = get_services()
        existing_services = [ServiceModel.from_dict(svc) for svc in existing_services_data]
        
        # Filter out the service to remove
        updated_services = []
        service_found = False
        
        for existing_service in existing_services:
            if (existing_service.name.lower() == name.lower() and 
                existing_service.project_id == project_id):
                # Found the service to remove - don't add it to updated list
                service_found = True
            else:
                # Keep this service
                updated_services.append(existing_service)
        
        # If no matching service was found, return error
        if not service_found:
            return {
                "success": False,
                "message": f"Service with name '{name}' not found for the specified project"
            }
        
        # Convert updated ServiceModel objects to dictionaries
        services_data = [service.to_dict() for service in updated_services]
        
        # Ensure the store directory exists
        store_dir = os.path.join(os.path.dirname(__file__), '../../store')
        os.makedirs(store_dir, exist_ok=True)
        
        # Write to services.json file
        services_file_path = os.path.join(store_dir, 'services.json')
        with open(services_file_path, 'w') as f:
            json.dump(services_data, f, indent=2)
        
        return {
            "success": True,
            "message": f"Service '{name}' removed successfully from project"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error removing service: {str(e)}"
        }

@ai_function
def get_service_by_name(name: str, project_id: str) -> dict:
    """Get a specific service by name and project ID from the services.json file.
    
    Args:
        name: The name of the service to find
        project_id: The ID of the project the service belongs to
        
    Returns:
        dict: Success status and service information if found
    """
    try:
        # Load existing services
        existing_services_data = get_services()
        
        # Search for the service by name and project ID (case-insensitive)
        for service_data in existing_services_data:
            service = ServiceModel.from_dict(service_data)
            if (service.name.lower() == name.lower() and 
                service.project_id == project_id):
                return {
                    "success": True,
                    "message": f"Service '{name}' found",
                    "service": service.to_dict()
                }
        
        # Service not found
        return {
            "success": False,
            "message": f"Service with name '{name}' not found for the specified project"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error searching for service: {str(e)}"
        }

@ai_function
def get_services_for_project(project_id: str) -> dict:
    """Get all services for a specific project.
    
    Args:
        project_id: The ID of the project to get services for
        
    Returns:
        dict: Success status and list of services for the project
    """
    try:
        # Load existing services
        existing_services_data = get_services()
        
        # Filter services for the specified project
        project_services = []
        for service_data in existing_services_data:
            service = ServiceModel.from_dict(service_data)
            if service.project_id == project_id:
                project_services.append(service.to_dict())
        
        return {
            "success": True,
            "message": f"Found {len(project_services)} services for project",
            "services": project_services
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting services for project: {str(e)}"
        }