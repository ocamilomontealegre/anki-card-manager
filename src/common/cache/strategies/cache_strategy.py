from typing import Any, Awaitable
from abc import ABC, abstractmethod


class CacheStrategy(ABC):
    @abstractmethod
    def connect(self) -> Awaitable:
        pass

    @abstractmethod
    def close_connection(self) -> Awaitable:
        pass

    @abstractmethod
    async def read(self, key: str) -> None:
        pass

    @abstractmethod
    async def write(self, key: str, value: Any) -> None:
        pass
