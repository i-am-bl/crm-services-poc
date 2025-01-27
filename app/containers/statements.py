from typing import Callable, TypedDict

from ..models.account_contracts import AccountContracts
from ..models.account_lists import AccountLists
from ..models.accounts import Accounts
from ..models.emails import Emails
from ..models.entities import Entities
from ..models.individuals import Individuals
from ..models.non_individuals import NonIndividuals
from ..models.individuals import Individuals
from ..models.invoices import Invoices
from ..models.non_individuals import NonIndividuals
from ..models.numbers import Numbers
from ..statements.account_contracts import AccountContractStms
from ..statements.account_lists import AccountListsStms
from ..statements.accounts import AccountsStms
from ..statements.emails import EmailsStms
from ..statements.entities import EntitiesStms
from ..statements.individuals import IndividualsStms
from ..statements.invoices import InvoicesStms
from ..statements.non_individuals import NonInvdividualsStms
from ..statements.numbers import NumberStms


class StatementsContainer(TypedDict):
    account_contracts_stms: AccountContractStms
    account_lists_stms: AccountListsStms
    accounts_stms: AccountsStms
    emails_stms: EmailsStms
    entites_stms: EntitiesStms
    individuals_stms: IndividualsStms
    invoice_stms: InvoicesStms
    non_individuals: NonInvdividualsStms
    numbers_stms: NumberStms


container: StatementsContainer = {
    "account_contracts_stms": lambda: AccountContractStms(model=AccountContracts),
    "account_lists_stms": lambda: AccountListsStms(model=AccountLists),
    "accounts_stms": lambda: AccountsStms(model=Accounts),
    "emails_stms": lambda: EmailsStms(model=Emails),
    "entites_stms": lambda: EntitiesStms(
        entities=Entities, individuals=Individuals, non_individuals=NonIndividuals
    ),
    "individuals_stms": lambda: IndividualsStms(model=Individuals),
    "invoice_stms": lambda: InvoicesStms(model=Invoices),
    "non_individuals": lambda: NonInvdividualsStms(model=NonIndividuals),
    "numbers_stms": lambda: NumberStms(model=Numbers),
}
