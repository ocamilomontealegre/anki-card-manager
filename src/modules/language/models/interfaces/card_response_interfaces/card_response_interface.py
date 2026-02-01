from pydantic import BaseModel, Field

from common.enums import Language, Usage, WordCategory


class Forms(BaseModel):
    singular_masculine: str = Field(
        ...,
        description="""
        Singular masculine form of word, leave empty if none
    """,
    )
    singular_feminine: str = Field(
        ...,
        description="""
        Singular masculine form of word, leave empty if none
    """,
    )
    plural_masculine: str = Field(
        ...,
        description="""
        Singular masculine form of word, leave empty if none
    """,
    )
    plural_feminine: str = Field(
        ...,
        description="""
        Singular masculine form of word, leave empty if none
    """,
    )


class CardResponseBase(BaseModel):
    word: str = Field(..., description="The main word to be defined and explained")
    language: Language
    definition: str = Field(
        ...,
        description="""
            Provide a clear, concise definition of the word suitable for learners.
            Guidelines:
            - Do not include the word itself.
            - Do not include any other word forms.
            - Example: For the word 'run', write 'to move swiftly on foot' instead of 'to run'.
        """,
    )
    category: WordCategory = Field(
        ...,
        description="The grammatical or semantic category of the word, like noun or verb.",
    )
    usage: Usage = Field(
        ..., description="The context or style in which the word is typically used."
    )
    frequency_rank: str | None = Field(
        None,
        description="""
            A numerical ranking representing how common the word is in general usage.
            Guidelines:
            - Lower numbers indicate more frequent/common words (e.g., 1 is the most common).
            - Higher numbers indicate rarer words.
            Example: 'The word "the" might have frequency_rank 1, while "scourge" might have 15342.'
        """,
    )
    forms: Forms | None
    conjugations: list[str] | None
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
            - Replace the target word fo {...}
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
