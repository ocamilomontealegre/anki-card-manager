from celery import Celery
from common.env.env_config import EnvVariables


class CeleryMq:
    def __init__(self):
        self._env = EnvVariables.get().redis
        self._broker = (
            f"redis://{self._env.host}:{self._env.port}/{self._env.mq}"
        )
        self._backend = (
            f"redis://{self._env.host}:{self._env.port}/{self._env.mq}"
        )

        self._app = Celery(
            main="app", broker=self._broker, backend=self._backend
        )

        self._config()

    def _config(self):
        self._app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
            task_acks_late=True,
        )
        self._app.autodiscover_tasks(
            [
                "modules.language.tasks.language_task",
                "modules.anki.tasks.anki_task",
            ]
        )

    def get_app(self) -> Celery:
        return self._app


celery_app = CeleryMq().get_app()
