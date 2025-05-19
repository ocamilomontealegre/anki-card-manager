from os import path
from injector import inject
from ..models.entities.word_entity import Word
from ..models.inferfaces.transformed_card_interface import TransformedCard


class WordTransformer:
    @inject
    def __init__(self):
        # This constructor is intentionally left empty because
        pass

    def __format_audio_path(self, audio_path) -> str:
        return f"[sound:{path.basename(audio_path)}]" if audio_path else ""

    def transform(self, word: Word) -> TransformedCard:
        word_dict = word.to_dict()

        print("SENTENCE: ", word_dict.get("sentence_audio"))

        return TransformedCard(
            id=word_dict.get("id", ""),
            word=word_dict.get("word", ""),
            category=word_dict.get("category", ""),
            definition=word_dict.get("definition", ""),
            sentence=word_dict.get("sentence", ""),
            sentence_audio=self.__format_audio_path(
                word_dict.get("sentence_audio", "")
            ),
            phonetics=f"/{word_dict.get('phonetics', '')}/",
            partial_sentence=word_dict.get("partial_sentence", ""),
            singular=word_dict.get("singular", ""),
            singular_audio=self.__format_audio_path(
                word_dict.get("singular_audio", "")
            ),
            plural=word_dict.get("plural", ""),
            plural_audio=self.__format_audio_path(
                word_dict.get("plural_audio", "")
            ),
            synonyms=word_dict.get("synonyms", ""),
            image=path.basename(word_dict.get("image", "")),
            image_2=path.basename(word_dict.get("image_2", "")),
        )
