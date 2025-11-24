"""Docker Agent - Generates Docker configuration."""

from typing import Optional
from smolagents import InferenceClientModel
from src.agents.base_agent import BaseAgent
from src.utils.logger import log
from src.utils.config import settings


class DockerAgent(BaseAgent):
    """Agent specialized in generating Docker and deployment configurations."""

    def _log_initialization(self):
        """Log docker agent initialization."""
        log.info("Initializing Docker Agent")
    
    def generate_docker_compose(self, project_name: str, has_database: bool = False) -> str:
        """
        Generate docker-compose.yml for the full stack.

        Args:
            project_name: Name of the project
            has_database: Whether to include a database service

        Returns:
            Result message
        """
        task = f"""
        Create Docker deployment configuration for {project_name}:

        CRITICAL INSTRUCTIONS - Follow these steps EXACTLY:

        STEP 0: PLAN THE STRUCTURE FIRST
        Before creating ANY files, call plan_project_structure("docker") to see the correct directory structure.

        STEP 1: CREATE DOCKER CONFIG FILES IN CORRECT LOCATIONS
        You MUST use the EXACT file paths shown below:

        a) docker-compose.yml - Create at ROOT level (NOT in subdirectory):
           - version: '3.8'
           - services:
             * backend:
               - build: ./backend
               - ports: ["8000:8000"]
               - environment: [API_HOST=0.0.0.0, API_PORT=8000]
               - depends_on: [database] (if has_database)
             * frontend:
               - build: ./frontend
               - ports: ["3000:80"]
               - environment: [REACT_APP_API_URL=http://localhost:8000]
               - depends_on: [backend]
             {f"* database: (include {settings.DEFAULT_DB} service configuration)" if has_database else ""}
           - networks: [app-network]

        b) README.md - Create at ROOT level (NOT in subdirectory):
           - Project title: {project_name}
           - Description of the application
           - Quick Start section with Docker commands:
             * docker-compose up --build
             * Access URLs (frontend, backend, API docs)
           - Manual Setup section
           - Project Structure section
           - API Documentation section

        c) .gitignore - Create at ROOT level:
           - __pycache__/
           - *.pyc
           - .env
           - node_modules/
           - build/
           - .pytest_cache/
           - *.log

        CRITICAL PATH RULES:
        ✓ CORRECT: "docker-compose.yml" (root level)
        ✓ CORRECT: "README.md" (root level)
        ✓ CORRECT: ".gitignore" (root level)
        ✗ WRONG: "backend/docker-compose.yml" (should be at root)
        ✗ WRONG: "frontend/README.md" (should be at root)

        NOTE: Dockerfiles for backend and frontend should already exist in their respective directories
        (backend/Dockerfile and frontend/Dockerfile). Do NOT recreate them here.

        Use the create_file_with_content tool for each file.
        """

        log.info(f"Generating Docker configuration for {project_name}")
        result = self.run_task(task)
        log.info("Docker configuration complete")
        return result

    def add_database_service(self, project_path: str, db_type: str = "postgres") -> str:
        """Add a database service to docker-compose.yml."""
        task = f"""
        Add {db_type} database service to docker-compose.yml at {project_path}:

        1. Read current docker-compose.yml
        2. Add {db_type} service with:
           - Proper image
           - Environment variables
           - Volume for data persistence
           - Port mapping
        3. Update backend service to depend on database
        4. Add database connection string to backend environment
        """
        return self.run_task(task)

    def add_nginx_reverse_proxy(self, project_path: str) -> str:
        """Add Nginx reverse proxy."""
        task = f"""
        Add Nginx reverse proxy to the deployment at {project_path}:

        1. Create nginx.conf with configuration
        2. Add nginx service to docker-compose.yml
        3. Update port mappings (nginx on port 80)
        4. Configure SSL if needed
        """
        return self.run_task(task)

    def generate_k8s_config(self, project_name: str) -> str:
        """Generate Kubernetes deployment files."""
        task = f"""
        Generate Kubernetes configuration for {project_name}:

        1. Create k8s directory
        2. Generate deployment.yaml for backend
        3. Generate deployment.yaml for frontend
        4. Generate service.yaml for each
        5. Generate ingress.yaml
        6. Generate configmap.yaml for environment variables
        """
        return self.run_task(task)
