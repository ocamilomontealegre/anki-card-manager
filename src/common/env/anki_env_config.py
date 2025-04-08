from pydantic import Field
from pydantic_settings import BaseSettings


class AnkiEnvVariables(BaseSettings):
    audios: str = Field(description="Path for storing the audios")
    output: str = Field(description="Path for storing csv output files")
