from pydantic import Field

from common.enums.language_enum import Language
from modules.language.models.interfaces.card_response_interfaces.card_response_interface import (
    CardResponseBase,
    Forms,
)


class EnglishCardResponse(CardResponseBase):
    language: Language = Field(
        Language.ENGLISH, description="The language in which the word is used"
    )
    forms: Forms | None = Field(
        ...,
        description="""
            The grammatical forms of the word, grouped by number and gender.
            Guidelines:
            - Just for nouns
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
        None,
        description="""
            A list of the verb conjugated forms in english
            Guidelines:
            - Just for english verbs
            - Follow the pattern infinitive, present, present third person, past tense, past participle, ing form
            - Optional: leave empty if the word is not a verb or has no conjugations.
            Example: ['to run', 'runs', 'ran', 'run', 'running']
        """,
    )
