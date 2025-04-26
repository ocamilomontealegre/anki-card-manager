from typing import Optional
from pydantic import BaseModel, Field
from modules.language.models.enums import Language, WordCategory


class CreateCardsDto(BaseModel):
    limit: Optional[int] = Field(
        default=100,
        ge=1,
        le=1000,
        examples=[10],
    )
    offset: Optional[int] = Field(default=None, ge=1, examples=[10])
    sort: Optional[str] = Field(
        default="asc", pattern="^(asc|dsc)$", examples=["asc"]
    )
    word: Optional[str] = Field(
        default=None, min_length=2, max_length=100, examples=["hello"]
    )
    category: Optional[WordCategory] = Field(
        default=None, examples=[WordCategory.NOUN.value]
    )
    language: Optional[Language] = Field(
        default=None, examples=[Language.ENGLISH.value]
    )
