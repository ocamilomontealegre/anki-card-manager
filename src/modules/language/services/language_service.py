import requests
from uuid import uuid4
from pathlib import Path
from typing import List, Optional
from injector import inject
from pandas import read_csv
from pyee import EventEmitter
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from modules.word.services.word_service import WordService
from modules.scraper.services.scraper_service import ScraperService
from modules.word.models.entities.word_entity import Word
from ..models.interfaces import CardResponse, Row


class LanguageService():
    @inject
    def __init__(
        self,
        word_service: WordService,
        scraper_service: ScraperService,
        event_emitter: EventEmitter
    ) -> None:
        self.__env = get_env_variables()

        self.__logger = AppLogger(label=LanguageService.__name__)

        self.__word_service = word_service
        self.__scraper_service = scraper_service

        self.__event_emitter = event_emitter
        self.__open_ai_client = OpenAI(api_key=self.__env.openai.key)

        self.__eleven_labs_client = ElevenLabs(api_key=self.__env.elevenlabs.key)

        self.__event_emitter.on("upload", self.process_csv)

    def __download_image(self, url: str, word: str) -> str:
        response = requests.get(url, stream=True)

        extension = ""
        if "giphy" in url:
            extension = "gif"
        else:
            extension = "jpg"

        path = Path(self.__env.anki.media) / f"{word}_{uuid4().hex[:8]}.{extension}"
        with open(path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        return str(path)

    def __transform_text_to_audio(self, text: str, word: str, prefix: str = "") -> str:
        try:
            audio = self.__eleven_labs_client.text_to_speech.convert(
                text=text,
                voice_id="JBFqnCBsd6RMkjVDRZzb",
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )

            audio_bytes = b''.join(audio)
            audio_path = f"{self.__env.anki.media}/{prefix}_{word}.mp3"
            with open(audio_path, "wb") as audio_file:
                audio_file.write(audio_bytes)
            return audio_path
        except Exception as e:
            self.__logger.error(f"Error transforming text to audio {e}")

    def __check_word_forms(self, base_word: str, word_forms: Optional[str]) -> str:
        if word_forms and word_forms != ", ":
            return word_forms[:-1] if word_forms[-1] == "," else word_forms
        else:
            return f"{base_word[0].upper()}{base_word[1:]}"

    def __transform_card(self, card_info: CardResponse) -> Word:
        try:
            card_info = card_info.dict()
            word = card_info["word"]
            plural = ", ".join(list(map(lambda x: x.capitalize(), card_info["plural"])))
            singular = ", ".join(list(map(lambda x: x.capitalize(), card_info["singular"])))
            synonyms = ", ".join(list(map(lambda x: x.capitalize(), card_info["synonyms"])))
            sentence = card_info["sentence"]
            partial_sentence = sentence.replace(word, "[...]")
            word_forms = f"{singular}, {plural}"

            giphy_image_url = self.__scraper_service.get_giphy_image_url(query=word)
            giphy_image = self.__download_image(url=giphy_image_url, word=word)

            unplash_url = self.__scraper_service.get_unplash_image_url(query=word)
            unplash_image = self.__download_image(url=unplash_url, word=word)

            sentence_path = self.__transform_text_to_audio(sentence, word)

            plural_audio_path = ''
            if len(plural) > 0:
                plural_audio_path = self.__transform_text_to_audio(plural, word, "plural")

            singular_audio_path = ''
            if len(singular) > 0:
                singular_audio_path = self.__transform_text_to_audio(singular, word, "singular")

            new_word = Word(
                word=self.__check_word_forms(word, word_forms),
                language=card_info["language"].value,
                category=card_info["category"].value.capitalize(),
                definition=card_info["definition"].capitalize(),
                sentence=sentence,
                phonetics=card_info["sentence_phonetics"],
                sentence_audio=sentence_path,
                partial_sentence=partial_sentence,
                singular=singular,
                singular_audio=singular_audio_path,
                plural=plural,
                plural_audio=plural_audio_path,
                synonyms=synonyms,
                image=self.__download_image(giphy_image, word),
                image_2=self.__download_image(unplash_image, word)
            )
            return new_word
        except Exception as e:
            self.__logger.error(f"Error transforming card: {e}", self.__transform_card.__name__)

    def process_cards(self, cards_info: List[CardResponse]) -> None:
        self.__word_service.create_many(cards_info)

    def process_row(self, row: Row) -> CardResponse:
        try:
            completion = self.__open_ai_client.beta.chat.completions.parse(
                model=self.__env.openai.model,
                messages=[
                    {"role": "system", "content": "You are a polyglot expert with over 10 years of experience"},
                    {"role": "user", "content": f"please look for the definition of the word: {row["word"]} in the {row["language"]} language"}
                ],
                response_format=CardResponse
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            self.__logger.error(f"Error processing row: {row}, Error: {e}", self.process_row.__name__)

    def process_csv(self, file_name: str) -> None:
        df = read_csv(file_name, delimiter=",")

        words_data: List[CardResponse] = []
        for _, row in df.iterrows():
            card_responses = self.process_row(row.to_dict())
            words_data.append(card_responses)

        transformed_words: List[Word] = []
        for card_response in words_data:
            self.__logger.debug(f"WORD: {card_response.word}")
            transformed_word = self.__transform_card(card_response)
            transformed_words.append(transformed_word)
            self.process_cards(transformed_words)
