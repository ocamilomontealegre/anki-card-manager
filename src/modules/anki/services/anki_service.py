import requests
from typing import List
from injector import inject
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from common.maps import language_model_map, language_deck_map
from modules.language.models.enums.language_enum import Language
from modules.word.services.word_service import WordService
from modules.word.models.entities.word_entity import Word
from modules.word.transformers.word_transformer import WordTransformer
from ..models.interfaces.create_cards_interface import CreateCards


class AnkiService:
    @inject
    def __init__(
        self, word_service: WordService, word_transformer: WordTransformer
    ) -> None:
        self.__anki_env = get_env_variables().anki

        self.__logger = AppLogger(label=AnkiService.__name__)

        self.__word_service = word_service
        self.__word_transformer = word_transformer

    def __get_deck_for_lang(self, language: Language) -> str:
        return language_deck_map.get(language, Language.ENGLISH.value)

    def __get_model_for_lang(self, language: Language) -> str:
        return language_model_map.get(language, Language.ENGLISH.value)

    def create_cards(self, filters: CreateCards):
        words: List[Word] = self.__word_service.find_all(filters=filters)[
            "items"
        ]
        results = []

        for word in words:
            print("WORD: ", word)
            word_dict = word.to_dict()
            transformed_word = self.__word_transformer.transform(word)

            language = word_dict.get("language", "")

            payload = {
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                        "deckName": self.__get_deck_for_lang(
                            language=language
                        ),
                        "modelName": self.__get_model_for_lang(
                            language=language
                        ),
                        "fields": transformed_word,
                        "options": {"allowDuplicate": False},
                        "tags": [
                            language,
                            transformed_word["category"],
                        ],
                    }
                },
            }

            try:
                response = requests.post(self.__anki_env.connect, json=payload)
                response.raise_for_status()
                data = response.json()

                if "error" in data and data["error"]:
                    self.__logger.error(
                        f"Error adding card for word: {word} -> {data['error']}"
                    )
                else:
                    results.append(data.get("result"))
            except requests.RequestException as e:
                self.__logger.error(f"Failed to connect to AnkiConnect: {e}")
                continue

        return results
