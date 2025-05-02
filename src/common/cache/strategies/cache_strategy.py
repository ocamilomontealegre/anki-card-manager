from abc import ABC, abstractmethod


class CacheStrategy(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass

    @abstractmethod
    def read(self) -> None:
        pass

    @abstractmethod
    def write(self) -> None:
        pass
