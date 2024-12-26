from injector import inject
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..services.upload_service import UploadService


class UploadController():
    @inject
    def __init__(self, upload_service: UploadService) -> None:
        self.__upload_service = upload_service
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        @self.__router.post("")
        async def upload(file: UploadFile = File(...)):
            if not file:
                raise HTTPException(status_code=400, detail="Not file provided")

            await self.__upload_service.process_file(file)

    def get_router(self) -> APIRouter:
        return self.__router
