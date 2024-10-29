from fastapi import APIRouter, File, UploadFile
from injector import inject
from file.services.file_service import FileService

class FileController:
    @inject
    def __init__(self, file_service: FileService):
        self.__file_service = file_service
        self.__router = APIRouter()

    def __register_routes(self):
        @self.__router.post("")
        async upload_file(file: UploadFile = File(...)):