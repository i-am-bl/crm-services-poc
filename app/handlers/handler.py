from typing import Any, Callable

from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.exceptions.crm_exceptions import CRMExceptions


def create_exception_handler(
    status_code: int,
    error_code: str,
    message: Any,
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exec: CRMExceptions):
        return JSONResponse(
            status_code=status_code,
            content={"error_code": error_code, "message": message},
        )

    return exception_handler
