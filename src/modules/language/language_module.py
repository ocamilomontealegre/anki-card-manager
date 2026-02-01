from injector import Binder, Module, singleton

from .controllers.language_controller import LanguageController
from .services.language_service import LanguageService
from .transformers.language_transformer import LanguageTransformer


class LanguageModule(Module):
    def configure(self, binder: Binder):
        binder.bind(LanguageController, to=LanguageController, scope=singleton)
        binder.bind(LanguageService, to=LanguageService, scope=singleton)
        binder.bind(LanguageTransformer, to=LanguageTransformer, scope=singleton)
