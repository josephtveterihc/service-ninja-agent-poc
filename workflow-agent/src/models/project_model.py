from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectModel:
    """Model representing a project in the Service Ninja system."""
    
    id: str
    name: str
    description: str
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        if not self.id:
            raise ValueError("Project ID cannot be empty")
        if not self.name:
            raise ValueError("Project name cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert the project model to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectModel":
        """Create a ProjectModel instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", "")
        )
    
    def __str__(self) -> str:
        """String representation of the project."""
        return f"Project(id='{self.id}', name='{self.name}', description='{self.description}')"
