from abc import ABC, abstractmethod
from pathlib import Path

from common.enums.language_enum import Language


class TtsAdapter(ABC):
    @abstractmethod
    async def synthetize_text(self, *, text: str, language: Language, output_file: Path) -> str:
        pass
