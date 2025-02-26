from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database_strategy import DatabaseStrategy
from common.env.env_config import get_env_variables


class PgStrategy(DatabaseStrategy):
    def __init__(self):
        self.__env_variables: get_env_variables().pg

        self.host = self.__env_variables.host
        self.port = self.__env_variables.port
        self.username = self.__env_variables.username
        self.password = self.__env_variables.password
        self.database = self.__env_variables.database

    def get_connection_url(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def create_engine(self):
        return create_engine(self.get_connection_url())

    def create_session(self):
        engine = self.create_engine()
        Session = sessionmaker(bind=engine)
        return Session()