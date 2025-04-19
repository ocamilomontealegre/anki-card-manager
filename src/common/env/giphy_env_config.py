from pydantic import Field
from pydantic_settings import BaseSettings


class GiphyEnvVariables(BaseSettings):
    url: str = Field(description="Giphy URL")
