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

        CRITICAL INSTRUCTIONS - Follow these steps EXACTLY:

        STEP 0: PLAN THE STRUCTURE FIRST
        Before creating ANY files, call plan_project_structure("tests-backend") to see the correct directory structure.

        STEP 1: CREATE TEST FILES IN CORRECT LOCATIONS
        You MUST use the EXACT file paths shown below:

        a) backend/tests/__init__.py - Empty file (just create with empty content)

        b) backend/tests/conftest.py - Pytest configuration with:
           - Import FastAPI TestClient
           - Import the app from main
           - Create test_client fixture
           - Create sample data fixtures for {resource_name}

        c) backend/tests/test_main.py - Comprehensive tests:
           - Test health check endpoint (GET /)
           - Test CRUD operations for {resource_name}:
             * test_get_all_{resource_name.lower()}s()
             * test_create_{resource_name.lower()}()
             * test_get_{resource_name.lower()}_by_id()
             * test_update_{resource_name.lower()}()
             * test_delete_{resource_name.lower()}()
           - Test error cases (404, 422)
           - Test data validation

        d) backend/tests/test_models.py - Pydantic model tests:
           - Test valid {resource_name} model creation
           - Test validation errors

        CRITICAL PATH RULES:
        ✓ CORRECT: "backend/tests/__init__.py"
        ✓ CORRECT: "backend/tests/conftest.py"
        ✓ CORRECT: "backend/tests/test_main.py"
        ✗ WRONG: "tests/test_main.py" (missing backend/ prefix)
        ✗ WRONG: "backend/tests" (this is a directory, not a file)

        Use pytest and FastAPI's TestClient.
        Add pytest>=7.4.0 and httpx to backend/requirements.txt if not already present.
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

        CRITICAL INSTRUCTIONS - Follow these steps EXACTLY:

        STEP 0: PLAN THE STRUCTURE FIRST
        Before creating ANY files, call plan_project_structure("tests-frontend") to see the correct directory structure.

        STEP 1: CREATE TEST FILES IN CORRECT LOCATIONS
        You MUST use the EXACT file paths shown below:

        a) frontend/src/setupTests.js - Jest-dom setup:
           - Import '@testing-library/jest-dom'

        b) frontend/src/App.test.js - App component tests:
           - Test component renders without crashing
           - Test loading state displays correctly
           - Test data fetching works
           - Test create operation works
           - Test delete operation works
           - Test error handling

        c) For each component in {components}, create corresponding test file in frontend/src/

        CRITICAL PATH RULES:
        ✓ CORRECT: "frontend/src/App.test.js"
        ✓ CORRECT: "frontend/src/setupTests.js"
        ✓ CORRECT: "frontend/src/components/Button.test.js"
        ✗ WRONG: "src/App.test.js" (missing frontend/ prefix)
        ✗ WRONG: "App.test.js" (missing frontend/src/ prefix)

        Ensure frontend/package.json includes testing dependencies:
        - @testing-library/react
        - @testing-library/jest-dom
        - @testing-library/user-event

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
