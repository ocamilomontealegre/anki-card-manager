import requests
from os import path
from injector import inject
from modules.word.services.word_service import WordService
from modules.word.models.entities.word_entity import Word


class AnkiService():
    @inject
    def __init__(self, word_service: WordService) -> None:
        self.__word_service = word_service

    def __format_audio_path(self, audio_path) -> str:
        if audio_path:
            return f"[sound:{path.basename(audio_path)}]"
        else:
            return ""

    def __transform(self, word: Word) -> dict:
        return {
            "id": word.id,
            "word": word.word,
            "category": word.category,
            "definition": word.definition,
            "sentence": word.sentence,
            "sentence_audio": self.__format_audio_path(word.sentence_audio),
            "phonetics": f"/{word.phonetics}/",
            "partial_sentence": word.partial_sentence,
            "singular": word.singular,
            "singular_audio": self.__format_audio_path(word.singular_audio),
            "plural": word.plural,
            "plural_audio": self.__format_audio_path(word.plural_audio),
            "synonyms": word.synonyms,
            "image": path.basename(word.image),
            "image_2": path.basename(word.image_2),
        }

    def create_cards(self):
        words = self.__word_service.find_all()

        for word in words:
            transformed_word = self.__transform(word)

            response = requests.post("http://localhost:8765", json={
                "action": "addNote",
                "version": 6,
                "params": transformed_word
            }).json()

            return response["result"]
