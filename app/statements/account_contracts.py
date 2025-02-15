from pydantic import UUID4
from sqlalchemy import Select, and_, func, update

from ..models.account_contracts import AccountContracts
from ..utilities.data import set_empty_strs_null


class AccountContractStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing account contracts.

    ivars:
    ivar: _account_contracts: AccountContracts: An instance of AccountContracts
    """

    def __init__(self, model: AccountContracts):
        self._account_contacts: AccountContracts = model
        """
        Initializes the AccountContractStms class.

        :param model: AccountContracts: An instance of AccountContracts.
        :return None
        """

    def get_account_contract(
        self, account_uuid: UUID4, account_contract_uuid: UUID4
    ) -> Select:
        """
        Selects an account contract by account_uuid and account_contract_uuid.

        :param account_uuid: UUID4: The account_uuid of the account contract.
        :param account_contract_uuid: UUID4 The account_contract_uuid of the account contract.
        :return: Select: A Select statement.
        """
        account_contacts = self._account_contacts
        return Select(account_contacts).where(
            account_contacts.account_uuid == account_uuid,
            account_contacts.uuid == account_contract_uuid,
            account_contacts.sys_deleted_at == None,
        )

    def get_account_contracts(
        self, account_uuid: UUID4, limit: int, offset: int
    ) -> Select:
        """
        Selects account contracts by account_uuid.

        :param account_uuid: UUID4: The account_uuid of the account contract.
        :param limit: int: The number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement.
        """
        account_contacts = self._account_contacts
        return (
            Select(account_contacts)
            .where(
                account_contacts.account_uuid == account_uuid,
                account_contacts.sys_deleted_at == None,
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def account_contracts_count(self, account_uuid: UUID4) -> Select:
        """
        Selects the count of account contracts by account_uuid.

        :param account_uuid: UUID4: The account_uuid of the account contract.
        :return: Select: A Select statement.
        """
        account_contacts = self._account_contacts
        return (
            Select(func.count())
            .select_from(account_contacts)
            .where(
                account_contacts.account_uuid == account_uuid,
                account_contacts.sys_deleted_at == None,
            )
        )

    def update_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        account_contract_data: object,
    ) -> Select:

        account_contacts = self._account_contacts
        return (
            update(account_contacts)
            .where(
                and_(
                    account_contacts.account_uuid == account_uuid,
                    account_contacts.uuid == account_contract_uuid,
                    account_contacts.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(values=account_contract_data))
            .returning(account_contacts)
        )
