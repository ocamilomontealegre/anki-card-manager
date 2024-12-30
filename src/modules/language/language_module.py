from injector import Module, Binder, singleton
from .controllers.language_controller import LanguageController
from .services.language_service import LanguageService


class LanguageModule(Module):
    def configure(self, binder: Binder):
        binder.bind(LanguageController, to=LanguageController, scope=singleton)
        binder.bind(LanguageService, to=LanguageService, scope=singleton)
