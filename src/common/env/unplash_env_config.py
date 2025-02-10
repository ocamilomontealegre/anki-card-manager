from pydantic import Field
from pydantic_settings import BaseSettings


class UnplashEnvVariables(BaseSettings):
    key: str = Field(description="Unplash API key")
