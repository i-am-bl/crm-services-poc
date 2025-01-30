from ..constants.messages import NUMBER_EXISTS, NUMBER_NOT_EXIST
from .crm_exceptions import CRMExceptions


class NumbersNotExist(CRMExceptions):
    """
    Custom exception raised when a specific number does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `NUMBER_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access or perform an operation on a number that does not exist.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of NUMBER_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = NUMBER_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class NumberExists(CRMExceptions):
    """
    Custom exception raised when a specific number already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `NUMBER_EXISTS`. This exception is typically raised
    when an attempt is made to create or register a number that already exists in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of NUMBER_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = NUMBER_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
