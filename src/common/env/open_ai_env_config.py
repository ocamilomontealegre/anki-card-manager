from pydantic import Field
from pydantic_settings import BaseSettings


class OpenAIEnvVariables(BaseSettings):
    key: str = Field(default="ok", description="Open AI API key")
    model: str = Field(default="ok", description="LLM model")
