from pydantic import Field

from common.enums.language_enum import Language
from modules.language.models.interfaces.card_response_interfaces.card_response_interface import (
    CardResponseBase,
    Forms,
)


class ItalianCardResponse(CardResponseBase):
    language: Language = Field(
        Language.ITALIAN, description="The language in which the word is used"
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
