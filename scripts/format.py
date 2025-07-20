from subprocess import CalledProcessError, check_call


def format() -> None:
    """Format using black"""
    try:
        check_call(["black", "src/"])
    except CalledProcessError as e:
        error_message = e.output.decode().strip() if e.output else "No output provided."
        print(f"Formatting failed with error code {e.returncode}: {error_message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
