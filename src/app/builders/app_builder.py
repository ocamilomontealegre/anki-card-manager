from contextlib import asynccontextmanager
from typing import TypedDict

from fastapi import FastAPI, HTTPException
from injector import Injector

from app.app_module import AppModule
from app.routers.app_router import AppRouter
from common.cache.strategies.cache_strategy import CacheStrategy
from common.database.strategies.database_strategy import DatabaseStrategy
from common.env.env_config import EnvVariables
from common.exception_handlers import (
    GeneralExceptionHandler,
    HTTPExceptionHandler,
)
from common.interceptors import HTTPInterceptor
from common.loggers.app_logger import AppLogger

file = "AppBuilder"


class LifespanDependencies(TypedDict):
    db: DatabaseStrategy
    cache: CacheStrategy


def create_lifespan(deps: LifespanDependencies):
    logger = AppLogger()

    db = deps["db"]
    cache = deps["cache"]

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        method = lifespan.__name__

        try:
            db.create_session()
            db.create_tables()
            logger.info(
                "Database connected successfully",
                file=file,
                method=method,
            )

            await cache.connect()
        except Exception as e:
            logger.error(
                f"Database connection failed: {e}",
                file=file,
                method=method,
            )
            raise
        yield
        try:
            db.disconnect()
            logger.info("Database connection closed", file=file, method=method)
        except Exception as e:
            logger.error(
                f"Error during database disconnection: {e}",
                file=file,
                method=method,
            )

        await cache.close_connection()

    return lifespan


class AppBuilder:
    def __init__(self):
        self.__injector = Injector([AppModule])
        self.__env = EnvVariables.get()
        self.__db = self.__injector.get(DatabaseStrategy)
        self.__cache = self.__injector.get(CacheStrategy)
        self.__lifespan = create_lifespan({"db": self.__db, "cache": self.__cache})

        self.__app = FastAPI(lifespan=self.__lifespan)
        self.__router = AppRouter(self.__injector).get_router()

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
            HTTPException,
            HTTPExceptionHandler.handle_exception,  # type: ignore
        )
        return self

    def set_router(self) -> "AppBuilder":
        env_variables = self.__env.app

        self.__app.include_router(
            self.__router,
            prefix=f"/{env_variables.global_prefix}/{env_variables.version}",
        )
        return self

    def build(self) -> FastAPI:
        return self.__app
