from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from common.env.app_env_config import AppEnvVariables
from common.env.open_api_env_config import OpenAPIEnvVariables


class EnvVariables(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_"
    )

    app: AppEnvVariables
    open_api: OpenAPIEnvVariables


def get_env_variables() -> EnvVariables:
    try:
        return EnvVariables()
    except ValidationError as e:
        print(f"Error validating env variables {e}")


if __name__ == "__main__":
    env_vars = get_env_variables()
    if env_vars:
        print(f"Loaded env vars: {env_vars}")
    else:
        print("Failed to load environment variables.")
