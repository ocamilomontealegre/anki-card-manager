from pydantic import Field
from pydantic_settings import BaseSettings


class ElevenLabsEnvVariables(BaseSettings):
    key: str = Field(description="Eleven labs API key")
