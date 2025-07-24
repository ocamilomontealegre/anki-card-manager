from typing import TypedDict
from googletrans import Translator
from src.common.enums import Language


class Translate(TypedDict):
    text: str
    source: Language
    target: Language


class LanguageUtils:
    @staticmethod
    async def translate(data: Translate):
        translator = Translator()
        result = await translator.translate(
            text=data["text"],
            src=data["source"].value,
            dest=data["target"].value,
        )
        return result.text
