from injector import Module, Binder, singleton
from modules.file.controllers.file_controller import FileController
from modules.file.services.file_service import FileService


class FileModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(FileController, to=FileController, scope=singleton)
        binder.bind(FileService, to=FileService, scope=singleton)
