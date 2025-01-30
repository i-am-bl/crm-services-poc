from ..constants.messages import ORDER_EXISTS, ORDER_NOT_EXIST
from .crm_exceptions import CRMExceptions


class OrderNotExist(CRMExceptions):
    """
    Custom exception raised when an order does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ORDER_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access, update, or perform an operation on an order that
    cannot be found in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ORDER_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = ORDER_NOT_EXIST, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


class OrderExists(CRMExceptions):
    """
    Custom exception raised when an order already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ORDER_EXISTS`. This exception is typically raised
    when an attempt is made to create or register an order that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ORDER_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = ORDER_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
