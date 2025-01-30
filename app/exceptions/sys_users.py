from ..constants.messages import SYS_USER_EXISTS, SYS_USER_NOT_EXIST
from .crm_exceptions import CRMExceptions


class SysUserNotExist(CRMExceptions):
    """
    Custom exception raised when a system user does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `SYS_USER_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access, update, or perform an operation on a system user
    that cannot be found in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of SYS_USER_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = SYS_USER_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class SysUserExists(CRMExceptions):
    """
    Custom exception raised when a system user already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `SYS_USER_EXISTS`. This exception is typically raised
    when an attempt is made to create or register a system user that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of SYS_USER_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = SYS_USER_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
