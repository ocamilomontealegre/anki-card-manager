from injector import inject
from fastapi import APIRouter, File, HTTPException, UploadFile
from common.enums import AppEndpoints
from ..services.upload_service import UploadService
from ..models.saved_file_model import SavedFile


class UploadController:
    @inject
    def __init__(self, upload_service: UploadService) -> None:
        self._upload_service = upload_service
        self._router = APIRouter(
            prefix=AppEndpoints.UPLOAD.value, tags=["Upload"]
        )
        self._register_routes()

    def _register_routes(self):

        @self._router.post(
            "",
            response_model=SavedFile,
            description="Upload a file",
            summary="Upload a file",
        )
        async def upload(file: UploadFile = File(...)):
            if not file:
                raise HTTPException(
                    status_code=400, detail="Not file provided"
                )

            return await self._upload_service.save_file(file)

    def get_router(self) -> APIRouter:
        return self._router
