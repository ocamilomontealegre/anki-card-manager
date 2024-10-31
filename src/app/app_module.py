from injector import Binder, Module
from health.health_module import HealthModule
from modules.file.file_module import FileModule


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(HealthModule())
        binder.install(FileModule())
