import os
import json
import requests
from typing import Dict, Optional
from agent_framework import ai_function
from src.models.service_model import ServiceModel

@ai_function
def check_service_alive(service_name: str, project_id: str, env_id: str, timeout: int = 30) -> dict:
    """Check if a service is alive by calling its health check endpoint.
    
    Args:
        service_name: The name of the service to check
        project_id: The ID of the project the service belongs to
        env_id: The ID of the environment the service belongs to
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        dict: Status check results with service_name, project_name, env_name and alive status
    """
    try:
        # Load services to find the specific service
        services_file_path = os.path.join(os.path.dirname(__file__), '../../store/services.json')
        if not os.path.exists(services_file_path):
            return {
                "success": False,
                "message": "Services file not found"
            }
        
        with open(services_file_path, 'r') as f:
            services_data = json.load(f)
        
        # Find the specific service
        service_found = None
        for service_data in services_data:
            service = ServiceModel.from_dict(service_data)
            if (service.name.lower() == service_name.lower() and 
                service.project_id == project_id and 
                service.env_id == env_id):
                service_found = service
                break
        
        if not service_found:
            return {
                "success": False,
                "message": f"Service '{service_name}' not found for project/environment combination"
            }
        
        # Get project name
        projects_file_path = os.path.join(os.path.dirname(__file__), '../../store/projects.json')
        project_name = "Unknown Project"
        if os.path.exists(projects_file_path):
            with open(projects_file_path, 'r') as f:
                projects_data = json.load(f)
                for project in projects_data:
                    if project.get('id') == project_id:
                        project_name = project.get('name', 'Unknown Project')
                        break
        
        # Get environment name
        environments_file_path = os.path.join(os.path.dirname(__file__), '../../store/project_environments.json')
        env_name = "Unknown Environment"
        if os.path.exists(environments_file_path):
            with open(environments_file_path, 'r') as f:
                environments_data = json.load(f)
                for env in environments_data:
                    if env.get('id') == env_id:
                        env_name = env.get('name', 'Unknown Environment')
                        break
        
        # Check if service has a health check URL
        endpoint_url = service_found.alive_check_url or service_found.health_check_url
        if not endpoint_url:
            return {
                "success": False,
                "service_name": service_name,
                "project_name": project_name,
                "env_name": env_name,
                "is_alive": False,
                "message": f"Service '{service_name}' has no health check URL configured"
            }
        
        import time
        start_time = time.time()
        
        # Make the HTTP request to the health check endpoint
        response = requests.get(
            endpoint_url,
            timeout=timeout,
            headers={'User-Agent': 'Service-Ninja-Agent/1.0'}
        )
        
        end_time = time.time()
        response_time_ms = round((end_time - start_time) * 1000, 2)
        
        # Check if the response indicates the service is alive
        is_alive = response.status_code >= 200 and response.status_code < 300
        
        return {
            "success": True,
            "service_name": service_name,
            "project_name": project_name,
            "env_name": env_name,
            "endpoint_url": endpoint_url if 'endpoint_url' in locals() else None,
            "is_alive": is_alive,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "message": f"Service '{service_name}' in {project_name}/{env_name} is {'alive' if is_alive else 'not responding'} (HTTP {response.status_code})",
            "response_headers": dict(response.headers),
            "response_body": response.text[:500] if response.text else None  # Limit response body to 500 chars
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "service_name": service_name,
            "project_name": project_name if 'project_name' in locals() else "Unknown Project",
            "env_name": env_name if 'env_name' in locals() else "Unknown Environment",
            "endpoint_url": endpoint_url if 'endpoint_url' in locals() else None,
            "is_alive": False,
            "error_type": "timeout",
            "message": f"Service '{service_name}' health check timed out after {timeout} seconds",
            "timeout": timeout
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "service_name": service_name,
            "project_name": project_name if 'project_name' in locals() else "Unknown Project",
            "env_name": env_name if 'env_name' in locals() else "Unknown Environment",
            "endpoint_url": endpoint_url if 'endpoint_url' in locals() else None,
            "is_alive": False,
            "error_type": "connection_error",
            "message": f"Service '{service_name}' is unreachable - connection failed"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "service_name": service_name,
            "project_name": project_name if 'project_name' in locals() else "Unknown Project",
            "env_name": env_name if 'env_name' in locals() else "Unknown Environment",
            "endpoint_url": endpoint_url if 'endpoint_url' in locals() else None,
            "is_alive": False,
            "error_type": "request_error",
            "message": f"Service '{service_name}' health check failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "service_name": service_name,
            "project_name": project_name if 'project_name' in locals() else "Unknown Project",
            "env_name": env_name if 'env_name' in locals() else "Unknown Environment",
            "endpoint_url": endpoint_url if 'endpoint_url' in locals() else None,
            "is_alive": False,
            "error_type": "unknown_error",
            "message": f"Unexpected error checking service '{service_name}': {str(e)}"
        }

@ai_function
def check_service_alive_by_id(service_id: str, endpoint_url: str, timeout: int = 30) -> dict:
    """Check if a service is alive by service ID.
    
    Args:
        service_id: The ID of the service to check
        endpoint_url: The URL of the health check endpoint
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        dict: Status check results including success, response time, and details
    """
    try:
        # Load services to find the service by ID
        services_file_path = os.path.join(os.path.dirname(__file__), '../../store/services.json')
        if not os.path.exists(services_file_path):
            return {
                "success": False,
                "message": "Services file not found"
            }
        
        with open(services_file_path, 'r') as f:
            services_data = json.load(f)
        
        # Find the service by ID
        service_found = None
        for service_data in services_data:
            if service_data.get('id') == service_id:
                service_found = ServiceModel.from_dict(service_data)
                break
        
        if not service_found:
            return {
                "success": False,
                "message": f"Service with ID '{service_id}' not found"
            }
        
        # Use the main check function
        return check_service_alive(
            service_name=service_found.name,
            project_id=service_found.project_id,
            env_id=service_found.env_id or "unknown",
            timeout=timeout
        )
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error checking service by ID: {str(e)}"
        }

@ai_function
def check_all_services_in_project(project_id: str, base_endpoint_pattern: str, timeout: int = 30) -> dict:
    """Check all services in a project for alive status.
    
    Args:
        project_id: The ID of the project
        base_endpoint_pattern: Base URL pattern with {service_name} placeholder (e.g., "https://{service_name}.example.com/health")
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        dict: Results for all services in the project
    """
    try:
        # Load services for the project
        services_file_path = os.path.join(os.path.dirname(__file__), '../../store/services.json')
        if not os.path.exists(services_file_path):
            return {
                "success": False,
                "message": "Services file not found"
            }
        
        with open(services_file_path, 'r') as f:
            services_data = json.load(f)
        
        # Filter services for this project
        project_services = [ServiceModel.from_dict(svc) for svc in services_data if svc.get('project_id') == project_id]
        
        if not project_services:
            return {
                "success": True,
                "message": f"No services found for project ID '{project_id}'",
                "project_id": project_id,
                "services_checked": 0,
                "results": []
            }
        
        # Check each service
        results = []
        alive_count = 0
        
        for service in project_services:
            # Replace service name in the endpoint pattern
            endpoint_url = base_endpoint_pattern.replace("{service_name}", service.name.lower().replace(" ", "-"))
            
            check_result = check_service_alive(
                service_name=service.name,
                project_id=service.project_id,
                env_id=service.env_id or "unknown",
                timeout=timeout
            )
            
            if check_result.get("is_alive", False):
                alive_count += 1
            
            results.append(check_result)
        
        return {
            "success": True,
            "message": f"Checked {len(project_services)} services for project. {alive_count} are alive, {len(project_services) - alive_count} are not responding",
            "project_id": project_id,
            "services_checked": len(project_services),
            "services_alive": alive_count,
            "services_down": len(project_services) - alive_count,
            "results": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error checking services in project: {str(e)}"
        }