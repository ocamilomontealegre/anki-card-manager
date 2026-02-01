from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from common.env.env_config import EnvVariables
from common.lib.ai_client.ai_client_adapter import AiClientAdapter

T = TypeVar("T", bound=BaseModel)


class OpenAiClientAdapter(AiClientAdapter):
    def __init__(self):
        self.__env = EnvVariables.get()
        self.__ai_client = OpenAI(api_key=self.__env.ai.key)

    def get_structured_response(self, *, prompt: str, response_interface: type[T]) -> T:
        completion = self.__ai_client.beta.chat.completions.parse(
            model=self.__env.ai.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a polyglot linguist with over 10 years of experience in semantics, lexicography, and language education. "
                        "You specialize in identifying the most common and natural usages of words across different languages, providing accurate and culturally aware definitions and examples."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format=response_interface,
        )
        data = completion.choices[0].message.parsed

        if data is None:
            raise ValueError("No parsed response returned by OpenAI")

        return data
