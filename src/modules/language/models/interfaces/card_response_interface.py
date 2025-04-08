from typing import List
from pydantic import BaseModel
from ..enums.word_category_enum import WordCategory


class CardResponse(BaseModel):
    word: str
    language: str
    definition: str
    category: WordCategory
    plural: List[str]
    singular: List[str]
    synonyms: List[str]
    sentence: str
    phonetics: str
