from os import remove
from pathlib import Path
from common.loggers.app_logger import AppLogger

logger = AppLogger(label="FileUtils")


class FileUtils:
    @staticmethod
    def create_folder(directory_name: str) -> Path:

        directory_path = Path(directory_name)

        if not FileUtils.check_folder_existence(directory_path):
            directory_path.mkdir(parents=True)
            logger.debug(f"Directory '{directory_name}' created")

        return directory_path

    @staticmethod
    def check_folder_existence(directory_path: Path) -> bool:
        return directory_path.exists() and directory_path.is_dir()

    @staticmethod
    def remove_file(file_path: Path) -> None:
        try:
            return remove(file_path)
        except FileNotFoundError:
            logger.error("File not found")
        except PermissionError:
            logger.error("You don't have permission to delete this file.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
