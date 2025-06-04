from pydantic import BaseModel
from typing import List
from ..enums import Language, WordCategory


class CardResponse(BaseModel):
    word: str
    language: Language
    definition: str
    category: WordCategory
    plural: List[str]
    singular: List[str]
    synonyms: List[str]
    sentence: str
    sentence_phonetics: str
