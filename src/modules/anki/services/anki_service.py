import requests
from typing import Dict
from injector import inject
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from modules.language.models.enums.language_enum import Language
from modules.word.services.word_service import WordService
from modules.word.transformers.word_transformer import WordTransformer


class AnkiService():
    @inject
    def __init__(self, word_service: WordService, word_transformer: WordTransformer) -> None:
        self.__anki_env = get_env_variables().anki

        self.__logger = AppLogger(label=AnkiService.__name__)

        self.__word_service = word_service
        self.__word_transformer = word_transformer

        self.__language_deck_map: Dict[Language, str] = {
            Language.ENGLISH.value: "Book 10 - Lava",
            Language.FRENCH.value: "Livre 2 - Lave",
            Language.GERMAN.value: "",
            Language.ITALIAN.value: "Livro 6 - Lava",
            Language.PORTUGUESE.value: ""
        }

        self.__language_model_map: Dict[Language, str] = {
            Language.ENGLISH.value: "English - Lava",
            Language.FRENCH.value: "Français - Lave",
            Language.GERMAN.value: "",
            Language.ITALIAN.value: "Italiano - Lava",
            Language.PORTUGUESE.value: ""
        }

    @property
    def language_deck_map(self):
        return self.__language_deck_map

    @property
    def language_model_map(self):
        return self.__language_model_map

    def __get_deck_for_lang(self, language: Language) -> str:
        return self.__language_deck_map.get(language, Language.ENGLISH.value)

    def __get_model_for_lang(self, language: Language) -> str:
        return self.__language_model_map.get(language, Language.ENGLISH.value)

    def create_cards(self):
        words = self.__word_service.find_all(filters={})
        results = []

        for word in words:
            transformed_word = self.__word_transformer.transform(word)

            payload = {
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                        "deckName": self.__get_deck_for_lang(word.get("language", "")),
                        "modelName": self.__get_model_for_lang(word.get("language", "")),
                        "fields": transformed_word,
                        "options": {
                            "allowDuplicate": False
                        },
                        "tags": [word.get("language", ""), transformed_word.get("category", "uncategorized")]
                    }
                }
            }

            try:
                response = requests.post(self.__anki_env.connect, json=payload)
                response.raise_for_status()
                data = response.json()

                if "error" in data and data["error"]:
                    self.__logger.error(f"Error adding card for word: {word} -> {data["error"]}")
                else:
                    results.append(data.get("result"))
            except requests.RequestException as e:
                self.__logger.error(f"Failed to connect to AnkiConnect: {e}")
                continue

        return results
