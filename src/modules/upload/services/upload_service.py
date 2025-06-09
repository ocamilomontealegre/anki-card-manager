from pathlib import Path
from injector import inject
from fastapi import UploadFile
from common.loggers.logger import AppLogger
from common.utils.file_utils import FileUtils
from ..models.saved_file_model import SavedFile


class UploadService:
    @inject
    def __init__(self):
        self.__logger = AppLogger(label=UploadService.__name__)

    async def _write_file_to_disk(
        self, file_path: Path, file_data: UploadFile
    ) -> Path:
        with open(file_path, "wb") as file:
            file.write(await file_data.read())
        self.__logger.debug(
            f"File {file_path} saved successfully",
            self._write_file_to_disk.__name__,
        )
        return file_path

    async def save_file(self, file: UploadFile) -> SavedFile:
        if not file.filename:
            raise ValueError("Uploaded file must have a filename")

        if file.content_type != "text/csv":
            raise ValueError(
                f"Content type {file.content_type} currently not supported"
            )

        file_path = FileUtils.create_folder("uploads") / str(file.filename)
        file_name = await self._write_file_to_disk(file_path, file)
        self.__logger.debug(
            f"File {file_name} processed successfully",
            self.save_file.__name__,
        )

        return SavedFile(
            name=file.filename,
            file_path=str(file_path),
            size=file.size,
            content_type=file.content_type,
        )
