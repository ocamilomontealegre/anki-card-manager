from subprocess import CalledProcessError, check_call

from .base_script import Script


class TestScript(Script):
    def execute(self):
        try:
            args: list[str] = ["poetry", "run", "pytest", "test"]
            check_call(args)
        except CalledProcessError as e:
            print(f"Test execution failed: {e}")
            exit(1)
        except Exception as e:
            print(f"Unknown error: {e}")
            exit(1)


test_script = TestScript()
