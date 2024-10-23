from ..constants.messages import SYS_USER_EXISTS, SYS_USER_NOT_EXIST
from .crm_exceptions import CRMExceptions


class SysUserNotExist(CRMExceptions):
    def __init__(
        self, message: str = SYS_USER_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class SysUserExists(CRMExceptions):
    def __init__(self, message: str = SYS_USER_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
