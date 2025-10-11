from sys import exit
from uvicorn import run
from debugpy import listen, wait_for_client
from app.builders.app_builder import AppBuilder
from common.loggers.app_logger import AppLogger
from common.env.env_config import EnvVariables

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
    if env_variables.debuggy.active:
        listen(("localhost", 5678))
        logger.debug(
            "Waiting for debugger to attach...",
            file=__file__,
        )

        wait_for_client()
        logger.debug("Debugger attached, continuing execution", file=__file__)

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
