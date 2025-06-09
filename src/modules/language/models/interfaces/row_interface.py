from typing import TypedDict
from typing_extensions import NotRequired
from ..enums import Language, WordCategory


class Row(TypedDict):
    word: str
    language: Language
    category: NotRequired[WordCategory]
