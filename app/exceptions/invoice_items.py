from ..constants.messages import INVOICE_ITEM_EXISTS, INVOICE_ITEM_NOT_EXIST
from .crm_exceptions import CRMExceptions


class InvoiceItemNotExist(CRMExceptions):
    """
    Custom exception raised when an invoice item does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `INVOICE_ITEM_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access or perform an operation on an invoice item that does not exist.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of INVOICE_ITEM_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = INVOICE_ITEM_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class InvoiceItemExists(CRMExceptions):
    """
    Custom exception raised when an invoice item already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `INVOICE_ITEM_EXISTS`. This exception is typically raised
    when an attempt is made to create or register an invoice item that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of INVOICE_ITEM_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = INVOICE_ITEM_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
