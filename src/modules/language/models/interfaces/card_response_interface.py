from typing import List, TypedDict
from ..enums import Language, WordCategory


class CardResponse(TypedDict):
    word: str
    language: Language
    definition: str
    category: WordCategory
    plural: List[str]
    singular: List[str]
    synonyms: List[str]
    sentence: str
    sentence_phonetics: str
