from subprocess import CalledProcessError, check_call
from sys import exit


def lint() -> None:
    """Run ruff linter on the src directory"""
    try:
        check_call(["ruff", "check", "src/"])
        check_call(["pyright", "src/"])
    except CalledProcessError:
        print("Linting failed")
        exit(1)
