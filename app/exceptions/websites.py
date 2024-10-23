from ..constants.messages import WEBSITE_EXISTS, WEBSITE_NOT_EXIST
from .crm_exceptions import CRMExceptions


class WebsitesNotExist(CRMExceptions):
    def __init__(
        self, message: str = WEBSITE_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class WebsitesExists(CRMExceptions):
    def __init__(self, message: str = WEBSITE_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
