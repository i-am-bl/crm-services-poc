from typing import TypedDict

from ..orchestrators.account_lists import AccountListsReadOrch
from ..orchestrators.account_products import AccountProductsReadOrch
from ..orchestrators.entity_accounts import EntityAccountsReadOrch
from .services import container as services_container


class OrchestratorsContainer(TypedDict):
    accounts_lists_read_orch: AccountListsReadOrch
    account_products_read_orch: AccountProductsReadOrch
    entity_accounts_read_orch: EntityAccountsReadOrch


container: OrchestratorsContainer = {
    "accounts_lists_read_orch": lambda: AccountListsReadOrch(),
    "account_products_read_orch": lambda: AccountProductsReadOrch(
        account_products_read_srvc=services_container["account_products_read"],
        products_read_srvc=services_container["products_read"],
    ),
    "entity_accounts_read_orch": lambda: EntityAccountsReadOrch(
        accounts_read_srvc=services_container["accounts_read"],
        entities_read_srvc=services_container["entities_read"],
        entity_accounts_read_srvc=services_container["entity_accounts_read"],
    ),
}
