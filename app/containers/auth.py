from typing import TypedDict

from .services import container as services_container
from ..services import token as token_srvcs


class AuthContainer(TypedDict):
    token_srvc: token_srvcs.TokenSrvc


container: AuthContainer = {
    "token_srvc": lambda: token_srvcs.TokenSrvc(
        sys_user_read_srvc=services_container["sys_users_read"]
    )
}
