from fastapi import File, HTTPException, UploadFile
from injector import inject

from modules.upload.services.upload_service import UploadService


class UploadController:
    @inject
    def __init__(self, upload_service: UploadService) -> None:
        self._upload_service = upload_service

    async def upload(self, file: UploadFile = File(...)):
        if not file:
            raise HTTPException(status_code=400, detail="Not file provided")

        return await self._upload_service.save_file(file)
