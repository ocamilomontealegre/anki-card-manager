from typing import TypedDict
from typing_extensions import NotRequired
from modules.language.models.enums import Language, WordCategory


class FindAllParams(TypedDict):
    limit: NotRequired[int]
    offset: NotRequired[int]
    sort: NotRequired[str]
    word: NotRequired[str]
    category: NotRequired[WordCategory]
    language: NotRequired[Language]
