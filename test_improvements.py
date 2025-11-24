"""Test script to demonstrate the improved agent capabilities."""

from src.tools.code_generation import (
    plan_project_structure,
    validate_file_path,
    create_file_with_content
)
from src.utils.logger import log

def test_planning_tool():
    """Test the new planning tool."""
    log.info("\n" + "="*60)
    log.info("TEST 1: Plan Project Structure Tool")
    log.info("="*60)

    # Test backend structure
    result = plan_project_structure("backend-fastapi", "Post")
    print("\n" + result)

    # Test frontend structure
    result = plan_project_structure("frontend-react", "Post")
    print("\n" + result)

    log.info("✅ Planning tool test complete\n")


def test_path_validation():
    """Test the path validation tool."""
    log.info("\n" + "="*60)
    log.info("TEST 2: Path Validation Tool")
    log.info("="*60)

    # Test valid paths
    test_paths = [
        ("backend/main.py", "python", "Should be VALID"),
        ("frontend/src/App.js", "javascript", "Should be VALID"),
        ("main.py", "python", "Should be INVALID - missing directory"),
        ("backend", "python", "Should be INVALID - no file extension"),
        ("backend/app.js", "python", "Should be INVALID - wrong file type"),
    ]

    for path, file_type, expectation in test_paths:
        print(f"\nTesting: {path} (type: {file_type})")
        print(f"Expected: {expectation}")
        result = validate_file_path(path, file_type)
        print(result)
        print("-" * 50)

    log.info("✅ Path validation test complete\n")


def test_file_creation_with_validation():
    """Test file creation with improved validation."""
    log.info("\n" + "="*60)
    log.info("TEST 3: File Creation with Validation")
    log.info("="*60)

    # Test creating valid files
    test_files = [
        {
            "path": "backend/main.py",
            "content": "from fastapi import FastAPI\napp = FastAPI()",
            "description": "FastAPI main file",
            "should_succeed": True
        },
        {
            "path": "main.py",
            "content": "print('hello')",
            "description": "Invalid - root level file",
            "should_succeed": False
        },
        {
            "path": "backend",
            "content": "test",
            "description": "Invalid - directory instead of file",
            "should_succeed": False
        }
    ]

    for test_file in test_files:
        print(f"\nAttempting to create: {test_file['path']}")
        print(f"Expected: {'SUCCESS' if test_file['should_succeed'] else 'FAILURE'}")
        result = create_file_with_content(
            test_file["path"],
            test_file["content"],
            test_file["description"]
        )
        print(f"Result: {result}")
        print("-" * 50)

    log.info("✅ File creation test complete\n")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  TESTING IMPROVED AGENT CAPABILITIES")
    print("="*70)

    try:
        # Test 1: Planning tool
        test_planning_tool()

        # Test 2: Path validation
        test_path_validation()

        # Test 3: File creation with validation
        test_file_creation_with_validation()

        print("\n" + "="*70)
        print("  ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)

    except Exception as e:
        log.error(f"Test failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
