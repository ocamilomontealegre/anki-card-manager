from pydantic import BaseModel, Field


class OpenAIEnvVariables(BaseModel):
    key: str = Field(default="ok", description="Open AI API key")
    model: str = Field(default="ok", description="LLM model")
