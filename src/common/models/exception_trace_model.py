from pydantic import BaseModel


class ExceptionTrace(BaseModel):
    filename: str
    line: str
    function: str
    message: str
