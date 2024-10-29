from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from common.types import DataType


class HTTPResponse(BaseModel):
    status: int = Field(default=200)
    success: bool = Field(default=True)
    message: str
    data: Optional[DataType] = Field(default=None)
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )
    )
