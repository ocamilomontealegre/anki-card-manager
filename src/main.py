from sys import exit

from uvicorn import run

from app.builders.app_builder import AppBuilder
from common.env.env_config import EnvVariables
from common.loggers.app_logger import AppLogger

logger = AppLogger()
env_variables = EnvVariables.get()
app = (
    AppBuilder()
    .set_open_api()
    .set_http_logging_middleware()
    .set_exception_handlers()
    .set_router()
    .build()
)

if __name__ == "__main__":
    try:
        run(
            "main:app",
            host=env_variables.app.host,
            port=env_variables.app.port,
            reload=True,
            log_level="debug",
        )
    except KeyboardInterrupt:
        logger.debug("Server interrupted. Shutting down gracefully...", file=__file__)
        exit(0)
