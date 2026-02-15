from datetime import datetime, timezone

from pydantic import BaseModel, Field

from src.common.types import DataType


class HTTPResponse(BaseModel):
    status: int = Field(default=200)
    success: bool = Field(default=True)
    message: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )
    )
    data: DataType | None = Field(default=None)
