from injector import inject
from pandas import read_csv, Series
from pyee import EventEmitter
from openai import OpenAI
from common.env.env_config import get_env_variables


class LanguageService():
    @inject
    def __init__(self, event_emitter: EventEmitter, open_ai_client: OpenAI) -> None:
        self.__env_variables = get_env_variables().open_ai

        self.__event_emitter = event_emitter
        self.__open_ai_client = open_ai_client

        self.__event_emitter.on("upload", self.process_csv)

    def process_row(self, row: Series):
        completion = self.__open_ai_client.beta.chat.completions.parse(
            model=self.__env_variables.model,
            messages=[
                {"role": "system", "content": "You are a polyglot expert with over 10 years of experience"},
                {"role": "user", "content": f"please look for the definition of the the word ${}"}
            ]
        )

    def process_csv(self, file_name: str):
        df = read_csv(file_name, delimiter=";")
        for _, row in df.iterrows():
            print("row: ", row.to_dict())

    
