from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ListPaginated(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
