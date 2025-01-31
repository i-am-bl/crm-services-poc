from typing import TypedDict

from .services import container as services_container
from ..services import token as token_srvcs


class AuthContainer(TypedDict):
    """
    A container that holds service dependencies related to authentication.

    This container is used to manage and inject dependencies for authentication services.
    """

    token_srvc: token_srvcs.TokenSrvc


# Container initialization for authentication services.
container: AuthContainer = {
    "token_srvc": lambda: token_srvcs.TokenSrvc(
        sys_user_read_srvc=services_container["sys_users_read"]()
    )
}
