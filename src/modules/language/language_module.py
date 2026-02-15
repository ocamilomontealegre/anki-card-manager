from injector import Binder, Module, singleton

from common.lib.http_client.http_client_adapter import HttpClientAdapter
from common.lib.http_client.httpx_adapter import HttpxAdapter
from common.lib.ipa_service.ipa_service_adapter import IpaServiceAdapter
from common.lib.ipa_service.phonemizer_adapter import PhonemizerAdapter
from common.lib.tts.google_tts_adapter import GoogleTtsAdapter
from common.lib.tts.tts_adapter import TtsAdapter
from modules.language.repositories.language_repository import LanguageRepository

from .controllers.language_controller import LanguageController
from .services.language_service import LanguageService
from .transformers.language_transformer import LanguageTransformer


class LanguageModule(Module):
    def configure(self, binder: Binder):
        binder.bind(LanguageController, to=LanguageController, scope=singleton)
        binder.bind(LanguageService, to=LanguageService, scope=singleton)
        binder.bind(LanguageTransformer, to=LanguageTransformer, scope=singleton)
        binder.bind(LanguageRepository, to=LanguageRepository, scope=singleton)
        binder.bind(IpaServiceAdapter, to=PhonemizerAdapter, scope=singleton)
        binder.bind(TtsAdapter, to=GoogleTtsAdapter, scope=singleton)
        binder.bind(HttpClientAdapter, to=HttpxAdapter, scope=singleton)
