from pyee import EventEmitter
from injector import Binder, Module, singleton
from health.health_module import HealthModule
from modules.upload.upload_module import UploadModule
from modules.language.language_module import LanguageModule


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(module=HealthModule)
        binder.install(module=UploadModule)
        binder.install(module=LanguageModule)
        binder.bind(EventEmitter, to=EventEmitter, scope=singleton)
