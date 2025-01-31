from ..constants.messages import EMAIL_EXISTS, EMAIL_NOT_EXIST
from .crm_exceptions import CRMExceptions


class EmailNotExist(CRMExceptions):
    """
    Custom exception raised when an email does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `EMAIL_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access or update a non-existing email record in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of EMAIL_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = EMAIL_NOT_EXIST, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


class EmailExists(CRMExceptions):
    """
    Custom exception raised when an email already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `EMAIL_EXISTS`. This exception is typically raised
    when an attempt is made to create or register an email that already exists in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of EMAIL_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = EMAIL_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
