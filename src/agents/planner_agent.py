"""Planner Agent - Analyzes user descriptions and creates project plans."""

import json
from typing import Dict, List, Optional
from smolagents import InferenceClientModel
from src.agents.base_agent import BaseAgent
from src.utils.logger import log


class PlannerAgent(BaseAgent):
    """
    Agent specialized in analyzing user descriptions and creating project specifications.

    This agent takes natural language descriptions of applications and extracts:
    - Project name
    - Main resources and their fields
    - Features to implement
    - Technology preferences
    """

    def _log_initialization(self):
        """Log planner agent initialization."""
        log.info("Initializing Planner Agent (Project Analysis)")

    def analyze_description(self, description: str) -> Dict:
        """
        Analyze a natural language description and extract project specifications.

        Args:
            description: User's description of the application to build

        Returns:
            Dictionary containing:
                - project_name: Extracted or generated project name
                - resources: List of resources with their fields
                - features: List of features to implement
                - tech_stack: Preferred technologies
                - include_tests: Whether to generate tests
                - include_docker: Whether to generate Docker config
                - add_database: Whether to add database integration
        """
        log.info("🔍 Analyzing project description...")

        analysis_task = f"""
Analyze the following application description and extract structured information.

USER DESCRIPTION:
{description}

YOUR TASK:
Extract and return a JSON object with the following structure:
{{
    "project_name": "A concise name for the project (kebab-case)",
    "description": "Brief description of what the app does",
    "resources": [
        {{
            "name": "ResourceName (singular, PascalCase)",
            "fields": [
                {{"name": "field_name", "type": "str|int|float|bool|date"}},
                ...
            ]
        }}
    ],
    "features": [
        "List of main features to implement"
    ],
    "tech_preferences": {{
        "backend": "fastapi|django|flask",
        "frontend": "react|vue|angular",
        "database": "sqlite|postgresql|mongodb|none"
    }},
    "include_tests": true|false,
    "include_docker": true|false,
    "add_database": true|false
}}

INSTRUCTIONS:
1. Identify the main entities/resources in the description
2. For each resource, determine appropriate fields with types
3. If no specific project name is mentioned, create a descriptive one
4. Default to: FastAPI + React + SQLite + Tests + Docker unless specified otherwise
5. Be smart about inferring field types (email → str, age → int, price → float, etc.)
6. Include common fields like 'id', 'created_at' automatically
7. Return ONLY the JSON object, no other text

EXAMPLE:
User: "I want to build a blog platform where users can create, edit and delete posts. Each post should have a title, content, author, and publication date."

Output:
{{
    "project_name": "blog-platform",
    "description": "A blog platform for creating and managing posts",
    "resources": [
        {{
            "name": "Post",
            "fields": [
                {{"name": "id", "type": "int"}},
                {{"name": "title", "type": "str"}},
                {{"name": "content", "type": "str"}},
                {{"name": "author", "type": "str"}},
                {{"name": "published_at", "type": "date"}},
                {{"name": "created_at", "type": "date"}}
            ]
        }}
    ],
    "features": [
        "Create new posts",
        "Edit existing posts",
        "Delete posts",
        "View all posts",
        "View single post details"
    ],
    "tech_preferences": {{
        "backend": "fastapi",
        "frontend": "react",
        "database": "sqlite"
    }},
    "include_tests": true,
    "include_docker": true,
    "add_database": true
}}

Now analyze the user's description above.
"""

        try:
            # Run analysis task
            result = self.run_task(analysis_task)

            # Parse JSON result
            # The LLM might return markdown code blocks, so clean it
            result_clean = result.strip()
            if result_clean.startswith("```"):
                # Remove markdown code blocks
                lines = result_clean.split("\n")
                result_clean = "\n".join(lines[1:-1]) if len(lines) > 2 else result_clean
                if result_clean.startswith("json"):
                    result_clean = result_clean[4:].strip()

            specification = json.loads(result_clean)

            # Validate and set defaults
            specification = self._validate_specification(specification)

            log.info(f"✅ Project analysis complete: {specification['project_name']}")
            log.info(f"   Resources: {[r['name'] for r in specification['resources']]}")
            log.info(f"   Features: {len(specification['features'])} identified")

            return specification

        except json.JSONDecodeError as e:
            log.error(f"Failed to parse LLM response as JSON: {str(e)}")
            log.error(f"Raw response: {result}")
            # Return a basic fallback structure
            return self._create_fallback_specification(description)
        except Exception as e:
            log.error(f"Analysis failed: {str(e)}")
            return self._create_fallback_specification(description)

    def _validate_specification(self, spec: Dict) -> Dict:
        """
        Validate and fill in missing specification fields.

        Args:
            spec: Specification dictionary from LLM

        Returns:
            Validated and complete specification
        """
        # Set defaults for missing fields
        defaults = {
            "project_name": "my-fullstack-app",
            "description": "A full-stack web application",
            "resources": [],
            "features": [],
            "tech_preferences": {
                "backend": "fastapi",
                "frontend": "react",
                "database": "sqlite"
            },
            "include_tests": True,
            "include_docker": True,
            "add_database": False
        }

        # Merge with defaults
        for key, default_value in defaults.items():
            if key not in spec or spec[key] is None:
                spec[key] = default_value

        # Ensure resources have proper structure
        for resource in spec.get("resources", []):
            if "fields" not in resource:
                resource["fields"] = [
                    {"name": "id", "type": "int"},
                    {"name": "created_at", "type": "date"}
                ]

            # Ensure all fields have name and type
            for field in resource["fields"]:
                if "name" not in field:
                    field["name"] = "unknown"
                if "type" not in field:
                    field["type"] = "str"

        return spec

    def _create_fallback_specification(self, description: str) -> Dict:
        """
        Create a basic fallback specification when analysis fails.

        Args:
            description: Original user description

        Returns:
            Basic specification
        """
        log.warning("Creating fallback specification due to analysis failure")

        # Try to extract a simple resource name from description
        words = description.lower().split()
        resource_name = "Item"

        # Look for common resource keywords
        resource_keywords = ["user", "post", "product", "article", "task", "item"]
        for keyword in resource_keywords:
            if keyword in words:
                resource_name = keyword.capitalize()
                break

        return {
            "project_name": "my-app",
            "description": description[:100],
            "resources": [{
                "name": resource_name,
                "fields": [
                    {"name": "id", "type": "int"},
                    {"name": "name", "type": "str"},
                    {"name": "description", "type": "str"},
                    {"name": "created_at", "type": "date"}
                ]
            }],
            "features": ["CRUD operations"],
            "tech_preferences": {
                "backend": "fastapi",
                "frontend": "react",
                "database": "sqlite"
            },
            "include_tests": True,
            "include_docker": True,
            "add_database": False
        }

    def refine_specification(
        self,
        specification: Dict,
        user_feedback: str
    ) -> Dict:
        """
        Refine a specification based on user feedback.

        Args:
            specification: Current specification
            user_feedback: User's feedback or requested changes

        Returns:
            Refined specification
        """
        log.info("🔄 Refining specification based on feedback...")

        refinement_task = f"""
Given this current project specification:

{json.dumps(specification, indent=2)}

And this user feedback:
{user_feedback}

Update the specification to incorporate the feedback.
Return the updated JSON object with the same structure.
Only return the JSON, no other text.
"""

        try:
            result = self.run_task(refinement_task)

            # Parse JSON result
            result_clean = result.strip()
            if result_clean.startswith("```"):
                lines = result_clean.split("\n")
                result_clean = "\n".join(lines[1:-1]) if len(lines) > 2 else result_clean
                if result_clean.startswith("json"):
                    result_clean = result_clean[4:].strip()

            refined_spec = json.loads(result_clean)
            refined_spec = self._validate_specification(refined_spec)

            log.info("✅ Specification refined successfully")
            return refined_spec

        except Exception as e:
            log.error(f"Refinement failed: {str(e)}")
            log.warning("Returning original specification")
            return specification
