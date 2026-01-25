import sys
from os import path

from alembic.config import Config

from alembic import command


def migrate(message: str) -> None:
    """Create a new migration and apply it using Alembic"""
    try:
        base_dir = path.dirname(__file__)
        project_root = path.dirname(base_dir)
        src_dir = path.join(project_root, "src")

        sys.path.insert(0, src_dir)

        alembic_ini = path.join(project_root, "alembic.ini")
        alembic_cfg = Config(alembic_ini)

        alembic_cfg.set_main_option("script_location", "alembic")

        command.revision(alembic_cfg, message=message, autogenerate=True)
        print("Migration revision executed")

        command.upgrade(alembic_cfg, "head")
        print("Migration applied")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
