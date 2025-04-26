from typing import Dict
from modules.language.models.enums import Language

language_voice_map: Dict[Language, Dict[str, str]] = {
    Language.ENGLISH.value: {
        "language_code": "en-US",
        "voice_model": "en-US-Wavenet-F"
    },
    Language.FRENCH.value: {
        "language_code": "fr-FR",
        "voice_model": "fr-FR-Wavenet-A"
    },
    Language.GERMAN.value: {
        "language_code": "de-DE",
        "voice_model": "de-DE-Wavenet-D"
    },
    Language.ITALIAN.value: {
        "language_code": "it-IT",
        "voice_model": "it-IT-Wavenet-C"
    },
    Language.PORTUGUESE.value: {
        "language_code": "pt-BR",
        "name": "pt-BR-Wavenet-B",
    },
}
