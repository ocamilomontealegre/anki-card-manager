from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Engine, exc
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from ..entities.base_entity import Base
from .database_strategy import DatabaseStrategy


class PgStrategy(DatabaseStrategy):
    def __init__(self):
        self.__logger = AppLogger(label=PgStrategy.__name__)

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
        try:
            return create_engine(self.get_connection_url())
        except exc.DatabaseError as e:
            self.__logger.error(f"Database engine error: {e}")
            raise
        except Exception as e:
            self.__logger.error(f"Unknown error: {e}")

    def create_session(self):
        try:
            engine = self.create_engine()
            session = sessionmaker(bind=engine)
            return session()
        except exc.DatabaseError as e:
            self.__logger.error(f"Error creating db session: {e}")
            raise
        except Exception as e:
            self.__logger.error(f"Unknown error: {e}")

    def create_tables(self):
        Base.metadata.create_all(self.__engine)

    def disconnect(self):
        try:
            if isinstance(self.__engine, Engine):
                self.__engine.dispose()
                self.__logger.debug("Database connection successfully closed")
        except exc.DatabaseError as e:
            self.__logger.error(f"Error closing db connection: {e}")
            raise
        except Exception as e:
            self.__logger.error(f"Unknown error: {e}")
