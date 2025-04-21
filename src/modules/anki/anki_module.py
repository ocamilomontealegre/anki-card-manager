from injector import Binder, Module, singleton
from .controllers.anki_controller import AnkiController
from .services.anki_service import AnkiService


class AnkiModule(Module):
    def configure(self, binder: Binder):
        binder.bind(AnkiController, to=AnkiController, scope=singleton)
        binder.bind(AnkiService, to=AnkiService, scope=singleton)
