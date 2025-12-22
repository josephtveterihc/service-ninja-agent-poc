from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectEnvironmentModel:
    """Model representing a project environment in the Service Ninja system."""
    
    id: str
    name: str
    description: str
    project_id: str
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        if not self.id:
            raise ValueError("Environment ID cannot be empty")
        if not self.name:
            raise ValueError("Environment name cannot be empty")
        if not self.project_id:
            raise ValueError("Project ID cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert the project environment model to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project_id": self.project_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectEnvironmentModel":
        """Create a ProjectEnvironmentModel instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            project_id=data.get("project_id", "")
        )
    
    def __str__(self) -> str:
        """String representation of the project environment."""
        return f"ProjectEnvironment(id='{self.id}', name='{self.name}', description='{self.description}', project_id='{self.project_id}')"