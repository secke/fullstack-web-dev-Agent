"""Example usage of the Full-Stack Multi-Agent System."""

import sys
sys.path.insert(0, 'fullstack-agent')

from src.agents.orchestrator import create_orchestrator
from src.utils.logger import log

def example_1_simple_blog():
    """Example 1: Create a simple blog application."""
    log.info("\n" + "=" * 60)
    log.info("EXAMPLE 1: Creating a Blog Application")
    log.info("=" * 60)
    
    # Create orchestrator
    orchestrator = create_orchestrator(verbose=False)
    
    # Define the application
    project_name = "Blog Platform"
    resource_name = "Post"
    fields = [
        {"name": "title", "type": "str"},
        {"name": "content", "type": "str"},
        {"name": "author", "type": "str"},
        {"name": "created_at", "type": "datetime"},
    ]
    
    # Generate the full-stack application
    results = orchestrator.create_fullstack_app(
        project_name=project_name,
        resource_name=resource_name,
        fields=fields,
        include_tests=True,
        include_docker=True,
        add_database=False  # Start simple with in-memory storage
    )
    
    log.info("\n✅ Blog Platform created successfully!")
    log.info("\nTo run the application:")
    log.info("  cd fullstack-agent/outputs/")
    log.info("  docker-compose up --build")


def example_2_todo_app():
    """Example 2: Create a Todo application with database."""
    log.info("\n" + "=" * 60)
    log.info("EXAMPLE 2: Creating a Todo Application")
    log.info("=" * 60)
    
    orchestrator = create_orchestrator(verbose=False)
    
    # Define the application
    project_name = "Todo App"
    resource_name = "Task"
    fields = [
        {"name": "title", "type": "str"},
        {"name": "description", "type": "str"},
        {"name": "completed", "type": "bool"},
        {"name": "priority", "type": "int"},
    ]
    
    # Generate with database integration
    results = orchestrator.create_fullstack_app(
        project_name=project_name,
        resource_name=resource_name,
        fields=fields,
        include_tests=True,
        include_docker=True,
        add_database=True  # With SQLite database
    )
    
    log.info("\n✅ Todo App created successfully!")


def example_3_user_management():
    """Example 3: User management system."""
    log.info("\n" + "=" * 60)
    log.info("EXAMPLE 3: Creating a User Management System")
    log.info("=" * 60)
    
    orchestrator = create_orchestrator(verbose=False)
    
    # Define the application
    project_name = "User Management"
    resource_name = "User"
    fields = [
        {"name": "username", "type": "str"},
        {"name": "email", "type": "str"},
        {"name": "full_name", "type": "str"},
        {"name": "is_active", "type": "bool"},
    ]
    
    # Generate the application
    results = orchestrator.create_fullstack_app(
        project_name=project_name,
        resource_name=resource_name,
        fields=fields,
        include_tests=True,
        include_docker=True,
        add_database=False
    )
    
    log.info("\n✅ User Management System created!")


def example_4_extend_with_auth():
    """Example 4: Extend an existing app with authentication."""
    log.info("\n" + "=" * 60)
    log.info("EXAMPLE 4: Adding Authentication to Existing App")
    log.info("=" * 60)
    
    orchestrator = create_orchestrator(verbose=False)
    
    # Extend the application with JWT auth
    result = orchestrator.extend_application(
        project_path="outputs/backend",
        extension_type="auth"
    )
    
    log.info(f"\nResult: {result}")


def main():
    """Run examples."""
    print("\n" + "=" * 70)
    print("  Full-Stack Multi-Agent System - Examples")
    print("=" * 70)
    
    print("\nAvailable examples:")
    print("  1. Simple Blog Platform")
    print("  2. Todo App with Database")
    print("  3. User Management System")
    print("  4. Extend with Authentication")
    
    # Run Example 1 by default
    # Uncomment others to try them
    
    example_1_simple_blog()
    # example_2_todo_app()
    # example_3_user_management()
    # example_4_extend_with_auth()


if __name__ == "__main__":
    main()
