"""Orchestrator Agent - Coordinates all specialized agents."""

from typing import Optional, List, Dict
from smolagents import InferenceClientModel
from src.agents.backend_agent import BackendAgent
from src.agents.frontend_agent import FrontendAgent
from src.agents.docker_agent import DockerAgent
from src.agents.test_agent import TestAgent
from src.agents.planner_agent import PlannerAgent
from src.utils.logger import log
from src.utils.config import settings


class OrchestratorAgent:
    """
    Master agent that coordinates the work of specialized agents.

    This agent understands high-level requirements and delegates tasks
    to specialized agents (Planner, Backend, Frontend, Docker, Test).

    Supports two modes:
    1. Manual mode: User provides structured parameters (project_name, resources, fields)
    2. Autonomous mode: User provides natural language description, system extracts everything
    """

    def __init__(self, model_id: Optional[str] = None, verbose: bool = True):
        self.model_id = model_id or settings.HF_MODEL
        self.verbose = verbose

        log.info("=" * 60)
        log.info("Initializing Full-Stack Multi-Agent System")
        log.info("=" * 60)

        # Create shared model instance for all agents (optimization!)
        log.info("Creating shared model instance...")
        self.shared_model = InferenceClientModel(model_id=self.model_id)

        # Initialize specialized agents with shared model
        self.planner_agent = PlannerAgent(model=self.shared_model, verbose=self.verbose)
        self.backend_agent = BackendAgent(model=self.shared_model, verbose=self.verbose)
        self.frontend_agent = FrontendAgent(model=self.shared_model, verbose=self.verbose)
        self.docker_agent = DockerAgent(model=self.shared_model, verbose=self.verbose)
        self.test_agent = TestAgent(model=self.shared_model, verbose=self.verbose)

        log.info("All specialized agents initialized with shared model")
        log.info("=" * 60)
    
    def create_from_description(self, description: str) -> Dict[str, str]:
        """
        Create a complete full-stack application from a natural language description.

        This is the AUTONOMOUS mode where the system analyzes the description
        and automatically extracts project specifications.

        Args:
            description: Natural language description of the application to build

        Returns:
            Dictionary with results from each agent

        Example:
            >>> orchestrator = OrchestratorAgent()
            >>> result = orchestrator.create_from_description(
            ...     "I want to build a blog platform where users can create, edit and delete posts. "
            ...     "Each post should have a title, content, author, and publication date."
            ... )
        """
        log.info("\n🤖 AUTONOMOUS MODE: Analyzing your description...")

        # Step 0: Analyze description using PlannerAgent
        specification = self.planner_agent.analyze_description(description)

        # Display analyzed specification for user confirmation
        log.info("\n📋 Project Specification:")
        log.info(f"   Name: {specification['project_name']}")
        log.info(f"   Description: {specification['description']}")
        log.info(f"   Resources: {[r['name'] for r in specification['resources']]}")
        log.info(f"   Features: {len(specification['features'])} identified")
        log.info(f"   Tech Stack: {specification['tech_preferences']}")

        # Use the main resource (first one) for the app generation
        if not specification['resources']:
            log.error("❌ No resources identified in description")
            return {"error": "Failed to identify resources from description"}

        main_resource = specification['resources'][0]
        resource_name = main_resource['name']
        fields = main_resource['fields']

        # Call the standard create_fullstack_app with extracted parameters
        return self.create_fullstack_app(
            project_name=specification['project_name'],
            resource_name=resource_name,
            fields=fields,
            include_tests=specification.get('include_tests', True),
            include_docker=specification.get('include_docker', True),
            add_database=specification.get('add_database', False),
        )

    def create_fullstack_app(
        self,
        project_name: str,
        resource_name: str,
        fields: List[Dict[str, str]],
        include_tests: bool = True,
        include_docker: bool = True,
        add_database: bool = False,
    ) -> Dict[str, str]:
        """
        Create a complete full-stack application (MANUAL mode).

        Args:
            project_name: Name of the project (e.g., "Blog Platform")
            resource_name: Main resource name (e.g., "Post", "User")
            fields: List of field dicts with 'name' and 'type' keys
            include_tests: Whether to generate tests
            include_docker: Whether to generate Docker configuration
            add_database: Whether to add database integration

        Returns:
            Dictionary with results from each agent
        """
        log.info(f"\n🚀 Starting full-stack application generation: {project_name}")
        log.info(f"   Resource: {resource_name}")
        log.info(f"   Fields: {fields}")
        
        results = {}
        
        # Step 1: Generate Backend
        log.info("\n📦 [1/4] Generating Backend (FastAPI)...")
        try:
            backend_result = self.backend_agent.generate_backend(
                project_name=project_name,
                resource_name=resource_name,
                fields=fields
            )
            results['backend'] = backend_result
            log.info("✅ Backend generation complete")
        except Exception as e:
            log.error(f"❌ Backend generation failed: {str(e)}")
            results['backend'] = f"Error: {str(e)}"
        
        # Optional: Add database
        if add_database:
            log.info("\n💾 Adding database integration...")
            try:
                db_result = self.backend_agent.add_database("backend", settings.DEFAULT_DB)
                results['database'] = db_result
                log.info("✅ Database integration complete")
            except Exception as e:
                log.error(f"❌ Database integration failed: {str(e)}")
                results['database'] = f"Error: {str(e)}"
        
        # Step 2: Generate Frontend
        log.info("\n🎨 [2/4] Generating Frontend (React)...")
        try:
            frontend_result = self.frontend_agent.generate_frontend(
                project_name=project_name,
                resource_name=resource_name
            )
            results['frontend'] = frontend_result
            log.info("✅ Frontend generation complete")
        except Exception as e:
            log.error(f"❌ Frontend generation failed: {str(e)}")
            results['frontend'] = f"Error: {str(e)}"
        
        # Step 3: Generate Tests
        if include_tests:
            log.info("\n🧪 [3/4] Generating Tests...")
            try:
                # Backend tests
                endpoints = [f"/{resource_name.lower()}s", "GET, POST, PUT, DELETE"]
                test_result = self.test_agent.generate_backend_tests(
                    project_name=project_name,
                    resource_name=resource_name,
                    endpoints=endpoints
                )
                results['tests_backend'] = test_result
                
                # Frontend tests
                frontend_test_result = self.test_agent.generate_frontend_tests(
                    project_name=project_name,
                    components=["App"]
                )
                results['tests_frontend'] = frontend_test_result
                log.info("✅ Tests generation complete")
            except Exception as e:
                log.error(f"❌ Tests generation failed: {str(e)}")
                results['tests'] = f"Error: {str(e)}"
        
        # Step 4: Generate Docker Configuration
        if include_docker:
            log.info("\n🐳 [4/4] Generating Docker Configuration...")
            try:
                docker_result = self.docker_agent.generate_docker_compose(
                    project_name=project_name,
                    has_database=add_database
                )
                results['docker'] = docker_result
                log.info("✅ Docker configuration complete")
            except Exception as e:
                log.error(f"❌ Docker configuration failed: {str(e)}")
                results['docker'] = f"Error: {str(e)}"
        
        # Summary
        log.info("\n" + "=" * 60)
        log.info("🎉 Full-Stack Application Generation Complete!")
        log.info("=" * 60)
        log.info(f"\nProject: {project_name}")
        log.info(f"Location: fullstack-agent/outputs/")
        log.info("\nComponents generated:")
        for component, result in results.items():
            status = "✅" if "Error" not in str(result) else "❌"
            log.info(f"  {status} {component}")
        
        log.info("\n📚 Next steps:")
        log.info(f"  1. Navigate to: {settings.OUTPUTS_DIR}")
        log.info("  2. Run: docker-compose up --build")
        log.info("  3. Access frontend at: http://localhost:3000")
        log.info("  4. Access API at: http://localhost:8000")
        log.info("  5. View API docs at: http://localhost:8000/docs")

        return results
    
    def extend_application(
        self,
        project_path: str,
        extension_type: str,
        **kwargs
    ) -> str:
        """
        Extend an existing application with additional features.
        
        Args:
            project_path: Path to the project
            extension_type: Type of extension (auth, database, form, routing, etc.)
            **kwargs: Additional arguments for the extension
        
        Returns:
            Result message
        """
        log.info(f"\n🔧 Extending application with: {extension_type}")
        
        if extension_type == "auth":
            return self.backend_agent.add_authentication(project_path)
        elif extension_type == "database":
            db_type = kwargs.get("db_type", "sqlite")
            return self.backend_agent.add_database(project_path, db_type)
        elif extension_type == "form":
            resource_name = kwargs.get("resource_name")
            fields = kwargs.get("fields", [])
            return self.frontend_agent.add_form(project_path, resource_name, fields)
        elif extension_type == "routing":
            return self.frontend_agent.add_routing(project_path)
        elif extension_type == "nginx":
            return self.docker_agent.add_nginx_reverse_proxy(project_path)
        elif extension_type == "k8s":
            return self.docker_agent.generate_k8s_config(kwargs.get("project_name"))
        elif extension_type == "coverage":
            return self.test_agent.add_coverage_config(project_path)
        else:
            return f"Unknown extension type: {extension_type}"


def create_orchestrator(model_id: Optional[str] = None, verbose: bool = True) -> OrchestratorAgent:
    """Factory function to create an OrchestratorAgent."""
    return OrchestratorAgent(model_id=model_id, verbose=verbose)
