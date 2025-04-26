from os import path
from injector import inject
from ..models.entities.word_entity import Word
from ..models.inferfaces.transformed_card_interface import TransformedCard


class WordTransformer:
    @inject
    def __init__(self):
        pass

    def __format_audio_path(self, audio_path) -> str:
        return f"[sound:{path.basename(audio_path)}]" if audio_path else ""

    def transform(self, word: Word) -> TransformedCard:
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
