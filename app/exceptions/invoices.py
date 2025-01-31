from ..constants.messages import INVOICE_EXISTS, INVOICE_NOT_EXIST
from .crm_exceptions import CRMExceptions


class InvoiceNotExist(CRMExceptions):
    """
    Custom exception raised when an invoice does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `INVOICE_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access or perform an operation on an invoice that does not exist.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of INVOICE_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = INVOICE_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class InvoiceExists(CRMExceptions):
    """
    Custom exception raised when an invoice already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `INVOICE_EXISTS`. This exception is typically raised
    when an attempt is made to create or register an invoice that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of INVOICE_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = INVOICE_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
