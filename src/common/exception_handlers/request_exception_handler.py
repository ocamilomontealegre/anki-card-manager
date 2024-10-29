from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from common.loggers.logger import AppLogger
from common.utils import extract_exception_details
from common.models import HTTPResponse


class RequestValidationExceptionHandler:
    @staticmethod
    async def handle_exception(
        request: Request, exc: RequestValidationError
    ) -> HTTPResponse:
        logger = AppLogger(label=RequestValidationExceptionHandler.__name__)

        exception_details = extract_exception_details(exc)

        response = HTTPResponse(status=400, success=False, message=exc.errors)

        logger.error(
            f"[INCOMING REQUEST] METHOD: {request.method} | URL: {request.url.path} | HEADERS: {request.headers} "
            f"[OUTGOING RESPONSE] STATUS: {response.status} | RESPONSE_BODY: {response} | EXCEPTION: {exception_details}",
        )

        return JSONResponse(content=response.dict(), status_code=400)
