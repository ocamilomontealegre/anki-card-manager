from pydantic import BaseModel, Field

from common.enums.language_enum import Language
from common.enums.word_category_enum import WordCategory
from modules.language.models.enums.usage_enum import Usage
from modules.language.models.interfaces.card_response_interfaces.card_response_interface import (
    Forms,
)


class ItalianCardResponse(BaseModel):
    word: str = Field(..., description="The main word to be defined and explained")
    language: Language = Field(
        ..., description="The language in which the word is used"
    )
    definition: str = Field(
        ...,
        description="""
            Provide a clear, concise definition of the word suitable for learners in Italian
            Guidelines:
            - Do not include the word itself.
            - Do not include any other word forms.
        """,
    )
    category: WordCategory = Field(
        ...,
        description="The grammatical or semantic category of the word, like noun or verb.",
    )
    usage: Usage = Field(
        ..., description="The context or style in which the word is typically used."
    )
    etymology: str | None = Field(
        None,
        description="""
            The origin and history of the word.
            Guidelines:
            - Explain where the word comes from (language, root words, historical usage).
            - Keep it concise and learner-friendly.
            - Avoid including unrelated definitions or examples.
            Example: 'The word "scourge" comes from Old French "escorgier", meaning to whip.'
        """,
    )
    frequency_rank: int | None = Field(
        None,
        description="""
            A numerical ranking representing how common the word is in general usage.
            Guidelines:
            - Lower numbers indicate more frequent/common words (e.g., 1 is the most common).
            - Higher numbers indicate rarer words.
            - Optional: leave empty if no reliable frequency data is available.
            Example: 'The word "the" might have frequency_rank 1, while "scourge" might have 15342.'
        """,
    )
    forms: Forms | None = Field(
        ...,
        description="""
            The grammatical forms of the word, grouped by number and gender.
            Guidelines:
            
            - Include singular and plural forms if applicable.
            - Include masculine and feminine forms if applicable.
            Example:
                singular_masculine: 'ami'
                singular_feminine: 'amie'
                plural_masculine: 'amis'
                plural_feminine: 'amies'
        """,
    )
    conjugations: list[str] | None = Field(
        [],
    )
    synonyms: list[str] = Field(
        default_factory=list,
        description="""
            A list of words that have a similar meaning to this word.
            Guidelines:
            - Include only words that can be used in a similar context.
            - Optional: leave empty if no close synonyms exist.
            Example: For 'happy', synonyms might be ['joyful', 'content', 'cheerful'].
        """,
    )
    sentence: str = Field(
        ...,
        description="""
            A single example sentence showing how the word is used in context for the Italian Language
            Guidelines:
            - Highlight the target word between []
            - Use the word correctly in a simple, learner-friendly sentence.
            - Use the exact provided word
            - Avoid idioms or overly complex sentences.
            Example: For 'scourge': 'The disease was a scourge on the village.'
        """,
    )
    partial_sentence: str = Field(
        ...,
        description="""
            The same sentence but with some transformations
            Guidelines:
            - Replace the target word for {...}
        """,
    )
    sentence_phonetics: str = Field(
        ...,
        description="""
            The phonetic transcription of the example sentence in IPA (International Phonetic Alphabet).
            Guidelines:
            - Transcribe the sentence exactly as it appears in `sentence`.
            - Use standard IPA symbols consistently throughout.
            Example: 
                Sentence: 'The disease was a scourge on the village.'
                IPA: 'ðə dɪˈziːz wəz ə skɜːrdʒ ɒn ðə ˈvɪlɪdʒ'
        """,
    )
    image: str = Field(
        ..., description="An image link related to the sentence and the target word"
    )