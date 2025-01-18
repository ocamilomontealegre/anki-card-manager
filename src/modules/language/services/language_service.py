from injector import inject
from pandas import read_csv
from pyee import EventEmitter
from openai import OpenAI
from common.env.env_config import get_env_variables
from ..models.interfaces import CardResponse, Row


class LanguageService():
    @inject
    def __init__(self, event_emitter: EventEmitter) -> None:
        self.__env = get_env_variables().open_ai

        self.__event_emitter = event_emitter
        self.__open_ai_client = OpenAI(api_key=self.__env.key)

        self.__event_emitter.on("upload", self.process_csv)

    def process_card(self, card_info: CardResponse):
        word = card_info.word
        plural = list(map(lambda x: x.capitalize(), card_info.plural))
        singular = card_info.singular
        synonyms = card_info.synonyms
        sentence = card_info.sentence

    def process_row(self, row: Row) -> CardResponse:
        completion = self.__open_ai_client.beta.chat.completions.parse(
            model=self.__env.model,
            messages=[
                {"role": "system", "content": "You are a polyglot expert with over 10 years of experience"},
                {"role": "user", "content": f"please look for the definition of the word: {row["word"]}"}
            ],
            response_format=CardResponse
        )
        print(completion.choices[0].message.parsed)
        return completion.choices[0].message.parsed

    def process_csv(self, file_name: str):
        df = read_csv(file_name, delimiter=",")
        for _, row in df.iterrows():
            self.process_row(row.to_dict())
