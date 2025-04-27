from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from common.loggers.logger import AppLogger
from common.env.app_env_config import AppEnvVariables
from common.env.anki_env_config import AnkiEnvVariables
from common.env.giphy_env_config import GiphyEnvVariables
from common.env.google_env_config import GoogleEnvVariables
from common.env.open_ai_env_config import OpenAIEnvVariables
from common.env.open_api_env_config import OpenAPIEnvVariables
from common.env.pg_env_config import PgEnvVariables
from common.env.redis_env_config import RedisEnvVariables
from common.env.unplash_env_config import UnplashEnvVariables

logger = AppLogger(label="Env")


class EnvVariables(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_"
    )

    anki: AnkiEnvVariables
    app: AppEnvVariables
    giphy: GiphyEnvVariables
    google: GoogleEnvVariables
    openai: OpenAIEnvVariables
    openapi: OpenAPIEnvVariables
    pg: PgEnvVariables
    redis: RedisEnvVariables
    unplash: UnplashEnvVariables


def get_env_variables() -> EnvVariables:
    try:
        env = EnvVariables()
        return env
    except ValidationError as e:
        logger.error(f"{e}")


if __name__ == "__main__":
    env_vars = get_env_variables()
    if env_vars:
        logger.info(f"Loaded env vars: {env_vars}")
    else:
        logger.error("Failed to load environment variables.")
