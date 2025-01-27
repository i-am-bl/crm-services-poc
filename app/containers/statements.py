from typing import Callable, TypedDict

from ..models.account_contracts import AccountContracts
from ..models.account_lists import AccountLists
from ..models.accounts import Accounts
from ..models.emails import Emails
from ..models.entities import Entities
from ..models.individuals import Individuals
from ..models.non_individuals import NonIndividuals
from ..models.individuals import Individuals
from ..statements.account_contracts import AccountContractStms, account_contract_stms
from ..statements.account_lists import AccountListsStms, account_lists_stms
from ..statements.accounts import AccountsStms, account_stms
from ..statements.emails import EmailsStms, email_stms
from ..statements.entities import EntitiesStms, entities_stms
from ..statements.individuals import IndividualsStms


class StatementsContainer(TypedDict):
    account_contracts_stms: AccountContractStms
    account_lists_stms: AccountListsStms
    accounts_stms: AccountsStms
    emails_stms: EmailsStms
    entites_stms: EntitiesStms
    individuals_stms: IndividualsStms


container: StatementsContainer = {
    "account_contracts_stms": lambda: AccountContractStms(model=AccountContracts),
    "account_lists_stms": lambda: AccountListsStms(model=AccountLists),
    "accounts_stms": lambda: AccountsStms(model=Accounts),
    "emails_stms": lambda: EmailsStms(model=Emails),
    "entites_stms": lambda: EntitiesStms(
        entities=Entities, individuals=Individuals, non_individuals=NonIndividuals
    ),
    "individuals_stms": lambda: IndividualsStms(model=Individuals),
}
