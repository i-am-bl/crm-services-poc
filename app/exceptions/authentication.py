from ..constants.messages import INVALID_CREDENTIALS
from .crm_exceptions import CRMExceptions


class InvalidCredentials(CRMExceptions):
    """
    Custom exception raised when invalid credentials are provided.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `INVALID_CREDENTIALS`. This exception is typically raised
    during authentication when the provided credentials (e.g., username or password) do not
    match the records in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of INVALID_CREDENTIALS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = INVALID_CREDENTIALS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
