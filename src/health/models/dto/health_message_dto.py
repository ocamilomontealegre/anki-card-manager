from pydantic import BaseModel


class HealthMessageDto(BaseModel):
    message: str
