from sys import executable
from subprocess import CalledProcessError, check_call


def start() -> None:
    """Start uvicorn server."""
    try:
        python_path = executable
        print(python_path)
        check_call([python_path, "src/main.py"])
    except KeyboardInterrupt:
        print("\nServer stopped manually.")
        exit(0)
    except CalledProcessError as e:
        print(f"Server start failed: {e}")
        exit(1)


def lint() -> None:
    """Run flake8 linter on the src directory"""
    try:
        check_call(["flake8", "src/"])
    except Exception as e:
        print(f"Linting failed: {e}")


def format() -> None:
    """Format using black"""
    try:
        check_call(["black", "src/"])
    except CalledProcessError as e:
        error_message = e.output.decode().strip() if e.output else "No output provided."
        print(f"Formatting failed with error code {e.returncode}: {error_message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
