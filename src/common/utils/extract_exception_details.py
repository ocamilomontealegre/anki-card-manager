from traceback import TracebackException
from typing import Union
from fastapi import HTTPException
from common.models import ExceptionTrace


union_exception = Union[HTTPException, Exception]


def extract_exception_details(exc: union_exception) -> ExceptionTrace:
    tb = TracebackException.from_exception(exc)

    exception_message = str(exc)

    if not tb.stack:
        return ExceptionTrace(
            filename="N/A",
            line="N/A",
            function="N/A",
            message=exception_message,
        )

    last_trace = tb.stack[-1]
    return ExceptionTrace(
        filename=last_trace.filename,
        line=f"{last_trace.line}, {last_trace.lineno}",
        function=last_trace.name,
        message=exception_message,
    )
