from injector import inject
from pandas import read_csv
from pyee import EventEmitter
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from common.env.env_config import get_env_variables
from ..models.interfaces import CardResponse, Row


class LanguageService():
    @inject
    def __init__(self, event_emitter: EventEmitter) -> None:
        self.__open_ai_env = get_env_variables().openai
        self.__eleven_labs_env = get_env_variables().elevenlabs

        self.__event_emitter = event_emitter
        self.__open_ai_client = OpenAI(api_key=self.__open_ai_env.key)
        self.__eleven_labs_client = ElevenLabs(api_key=self.__eleven_labs_env.key)

        self.__event_emitter.on("upload", self.process_csv)

    def process_card(self, card_info: CardResponse):
        word = card_info["word"]
        plural = list(map(lambda x: x.capitalize(), card_info["plural"]))
        singular = list(map(lambda x: x.capitalize(), card_info["singular"]))
        synonyms = list(map(lambda x: x.capitalize(), card_info["synonyms"]))
        sentence = card_info["sentence"]
        partial_sentence = sentence.replace(word, "[...]")

        audio = self.__eleven_labs_client.text_to_speech.convert(
            text=sentence,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        # Assuming `audio` is a generator:
        audio_bytes = b''.join(audio)

        # Now you can write the bytes to a file
        with open("uploads/output_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_bytes)

        new_dict = {
            "word": word,
            "plural": plural,
            "singular": singular,
            "synonyms": synonyms,
            "sentence": sentence,
            "partial_sentence": partial_sentence
        }
        print("🚀 Dict: ", new_dict)

    def process_row(self, row: Row) -> CardResponse:
        completion = self.__open_ai_client.beta.chat.completions.parse(
            model=self.__open_ai_env.model,
            messages=[
                {"role": "system", "content": "You are a polyglot expert with over 10 years of experience"},
                {"role": "user", "content": f"please look for the definition of the word: {row["word"]} in the {row["language"]} language"}
            ],
            response_format=CardResponse
        )
        print(completion.choices[0].message.parsed)
        return completion.choices[0].message.parsed

    def process_csv(self, file_name: str):
        # df = read_csv(file_name, delimiter=",")

        words_data = [
            {
                'word': 'hello',
                'definition': 'A greeting or expression of goodwill used when meeting someone, answering the phone, or initiating a conversation.',
                'plural': [],
                'singular': ['hello'],
                'synonyms': ['hi', 'greetings', 'salutation'],
                'sentence': "When answering the phone, she always starts with a cheerful 'hello'."
            },
            {
                'word': 'salut',
                'definition': "Salut est une interjection française utilisée pour saluer quelqu'un. Elle peut également être employée comme un toast lors de la consommation de boissons.",
                'plural': ['saluts'],
                'singular': ['salut'],
                'synonyms': ['bonjour', 'salutation'],
                'sentence': 'Je lui ai dit salut en entrant dans la pièce.'
            },
            {
                'word': 'calcio',
                'definition': 'Sport di squadra giocato tra due squadre di undici giocatori su un campo di gioco rettangolare, in cui i giocatori tentano di segnare gol calciando una palla in rete.',
                'plural': ['calci', 'calcio'],
                'singular': ['calcio'],
                'synonyms': ['calcio a 11', 'calcio moderno'],
                'sentence': 'Il calcio è lo sport più popolare in Italia e in molti altri paesi.'
            }
        ]

        for data in words_data:
            self.process_card(card_info=data)

        # for _, row in df.iterrows():
        #     self.process_row(row.to_dict())