from typing import TypedDict
from modules.language.models.enums.word_category_enum import WordCategory


class TransformedCard(TypedDict):
    id: str
    word: str
    category: WordCategory
    definition: str
    sentence: str
    sentence_audio: str
    phonetics: str
    partial_sentence: str
    singular: str
    singular_audio: str
    plural: str
    plural_audio: str
    synonyms: str
    image: str
    image_2: str
