from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from ..entities.base_entity import Base
from .database_strategy import DatabaseStrategy
from common.env.env_config import get_env_variables


class PgStrategy(DatabaseStrategy):
    def __init__(self):
        self.__env_variables = get_env_variables().pg
        self.__engine = self.create_engine()

    def get_connection_url(self):
        host = self.__env_variables.host
        port = self.__env_variables.port
        username = self.__env_variables.username
        password = self.__env_variables.password
        database = self.__env_variables.database
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"

    def create_engine(self):
        return create_engine(self.get_connection_url())

    def create_session(self):
        engine = self.create_engine()
        session = sessionmaker(bind=engine)
        return session()

    def create_tables(self):
        Base.metadata.create_all(self.__engine)

    def disconnect(self):
        if isinstance(self.__engine, Engine):
            self.__engine.dispose()
