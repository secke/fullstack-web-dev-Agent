"""Code generation tools for agents."""

from smolagents import tool
from src.utils.logger import log
from src.utils.config import settings


@tool
def create_file_with_content(file_path: str, content: str, description: str = "") -> str:
    """
    Creates a new file with the specified content.

    Args:
        file_path: Path where the file should be created (relative to outputs/)
                   Example: "backend/main.py", "frontend/src/App.js"
                   DO NOT use paths like "backend" (that's a directory, not a file)
                   Always include a file extension (.py, .js, .json, .yml, etc.)
        content: Content to write in the file
        description: Description of what this file contains

    Returns:
        Success message or error

    Examples:
        ✓ create_file_with_content("backend/main.py", code, "FastAPI main file")
        ✓ create_file_with_content("frontend/package.json", json_content, "NPM config")
        ✗ create_file_with_content("backend", code, "Backend")  # Wrong! This is a directory
        ✗ create_file_with_content("main.py", code, "Main")  # Missing parent directory!
    """
    try:
        # Ensure path is relative to outputs directory
        base_dir = settings.OUTPUTS_DIR
        full_path = base_dir / file_path

        # Validate that this looks like a file path, not a directory
        if not full_path.suffix:
            warning_msg = f"⚠️  WARNING: '{file_path}' has no file extension. Are you trying to create a directory instead of a file?"
            log.warning(warning_msg)
            return f"✗ Invalid file path '{file_path}': No file extension detected. Use create_directory_structure for directories."

        # Validate path structure - files should be in subdirectories
        if len(full_path.relative_to(base_dir).parts) < 2:
            warning_msg = f"⚠️  WARNING: '{file_path}' is at root level. Files should be in subdirectories like 'backend/', 'frontend/', etc."
            log.warning(warning_msg)
            return f"✗ Invalid file path '{file_path}': Files should be organized in subdirectories (backend/, frontend/, etc.)"

        # Detect common mistakes
        path_lower = file_path.lower()
        if file_path.startswith(("backend/", "frontend/")):
            # Check for backend files in frontend and vice versa
            if file_path.startswith("backend/") and any(ext in path_lower for ext in [".js", ".jsx", ".tsx", ".html", ".css"]):
                log.warning(f"⚠️  Suspicious: JavaScript/frontend file in backend directory: {file_path}")
            elif file_path.startswith("frontend/") and path_lower.endswith(".py"):
                log.warning(f"⚠️  Suspicious: Python file in frontend directory: {file_path}")

        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        full_path.write_text(content)

        log.info(f"✓ Created file: {file_path}")
        if description:
            log.info(f"  Description: {description}")

        return f"✓ File created successfully: {file_path}"

    except Exception as e:
        error_msg = f"Error creating file {file_path}: {str(e)}"
        log.error(error_msg)
        return f"✗ {error_msg}"


@tool
def create_directory_structure(base_path: str, directories: str) -> str:
    """
    Creates a directory structure.
    
    Args:
        base_path: Base path for the structure (relative to outputs/)
        directories: Comma-separated list of directories to create
    
    Returns:
        Success message with created directories
    """
    try:
        base_dir = settings.OUTPUTS_DIR / base_path
        dir_list = [d.strip() for d in directories.split(",")]
        
        created = []
        for dir_name in dir_list:
            dir_path = base_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            created.append(dir_name)
        
        log.info(f"Created directory structure in {base_path}: {', '.join(created)}")
        return f"✓ Created directories: {', '.join(created)}"
        
    except Exception as e:
        error_msg = f"Error creating directories: {str(e)}"
        log.error(error_msg)
        return f"✗ {error_msg}"


@tool
def read_file_content(file_path: str) -> str:
    """
    Reads the content of a file.
    
    Args:
        file_path: Path to the file (relative to outputs/)
    
    Returns:
        File content or error message
    """
    try:
        base_dir = settings.OUTPUTS_DIR
        full_path = base_dir / file_path
        
        if not full_path.exists():
            return f"✗ File not found: {file_path}"
        
        content = full_path.read_text()
        log.info(f"Read file: {file_path} ({len(content)} chars)")
        return content
        
    except Exception as e:
        error_msg = f"Error reading file {file_path}: {str(e)}"
        log.error(error_msg)
        return f"✗ {error_msg}"


@tool
def list_generated_files(base_path: str = ".") -> str:
    """
    Lists all generated files in a directory.
    
    Args:
        base_path: Base path to list (relative to outputs/)
    
    Returns:
        List of files and directories
    """
    try:
        base_dir = settings.OUTPUTS_DIR / base_path

        if not base_dir.exists():
            return f"✗ Directory not found: {base_path}"
        
        files = []
        for item in base_dir.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(base_dir)
                files.append(str(rel_path))
        
        result = f"Files in {base_path}:\n" + "\n".join(f"  - {f}" for f in sorted(files))
        log.info(f"Listed {len(files)} files in {base_path}")
        return result
        
    except Exception as e:
        error_msg = f"Error listing files: {str(e)}"
        log.error(error_msg)
        return f"✗ {error_msg}"


@tool
def validate_python_syntax(code: str) -> str:
    """
    Validates Python code syntax.

    Args:
        code: Python code to validate

    Returns:
        Validation result
    """
    try:
        compile(code, '<string>', 'exec')
        return "✓ Python syntax is valid"
    except SyntaxError as e:
        return f"✗ Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return f"✗ Validation error: {str(e)}"


@tool
def plan_project_structure(project_type: str, component_name: str = "") -> str:
    """
    Returns the recommended directory structure for a project component.
    Use this BEFORE creating files to understand the correct structure.

    Args:
        project_type: Type of project component ("backend-fastapi", "frontend-react", "tests-backend", "tests-frontend", "docker")
        component_name: Optional name of the resource/component

    Returns:
        Recommended directory structure with example file paths

    Examples:
        plan_project_structure("backend-fastapi", "Post")
        plan_project_structure("frontend-react", "User")
        plan_project_structure("docker")
    """
    structures = {
        "backend-fastapi": f"""
📁 Backend FastAPI Structure:

backend/
├── main.py                 ← FastAPI app, routes, models
├── requirements.txt        ← Python dependencies
├── Dockerfile              ← Container definition
├── .dockerignore          ← Docker ignore file
├── models.py              ← Pydantic models (optional)
├── database.py            ← Database config (optional)
└── tests/
    ├── __init__.py
    ├── conftest.py        ← Pytest fixtures
    └── test_main.py       ← API tests

CORRECT file paths to use with create_file_with_content:
  ✓ "backend/main.py"
  ✓ "backend/requirements.txt"
  ✓ "backend/Dockerfile"
  ✓ "backend/tests/__init__.py"
  ✓ "backend/tests/test_main.py"

WRONG paths to avoid:
  ✗ "main.py" (missing backend/ prefix)
  ✗ "backend" (this is a directory, not a file)
""",
        "frontend-react": f"""
📁 Frontend React Structure:

frontend/
├── package.json           ← NPM dependencies
├── Dockerfile             ← Container definition
├── .dockerignore         ← Docker ignore file
├── public/
│   └── index.html        ← HTML template
└── src/
    ├── index.js          ← React entry point
    ├── index.css         ← Global styles
    ├── App.js            ← Main component
    ├── App.css           ← App styles
    └── components/       ← Reusable components
        └── ...

CORRECT file paths to use with create_file_with_content:
  ✓ "frontend/package.json"
  ✓ "frontend/Dockerfile"
  ✓ "frontend/public/index.html"
  ✓ "frontend/src/index.js"
  ✓ "frontend/src/App.js"
  ✓ "frontend/src/App.css"

WRONG paths to avoid:
  ✗ "src/App.js" (missing frontend/ prefix)
  ✗ "frontend/src" (this is a directory, not a file)
""",
        "tests-backend": f"""
📁 Backend Tests Structure:

backend/tests/
├── __init__.py            ← Package marker
├── conftest.py           ← Pytest configuration and fixtures
├── test_main.py          ← Main API tests
├── test_models.py        ← Model tests (if applicable)
└── test_auth.py          ← Auth tests (if applicable)

CORRECT file paths:
  ✓ "backend/tests/__init__.py"
  ✓ "backend/tests/conftest.py"
  ✓ "backend/tests/test_main.py"
""",
        "tests-frontend": f"""
📁 Frontend Tests Structure:

frontend/src/
├── App.test.js           ← App component tests
├── setupTests.js         ← Jest/RTL setup
└── components/
    └── ComponentName.test.js

CORRECT file paths:
  ✓ "frontend/src/App.test.js"
  ✓ "frontend/src/setupTests.js"
  ✓ "frontend/src/components/Button.test.js"
""",
        "docker": f"""
📁 Docker Structure (root level):

docker-compose.yml         ← Service orchestration
README.md                  ← Project documentation
.gitignore                ← Git ignore rules
.env.example              ← Environment variables template (optional)

CORRECT file paths:
  ✓ "docker-compose.yml"
  ✓ "README.md"
  ✓ ".gitignore"

Note: Individual Dockerfiles go in their respective directories:
  ✓ "backend/Dockerfile"
  ✓ "frontend/Dockerfile"
"""
    }

    structure = structures.get(project_type)
    if not structure:
        return f"✗ Unknown project type: {project_type}. Available types: {', '.join(structures.keys())}"

    log.info(f"📋 Planning structure for: {project_type}")
    return structure


@tool
def validate_file_path(file_path: str, expected_type: str = "any") -> str:
    """
    Validates if a file path is correct before creating it.
    Use this to check paths BEFORE calling create_file_with_content.

    Args:
        file_path: The file path to validate (e.g., "backend/main.py")
        expected_type: Expected file type ("python", "javascript", "config", "any")

    Returns:
        Validation result with suggestions if path is incorrect

    Examples:
        validate_file_path("backend/main.py", "python")  → ✓ Valid
        validate_file_path("main.py", "python")  → ✗ Invalid (missing directory)
        validate_file_path("backend", "python")  → ✗ Invalid (no file extension)
    """
    from pathlib import Path

    issues = []
    suggestions = []

    # Check if it has a file extension
    path = Path(file_path)
    if not path.suffix:
        issues.append(f"No file extension detected in '{file_path}'")
        suggestions.append("Add appropriate extension (.py, .js, .json, .yml, etc.)")

    # Check if it's in a subdirectory
    if len(path.parts) < 2:
        issues.append(f"File '{file_path}' is at root level")
        suggestions.append("Files should be in subdirectories: 'backend/', 'frontend/', etc.")

    # Check for correct directory based on file type
    if expected_type == "python" and not file_path.endswith(".py"):
        issues.append(f"Expected Python file but got: {path.suffix}")
        suggestions.append("Python files should end with .py")

    if expected_type == "javascript" and not any(file_path.endswith(ext) for ext in [".js", ".jsx", ".ts", ".tsx"]):
        issues.append(f"Expected JavaScript file but got: {path.suffix}")
        suggestions.append("JavaScript files should end with .js, .jsx, .ts, or .tsx")

    # Check directory/file type consistency
    if file_path.startswith("backend/"):
        if path.suffix in [".js", ".jsx", ".tsx", ".html", ".css"]:
            issues.append(f"Frontend file type ({path.suffix}) in backend directory")
            suggestions.append(f"Move to 'frontend/' directory")
    elif file_path.startswith("frontend/"):
        if path.suffix == ".py":
            issues.append(f"Python file in frontend directory")
            suggestions.append(f"Move to 'backend/' directory")

    # Return result
    if issues:
        result = f"✗ Invalid path: {file_path}\n"
        result += "\nIssues:\n" + "\n".join(f"  • {issue}" for issue in issues)
        result += "\n\nSuggestions:\n" + "\n".join(f"  → {sug}" for sug in suggestions)
        log.warning(f"Path validation failed: {file_path}")
        return result
    else:
        log.info(f"✓ Path validation passed: {file_path}")
        return f"✓ Valid file path: {file_path}"


@tool
def create_multiple_files(files_json: str) -> str:
    """
    Creates multiple files at once with validation.
    Useful for creating a complete project structure in one call.

    Args:
        files_json: JSON string with list of files to create
                    Format: [{"path": "backend/main.py", "content": "...", "description": "..."}]

    Returns:
        Summary of created files and any errors

    Example:
        files = [
            {"path": "backend/main.py", "content": "from fastapi import FastAPI\\napp = FastAPI()", "description": "FastAPI app"},
            {"path": "backend/requirements.txt", "content": "fastapi\\nuvicorn", "description": "Dependencies"}
        ]
        create_multiple_files(json.dumps(files))
    """
    import json

    try:
        files_list = json.loads(files_json)

        if not isinstance(files_list, list):
            return "✗ Error: files_json must be a JSON array"

        results = {
            "created": [],
            "failed": [],
            "warnings": []
        }

        for file_info in files_list:
            if not isinstance(file_info, dict):
                results["failed"].append({"path": "unknown", "error": "Invalid file entry format"})
                continue

            file_path = file_info.get("path")
            content = file_info.get("content", "")
            description = file_info.get("description", "")

            if not file_path:
                results["failed"].append({"path": "unknown", "error": "Missing 'path' field"})
                continue

            # Validate path first
            validation_result = validate_file_path(file_path)
            if validation_result.startswith("✗"):
                results["warnings"].append({"path": file_path, "warning": validation_result})

            # Create file
            create_result = create_file_with_content(file_path, content, description)

            if create_result.startswith("✓"):
                results["created"].append(file_path)
            else:
                results["failed"].append({"path": file_path, "error": create_result})

        # Build summary
        summary = f"📊 File Creation Summary:\n"
        summary += f"  ✓ Created: {len(results['created'])} files\n"
        summary += f"  ✗ Failed: {len(results['failed'])} files\n"
        summary += f"  ⚠️  Warnings: {len(results['warnings'])}\n"

        if results["created"]:
            summary += "\n✓ Successfully created:\n"
            for path in results["created"]:
                summary += f"  • {path}\n"

        if results["failed"]:
            summary += "\n✗ Failed to create:\n"
            for fail in results["failed"]:
                summary += f"  • {fail['path']}: {fail['error']}\n"

        if results["warnings"]:
            summary += "\n⚠️  Warnings:\n"
            for warn in results["warnings"]:
                summary += f"  • {warn['path']}\n"

        log.info(summary)
        return summary

    except json.JSONDecodeError as e:
        error_msg = f"✗ Invalid JSON format: {str(e)}"
        log.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"✗ Error creating multiple files: {str(e)}"
        log.error(error_msg)
        return error_msg


# List of all code generation tools
CODE_GENERATION_TOOLS = [
    create_file_with_content,
    create_directory_structure,
    read_file_content,
    list_generated_files,
    validate_python_syntax,
    plan_project_structure,
    validate_file_path,
    create_multiple_files,
]
