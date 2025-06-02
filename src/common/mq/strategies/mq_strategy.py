from typing import Any
from abc import ABC, abstractmethod


class MqStrategy(ABC):
    @abstractmethod
    def get_app(self) -> Any:
        """Return the underlying message queue application/client instance"""
        pass

    @abstractmethod
    def send_task(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Send a task to a queue message"""
        pass

    @abstractmethod
    def close_connection(self) -> None:
        """Close the connection"""
        pass
