from functools import wraps
from typing import Any, Callable, Dict, List, Type

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from ..exceptions import UnhandledException
from ..exceptions.crm_exceptions import CRMExceptions


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


def handle_exceptions(exception_classe: List[Type[Exception]]):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except tuple(exception_classe):
                raise
            except Exception as e:
                raise UnhandledException

        return wrapper

    return decorator


def handle_exeception_registration(
    app: FastAPI, handlers: Dict[str, List[Dict[str, Any]]]
) -> None:
    def register_exception_handlers(
        exec: Type[CRMExceptions],
        error_code: str,
        status_code: int,
        message: str,
    ):
        app.add_exception_handler(
            exc_class_or_status_code=exec,
            handler=create_exception_handler(
                status_code=status_code, error_code=error_code, message=message
            ),
        )

    for values in handlers.values():
        for value in values:
            exec = value["class"]
            error_code = value["error_code"]
            status_code = value["status_code"]
            message = value["message"]

            register_exception_handlers(
                exec=exec,
                error_code=error_code,
                status_code=status_code,
                message=message,
            )
