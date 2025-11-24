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

        CRITICAL INSTRUCTIONS - Follow these steps EXACTLY:

        STEP 0: PLAN THE STRUCTURE FIRST
        Before creating ANY files, call plan_project_structure("frontend-react") to see the correct directory structure.
        Study the output carefully to understand where each file should be placed.

        STEP 1: CREATE FRONTEND FILES IN CORRECT LOCATIONS
        You MUST use the EXACT file paths shown below. DO NOT create files at the root level or wrong locations!

        Create these files using create_file_with_content tool:

        a) frontend/package.json - Include:
           {{
             "name": "{project_name.lower().replace(' ', '-')}",
             "version": "0.1.0",
             "private": true,
             "dependencies": {{
               "react": "^18.2.0",
               "react-dom": "^18.2.0"
             }},
             "scripts": {{
               "start": "react-scripts start",
               "build": "react-scripts build",
               "test": "react-scripts test"
             }}
           }}

        b) frontend/public/index.html - Basic HTML template with:
           - <!DOCTYPE html> and proper structure
           - <div id="root"></div>
           - Title: {project_name}

        c) frontend/src/index.js - React entry point:
           - Import React, ReactDOM, index.css, App
           - ReactDOM.createRoot(document.getElementById('root')).render(<App />)

        d) frontend/src/index.css - Global styles

        e) frontend/src/App.js - Main React component with:
           - useState for managing {resource_name} items
           - useEffect to fetch from {api_url}/{resource_name.lower()}s on mount
           - Display list of {resource_name} items
           - Add new {resource_name} functionality
           - Delete {resource_name} functionality
           - Modern, clean UI

        f) frontend/src/App.css - Styling for App component

        g) frontend/Dockerfile - Multi-stage build:
           - Stage 1: Build with node:16-alpine
           - Stage 2: Serve with nginx:alpine
           - Copy build files to nginx html directory

        h) frontend/.dockerignore - Exclude:
           node_modules/
           build/
           .git/

        CRITICAL PATH RULES:
        ✓ CORRECT: "frontend/package.json"
        ✓ CORRECT: "frontend/public/index.html"
        ✓ CORRECT: "frontend/src/App.js"
        ✓ CORRECT: "frontend/src/App.css"
        ✗ WRONG: "package.json" (missing frontend/ prefix)
        ✗ WRONG: "src/App.js" (missing frontend/ prefix)
        ✗ WRONG: "frontend/src" (this is a directory, not a file)

        STEP 2: VERIFY ALL PATHS
        Before calling create_file_with_content, you can optionally use validate_file_path to verify the path is correct.

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
