"""
Example: Using Autonomous Mode

This example demonstrates how to use the new autonomous mode where you simply
provide a natural language description of your application, and the system
automatically extracts all necessary information.
"""

import sys
sys.path.insert(0, 'fullstack-agent')

from src.agents import OrchestratorAgent


def example_1_simple_blog():
    """Create a simple blog platform using natural language description."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Simple Blog Platform (Autonomous Mode)")
    print("=" * 70)

    # Initialize orchestrator
    orchestrator = OrchestratorAgent(verbose=True)

    # Just describe what you want in natural language!
    description = """
    I want to build a blog platform where users can create, edit, and delete posts.
    Each post should have a title, content, author, and publication date.
    """

    # Let the system figure out everything automatically
    result = orchestrator.create_from_description(description)

    print("\n✅ Blog platform generated!")
    return result


def example_2_ecommerce():
    """Create an e-commerce platform."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: E-Commerce Platform (Autonomous Mode)")
    print("=" * 70)

    orchestrator = OrchestratorAgent(verbose=True)

    description = """
    Build an online store where customers can browse products and make purchases.
    Each product should have a name, description, price, stock quantity, and category.
    Include a shopping cart and checkout functionality.
    """

    result = orchestrator.create_from_description(description)

    print("\n✅ E-commerce platform generated!")
    return result


def example_3_task_manager():
    """Create a task management application."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Task Manager (Autonomous Mode)")
    print("=" * 70)

    orchestrator = OrchestratorAgent(verbose=True)

    description = """
    Create a task management system where users can create tasks with a title,
    description, due date, priority level (high, medium, low), and status
    (todo, in progress, done). Users should be able to filter tasks by status
    and priority.
    """

    result = orchestrator.create_from_description(description)

    print("\n✅ Task manager generated!")
    return result


def example_4_recipe_app():
    """Create a recipe sharing application."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Recipe Sharing App (Autonomous Mode)")
    print("=" * 70)

    orchestrator = OrchestratorAgent(verbose=True)

    description = """
    I need a recipe sharing platform where users can post their favorite recipes.
    Each recipe should have:
    - A catchy name
    - List of ingredients
    - Step-by-step cooking instructions
    - Preparation time in minutes
    - Difficulty level (easy, medium, hard)
    - Cuisine type (Italian, Mexican, Chinese, etc.)
    - A photo URL

    Users should be able to search recipes by name or cuisine type.
    """

    result = orchestrator.create_from_description(description)

    print("\n✅ Recipe app generated!")
    return result


def comparison_manual_vs_autonomous():
    """Compare manual mode vs autonomous mode."""
    print("\n" + "=" * 70)
    print("COMPARISON: Manual Mode vs Autonomous Mode")
    print("=" * 70)

    orchestrator = OrchestratorAgent(verbose=False)

    print("\n📌 OLD WAY (Manual Mode):")
    print("   You had to manually specify:")
    print("   - project_name='blog-platform'")
    print("   - resource_name='Post'")
    print("   - fields=[{'name': 'title', 'type': 'str'}, ...]")
    print("   - include_tests=True")
    print("   - include_docker=True")
    print("   - add_database=False")

    print("\n✨ NEW WAY (Autonomous Mode):")
    print("   Just describe what you want:")
    print('   "I want to build a blog with posts..."')
    print("   The system extracts everything automatically!")

    # Use autonomous mode
    description = "Build a simple blog where users can post articles with titles and content."

    print("\n🤖 Running autonomous mode...")
    result = orchestrator.create_from_description(description)

    print("\n✅ Done! Much easier, right?")
    return result


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        Full-Stack Multi-Agent System - Autonomous Mode           ║
║                                                                   ║
║  New Feature: Just describe your app in natural language!        ║
║  The AI agents will figure out everything automatically.         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    print("\nChoose an example to run:")
    print("1. Simple Blog Platform")
    print("2. E-Commerce Platform")
    print("3. Task Manager")
    print("4. Recipe Sharing App")
    print("5. Comparison: Manual vs Autonomous Mode")
    print("0. Run all examples")

    choice = input("\nEnter your choice (0-5): ").strip()

    if choice == "1":
        example_1_simple_blog()
    elif choice == "2":
        example_2_ecommerce()
    elif choice == "3":
        example_3_task_manager()
    elif choice == "4":
        example_4_recipe_app()
    elif choice == "5":
        comparison_manual_vs_autonomous()
    elif choice == "0":
        example_1_simple_blog()
        example_2_ecommerce()
        example_3_task_manager()
        example_4_recipe_app()
        comparison_manual_vs_autonomous()
    else:
        print("Invalid choice!")

    print("\n" + "=" * 70)
    print("🎉 All done! Check the outputs/ directory for your generated apps.")
    print("=" * 70)
