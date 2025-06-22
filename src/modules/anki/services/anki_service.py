import httpx
from requests import RequestException
from injector import inject
from common.loggers.models.abstracts.logger_abstract import Logger
from common.env.env_config import EnvVariables
from common.maps import language_model_map, language_deck_map
from common.enums import Language
from modules.word.services.word_service import WordService
from modules.word.models.inferfaces.find_all_params import FindAllParams
from modules.word.transformers.word_transformer import WordTransformer


class AnkiService:
    @inject
    def __init__(
        self,
        word_service: WordService,
        word_transformer: WordTransformer,
        logger: Logger,
    ) -> None:
        self._file = AnkiService.__name__

        self._anki_env = EnvVariables.get().anki

        self._logger = logger

        self._word_service = word_service
        self._word_transformer = word_transformer

    def _get_deck_for_lang(self, language: Language) -> str:
        return language_deck_map.get(language, Language.ENGLISH.value)

    def _get_model_for_lang(self, language: Language) -> str:
        return language_model_map.get(language, Language.ENGLISH.value)

    async def create_cards(self, filters: FindAllParams):
        method = self.create_cards.__name__

        (words, size) = self._word_service.list_paginated(filters=filters)

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
                async with httpx.AsyncClient() as client:
                    self._logger.debug(
                        f"Adding card for word: {word}",
                        file=self._file,
                        method=method,
                    )

                    response = await client.post(
                        self._anki_env.connect, json=payload
                    )
                    response.raise_for_status()
                    data = response.json()

                if "error" in data and data["error"]:
                    self._logger.error(
                        f"Error adding card for word: {word} -> {data['error']}",
                        file=self._file,
                        method=method,
                    )
                else:
                    results.append(data.get("result"))
            except RequestException as e:
                self._logger.error(
                    f"Failed to connect to AnkiConnect: {e}",
                    file=self._file,
                    method=method,
                )
                continue

        return results
