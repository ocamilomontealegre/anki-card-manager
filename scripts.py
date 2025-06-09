from os import path, environ
from sys import executable
from subprocess import CalledProcessError, check_call
from alembic import command
from alembic.config import Config


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


def start_mq() -> None:
    """Start Celery worker."""
    try:
        env = environ.copy()
        env["PYTHONPATH"] = "src"
        check_call(
            [
                "poetry",
                "run",
                "celery",
                "-A",
                "common.mq.celery",
                "worker",
                "--loglevel=info",
                "--pool=solo",
            ],
            env=env,
        )
    except KeyboardInterrupt:
        print("\nCelery worker stopped manually.")
        exit(0)
    except CalledProcessError as e:
        print(f"Celery worker start failed: {e}")
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


def migrate(message: str) -> None:
    """Make migration with alembic"""
    try:
        alembic_init_path = path.join(path.dirname(__file__), "alembic.ini")
        alembic_cfg = Config(alembic_init_path)

        command.revision(alembic_cfg, message=message, autogenerate=True)
        print("Migration revision executed")
        command.upgrade(alembic_cfg, "head")
        print("Migration applied")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
