from pydantic import Field
from pydantic_settings import BaseSettings


class AnkiEnvVariables(BaseSettings):
    media: str = Field(
        description="Path for storing the media like images an audio"
    )
    output: str = Field(description="Path for storing csv output files")
    connect: str = Field(description="AnkiConnect uri")
