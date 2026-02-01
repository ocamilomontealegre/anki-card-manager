from typing import TypedDict

from typing_extensions import NotRequired

from common.enums.language_enum import Language
from common.enums.word_category_enum import WordCategory


class CreateCards(TypedDict):
    limit: NotRequired[int]
    offset: NotRequired[int]
    sort: NotRequired[str]
    word: NotRequired[str]
    category: NotRequired[WordCategory]
    language: NotRequired[Language]
