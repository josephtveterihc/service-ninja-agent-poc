from dataclasses import dataclass
from typing import Optional


@dataclass
class ServiceModel:
    """Model representing a service in the Service Ninja system."""
    
    id: str
    name: str
    description: str
    project_id: str
    env_id: Optional[str] = None
    health_check_url: Optional[str] = None
    alive_check_url: Optional[str] = None
    apikey: Optional[str] = None
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        if not self.id:
            raise ValueError("Service ID cannot be empty")
        if not self.name:
            raise ValueError("Service name cannot be empty")
        if not self.project_id:
            raise ValueError("Service project_id cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert ServiceModel to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project_id": self.project_id,
            "env_id": self.env_id,
            "health_check_url": self.health_check_url,
            "alive_check_url": self.alive_check_url,
            "apikey": self.apikey
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ServiceModel':
        """Create ServiceModel from dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            project_id=data.get("project_id", ""),
            env_id=data.get("env_id"),
            health_check_url=data.get("health_check_url"),
            alive_check_url=data.get("alive_check_url"),
            apikey=data.get("apikey")
        )
    
    def __str__(self) -> str:
        """String representation of ServiceModel."""
        return f"Service(id={self.id}, name={self.name}, project_id={self.project_id}, env_id={self.env_id})"