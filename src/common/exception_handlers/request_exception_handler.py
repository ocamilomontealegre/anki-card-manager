from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from common.loggers.app_logger import AppLogger
from common.utils import extract_exception_details
from common.models import HTTPResponse


class RequestValidationExceptionHandler:
    @staticmethod
    async def handle_exception(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        file = RequestValidationExceptionHandler.__name__

        logger = AppLogger()

        exception_details = extract_exception_details(exc)

        response = HTTPResponse(status=400, success=False, message=str(exc.errors))

        logger.error(
            f"[INCOMING REQUEST] METHOD: {request.method} | URL: {request.url.path} | HEADERS: {request.headers} "
            f"[OUTGOING RESPONSE] STATUS: {response.status} | RESPONSE_BODY: {response} | EXCEPTION: {exception_details}",
            file=file,
            method=RequestValidationExceptionHandler.handle_exception.__name__,
        )

        return JSONResponse(content=response.model_dump(), status_code=400)
