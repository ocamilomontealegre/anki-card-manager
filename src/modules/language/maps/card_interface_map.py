from common.enums.language_enum import Language
from modules.language.models.interfaces.card_response_interfaces.card_response_interface import (
    CardResponseBase,
)

from ..models.interfaces import (
    EnglishCardResponse,
    FrenchCardResponse,
    ItalianCardResponse,
)

card_interface_map: dict[str, type[CardResponseBase]] = {
    Language.ENGLISH.value: EnglishCardResponse,
    Language.FRENCH.value: FrenchCardResponse,
    Language.ITALIAN.value: ItalianCardResponse,
    Language.GERMAN.value: EnglishCardResponse,
    Language.PORTUGUESE.value: EnglishCardResponse,
}
