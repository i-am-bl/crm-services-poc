from ..constants.messages import WEBSITE_EXISTS, WEBSITE_NOT_EXIST
from .crm_exceptions import CRMExceptions


class WebsitesNotExist(CRMExceptions):
    """
    Custom exception raised when a website does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `WEBSITE_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access, update, or perform an operation on a website
    that cannot be found in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of WEBSITE_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = WEBSITE_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class WebsitesExists(CRMExceptions):
    """
    Custom exception raised when a website already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `WEBSITE_EXISTS`. This exception is typically raised
    when an attempt is made to create or register a website that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of WEBSITE_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = WEBSITE_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
