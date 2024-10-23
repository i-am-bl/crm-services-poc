from ..constants.messages import INVOICE_EXISTS, INVOICE_NOT_EXIST
from .crm_exceptions import CRMExceptions


class InvoiceNotExist(CRMExceptions):
    def __init__(
        self, message: str = INVOICE_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class InvoiceExists(CRMExceptions):
    def __init__(self, message: str = INVOICE_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
