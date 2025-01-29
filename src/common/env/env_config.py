from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from common.env.app_env_config import AppEnvVariables
from common.env.eleven_labs_env_config import ElevenLabsEnvVariables
from common.env.open_ai_env_config import OpenAIEnvVariables
from common.env.open_api_env_config import OpenAPIEnvVariables


class EnvVariables(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_"
    )

    app: AppEnvVariables
    elevenlabs: ElevenLabsEnvVariables
    openai: OpenAIEnvVariables
    openapi: OpenAPIEnvVariables


def get_env_variables() -> EnvVariables:
    try:
        env = EnvVariables()
        return env
    except ValidationError as e:
        print(f"Error validating env variables {e}")


if __name__ == "__main__":
    env_vars = get_env_variables()
    if env_vars:
        print(f"Loaded env vars: {env_vars}")
    else:
        print("Failed to load environment variables.")
