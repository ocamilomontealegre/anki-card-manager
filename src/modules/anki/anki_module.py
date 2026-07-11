from injector import Binder, Module, singleton

from modules.anki.routers.anki_router import AnkiRouter

from .controllers.anki_controller import AnkiController
from .services.anki_service import AnkiService


class AnkiModule(Module):
    def configure(self, binder: Binder):
        binder.bind(AnkiRouter, to=AnkiRouter, scope=singleton)
        binder.bind(AnkiController, to=AnkiController, scope=singleton)
        binder.bind(AnkiService, to=AnkiService, scope=singleton)
