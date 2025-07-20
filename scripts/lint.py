from subprocess import check_call


def lint() -> None:
    """Run flake8 linter on the src directory"""
    try:
        check_call(["flake8", "src/"])
    except Exception as e:
        print(f"Linting failed: {e}")