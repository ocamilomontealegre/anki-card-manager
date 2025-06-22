import httpx
from requests import RequestException
from injector import inject
from common.loggers.app_logger import AppLogger
from common.env.env_config import get_env_variables
from common.maps import language_model_map, language_deck_map
from common.enums import Language
from modules.word.services.word_service import WordService
from modules.word.models.inferfaces.find_all_params import FindAllParams
from modules.word.transformers.word_transformer import WordTransformer


class AnkiService:
    @inject
    def __init__(
        self, word_service: WordService, word_transformer: WordTransformer
    ) -> None:
        self._anki_env = get_env_variables().anki

        self._logger = AppLogger(label=AnkiService.__name__)

        self._word_service = word_service
        self._word_transformer = word_transformer

    def _get_deck_for_lang(self, language: Language) -> str:
        return language_deck_map.get(language, Language.ENGLISH.value)

    def _get_model_for_lang(self, language: Language) -> str:
        return language_model_map.get(language, Language.ENGLISH.value)

    async def create_cards(self, filters: FindAllParams):
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
                    response = await client.post(
                        self._anki_env.connect, json=payload
                    )
                    response.raise_for_status()
                    data = response.json()

                if "error" in data and data["error"]:
                    self._logger.error(
                        f"Error adding card for word: {word} -> {data['error']}"
                    )
                else:
                    results.append(data.get("result"))
            except RequestException as e:
                self._logger.error(f"Failed to connect to AnkiConnect: {e}")
                continue

        return results
