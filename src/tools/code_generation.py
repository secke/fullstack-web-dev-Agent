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
        content: Content to write in the file
        description: Description of what this file contains
    
    Returns:
        Success message or error
    """
    try:
        # Ensure path is relative to outputs directory
        base_dir = settings.OUTPUTS_DIR
        full_path = base_dir / file_path
        
        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        full_path.write_text(content)
        
        log.info(f"Created file: {file_path}")
        if description:
            log.info(f"  Description: {description}")
        
        return f"✓ File created: {file_path}"
        
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


# List of all code generation tools
CODE_GENERATION_TOOLS = [
    create_file_with_content,
    create_directory_structure,
    read_file_content,
    list_generated_files,
    validate_python_syntax,
]
