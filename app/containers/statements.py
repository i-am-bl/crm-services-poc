from typing import TypedDict

from ..models.account_contracts import AccountContracts
from ..models.account_lists import AccountLists
from ..models.account_products import AccountProducts
from ..models.accounts import Accounts
from ..models.addresses import Addresses
from ..models.emails import Emails
from ..models.entity_accounts import EntityAccounts
from ..models.entities import Entities
from ..models.individuals import Individuals
from ..models.non_individuals import NonIndividuals
from ..models.individuals import Individuals
from ..models.invoice_items import InvoiceItems
from ..models.invoices import Invoices
from ..models.non_individuals import NonIndividuals
from ..models.numbers import Numbers
from ..models.order_items import OrderItems
from ..models.orders import Orders
from ..models.product_list_items import ProductListItems
from ..models.product_lists import ProductLists
from ..models.products import Products
from ..models.sys_users import SysUsers
from ..models.websites import Websites
from ..statements.account_contracts import AccountContractStms
from ..statements.account_lists import AccountListsStms
from ..statements.accounts_products import AccountProductsStms
from ..statements.accounts import AccountsStms
from ..statements.addresses import AddressesStms
from ..statements.emails import EmailsStms
from ..statements.entity_accounts import EntityAccountsStms
from ..statements.entities import EntitiesStms
from ..statements.individuals import IndividualsStms
from ..statements.invoice_items import InvoiceItemsStms
from ..statements.invoices import InvoicesStms
from ..statements.non_individuals import NonIndivididualsStms
from ..statements.numbers import NumbersStms
from ..statements.order_items import OrderItemsStms
from ..statements.orders import OrdersStms
from ..statements.product_list_items import ProductListItemsStms
from ..statements.product_lists import ProductListsStms
from ..statements.products import ProductsStms
from ..statements.sys_users import SysUsersStms
from ..statements.websites import WebsitesStms


class StatementsContainer(TypedDict):
    account_contracts_stms: AccountContractStms
    account_lists_stms: AccountListsStms
    account_products_stms: AccountProductsStms
    accounts_stms: AccountsStms
    addresses_stms: AddressesStms
    emails_stms: EmailsStms
    entity_accounts_stms: EntityAccountsStms
    entites_stms: EntitiesStms
    individuals_stms: IndividualsStms
    invoice_items_stms: InvoiceItemsStms
    invoice_stms: InvoicesStms
    non_individuals: NonIndivididualsStms
    numbers_stms: NumbersStms
    order_items_stms: OrderItemsStms
    orders_stms: OrdersStms
    product_lists: ProductListsStms
    products_stms: ProductsStms
    sys_users_stms: SysUsersStms
    websites_stms: Websites
    product_list_items_stms: ProductListItems


container: StatementsContainer = {
    "account_contracts_stms": lambda: AccountContractStms(model=AccountContracts),
    "account_lists_stms": lambda: AccountListsStms(model=AccountLists),
    "account_products_stms": lambda: AccountProductsStms(model=AccountProducts),
    "accounts_stms": lambda: AccountsStms(model=Accounts),
    "addresses_stms": lambda: AddressesStms(model=Addresses),
    "emails_stms": lambda: EmailsStms(model=Emails),
    "entity_accounts_stms": lambda: EntityAccountsStms(model=EntityAccounts),
    "entites_stms": lambda: EntitiesStms(
        entities=Entities, individuals=Individuals, non_individuals=NonIndividuals
    ),
    "individuals_stms": lambda: IndividualsStms(model=Individuals),
    "invoice_items_stms": lambda: InvoiceItemsStms(model=InvoiceItems),
    "invoice_stms": lambda: InvoicesStms(model=Invoices),
    "non_individuals": lambda: NonIndivididualsStms(model=NonIndividuals),
    "numbers_stms": lambda: NumbersStms(model=Numbers),
    "order_items_stms": lambda: OrderItemsStms(model=OrderItems),
    "orders_stms": lambda: OrdersStms(model=Orders),
    "product_lists": lambda: ProductListsStms(model=ProductLists),
    "products_stms": lambda: ProductsStms(model=Products),
    "websites_stms": lambda: WebsitesStms(model=Websites),
    "sys_users_stms": lambda: SysUsersStms(model=SysUsers),
    "product_list_items_stms": lambda: ProductListItemsStms(model=ProductListItems),
}
