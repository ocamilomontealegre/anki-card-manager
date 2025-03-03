from fastapi import FastAPI, HTTPException
from injector import Injector
from app.app_module import AppModule
from app.routers.app_router import AppRouter
from common.interceptors import HTTPInterceptor
from common.database.strategies.database_strategy import DatabaseStrategy
from common.exception_handlers import (
    GeneralExceptionHandler,
    HTTPExceptionHandler,
)
from common.env import get_env_variables


class AppBuilder:
    def __init__(self):
        self.__app = FastAPI()
        self.__injector = Injector([AppModule])
        self.__router = AppRouter(self.__injector).get_router()
        self.__env = get_env_variables()

    def set_open_api(self) -> "AppBuilder":
        env_variables = self.__env.openapi

        self.__app.title = env_variables.title
        self.__app.description = env_variables.description
        self.__app.version = env_variables.version
        return self

    def set_http_logging_middleware(self) -> "AppBuilder":
        self.__app.add_middleware(HTTPInterceptor)
        return self

    def set_exception_handlers(self) -> "AppBuilder":
        self.__app.add_exception_handler(
            Exception, GeneralExceptionHandler.handle_exception
        )
        self.__app.add_exception_handler(
            HTTPException, HTTPExceptionHandler.handle_exception
        )
        return self

    def set_router(self) -> "AppBuilder":
        env_variables = self.__env.app

        self.__app.include_router(
            self.__router,
            prefix=f"/{env_variables.global_prefix}/{env_variables.version}",
        )
        return self

    def set_database(self) -> "AppBuilder":
        db = self.__injector.get(DatabaseStrategy)
        db.create_session()
        db.create_tables()

        return self

    def build(self):
        return self.__app
