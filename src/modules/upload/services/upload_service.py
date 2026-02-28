from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile
from injector import inject

from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils.file_utils import FileUtils

from ..models.saved_file_model import SavedFile


class UploadService:
    @inject
    def __init__(self, logger: Logger):
        self.__logger = logger

    def _build_file_name(self, base_filename: str):
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{base_filename}"

    async def _write_file_to_disk(
        self,
        file: UploadFile,
        destination: Path,
    ) -> Path:
        with open(destination, "wb") as buffer:
            buffer.write(await file.read())
        self.__logger.debug(
            f"File {destination} saved successfully",
        )
        return destination

    async def save_file(self, file: UploadFile) -> SavedFile:
        if not file.filename:
            raise ValueError("Uploaded file must have a filename")

        if file.content_type != "text/csv":
            raise ValueError(
                f"Content type {file.content_type} currently not supported"
            )

        file_name = self._build_file_name(file.filename)
        file_path = FileUtils.create_folder("uploads") / file_name
        await self._write_file_to_disk(file, file_path)
        self.__logger.debug(
            f"File {file_name} processed successfully",
        )

        return SavedFile(
            name=file_name,
            file_path=str(file_path),
            size=file.size,
            content_type=file.content_type,
        )
