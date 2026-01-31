from pydantic import BaseModel, Field

from common.enums import Language

from ...enums import Usage, WordCategory


class Forms(BaseModel):
    singular_masculine: str = Field(..., description="""
        Singular masculine form of word, leave empty if none
    """)
    singular_feminine: str = Field(..., description="""
        Singular masculine form of word, leave empty if none
    """)
    plural_masculine: str = Field(..., description="""
        Singular masculine form of word, leave empty if none
    """)
    plural_feminine: str = Field(..., description="""
        Singular masculine form of word, leave empty if none
    """)

class CardResponseBase(BaseModel):
    word: str
    language: Language
    definition: str
    category: WordCategory
    usage: Usage
    etymology: str | None
    frequency_rank: int | None
    forms: Forms | None
    conjugations: list[str] | None
    synonyms: list[str]
    sentence: str
    partial_sentence: str
    sentence_phonetics: str
    image: str
