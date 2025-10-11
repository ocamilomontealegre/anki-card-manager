from injector import inject
from sqlalchemy import create_engine, Engine, exc
from sqlalchemy.orm import sessionmaker, Session

from common.loggers.models.abstracts.logger_abstract import Logger
from common.env.env_config import EnvVariables
from ..entities.base_entity import Base
from .database_strategy import DatabaseStrategy


class PgStrategy(DatabaseStrategy):
    @inject
    def __init__(self, logger: Logger):
        self._file = PgStrategy.__name__

        self._logger = logger

        self._env = EnvVariables.get().pg
        self._engine = self.create_engine()

    def get_connection_url(self) -> str:
        host = self._env.host
        port = self._env.port
        username = self._env.username
        password = self._env.password
        database = self._env.database
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"

    def create_engine(self) -> Engine:
        method = self.create_engine.__name__

        try:
            return create_engine(self.get_connection_url())
        except exc.DatabaseError as e:
            self._logger.error(
                f"Database engine error: {e}",
                file=self._file,
                method=method,
            )
            raise
        except Exception as e:
            self._logger.error(f"Unknown error: {e}", file=self._file, method=method)
            raise RuntimeError(
                "Failed to create a database engine due to an unknown error."
            )

    def create_session(self) -> Session:
        method = self.create_session.__name__

        try:
            engine = self.create_engine()
            session = sessionmaker(bind=engine)
            return session()
        except exc.DatabaseError as e:
            self._logger.error(
                f"Error creating db session: {e}",
                file=self._file,
                method=method,
            )
            raise
        except Exception as e:
            self._logger.error(f"Unknown error: {e}", file=self._file, method=method)
            raise RuntimeError(
                "Failed to create a database session due to an unknown error."
            )

    def create_tables(self):
        Base.metadata.create_all(self._engine)

    def disconnect(self) -> None:
        method = self.disconnect.__name__

        try:
            if isinstance(self._engine, Engine):
                self._engine.dispose()
                self._logger.debug(
                    "Database connection successfully closed",
                    file=self._file,
                    method=method,
                )
        except exc.DatabaseError as e:
            self._logger.error(
                f"Error closing db connection: {e}",
                file=self._file,
                method=method,
            )
            raise
        except Exception as e:
            self._logger.error(f"Unknown error: {e}", file=self._file, method=method)
