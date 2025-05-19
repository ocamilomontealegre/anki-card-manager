from abc import ABC, abstractmethod
from sqlalchemy import Engine
from sqlalchemy.orm import Session


class DatabaseStrategy(ABC):
    @abstractmethod
    def get_connection_url(self) -> str:
        pass

    @abstractmethod
    def create_engine(self) -> Engine:
        pass

    @abstractmethod
    def create_session(self) -> Session:
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
