from injector import Module, Binder, singleton
from .controllers.word_controller import WordController
from .services.word_service import WordService
from .transformers.word_transformer import WordTransformer


class WordModule(Module):
    def configure(self, binder: Binder):
        binder.bind(WordController, to=WordController, scope=singleton)
        binder.bind(WordService, to=WordService, scope=singleton)
        binder.bind(WordTransformer, to=WordTransformer, scope=singleton)
