from pydantic import BaseModel, Field


class VerbCardResponse(BaseModel):
    word: str = Field(..., )
    language: str
    definition: str
    usage: str
    verb_form: str
    synonyms: list[str]
    sentence: str
    sentence_phonetics: str