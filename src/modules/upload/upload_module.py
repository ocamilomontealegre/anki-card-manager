from injector import Binder, Module, singleton

from modules.upload.routers.upload_router import UploadRouter

from .controllers.upload_controller import UploadController
from .services.upload_service import UploadService


class UploadModule(Module):
    def configure(self, binder: Binder):
        binder.bind(UploadRouter, to=UploadRouter, scope=singleton)
        binder.bind(UploadController, to=UploadController, scope=singleton)
        binder.bind(UploadService, to=UploadService, scope=singleton)
