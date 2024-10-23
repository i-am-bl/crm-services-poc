from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import APIRouter, Depends, FastAPI, Response, routing
from fastapi.datastructures import Default
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.utils import generate_unique_id

from ..exceptions import SysUserNotExist, UnhandledException
from ..exceptions.crm_exceptions import CRMExceptions
from ..utilities.logger import logger


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
            except SysUserNotExist:
                raise
            except Exception as e:
                raise UnhandledException

        return wrapper

    return decorator


def handle_exeception_registration(
    app: FastAPI, handlers: Dict[str, List[Dict[str, Any]]]
) -> None:
    """
    Factory method for orchestrating the process or registering exception handlers with FastAPI.

    """

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
            allow_registration = value["allow_registration"]
            class_name = exec.__name__
            if allow_registration:
                logger.info("registered handler: %s", class_name)
                register_exception_handlers(
                    exec=exec,
                    error_code=error_code,
                    status_code=status_code,
                    message=message,
                )


def handle_router_registration(
    app: FastAPI,
    routers: Dict[str, List[Dict[str, Any]]],
) -> None:
    """
    Factory method for orchestrating the process or registering routers with FastAPI.

    """

    def register_routers(
        router: APIRouter,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = False,
        include_in_schema: Optional[bool] = True,
        default_response_class: Type[Response] = JSONResponse,
        callbacks: Optional[List[str]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = None,
    ):
        """
        Dynamically registers routers.

        Allows for router abstraction from main.py for more modular code.
        """
        app.include_router(
            router=router,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses=responses,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            default_response_class=default_response_class,
            callbacks=callbacks,
            generate_unique_id_function=generate_unique_id_function,
        )

    for values in routers.values():
        for value in values:
            name = value["name"]
            router = value["router"]
            prefix = value["prefix"]
            tags = value["tags"]
            dependencies = value["dependencies"]
            responses = value["responses"]
            deprecated = value["deprecated"]
            include_in_schema = value["include_in_schema"]
            default_response_class = value["default_response_class"]
            callbacks = value["callbacks"]
            generate_unique_id = value["generate_unique_id"]
            allow_registration = value["allow_registration"]

            if allow_registration:
                route_info = [
                    f"{name}: {route.methods}: {route.path}" for route in router.routes
                ]
                logger.info(f"registered router paths: \n%s", "\n".join(route_info))
                register_routers(
                    router=router,
                    prefix=prefix,
                    tags=tags,
                    dependencies=dependencies,
                    responses=responses,
                    deprecated=deprecated,
                    include_in_schema=include_in_schema,
                    default_response_class=default_response_class,
                    callbacks=callbacks,
                    generate_unique_id_function=generate_unique_id,
                )
