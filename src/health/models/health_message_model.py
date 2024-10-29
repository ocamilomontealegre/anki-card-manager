from pydantic import BaseModel


class HealthMessage(BaseModel):
    message: str
