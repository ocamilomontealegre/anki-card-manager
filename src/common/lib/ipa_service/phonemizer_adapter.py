
from phonemizer import phonemize

from common.enums.language_enum import Language
from common.lib.ipa_service.ipa_service_adapter import IpaServiceAdapter


class PhonemizerAdapter(IpaServiceAdapter):
    def __init__(self):
        self.language_map: dict[Language, str] = {
            Language.ENGLISH: "en-us",
            Language.FRENCH: "fr-fr",
            Language.GERMAN: "de",
            Language.ITALIAN: "it",
            Language.PORTUGUESE: "pt-br",
        }

    def transform_text_to_ipa(self, *, text: str, language: Language) -> str:
        result = phonemize(text, language=self.language_map[language], strip=True)
        return str(result)
