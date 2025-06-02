from typing import Any
from celery import Celery
from common.env.env_config import get_env_variables
from .mq_strategy import MqStrategy


class CeleryStrategy(MqStrategy):
    def __init__(self):
        self._env = get_env_variables().redis
        self._broker = (
            f"redis://{self._env.host}:{self._env.port}/{self._env.mq}"
        )
        self._backend = (
            f"redis://{self._env.host}:{self._env.port}/{self._env.mq}"
        )

        self._app = Celery(
            main="app", broker=self._broker, backend=self._backend
        )

        self._app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
            task_acks_late=True,
        )

    def get_app(self) -> Any:
        return self._app

    def send_task(self, name: str, *args: Any, **kwargs: Any) -> Any:
        return self._app.send_task(name, args=args, kwargs=kwargs)

    def close_connection(self) -> None:
        return self._app.close()
