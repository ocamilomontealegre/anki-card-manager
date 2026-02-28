from typing import Any

from injector import inject
from redis.asyncio import Redis, RedisError

from common.env.env_config import EnvVariables
from common.loggers.models.abstracts.logger_abstract import Logger

from .cache_strategy import CacheStrategy


class RedisStrategy(CacheStrategy):
    @inject
    def __init__(self, logger: Logger):
        self._logger = logger

        self._env = EnvVariables.get().redis
        self._redis = Redis(
            host=self._env.host,
            port=self._env.port,
            db=self._env.db,
            decode_responses=True,
        )

    async def connect(self):
        await self._redis.ping()
        self._logger.debug(
            "Redis connection up!",
        )

    async def close_connection(self):
        try:
            await self._redis.close()
            self._logger.debug(
                "Redis connection successfully closed",
            )
        except RedisError as e:
            self._logger.error(
                f"Redis connection error when close: {e}",
            )
            raise

    async def read(self, key: str):
        self._logger.debug(f"Reading key[{key}]")
        return await self._redis.get(name=key)

    async def write(self, key: str, value: Any):
        self._logger.debug(f"Writing key[{key}]")
        await self._redis.set(name=key, value=value, ex=120)
