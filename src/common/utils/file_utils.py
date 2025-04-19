from pathlib import Path
from common.loggers.logger import AppLogger


class FileUtils:
    @staticmethod
    def create_folder(directory_name: str) -> Path:
        logger = AppLogger()

        directory_path = Path(directory_name)

        if not FileUtils.check_folder_existence(directory_path):
            directory_path.mkdir(parents=True)
            logger.info(f"Directory '{directory_name}' created")

        return directory_path

    @staticmethod
    def check_folder_existence(directory_path: Path) -> bool:
        return directory_path.exists() and directory_path.is_dir()
