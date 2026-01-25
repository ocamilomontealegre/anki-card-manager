from typing import Any

from ..models.enums import Language
from ..models.interfaces import (
    EnglishCardResponse,
    FrenchCardResponse,
    ItalianCardResponse,
)

card_interface_map: dict[str, Any] = {
    Language.ENGLISH.value: EnglishCardResponse,
    Language.FRENCH.value: FrenchCardResponse,
    Language.ITALIAN.value: ItalianCardResponse,
}
