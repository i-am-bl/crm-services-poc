from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import APIRouter, Depends, FastAPI, Response, routing
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from ..exceptions import SysUserNotExist, UnhandledException
from ..exceptions.crm_exceptions import CRMExceptions
from ..utilities.logger import logger

"""
This module contains functions for dynamically handling the registration of exception handlers and routers in FastAPI applications.

- `create_exception_handler`: Creates custom exception handlers for structured JSON responses.
- `handle_exceptions`: A decorator that catches specified exceptions and raises an `UnhandledException` for any unhandled cases.
- `handle_exception_registration`: Registers exception handlers dynamically based on provided configurations.
- `handle_router_registration`: Registers routers with FastAPI dynamically, including configuration such as prefixes, tags, and response settings.
"""


def create_exception_handler(
    status_code: int,
    error_code: str,
    message: Any,
) -> Callable[[Request, Exception], JSONResponse]:
    """
    Creates a custom exception handler for a given exception.

    This function returns an exception handler for a specific exception type
    that can be used by FastAPI to return a structured JSON response when the
    exception is raised. The response includes a status code, an error code, and
    a message.

    :param status_code: The HTTP status code to return in the response.
    :param error_code: A custom error code to include in the response.
    :param message: A message that describes the error. Can be a string or any type.
    :return: A callable function that handles the exception and returns a JSON response.
    """

    async def exception_handler(request: Request, exec: CRMExceptions):
        return JSONResponse(
            status_code=status_code,
            content={"error_code": error_code, "message": message},
        )

    return exception_handler


def handle_exceptions(exception_classes: List[Type[Exception]]):
    """
    Decorator to handle multiple exceptions raised by a function.

    This decorator is used to wrap a function, intercepting any exceptions
    that match the types provided in the `exception_classes` list. It also
    catches `SysUserNotExist` and any general `Exception`, raising an
    `UnhandledException` for any unhandled cases.

    :param exception_classes: A list of exception types to catch and re-raise.
    :return: A decorator that wraps a function with exception handling logic.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except tuple(exception_classes):
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
    Registers exception handlers dynamically with FastAPI.

    This function orchestrates the process of registering exception handlers for
    various custom exception classes in FastAPI, using the handler configurations
    provided in the `handlers` argument. Each handler will be associated with a
    specific exception class, error code, status code, and message.

    :param app: The FastAPI application instance to register the handlers with.
    :param handlers: A dictionary where keys are handler names, and values are lists
                     of dictionaries that define exception handler details.
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
    Registers routers dynamically with FastAPI.

    This function orchestrates the registration of routers, along with associated
    configuration such as prefix, tags, and response settings. The routers and
    their configurations are passed as a dictionary in the `routers` argument.

    :param app: The FastAPI application instance to register the routers with.
    :param routers: A dictionary where keys are router names, and values are lists
                    of dictionaries that define router registration details.
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
        Registers a router with FastAPI.

        This method registers a given router along with configuration options like
        prefix, tags, and response settings. It allows for more modular, dynamic
        registration of routes.

        :param router: The APIRouter instance to register with FastAPI.
        :param prefix: The prefix to prepend to all route paths in the router.
        :param tags: A list of tags to associate with all routes in the router.
        :param dependencies: Dependencies to include in the router's routes.
        :param responses: Custom responses for specific HTTP status codes.
        :param deprecated: Whether the router is deprecated.
        :param include_in_schema: Whether to include the router in the OpenAPI schema.
        :param default_response_class: The default response class for the router.
        :param callbacks: Callback functions to run during router setup.
        :param generate_unique_id_function: Function to generate unique route IDs.
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
