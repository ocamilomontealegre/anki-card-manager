from abc import ABC, abstractmethod

from common.enums.language_enum import Language


class IpaServiceAdapter(ABC):
    @abstractmethod
    def transform_text_to_ipa(self, *, text: str, language: Language) -> str:
        pass
