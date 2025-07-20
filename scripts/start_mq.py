from os import environ
from subprocess import CalledProcessError, check_call


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
