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
        FIELDS: {fields}

        CRITICAL INSTRUCTIONS - Follow these steps EXACTLY:

        STEP 0: PLAN THE STRUCTURE FIRST
        Before creating ANY files, call plan_project_structure("backend-fastapi") to see the correct directory structure.
        Study the output carefully to understand where each file should be placed.

        STEP 1: CREATE BACKEND FILES IN CORRECT LOCATIONS
        You MUST use the EXACT file paths shown below. DO NOT create files at the root level!

        Create these files using create_file_with_content tool:

        a) backend/main.py - FastAPI application with:
           - Import FastAPI and necessary modules
           - CORS middleware configuration
           - Pydantic model for {resource_name} with fields: {fields}
           - In-memory storage list (e.g., posts_db = [])
           - Health check endpoint: GET /
           - CRUD endpoints for {resource_name.lower()}s:
             * GET /{resource_name.lower()}s - List all
             * POST /{resource_name.lower()}s - Create new
             * GET /{resource_name.lower()}s/{{id}} - Get by ID
             * PUT /{resource_name.lower()}s/{{id}} - Update by ID
             * DELETE /{resource_name.lower()}s/{{id}} - Delete by ID

        b) backend/requirements.txt - Include:
           fastapi>=0.104.0
           uvicorn[standard]>=0.24.0
           pydantic>=2.0.0

        c) backend/Dockerfile - Multi-stage build:
           - Base: python:3.11-slim
           - Install dependencies from requirements.txt
           - Copy main.py
           - Expose port 8000
           - CMD: uvicorn main:app --host 0.0.0.0 --port 8000

        d) backend/.dockerignore - Exclude:
           __pycache__/
           *.pyc
           .pytest_cache/
           .env

        CRITICAL PATH RULES:
        ✓ CORRECT: "backend/main.py"
        ✓ CORRECT: "backend/requirements.txt"
        ✓ CORRECT: "backend/Dockerfile"
        ✗ WRONG: "main.py" (missing backend/ prefix)
        ✗ WRONG: "backend" (this is a directory, not a file)

        STEP 2: VERIFY ALL PATHS
        Before calling create_file_with_content, you can optionally use validate_file_path to verify the path is correct.

        STEP 3: VALIDATE PYTHON CODE
        After generating main.py, use validate_python_syntax to check for syntax errors.

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
