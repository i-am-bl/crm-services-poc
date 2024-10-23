from ..constants.messages import INDIVIDUAL_EXISTS, INDIVIDUAL_NOT_EXIST
from .crm_exceptions import CRMExceptions


class IndividualNotExist(CRMExceptions):
    def __init__(
        self, message: str = INDIVIDUAL_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class IndividualExists(CRMExceptions):
    def __init__(
        self, message: str = INDIVIDUAL_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
