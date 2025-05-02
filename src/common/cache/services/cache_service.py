from injector import inject
from common.env.env_config import get_env_variables
from redis.asyncio import Redis


class CacheService:
    @inject
    def __init__(self) -> None:
        self.__env = get_env_variables().redis
        self.__redis = Redis(host=self.__env.host, port=self.__env.port, db=self.__env.db, decode_responses=True)

    async def connect(self) -> None:
        await self.__redis.ping()

    async def disconnect(self) -> None:
        await self.__redis.close()
