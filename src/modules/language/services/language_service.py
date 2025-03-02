import requests
from injector import inject
from pandas import read_csv
from pyee import EventEmitter
from openai import OpenAI
from sqlalchemy.orm import Session
from elevenlabs.client import ElevenLabs
from common.database.strategies.database_strategy import DatabaseStrategy
from common.env.env_config import get_env_variables
from ..models.entities.word_entity import Word
from ..models.interfaces import CardResponse, Row


class LanguageService():
    @inject
    def __init__(self, db: DatabaseStrategy, event_emitter: EventEmitter) -> None:
        self.__env = get_env_variables()

        self.__session = db.create_session()

        self.__event_emitter = event_emitter
        self.__open_ai_client = OpenAI(api_key=self.__env.openai.key)
        self.__eleven_labs_client = ElevenLabs(api_key=self.__env.elevenlabs.key)

        self.__giphy_base_url = "https://api.giphy.com/v1/gifs/"
        self.__unplash_base_url = "https://api.unsplash.com/"

        self.__event_emitter.on("upload", self.process_csv)

    def process_card(self, card_info: CardResponse):
        word = card_info["word"]
        plural = list(map(lambda x: x.capitalize(), card_info["plural"]))
        singular = list(map(lambda x: x.capitalize(), card_info["singular"]))
        synonyms = list(map(lambda x: x.capitalize(), card_info["synonyms"]))
        sentence = card_info["sentence"]
        partial_sentence = sentence.replace(word, "[...]")

        url = f'{self.__giphy_base_url}search?q={word}&api_key={self.__env.giphy.key}&limit=1'
        response = requests.get(url)
        image: str = ''
        if response.status_code == 200:
            image = response.json()['data'][0]['url']

        url2 = f"{self.__unplash_base_url}search/photos?query={word}&client_id={self.__env.unplash.key}&per_page=1"
        response2 = requests.get(url2)
        image2: str = ''
        if response2.status_code == 200:
            image2 = response2.json()['results'][0]['urls']['regular']

        # audio = self.__eleven_labs_client.text_to_speech.convert(
        #     text=sentence,
        #     voice_id="JBFqnCBsd6RMkjVDRZzb",
        #     model_id="eleven_multilingual_v2",
        #     output_format="mp3_44100_128",
        # )
        # # Assuming `audio` is a generator:
        # audio_bytes = b''.join(audio)
        # audio_path = f"{self.__anki_env.audios}/{word}.mp3"

        # # Now you can write the bytes to a file
        # with open(audio_path, "wb") as audio_file:
        #     audio_file.write(audio_bytes)

        plural_audio_path = ''
        # if len(plural) > 0:
        #     plural_audio = self.__eleven_labs_client.text_to_speech.convert(
        #         text=', '.join(plural),
        #         voice_id="JBFqnCBsd6RMkjVDRZzb",
        #         model_id="eleven_multilingual_v2",
        #         output_format="mp3_44100_128",
        #     )
        #     plural_audio_bytes = b''.join(plural_audio)
        #     plural_audio_path = f"{self.__anki_env.audios}/plural_{word}.mp3"
        #     with open(plural_audio_path, "wb") as audio_file:
        #         audio_file.write(plural_audio_bytes)
            
        singular_audio_path = ''
        # if len(singular) > 0:
        #     singular_audio = self.__eleven_labs_client.text_to_speech.conver(
        #         text=plural,
        #         voice_id="JBFqnCBsd6RMkjVDRZzb",
        #         model_id="eleven_multilingual_v2",
        #         output_format="mp3_44100_128",
        #     )

        new_word = Word(
            word=f"{', '.join(singular)}, {', '.join(plural)}",
            definition=card_info["definition"],
            sentence=sentence,
            sentence_audio="", 
            partial_sentence=partial_sentence,
            singular=singular,
            singular_audio=singular_audio_path,
            plural=plural,
            plural_audio=plural_audio_path,
            synonyms=synonyms,
            image=image,
            image2=image2
        )
        self.__session.add(new_word)
        self.__session.commit()
        
        print("🚀 Dict: ", new_word)

    def process_row(self, row: Row) -> CardResponse:
        completion = self.__open_ai_client.beta.chat.completions.parse(
            model=self.__env.openai.model,
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