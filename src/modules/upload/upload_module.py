from injector import Binder, Module, singleton
from .controllers.upload_controller import UploadController
from .services.upload_service import UploadService


class UploadModule(Module):
    def configure(self, binder: Binder):
        binder.bind(UploadController, to=UploadController, scope=singleton)
        binder.bind(UploadService, to=UploadService, scope=singleton)
