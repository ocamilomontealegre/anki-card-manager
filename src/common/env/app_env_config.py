from pydantic import Field
from pydantic_settings import BaseSettings


class AppEnvVariables(BaseSettings):
    host: str = Field(default="localhost", description="App server host")
    port: int = Field(
        ge=0, le=65535, default=8000, description="App server port"
    )
    global_prefix: str = Field(default="api", description="App global prefix")
    version: str = Field(default="v1", description="App version")
