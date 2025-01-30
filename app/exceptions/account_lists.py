from ..constants.messages import ACCCOUNT_LIST_EXISTS, ACCCOUNT_LIST_NOT_EXIST
from .crm_exceptions import CRMExceptions


class AccListNotExist(CRMExceptions):
    """
    Exception raised when an account list does not exist.

    This exception is typically raised when attempting to access or perform
    an operation on an account list that does not exist in the system.

    :param message: The error message to display, defaulting to the
                    ACCCOUNT_LIST_NOT_EXIST message.
    :param args: Additional positional arguments to pass to the base exception.
    :param kwargs: Additional keyword arguments to pass to the base exception.
    """

    def __init__(
        self, message: str = ACCCOUNT_LIST_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AccListExists(CRMExceptions):
    """
    Exception raised when an account list already exists.

    This exception is typically raised when attempting to create an account
    list that already exists in the system.

    :param message: The error message to display, defaulting to the
                    ACCCOUNT_LIST_EXISTS message.
    :param args: Additional positional arguments to pass to the base exception.
    :param kwargs: Additional keyword arguments to pass to the base exception.
    """

    def __init__(
        self, message: str = ACCCOUNT_LIST_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
