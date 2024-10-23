from ..constants.messages import INVOICE_ITEM_EXISTS, INVOICE_ITEM_NOT_EXIST
from .crm_exceptions import CRMExceptions


class InvoiceItemNotExist(CRMExceptions):
    def __init__(
        self, message: str = INVOICE_ITEM_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class InvoiceItemExists(CRMExceptions):
    def __init__(
        self, message: str = INVOICE_ITEM_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
