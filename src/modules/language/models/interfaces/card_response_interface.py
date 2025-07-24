from pydantic import BaseModel, Field
from common.enums import Language
from ..enums import WordCategory


class CardResponse(BaseModel):
    word: str = Field(..., description="The main word to define and explain")
    language: Language = Field(
        ..., description="The language in which the word is used"
    )
    definition: str = Field(
        ...,
        description=(
            "A clear and concise definition of the word suitable for learners. "
            "Do not include the word itself in the definition."
            "Do not include any other word forms in the definition"
        ),
    )
    category: WordCategory = Field(
        ...,
        description="The grammatical or semantic category of the word, like noun or verb.",
    )
    plural: list[str] = Field(
        default_factory=list,
        description="A list of plural forms of the word, if applicable, including both feminine and masculine forms. Leave empty if not relevant.",
    )
    singular: list[str] = Field(
        default_factory=list,
        description=(
            "A list of singular forms of the word, if applicable, including both feminine and masculine forms. Leave empty if not relevant."
            "If the word is a verb, add the forms following this pattern 'infinitive', 'present', 'present third person', 'past tense', 'past participle', 'ing form'"
        ),
    )
    synonyms: list[str] = Field(
        default_factory=list,
        description="A list of synonyms or words with similar meanings.",
    )
    sentence: str = Field(
        ...,
        description=(
            "An example sentence using the exact word in context"
            "Do not include any other word forms in the sentence, it has to be the exact one"
        ),
    )
    sentence_phonetics: str = Field(
        ...,
        description="The official IPA (International Phonetic Alphabet) transcription of the sentence",
    )
