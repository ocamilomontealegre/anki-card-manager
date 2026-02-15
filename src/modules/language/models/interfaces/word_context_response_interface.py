from pydantic import BaseModel, Field

from common.enums.word_category_enum import WordCategory


class Context(BaseModel):
    category: WordCategory
    definition: str


class WordContextResponse(BaseModel):
    word: str = Field(
        ...,
    )
    context: list[Context]

