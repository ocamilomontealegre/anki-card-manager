from fastapi import Request
from fastapi.responses import JSONResponse
from common.loggers.logger import AppLogger
from common.utils import extract_exception_details
from common.models import HTTPResponse
from common.constants import STATUS_MESSAGES


class GeneralExceptionHandler:
    @staticmethod
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        logger = AppLogger(label=GeneralExceptionHandler.__name__)

        exception_details = extract_exception_details(exc)

        response = HTTPResponse(
            status=500,
            success=False,
            message=STATUS_MESSAGES.get(500),
        )

        logger.error(
            f"[INCOMING REQUEST] METHOD: {request.method} | URL: {request.url.path} | HEADERS: {request.headers} "
            f"[OUTGOING RESPONSE] STATUS: {response.status} | RESPONSE_BODY: {response} | EXCEPTION: {exception_details}",
        )

        return JSONResponse(content=response.dict(), status_code=500)
