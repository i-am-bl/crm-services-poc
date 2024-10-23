from ..constants.messages import INVALID_CREDENTIALS
from .crm_exceptions import CRMExceptions


class InvalidCredentials(CRMExceptions):
    def __init__(
        self, message: str = INVALID_CREDENTIALS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
