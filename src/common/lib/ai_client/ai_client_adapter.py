from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class AiClientAdapter(ABC):
    @abstractmethod
    def get_structured_response(self, *, prompt: str, response_interface: type[T]) -> T:
        pass
