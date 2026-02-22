from injector import inject
from requests import RequestException

from common.enums import Language
from common.env.env_config import EnvVariables
from common.lib.http_client.http_client_adapter import HttpOptions
from common.lib.http_client.httpx_adapter import HttpxAdapter
from common.loggers.models.abstracts.logger_abstract import Logger
from common.maps import language_deck_map, language_model_map
from modules.word.models.interfaces.list_params import ListParams
from modules.word.repositories.word_repository import WordRepository
from modules.word.transformers.word_transformer import WordTransformer


class AnkiService:
    @inject
    def __init__(
        self,
        word_repository: WordRepository,
        word_transformer: WordTransformer,
        http_client: HttpxAdapter,
        logger: Logger,
    ) -> None:
        self._file = AnkiService.__name__

        self._word_repository = word_repository
        self._word_transformer = word_transformer

        self._http_client = http_client
        self._logger = logger

        self._anki_env = EnvVariables.get().anki

    def _get_deck_for_lang(self, language: Language) -> str:
        return language_deck_map.get(language.value, Language.ENGLISH.value)

    def _get_model_for_lang(self, language: Language) -> str:
        return language_model_map.get(language.value, Language.ENGLISH.value)

    async def create_cards(self, params: ListParams):
        method = self.create_cards.__name__

        words = self._word_repository.list(params=params)

        results = []
        for word in words:
            transformed_word = self._word_transformer.transform(word)
            language = word.language

            payload = {
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                        "deckName": self._get_deck_for_lang(
                            language=Language(language)
                        ),
                        "modelName": self._get_model_for_lang(
                            language=Language(language)
                        ),
                        "fields": transformed_word.model_dump(mode="json"),
                        "options": {"allowDuplicate": False},
                        "tags": [
                            language,
                            transformed_word.category,
                        ],
                    }
                },
            }

            try:
                self._logger.debug(
                    f"Adding card for word: {word}",
                    file=self._file,
                    method=method,
                )

                response = await self._http_client.request(
                    self._anki_env.connect,
                    http_options=HttpOptions(method="POST", body=payload),
                )

                if "error" in response and response["error"]:
                    self._logger.error(
                        f"Error adding card for word: {word} -> {response['error']}",
                        file=self._file,
                        method=method,
                    )
                else:
                    results.append(response.get("result"))
            except RequestException as e:
                self._logger.error(
                    f"Failed to connect to AnkiConnect: {e}",
                    file=self._file,
                    method=method,
                )
                continue

        return results
