from typing import Callable, TypedDict

from .database import container as database_container
from .statements import container as statements_container
from ..models.account_contracts import AccountContracts
from ..models.account_lists import AccountLists
from ..models.accounts import Accounts
from ..models.emails import Emails
from ..models.entities import Entities
from ..models.individuals import Individuals
from ..models.non_individuals import NonIndividuals
from ..models.invoices import Invoices
from ..models.numbers import Numbers
from ..models.orders import Orders
from ..models.products import Products
from ..models.sys_users import SysUsers
from ..models.websites import Websites
from ..services import account_contracts as account_contracts_srvcs
from ..services import account_lists as account_lists_srvcs
from ..services import accounts as accounts_srvcs
from ..services import emails as emails_srvcs
from ..services import entities as entities_srvcs
from ..services import individuals as individuals_srvcs
from ..services import invoices as invoices_srvcs
from ..services import non_individuals as non_individual_srvcs
from ..services import numbers as numbers_srvcs
from ..services import orders as orders_srvcs
from ..services import products as products_srvcs
from ..services import sys_users as sys_users_srvcs
from ..services import websites as websites_srvcs


class ServicesContainer(TypedDict):
    # account contract services
    account_contracts_create: Callable[[], account_contracts_srvcs.CreateSrvc]
    account_contracts_read: Callable[[], account_contracts_srvcs.ReadSrvc]
    account_contracts_update: Callable[[], account_contracts_srvcs.UpdateSrvc]
    account_contracts_delete: Callable[[], account_contracts_srvcs.DeleteSrvc]
    # account list services
    account_lists_create: account_lists_srvcs.CreateSrvc
    account_lists_read: account_lists_srvcs.ReadSrvc
    account_lists_update: account_lists_srvcs.UpdateSrvc
    account_lists_delete: account_lists_srvcs.DeleteSrvc
    # account services
    accounts_create: accounts_srvcs.CreateSrvc
    accounts_read: accounts_srvcs.ReadSrvc
    accounts_update: accounts_srvcs.UpdateSrvc
    accounts_delete: accounts_srvcs.DelSrvc
    # emails services
    emails_create: emails_srvcs.CreateSrvc
    emails_read: emails_srvcs.ReadSrvc
    emails_update: emails_srvcs.UpdateSrvc
    emails_delete: emails_srvcs.DelSrvc
    # entities services
    entities_create: entities_srvcs.CreateSrvc
    entities_read: entities_srvcs.ReadSrvc
    entities_update: entities_srvcs.UpdateSrvc
    entities_delete: entities_srvcs.DelSrvc
    # individuals services
    individuals_create: individuals_srvcs.CreateSrvc
    individuals_read: individuals_srvcs.ReadSrvc
    individuals_update: individuals_srvcs.UpdateSrvc
    individuals_delete: individuals_srvcs.DelSrvc
    # invoices services
    invoices_create: invoices_srvcs.CreateSrvc
    invoices_read: invoices_srvcs.ReadSrvc
    invoices_update: invoices_srvcs.UpdateSrvc
    invoices_delete: invoices_srvcs.DelSrvc
    # non-individual services
    non_individuals_create: non_individual_srvcs.CreateSrvc
    non_individuals_read: non_individual_srvcs.ReadSrvc
    non_individuals_update: non_individual_srvcs.UpdateSrvc
    non_individuals_delete: non_individual_srvcs.DelSrvc
    # numbers services
    numbers_create: numbers_srvcs.CreateSrvc
    numbers_read: numbers_srvcs.ReadSrvc
    numbers_update: numbers_srvcs.UpdateSrvc
    numbers_delete: numbers_srvcs.DelSrvc
    # orders services
    orders_create: orders_srvcs.CreateSrvc
    orders_read: orders_srvcs.ReadSrvc
    orders_update: orders_srvcs.UpdateSrvc
    orders_delete: orders_srvcs.DelSrvc
    # products services
    products_create: products_srvcs.CreateSrvc
    products_read: products_srvcs.ReadSrvc
    products_update: products_srvcs.UpdateSrvc
    products_delete: products_srvcs.DelSrvc
    # sys_users services
    sys_users_create: sys_users_srvcs.CreateSrvc
    sys_users_read: sys_users_srvcs.ReadSrvc
    sys_users_update: sys_users_srvcs.UpdateSrvc
    sys_users_delete: sys_users_srvcs.DelSrvc
    # websites services
    websites_create: websites_srvcs.CreateSrvc
    websites_read: websites_srvcs.ReadSrvc
    websites_update: websites_srvcs.UpdateSrvc
    websites_delete: websites_srvcs.DelSrvc


container: ServicesContainer = {
    # account contract services
    "account_contracts_create": lambda: (
        account_contracts_srvcs.account_contract_create_srvc(
            operations=database_container["operations"], model=AccountContracts
        )
    ),
    "account_contracts_read": lambda: (
        account_contracts_srvcs.account_contract_read_srvc(
            operations=database_container["operations"],
            statements=statements_container["account_contracts_stms"],
        )
    ),
    "account_contracts_update": lambda: (
        account_contracts_srvcs.account_contract_update_srvc(
            operations=database_container["operations"],
            statements=statements_container["account_contracts_stms"],
        )
    ),
    "account_contracts_delete": lambda: (
        account_contracts_srvcs.account_contract_delete_srvc(
            operations=database_container["operations"],
            statements=statements_container["account_contracts_stms"],
        )
    ),
    # account list services
    "account_lists_create": lambda: account_lists_srvcs.CreateSrvc(
        model=AccountLists,
        statements=statements_container["account_lists_stms"],
        db_operations=database_container["operations"],
    ),
    "account_lists_read": lambda: account_lists_srvcs.ReadSrvcSrvc(
        statements=statements_container["account_lists_stms"],
        db_operations=database_container["operations"],
    ),
    "account_lists_update": lambda: account_lists_srvcs.UpdateSrvc(
        statements=statements_container["account_lists_stms"],
        db_operations=database_container["operations"],
    ),
    "account_lists_delete": lambda: account_lists_srvcs.DelSrvc(
        statements=statements_container["account_lists_stms"],
        db_operations=database_container["operations"],
    ),
    # account services
    "accounts_create": lambda: accounts_srvcs.CreateSrvc(
        model=Accounts, db_operations=database_container["operations"]
    ),
    "accounts_read": lambda: accounts_srvcs.ReadSrvc(
        statements=statements_container["accounts_stms"],
        db_operations=database_container["operations"],
    ),
    "accounts_update": lambda: accounts_srvcs.UpdateSrvc(
        statements=statements_container["accounts_stms"],
        db_operations=database_container["operations"],
    ),
    "accounts_delete": lambda: accounts_srvcs.DelSrvc(
        statements=statements_container["accounts_stms"],
        db_operations=database_container["operations"],
    ),
    # emails services
    "emails_create": lambda: emails_srvcs.CreateSrvc(
        statements=statements_container["emails_stms"],
        db_operations=database_container["operations"],
        model=Emails,
    ),
    "emails_read": lambda: emails_srvcs.ReadSrvc(
        statements=statements_container["emails_stms"],
        db_operations=database_container["operations"],
    ),
    "emails_update": lambda: emails_srvcs.UpdateSrvc(
        statements=statements_container["emails_stms"],
        db_operations=database_container["operations"],
    ),
    "emails_delete": lambda: emails_srvcs.DelSrvc(
        statements=statements_container["emails_stms"],
        db_operations=database_container["operations"],
    ),
    # entities services
    "entities_create": lambda: entities_srvcs.CreateSrvc(
        statements=statements_container["entites_stms"],
        db_operations=database_container["operations"],
        model=Entities,
    ),
    "entities_read": lambda: entities_srvcs.ReadSrvc(
        statements=statements_container["entites_stms"],
        db_operations=database_container["operations"],
    ),
    "entities_update": lambda: entities_srvcs.UpdateSrvc(
        statements=statements_container["entites_stms"],
        db_operations=database_container["operations"],
    ),
    "entities_delete": lambda: entities_srvcs.DelSrvc(
        statements=statements_container["entites_stms"],
        db_operations=database_container["operations"],
    ),
    # individuals services
    "individuals_create": lambda: individuals_srvcs.CreateSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
        model=Invoices,
    ),
    "individuals_read": lambda: individuals_srvcs.ReadSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
    ),
    "individuals_update": lambda: individuals_srvcs.UpdateSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
    ),
    "individuals_delete": lambda: individuals_srvcs.DelSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
    ),
    # invoices services
    "invoices_create": lambda: invoices_srvcs.CreateSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
        model=Invoices,
    ),
    "invoices_read": lambda: invoices_srvcs.ReadSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
    ),
    "invoices_update": lambda: invoices_srvcs.UpdateSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
    ),
    "invoices_delete": lambda: invoices_srvcs.DelSrvc(
        statements=statements_container["invoice_stms"],
        db_operations=database_container["operations"],
    ),
    # non-individual services
    "non_individuals_create": lambda: non_individual_srvcs.CreateSrvc(
        statements=statements_container["non_individuals"],
        db_operations=database_container["operations"],
        model=NonIndividuals,
    ),
    "non_individuals_read": lambda: non_individual_srvcs.ReadSrvc(
        statements=statements_container["non_individuals"],
        db_operations=database_container["operations"],
    ),
    "non_individuals_update": lambda: non_individual_srvcs.UpdateSrvc(
        statements=statements_container["non_individuals"],
        db_operations=database_container["operations"],
    ),
    "non_individuals_delete": lambda: non_individual_srvcs.DelSrvc(
        statements=statements_container["non_individuals"],
        db_operations=database_container["operations"],
    ),
    # number services
    "numbers_create": lambda: numbers_srvcs.CreateSrvc(
        statements=statements_container["numbers_stms"],
        db_operations=database_container["operations"],
        model=Numbers,
    ),
    "numbers_read": lambda: numbers_srvcs.ReadSrvc(
        statements=statements_container["numbers_stms"],
        db_operations=database_container["operations"],
    ),
    "numbers_update": lambda: numbers_srvcs.UpdateSrvc(
        statements=statements_container["numbers_stms"],
        db_operations=database_container["operations"],
    ),
    "numbers_delete": lambda: numbers_srvcs.DelSrvc(
        statements=statements_container["numbers_stms"],
        db_operations=database_container["operations"],
    ),
    # orders services
    "orders_create": lambda: orders_srvcs.CreateSrvc(
        db_operations=database_container["operations"], model=Orders
    ),
    "orders_read": lambda: orders_srvcs.ReadSrvc(
        statements=statements_container["orders_stms"],
        db_operations=database_container["operations"],
    ),
    "orders_update": lambda: orders_srvcs.UpdateSrvc(
        statements=statements_container["orders_stms"],
        db_operations=database_container["operations"],
    ),
    "orders_delete": lambda: orders_srvcs.DelSrvc(
        statements=statements_container["orders_stms"],
        db_operations=database_container["operations"],
    ),
    # products services
    "products_create": lambda: products_srvcs.CreateSrvc(
        statements=statements_container["products_stms"],
        db_operations=database_container["operations"],
        model=Products,
    ),
    "products_read": lambda: products_srvcs.ReadSrvc(
        statements=statements_container["products_stms"],
        db_operations=database_container["operations"],
    ),
    "products_update": lambda: products_srvcs.UpdateSrvc(
        statements=statements_container["products_stms"],
        db_operations=database_container["operations"],
    ),
    "products_delete": lambda: products_srvcs.DelSrvc(
        statements=statements_container["products_stms"],
        db_operations=database_container["operations"],
    ),
    # sys_users services
    "sys_users_create": lambda: sys_users_srvcs.CreateSrvc(
        statements=statements_container["sys_users_stms"],
        db_operations=database_container["operations"],
        model=SysUsers,
    ),
    "sys_users_read": lambda: sys_users_srvcs.ReadSrvc(
        statements=statements_container["sys_users_stms"],
        db_operations=database_container["operations"],
    ),
    "sys_users_update": lambda: sys_users_srvcs.UpdateSrvc(
        statements=statements_container["sys_users_stms"],
        db_operations=database_container["operations"],
    ),
    "sys_users_delete": lambda: sys_users_srvcs.DelSrvc(
        statements=statements_container["sys_users_stms"],
        db_operations=database_container["operations"],
    ),
    # websites services
    "websites_create": lambda: websites_srvcs.CreateSrvc(
        statements=statements_container["websites_stms"],
        db_operations=database_container["operations"],
        model=Websites,
    ),
    "websites_read": lambda: websites_srvcs.ReadSrvc(
        statements=statements_container["websites_stms"],
        db_operations=database_container["operations"],
    ),
    "websites_update": lambda: websites_srvcs.UpdateSrvc(
        statements=statements_container["websites_stms"],
        db_operations=database_container["operations"],
    ),
    "websites_delete": lambda: websites_srvcs.DelSrvc(
        statements=statements_container["websites_stms"],
        db_operations=database_container["operations"],
    ),
}
