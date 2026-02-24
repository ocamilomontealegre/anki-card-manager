from fastapi import APIRouter
from injector import inject

from modules.upload.controllers.upload_controller import UploadController


class UploadRouter:
    @inject
    def __init__(self, upload_controller: UploadController):
        self._upload_controller = upload_controller

        self._router = APIRouter()
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.add_api_route(
            "/",
            self._upload_controller.upload,
            methods=["POST"],
        )
