from pathlib import Path
from injector import inject
from fastapi import UploadFile
from pyee import EventEmitter
from common.loggers.logger import AppLogger
from common.utils.file_utils import FileUtils


class UploadService():
    @inject
    def __init__(self, event_emitter: EventEmitter):
        self.__event_emitter = event_emitter

        self.__logger = AppLogger(label=UploadService.__name__)

    async def __save_file(self, file_path: str, file_data: UploadFile) -> Path:
        with open(file_path, "wb") as file:
            file.write(await file_data.read())
        self.__logger.info(f"File {file_path} saved successfully", self.__save_file.__name__)
        return file_path

    async def process_file(self, file: UploadFile):
        file_path = FileUtils.create_folder("uploads") / file.filename
        file_name = await self.__save_file(file_path, file)
        self.__logger.info(f"File {file_name} processed successfully", self.process_file.__name__)
        self.__event_emitter.emit("upload", file_name)

        return {"status": "OK"}
