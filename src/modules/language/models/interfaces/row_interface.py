from typing import TypedDict
from typing_extensions import NotRequired
from ..enums import Language, WordCategory


class Row(TypedDict):
    language: Language
    word: str
    category: NotRequired[WordCategory]
