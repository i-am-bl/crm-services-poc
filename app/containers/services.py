from typing import Callable, TypedDict

from .database import container as database_container
from .statements import container as statements_container
from ..models.account_contracts import AccountContracts
from ..models.account_lists import AccountLists
from ..models.accounts import Accounts
from ..models.emails import Emails
from ..services import account_contracts as account_contracts_srvcs
from ..services import account_lists as account_lists_srvcs
from ..services import accounts as accounts_srvcs
from ..services import emails as emails_srvcs


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
}
