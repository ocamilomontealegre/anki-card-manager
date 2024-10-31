from fastapi import APIRouter, File, UploadFile
from injector import inject
from modules.file.services.file_service import FileService


class FileController:
    @inject
    def __init__(self, file_service: FileService):
        self.__file_service = file_service
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        @self.__router.post("/upload")
        async def upload_file(file: UploadFile = File(...)):
            await self.__file_service.process_file(file)

    def get_router(self) -> APIRouter:
        return self.__router
