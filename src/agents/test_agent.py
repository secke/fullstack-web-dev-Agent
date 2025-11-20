"""Test Agent - Generates test files."""

from typing import Optional
from smolagents import InferenceClientModel
from src.agents.base_agent import BaseAgent
from src.utils.logger import log


class TestAgent(BaseAgent):
    """Agent specialized in generating test files."""

    def _log_initialization(self):
        """Log test agent initialization."""
        log.info("Initializing Test Agent")
    
    def generate_backend_tests(self, project_name: str, resource_name: str, endpoints: list) -> str:
        """
        Generate pytest tests for the FastAPI backend.
        
        Args:
            project_name: Name of the project
            resource_name: Main resource name
            endpoints: List of endpoints to test
        
        Returns:
            Result message
        """
        task = f"""
        Create comprehensive tests for the FastAPI backend:
        
        PROJECT: {project_name}
        RESOURCE: {resource_name}
        ENDPOINTS TO TEST: {endpoints}
        
        STEPS:
        1. Create backend/tests directory
        2. Generate tests/__init__.py
        3. Generate tests/conftest.py with:
           - Test client fixture
           - Database fixture (if applicable)
           - Sample data fixtures
        
        4. Generate tests/test_main.py with tests for:
           - Health check endpoint
           - Root endpoint
           - All CRUD operations for {resource_name}:
             * GET /{resource_name.lower()}s (list all)
             * GET /{resource_name.lower()}s/{{id}} (get one)
             * POST /{resource_name.lower()}s (create)
             * PUT /{resource_name.lower()}s/{{id}} (update)
             * DELETE /{resource_name.lower()}s/{{id}} (delete)
           - Error cases (404, 422, etc.)
           - Data validation
        
        5. Generate tests/test_models.py for Pydantic model validation
        
        Use pytest and FastAPI's TestClient.
        Add pytest, httpx to backend requirements if not present.
        """

        log.info(f"Generating backend tests for {project_name}")
        result = self.run_task(task)
        log.info("Backend tests generation complete")
        return result

    def generate_frontend_tests(self, project_name: str, components: list) -> str:
        """
        Generate Jest/React Testing Library tests for frontend.
        
        Args:
            project_name: Name of the project
            components: List of components to test
        
        Returns:
            Result message
        """
        task = f"""
        Create tests for the React frontend:
        
        PROJECT: {project_name}
        COMPONENTS TO TEST: {components}
        
        STEPS:
        1. Update package.json to ensure testing dependencies are present:
           - @testing-library/react
           - @testing-library/jest-dom
           - @testing-library/user-event
        
        2. Generate src/App.test.js with tests for:
           - Component renders without crashing
           - Loading state displays correctly
           - Data fetching works
           - Create/Delete operations work
           - Error handling
        
        3. For each component in {components}, generate corresponding test file
        
        4. Generate src/setupTests.js if needed
        
        Use React Testing Library best practices.
        """

        log.info(f"Generating frontend tests for {project_name}")
        result = self.run_task(task)
        log.info("Frontend tests generation complete")
        return result

    def generate_integration_tests(self, project_name: str) -> str:
        """Generate end-to-end integration tests."""
        task = f"""
        Create integration tests for {project_name}:

        1. Create tests/integration directory
        2. Generate test_full_workflow.py that tests:
           - Starting both backend and frontend
           - Creating an item through the API
           - Fetching the item
           - Updating the item
           - Deleting the item
        3. Add instructions in README for running integration tests
        """
        return self.run_task(task)

    def add_coverage_config(self, project_path: str) -> str:
        """Add code coverage configuration."""
        task = f"""
        Add code coverage to the project at {project_path}:

        Backend:
        1. Add pytest-cov to requirements.txt
        2. Create pytest.ini or setup.cfg with coverage config
        3. Update README with coverage commands

        Frontend:
        1. Update package.json scripts to include coverage
        2. Create jest.config.js if needed
        """
        return self.run_task(task)
