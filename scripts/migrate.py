
from os import path
from alembic import command
from alembic.config import Config


def migrate(message: str) -> None:
    """Make migration with alembic"""
    try:
        alembic_init_path = path.join(path.dirname(__file__), "alembic.ini")
        alembic_cfg = Config(alembic_init_path)

        command.revision(alembic_cfg, message=message, autogenerate=True)
        print("Migration revision executed")
        command.upgrade(alembic_cfg, "head")
        print("Migration applied")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
