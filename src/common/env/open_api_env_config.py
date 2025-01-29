from pydantic import Field
from pydantic_settings import BaseSettings


class OpenAPIEnvVariables(BaseSettings):
    title: str = Field(
        default="My Awesome API", description="Title for the app documentation"
    )
    description: str = Field(
        default="This is a mock description",
        description="Description for the app documentation",
    )
    version: str = Field(
        default="1.0.0", description="Version of the app documentation"
    )
