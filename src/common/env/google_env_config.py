from pydantic import Field
from pydantic_settings import BaseSettings


class GoogleEnvVariables(BaseSettings):
    credentials: str = Field(description="Path to .json google credentials")
