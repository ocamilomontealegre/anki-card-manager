from pathlib import Path
from datetime import datetime, timezone

from injector import inject
from fastapi import UploadFile

from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils.file_utils import FileUtils
from ..models.saved_file_model import SavedFile


class UploadService:
    @inject
    def __init__(self, logger: Logger):
        self._file = UploadService.__name__

        self.__logger = logger

    async def _write_file_to_disk(self, file_path: Path, file_data: UploadFile) -> Path:
        with open(file_path, "wb") as file:
            file.write(await file_data.read())
        self.__logger.debug(
            f"File {file_path} saved successfully",
            file=self._file,
            method=self._write_file_to_disk.__name__,
        )
        return file_path

    async def save_file(self, file: UploadFile) -> SavedFile:
        if not file.filename:
            raise ValueError("Uploaded file must have a filename")

        if file.content_type != "text/csv":
            raise ValueError(
                f"Content type {file.content_type} currently not supported"
            )

        timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}_{file.filename}"
        file_path = FileUtils.create_folder("uploads") / file_name
        await self._write_file_to_disk(file_path, file)
        self.__logger.debug(
            f"File {file_name} processed successfully",
            file=self._file,
            method=self.save_file.__name__,
        )

        return SavedFile(
            name=file_name,
            file_path=str(file_path),
            size=file.size,
            content_type=file.content_type,
        )
