from pydantic import Field
from pydantic_settings import BaseSettings


class RedisEnvVariables(BaseSettings):
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(ge=0, default=6379, description="Redis port")
    db: int = Field(ge=0, default=0, description="Redis database database")
    mq: int = Field(ge=0, default=1, description="Redis message queue database")
