from typing import List
from pydantic import BaseModel


class CardResponse(BaseModel):
    word: str
    definition: str
    plural: List[str]
    singular: List[str]
    synonyms: List[str]
    sentence: str
    phonetics: str
