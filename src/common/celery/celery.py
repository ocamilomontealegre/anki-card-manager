from celery import Celery
from ..env.env_config import get_env_variables


class CeleryApp:
    def __init__(self) -> None:
        self.__env = get_env_variables().redis
        self.__broker = f"redis://{self.__env.host}:{self.__env.port}/{self.__env.mq}"
        self.__backend = f"redis://{self.__env.host}:{self.__env.port}/{self.__env.mq}"

        self.__app = Celery(
            main="app",
            broker=self.__broker,
            backend=self.__backend
        )

    def __configure(self) -> None:
        self.__app.conf.update(
            
        )

    def get_app(self) -> Celery:
        return self.__app
