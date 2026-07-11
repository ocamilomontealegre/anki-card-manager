from fastapi import APIRouter
from injector import inject

from common.enums.app_endpoints_enum import AppEndpoints
from modules.upload.controllers.upload_controller import UploadController
from modules.upload.models.saved_file_model import SavedFile


class UploadRouter:
    @inject
    def __init__(self, upload_controller: UploadController):
        self._upload_controller = upload_controller

        self._router = APIRouter(prefix=AppEndpoints.UPLOAD.value, tags=["upload"])
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.add_api_route(
            "",
            self._upload_controller.upload,
            methods=["POST"],
            response_model=SavedFile,
        )
