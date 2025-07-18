from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from common.loggers.app_logger import AppLogger
from common.env.app_env_config import AppEnvVariables
from common.env.anki_env_config import AnkiEnvVariables
from common.env.google_env_config import GoogleEnvVariables
from common.env.open_ai_env_config import OpenAIEnvVariables
from common.env.open_api_env_config import OpenAPIEnvVariables
from common.env.pg_env_config import PgEnvVariables
from common.env.redis_env_config import RedisEnvVariables
from common.env.debuggy_env_config import DebuggyEnvVariables
from common.env.actions_env_config import ActionsEnvVariables

logger = AppLogger()


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_"
    )

    actions: ActionsEnvVariables
    anki: AnkiEnvVariables
    app: AppEnvVariables
    debuggy: DebuggyEnvVariables
    google: GoogleEnvVariables
    openai: OpenAIEnvVariables
    openapi: OpenAPIEnvVariables
    pg: PgEnvVariables
    redis: RedisEnvVariables


class EnvVariables:
    @staticmethod
    def get() -> EnvConfig:
        try:
            env = EnvConfig()  # type: ignore
            return env
        except ValidationError as e:
            logger.error(
                f"{e}",
                file=EnvVariables.__name__,
                method=EnvVariables.get.__name__,
            )
        raise


if __name__ == "__main__":
    env_vars = EnvVariables.get()
    if env_vars:
        logger.info(f"Loaded env vars: {env_vars}", file=EnvVariables.__name__)
    else:
        logger.error(
            "Failed to load environment variables.", file=EnvVariables.__name__
        )
