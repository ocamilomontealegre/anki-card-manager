from abc import ABC, abstractmethod


class DatabaseStrategy(ABC):
    @abstractmethod
    def get_connection_url(self):
        pass

    @abstractmethod
    def create_engine(self):
        pass

    @abstractmethod
    def create_session(self):
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
