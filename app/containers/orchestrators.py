from typing import TypedDict

from ..orchestrators.account_lists import AccountListsReadOrch
from ..orchestrators.account_products import AccountProductsReadOrch
from ..orchestrators.entities import EntitiesCreateOrch
from ..orchestrators.entity_accounts import (
    EntityAccountsReadOrch,
    EntityAccountsCreateOrch,
)
from .services import container as services_container


class OrchestratorsContainer(TypedDict):
    accounts_lists_read_orch: AccountListsReadOrch
    account_products_read_orch: AccountProductsReadOrch
    entities_create_orch: EntitiesCreateOrch
    entity_accounts_read_orch: EntityAccountsReadOrch
    entity_accounts_create_orch: EntityAccountsCreateOrch


container: OrchestratorsContainer = {
    "accounts_lists_read_orch": lambda: AccountListsReadOrch(
        account_lists_read_srvc=services_container["account_lists_read"],
        product_lists_read_srvc=services_container["product_lists_read"],
    ),
    "account_products_read_orch": lambda: AccountProductsReadOrch(
        account_products_read_srvc=services_container["account_products_read"],
        products_read_srvc=services_container["products_read"],
    ),
    "entities_create_orch": lambda: EntitiesCreateOrch(
        entities_create_srvc=services_container["entities_create"],
        individuals_create_srvc=services_container["individuals_create"],
        non_individuals_create_srvc=services_container["non_individuals_create"],
    ),
    "entity_accounts_read_orch": lambda: EntityAccountsReadOrch(
        accounts_read_srvc=services_container["accounts_read"],
        entities_read_srvc=services_container["entities_read"],
        entity_accounts_read_srvc=services_container["entity_accounts_read"],
    ),
    "entity_accounts_create_orch": lambda: EntityAccountsCreateOrch(
        accounts_create_srvc=services_container["accounts_create"],
        entity_accounts_create_srvc=services_container["entity_accounts_create"],
    ),
}
