from ..constants.messages import PRODUCT_LIST_EXISTS, PRODUCT_LIST_ITEM_EXISTS
from .crm_exceptions import CRMExceptions


class ProductListItemNotExist(CRMExceptions):
    """
    Custom exception raised when a product list item does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `PRODUCT_LIST_EXISTS`. This exception is typically raised
    when an attempt is made to access, update, or perform an operation on a product list item
    that cannot be found in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of PRODUCT_LIST_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = PRODUCT_LIST_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class ProductListItemExists(CRMExceptions):
    """
    Custom exception raised when a product list item already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `PRODUCT_LIST_ITEM_EXISTS`. This exception is typically raised
    when an attempt is made to create or register a product list item that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of PRODUCT_LIST_ITEM_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = PRODUCT_LIST_ITEM_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
