from typing import Optional
from ..utilities.logger import logger


class CRMExceptions(Exception):
    """
    Base class for all custom exceptions in the CRM application.

    This exception class inherits from Python's built-in Exception class and serves as the base
    for creating custom exceptions in the CRM system. It provides the functionality to log
    the exception message whenever an exception is raised.

    :param message: The error message to display when the exception is raised.
                    Defaults to None, meaning no message is provided unless explicitly specified.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: Optional[str] = None, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
        if message:
            self.log_exception(message=message)

    def log_exception(self, message: str):
        """Logs the exception message at the warning level with the class name."""
        logger.warning(f"{self.__class__.__name__}: {message}")
