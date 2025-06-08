from typing import Literal
from pydantic import BaseModel


class DeleteMany(BaseModel):
    deleted: Literal["OK"]
    total: int
