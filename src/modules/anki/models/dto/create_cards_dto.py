from pydantic import BaseModel, Field

from common.enums.language_enum import Language
from common.enums.word_category_enum import WordCategory


class CreateCardsDto(BaseModel):
    limit: int | None = Field(
        default=100,
        ge=1,
        le=1000,
        examples=[10],
    )
    offset: int | None = Field(default=None, ge=1, examples=[10])
    sort: str | None = Field(default="asc", pattern="^(asc|dsc)$", examples=["asc"])
    word: str | None = Field(
        default=None, min_length=2, max_length=100, examples=["hello"]
    )
    category: WordCategory | None = Field(
        default=None, examples=[WordCategory.NOUN.value]
    )
    language: Language | None = Field(default=None, examples=[Language.ENGLISH.value])
