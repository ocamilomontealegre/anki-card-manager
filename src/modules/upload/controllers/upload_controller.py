from injector import inject
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..services.upload_service import UploadService


class UploadController:
    @inject
    def __init__(self, upload_service: UploadService) -> None:
        self._upload_service = upload_service
        self._router = APIRouter()
        self.__register_routes()

    def __register_routes(self):

        @self._router.post("")
        async def upload(file: UploadFile = File(...)):
            if not file:
                raise HTTPException(
                    status_code=400, detail="Not file provided"
                )

            return await self._upload_service.save_file(file)

    def get_router(self) -> APIRouter:
        return self._router
