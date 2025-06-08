from typing import TypedDict
from ..enums import Language, WordCategory


class Row(TypedDict):
    language: Language
    word: str
    category: WordCategory
