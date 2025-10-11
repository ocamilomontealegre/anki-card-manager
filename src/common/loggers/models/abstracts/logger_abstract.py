from typing import Optional
from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def debug(self, message: str, *, file: str, method: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def info(self, message: str, *, file: str, method: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, *, file: str, method: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, *, file: str, method: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def critical(
        self, message: str, *, file: str, method: Optional[str] = None
    ) -> None:
        pass
