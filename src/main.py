from uvicorn import run
from app.builders.app_builder import AppBuilder
from common.env.env_config import get_env_variables

app_env_variables = get_env_variables().app
app = (
    AppBuilder()
    .set_open_api()
    .set_http_logging_middleware()
    .set_exception_handlers()
    .set_router()
    .build()
)

if __name__ == "__main__":
    run(
        "main:app",
        host=app_env_variables.host,
        port=app_env_variables.port,
        reload=True,
        log_level="debug",
    )
