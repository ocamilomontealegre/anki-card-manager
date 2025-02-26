from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from common.env.app_env_config import AppEnvVariables
from common.env.eleven_labs_env_config import ElevenLabsEnvVariables
from common.env.anki_env_config import AnkiEnvVariables
from common.env.giphy_env_config import GiphyEnvVariables
from common.env.open_ai_env_config import OpenAIEnvVariables
from common.env.open_api_env_config import OpenAPIEnvVariables
from common.env.unplash_env_config import UnplashEnvVariables
from common.env.pg_env_config import PgEnvVariables


class EnvVariables(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_"
    )

    anki: AnkiEnvVariables
    app: AppEnvVariables
    elevenlabs: ElevenLabsEnvVariables
    giphy: GiphyEnvVariables
    openai: OpenAIEnvVariables
    openapi: OpenAPIEnvVariables
    pg: PgEnvVariables
    unplash: UnplashEnvVariables


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
