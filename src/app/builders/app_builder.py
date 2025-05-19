from contextlib import asynccontextmanager

from injector import Injector
from fastapi import FastAPI, HTTPException

from app.app_module import AppModule
from app.routers.app_router import AppRouter
from common.database.strategies.database_strategy import DatabaseStrategy
from common.cache.strategies.cache_strategy import CacheStrategy
from common.interceptors import HTTPInterceptor
from common.loggers.logger import AppLogger
from common.exception_handlers import (
    GeneralExceptionHandler,
    HTTPExceptionHandler,
)
from common.env import get_env_variables


def create_lifespan(db: DatabaseStrategy, cache: CacheStrategy):
    logger = AppLogger()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            db.create_session()
            logger.info("Database connected successfully")

            await cache.connect()
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
        yield
        try:
            db.disconnect()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error during database disconnection: {e}")

        await cache.close_connection()

    return lifespan


class AppBuilder:

    def __init__(self):
        self.__injector = Injector([AppModule])
        self.__env = get_env_variables()
        self.__db = self.__injector.get(DatabaseStrategy)
        self.__cache = self.__injector.get(CacheStrategy)
        self.__lifespan = create_lifespan(db=self.__db, cache=self.__cache)

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

    def build(self) -> FastAPI:
        return self.__app
