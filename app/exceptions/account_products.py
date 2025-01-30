from ..constants.messages import ACCCOUNT_PRODUCTS_EXISTS, ACCCOUNT_PRODUCTS_NOT_EXIST
from .crm_exceptions import CRMExceptions


class AccProductstNotExist(CRMExceptions):
    """
    Custom exception raised when an account product does not exist.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ACCCOUNT_PRODUCTS_NOT_EXIST`. This exception can be
    raised when trying to access or modify an account product that is not found in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ACCCOUNT_PRODUCTS_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = ACCCOUNT_PRODUCTS_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AccProductsExists(CRMExceptions):
    """
    Custom exception raised when an account product already exists.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ACCCOUNT_PRODUCTS_EXISTS`. This exception can be
    raised when trying to create or add an account product that already exists in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ACCCOUNT_PRODUCTS_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = ACCCOUNT_PRODUCTS_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
