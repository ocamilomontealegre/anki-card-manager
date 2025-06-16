from pydantic import Field
from pydantic_settings import BaseSettings


class DebuggyEnvVariables(BaseSettings):
    active: int = Field(description="Debuggy flag")
