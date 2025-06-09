from pydantic import BaseModel, Field


class HealthMessageDto(BaseModel):
    """
    Data Transfer Object for health check messages.
    """
    message: str = Field(..., description="Health status message")
