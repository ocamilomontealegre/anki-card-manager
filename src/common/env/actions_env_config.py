from pydantic import Field
from pydantic_settings import BaseSettings


class ActionsEnvVariables(BaseSettings):
    delete: int = Field(description="Delete file after read flag")
