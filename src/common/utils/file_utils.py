from os import remove
from pathlib import Path
from src.common.loggers.app_logger import AppLogger

logger = AppLogger()

file = "FileUtils"


class FileUtils:
    @staticmethod
    def create_folder(directory_name: str) -> Path:

        directory_path = Path(directory_name)

        if not FileUtils.check_folder_existence(directory_path):
            directory_path.mkdir(parents=True)
            logger.debug(
                f"Directory '{directory_name}' created",
                file=file,
                method=FileUtils.create_folder.__name__,
            )

        return directory_path

    @staticmethod
    def check_folder_existence(directory_path: Path) -> bool:
        return directory_path.exists() and directory_path.is_dir()

    @staticmethod
    def remove_file(file_path: Path) -> None:
        method = FileUtils.remove_file.__name__

        try:
            return remove(file_path)
        except FileNotFoundError:
            logger.error("File not found", file=file, method=method)
        except PermissionError:
            logger.error(
                "You don't have permission to delete this file.",
                file=file,
                method=method,
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}", file=file, method=method)
