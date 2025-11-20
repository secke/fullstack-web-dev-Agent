"""Backend Agent - Generates FastAPI code."""

from typing import List, Optional
from smolagents import InferenceClientModel
from src.agents.base_agent import BaseAgent
from src.utils.logger import log


class BackendAgent(BaseAgent):
    """Agent specialized in generating FastAPI backend code."""

    def _log_initialization(self):
        """Log backend agent initialization."""
        log.info("Initializing Backend Agent (FastAPI)")
    
    def generate_backend(self, project_name: str, resource_name: str, fields: List[dict]) -> str:
        """
        Generate a complete FastAPI backend.
        
        Args:
            project_name: Name of the project
            resource_name: Name of the main resource (e.g., "Post", "User")
            fields: List of field dictionaries with 'name' and 'type' keys
        
        Returns:
            Result message
        """
        task = f"""
        Create a FastAPI backend project with the following specifications:
        
        PROJECT: {project_name}
        RESOURCE: {resource_name}
        
        STEPS:
        1. Create project structure: backend directory with subdirectories if needed
        2. Generate main.py with FastAPI app including:
           - CORS middleware
           - Pydantic model for {resource_name} with these fields: {fields}
           - Full CRUD endpoints for {resource_name}
           - Health check endpoint
        3. Generate requirements.txt with FastAPI dependencies
        4. Generate Dockerfile for containerization
        
        Use the create_file_with_content tool for each file.
        Start with creating the directory structure, then create each file.
        
        The resource should be named {resource_name} (singular) with endpoints using {resource_name.lower()}s (plural).
        """

        log.info(f"Generating FastAPI backend for {project_name}")
        result = self.run_task(task)
        log.info("Backend generation complete")
        return result
    
    def add_authentication(self, project_path: str) -> str:
        """Add JWT authentication to the backend."""
        task = f"""
        Add JWT authentication to the FastAPI backend at {project_path}:

        1. Add dependencies: python-jose, passlib, bcrypt to requirements.txt
        2. Create auth.py with JWT token generation and verification
        3. Add login endpoint to main.py
        4. Add protected routes example
        """
        return self.run_task(task)

    def add_database(self, project_path: str, db_type: str = "sqlite") -> str:
        """Add database integration (SQLAlchemy)."""
        task = f"""
        Add {db_type} database integration to the backend at {project_path}:

        1. Add SQLAlchemy to requirements.txt
        2. Create database.py with SQLAlchemy setup
        3. Create models.py with database models
        4. Update main.py to use database instead of in-memory list
        """
        return self.run_task(task)
