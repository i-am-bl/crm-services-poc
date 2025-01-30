from ..constants.messages import ACCCOUNT_CONTRACT_EXISTS, ACCCOUNT_CONTRACT_NOT_EXIST
from .crm_exceptions import CRMExceptions


class AccContractNotExist(CRMExceptions):
    """
    Exception raised when an account contract does not exist.

    This exception is typically raised when attempting to access or perform
    an operation on an account contract that does not exist in the system.

    :param message: The error message to display, defaulting to the
                    ACCCOUNT_CONTRACT_NOT_EXIST message.
    :param args: Additional positional arguments to pass to the base exception.
    :param kwargs: Additional keyword arguments to pass to the base exception.
    """

    def __init__(
        self, message: str = ACCCOUNT_CONTRACT_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AccContractExists(CRMExceptions):
    """
    Exception raised when an account contract already exists.

    This exception is typically raised when attempting to create an account
    contract that already exists in the system.

    :param message: The error message to display, defaulting to the
                    ACCCOUNT_CONTRACT_EXISTS message.
    :param args: Additional positional arguments to pass to the base exception.
    :param kwargs: Additional keyword arguments to pass to the base exception.
    """

    def __init__(
        self, message: str = ACCCOUNT_CONTRACT_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
