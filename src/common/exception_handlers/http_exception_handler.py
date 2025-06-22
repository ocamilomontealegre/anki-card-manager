from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from common.loggers.app_logger import AppLogger
from common.utils import ExceptionUtils
from common.models import HTTPResponse
from common.constants import STATUS_MESSAGES


class HTTPExceptionHandler:
    @staticmethod
    async def handle_exception(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        logger = AppLogger(label=HTTPExceptionHandler.__name__)

        exception_details = ExceptionUtils.extract_details(exc)
        message = STATUS_MESSAGES.get(exc.status_code)

        response = HTTPResponse(
            status=exc.status_code,
            success=False,
            message=exc.detail if exc.detail else (message or ""),
        )

        logger.error(
            f"[INCOMING REQUEST] METHOD: {request.method} | URL: {request.url.path} | HEADERS: {request.headers} "
            f"[OUTGOING RESPONSE] STATUS: {response.status} | RESPONSE_BODY: {response} | EXCEPTION: {exception_details}"
        )

        return JSONResponse(
            content=response.model_dump(), status_code=exc.status_code
        )
