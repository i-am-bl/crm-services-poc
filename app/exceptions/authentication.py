from .crm_exceptions import CRMExceptions


class InvalidCredentials(CRMExceptions):
    """Exception raised for invalid credentials.

    Invalid username or password is invalid.
    """

    pass
