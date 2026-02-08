from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)



class AiClientAdapter(ABC):
    @abstractmethod
    def get_structured_response(
        self, *, messages: list[dict[str, str]], response_interface: type[T]
    ) -> T:
        pass
