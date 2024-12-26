from pyee import EventEmitter
from injector import Binder, Module, singleton
from health.health_module import HealthModule
from modules.file.file_module import FileModule
from modules.upload.upload_module import UploadModule


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(HealthModule())
        binder.install(FileModule())
        binder.install(UploadModule())
        binder.bind(EventEmitter, to=EventEmitter(), scope=singleton)
