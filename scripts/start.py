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
