from pydantic import BaseModel, Field


class OpenAIEnvVariables(BaseModel):
    key: str = Field(description="Open AI API key")
    model: str = Field(description="LLM model")
