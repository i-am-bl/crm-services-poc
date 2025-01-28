from typing import TypedDict

from ..orchestrators.account_products import AccountProductsReadOrch
from .services import container as services_container


class OrchestratorsContainer(TypedDict):
    account_products_read_orch: AccountProductsReadOrch


container: OrchestratorsContainer = {
    "account_products_read_orch": lambda: AccountProductsReadOrch(
        account_products_read_srvc=services_container["account_products_read"],
        products_read_srvc=services_container["products_read"],
    )
}
