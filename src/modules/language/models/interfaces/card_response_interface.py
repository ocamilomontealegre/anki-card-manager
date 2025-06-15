from pydantic import BaseModel, Field
from typing import List
from common.enums import Language
from ..enums import WordCategory


class CardResponse(BaseModel):
    word: str
    language: Language
    definition: str
    category: WordCategory
    plural: List[str]
    singular: List[str]
    synonyms: List[str]
    sentence: str
    sentence_phonetics: str = Field(
        ...,
        description="Official IPA",
    )
