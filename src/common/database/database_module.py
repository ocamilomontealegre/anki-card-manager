from injector import Module, Binder, singleton
from .strategies.database_strategy import DatabaseStrategy
from .strategies.pg_strategy import PgStrategy


class DatabaseModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(DatabaseStrategy, to=PgStrategy, scope=singleton)
