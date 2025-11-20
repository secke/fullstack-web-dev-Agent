"""Frontend Agent - Generates React code."""

from typing import Optional
from smolagents import InferenceClientModel
from src.agents.base_agent import BaseAgent
from src.utils.logger import log


class FrontendAgent(BaseAgent):
    """Agent specialized in generating React frontend code."""

    def _log_initialization(self):
        """Log frontend agent initialization."""
        log.info("Initializing Frontend Agent (React)")
    
    def generate_frontend(self, project_name: str, resource_name: str, api_url: str = "http://localhost:8000") -> str:
        """
        Generate a complete React frontend.
        
        Args:
            project_name: Name of the project
            resource_name: Name of the main resource (must match backend)
            api_url: URL of the backend API
        
        Returns:
            Result message
        """
        task = f"""
        Create a React frontend project with the following specifications:
        
        PROJECT: {project_name}
        RESOURCE: {resource_name}
        API URL: {api_url}
        
        STEPS:
        1. Create frontend directory structure: frontend/src, frontend/public
        2. Generate package.json with React dependencies
        3. Generate public/index.html
        4. Generate src/index.js
        5. Generate src/index.css
        6. Generate src/App.js with:
           - State management for {resource_name} list
           - Fetch data from API on mount
           - Display list of items
           - Add/Delete functionality
           - Modern styling
        7. Generate src/App.css with attractive styling
        8. Generate Dockerfile for production build
        
        Use the create_file_with_content tool for each file.
        The API endpoints should match: /{resource_name.lower()}s for the list.
        """

        log.info(f"Generating React frontend for {project_name}")
        result = self.run_task(task)
        log.info("Frontend generation complete")
        return result

    def add_form(self, project_path: str, resource_name: str, fields: list) -> str:
        """Add a form component for creating/editing resources."""
        task = f"""
        Add a form component to the React frontend at {project_path}:

        1. Create src/components/Form.js with form for {resource_name}
        2. Include fields: {fields}
        3. Add form validation
        4. Integrate with App.js for creating new items
        """
        return self.run_task(task)

    def add_routing(self, project_path: str) -> str:
        """Add React Router for navigation."""
        task = f"""
        Add React Router to the frontend at {project_path}:

        1. Add react-router-dom to package.json
        2. Create src/components/Navbar.js
        3. Create src/pages/Home.js, About.js, etc.
        4. Update App.js with routing configuration
        """
        return self.run_task(task)

    def improve_styling(self, project_path: str, style_framework: str = "custom") -> str:
        """Improve styling with a framework."""
        task = f"""
        Improve the frontend styling at {project_path}:

        {f"1. Add {style_framework} to package.json" if style_framework != "custom" else "1. Enhance custom CSS"}
        2. Update components with better styling
        3. Add responsive design
        4. Add loading states and error handling UI
        """
        return self.run_task(task)
