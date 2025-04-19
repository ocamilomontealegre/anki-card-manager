from pydantic import Field
from pydantic_settings import BaseSettings


class UnplashEnvVariables(BaseSettings):
    url: str = Field(description="Unplash url")
