from sys import exit
from uvicorn import run
from debugpy import listen, wait_for_client
from app.builders.app_builder import AppBuilder
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables

logger = AppLogger()
env_variables = get_env_variables()
app = (
    AppBuilder()
    .set_open_api()
    .set_http_logging_middleware()
    .set_exception_handlers()
    .set_router()
    .build()
)

if __name__ == "__main__":
    # listen(("localhost", 5678))
    # print("Waiting for debugger to attach...")

    # wait_for_client()
    # print("Debugger attached, continuing execution")

    try:
        run(
            "main:app",
            host=env_variables.app.host,
            port=env_variables.app.port,
            reload=True,
            log_level="debug",
        )
    except KeyboardInterrupt:
        print("Server interrupted. Shutting down gracefully...")
        exit(0)
