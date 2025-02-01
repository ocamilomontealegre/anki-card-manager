from pydantic import Field
from pydantic_settings import BaseSettings


class GiphyEnvVariables(BaseSettings):
    key: str = Field(description="Giphy API key")
