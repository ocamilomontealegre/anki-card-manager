from typing import Any
from redis.asyncio import Redis, RedisError
from common.env.env_config import get_env_variables
from common.loggers.logger import AppLogger
from cache_strategy import CacheStrategy


class RedisStrategy(CacheStrategy):
    def __init__(self):
        self.__logger = AppLogger(label=RedisStrategy.__name__)

        self.__env = get_env_variables().redis
        self.__redis = Redis(host=self.__env.host, port=self.__env.port, db=self.__env.db, decode_responses=True)

    async def connect(self):
        await self.__redis.ping()
        self.__logger.debug("Redis connection up!")

    async def close_connection(self):
        try:
            await self.__redis.close()
            self.__logger.debug("Redis connection successfully closed")
        except RedisError as e:
            self.__logger.error(f"Redis connection error when close: {e}")
            raise

    async def read(self, key: str):
        return await self.__redis.get(name=key)

    async def write(self, key: str, value: Any):
        await self.__redis.set(name=key, value=value)
