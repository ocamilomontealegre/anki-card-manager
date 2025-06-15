from pydantic import Field
from pydantic_settings import BaseSettings


class PinterestEnvVariables(BaseSettings):
    url: str = Field(description="Unplash url")
