from typing import Any
from abc import ABC, abstractmethod


class CacheStrategy(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass

    @abstractmethod
    def read(self, key: str) -> None:
        pass

    @abstractmethod
    def write(self, key: str, value: Any) -> None:
        pass
