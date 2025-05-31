from typing import TypedDict
from ..enums.language_enum import Language


class Row(TypedDict):
    language: Language
    word: str
