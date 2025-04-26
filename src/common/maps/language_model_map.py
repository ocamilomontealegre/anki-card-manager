from typing import Dict
from modules.language.models.enums.language_enum import Language

language_model_map: Dict[Language, str] = {
    Language.ENGLISH.value: "English - Lava",
    Language.FRENCH.value: "Français - Lave",
    Language.GERMAN.value: "",
    Language.ITALIAN.value: "Italiano - Lava",
    Language.PORTUGUESE.value: "",
}
