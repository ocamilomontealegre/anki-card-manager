from injector import Binder, Module, singleton

from modules.word.repositories.word_repository import WordRepository
from modules.word.routers.word_router import WordRouter

from .controllers.word_controller import WordController
from .services.word_service import WordService
from .transformers.word_transformer import WordTransformer


class WordModule(Module):
    def configure(self, binder: Binder):
        binder.bind(WordRouter, to=WordRouter, scope=singleton)
        binder.bind(WordController, to=WordController, scope=singleton)
        binder.bind(WordService, to=WordService, scope=singleton)
        binder.bind(WordRepository, to=WordRepository, scope=singleton)
        binder.bind(WordTransformer, to=WordTransformer, scope=singleton)
