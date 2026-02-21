from pydantic import Field

from modules.language.models.interfaces.card_response_interfaces.card_response_interface import (
    CardResponseBase,
)


class CardVerbResponse(CardResponseBase):
    word: str = Field(..., description="Verb form to be defined and explained")
    definition: str = Field(
        ...,
        description="""
            A string covering the thense, the person, and the base verb        
            Example: For: 'mangio': Present - First Person - Parlare
        """
    )
    sentence: str = Field(
        ...,
        description="""
            A single example sentence showing how the word (verb form) is used in context for the target Language
            Guidelines:
            - Highlight the target word between []
            - Use the word correctly in a simple, learner-friendly sentence.
            - Use the exact provided word
            Example: For 'mangio': 'Io [mangio] pasta tutti giorni'
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

