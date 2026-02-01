from typing import TypedDict

from typing_extensions import NotRequired

from common.enums.language_enum import Language
from common.enums.word_category_enum import WordCategory


class Row(TypedDict):
    word: str
    language: Language
    category: NotRequired[WordCategory]
    context: NotRequired[str]
