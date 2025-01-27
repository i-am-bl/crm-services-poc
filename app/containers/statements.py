from typing import Callable, TypedDict

from ..models.account_contracts import AccountContracts
from ..models.account_lists import AccountLists
from ..models.accounts import Accounts
from ..models.emails import Emails
from ..statements.account_contracts import AccountContractStms, account_contract_stms
from ..statements.account_lists import AccountListsStms, account_lists_stms
from ..statements.accounts import AccountsStms, account_stms
from ..statements.emails import EmailsStms, email_stms


class StatementsContainer(TypedDict):
    account_contracts_stms: Callable[[], AccountContractStms]
    account_lists_stms: Callable[[], AccountListsStms]
    accounts_stms: Callable[[], AccountsStms]
    emails_stms: Callable[[], EmailsStms]


container: StatementsContainer = {
    "account_contracts_stms": lambda: (account_contract_stms(model=AccountContracts)),
    "account_lists_stms": lambda: (account_lists_stms(model=AccountLists)),
    "accounts_stms": lambda: account_stms(model=Accounts),
    "emails_stms": lambda: email_stms(model=Emails),
}
