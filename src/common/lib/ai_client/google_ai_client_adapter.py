from typing import TypeVar

from google import genai
from pydantic import BaseModel

from common.env.env_config import EnvVariables
from common.lib.ai_client.ai_client_adapter import AiClientAdapter

T = TypeVar("T", bound=BaseModel)


class GoogleClientAdapter(AiClientAdapter):
    def __init__(self):
        self.__env = EnvVariables().get()
        self.__ai_client = genai.Client(api_key=self.__env.ai.key)

    def get_structured_response(
        self, *, messages: list[dict[str, str]], response_interface: type[T]
    ) -> T:
        prompt = "\n".join(
            f"{message['role'].upper()}: {message['content']}" for message in messages
        )

        response = self.__ai_client.models.generate_content(
            model=self.__env.ai.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": response_interface.model_json_schema(),
            },
        )

        if response.text is None:
            raise ValueError("No parsed response returned by Gemini")

        return response_interface.model_validate_json(response.text)
