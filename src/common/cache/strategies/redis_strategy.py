from typing import Any
from redis.asyncio import Redis, RedisError
from common.env.env_config import EnvVariables
from common.loggers.app_logger import AppLogger
from .cache_strategy import CacheStrategy


class RedisStrategy(CacheStrategy):
    def __init__(self):
        self._file = RedisStrategy.__name__

        self._logger = AppLogger(label=RedisStrategy.__name__)

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
            file=self._file,
            method=self.connect.__name__,
        )

    async def close_connection(self):
        method = self.close_connection.__name__

        try:
            await self._redis.close()
            self._logger.debug(
                "Redis connection successfully closed",
                file=self._file,
                method=method,
            )
        except RedisError as e:
            self._logger.error(
                f"Redis connection error when close: {e}",
                file=self._file,
                method=method,
            )
            raise

    async def read(self, key: str):
        self._logger.debug(
            f"Reading key[{key}]", file=self._file, method=self.read.__name__
        )
        return await self._redis.get(name=key)

    async def write(self, key: str, value: Any):
        self._logger.debug(
            f"Writing key[{key}]", file=self._file, method=self.read.__name__
        )
        await self._redis.set(name=key, value=value, ex=120)
