from typing import Union
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LoggerData:
    message: str
    file: str
    method: Union[str, None] = None


class Logger(ABC):
    @abstractmethod
    def debug(self, data: LoggerData) -> None:
        pass
