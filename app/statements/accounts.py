from typing import List

from pydantic import UUID4
from sqlalchemy import Select, and_, func, select, update, Update

from ..models.accounts import Accounts
from ..utilities.data import set_empty_strs_null


class AccountsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing accounts.

    ivars:
    ivar: _accounts: Accounts: An instance of Accounts.
    """

    def __init__(self, model: Accounts) -> None:
        """
        Initializes the AccountsStms class.

        :param model: Accounts: An instance of Accounts.
        :return None
        """
        self._accounts: Accounts = model

    @property
    def accounts(self) -> Accounts:
        """
        Returns the model instance for accounts.

        :return: Accounts: The Accounts model instance.
        """
        return self._accounts

    def get_account(self, account_uuid: UUID4) -> Select:
        """
        Selects an account by account_uuid.

        :param account_uuid: UUID4: The UUID of the account.
        :return: Select: A Select statement.
        """
        accounts = self._accounts
        return Select(accounts).where(
            and_(accounts.uuid == account_uuid, accounts.sys_deleted_at == None)
        )

    def get_accounts_by_uuids(self, account_uuids: List[UUID4]) -> Select:
        """
        Selects accounts by a list of account_uuids.

        :param account_uuids: List[UUID4]: A list of account UUIDs.
        :return: Select: A Select statement.
        """
        accounts = self._accounts
        return Select(accounts).where(
            and_(accounts.uuid.in_(account_uuids), accounts.sys_deleted_at == None)
        )

    def get_accounts(self, offset: int, limit: int) -> Select:
        """
        Selects accounts with pagination support.

        :param offset: int: The number of records to skip.
        :param limit: int: The number of records to return.
        :return: Select: A Select statement.
        """
        accounts = self._accounts
        return (
            Select(accounts)
            .where(accounts.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_accounts_ct(self) -> Select:
        """
        Selects the count of all accounts.

        :return: Select: A Select statement with a count of accounts.
        """
        accounts = self._accounts
        return (
            select(func.count())
            .select_from(accounts)
            .where(accounts.sys_deleted_at == None)
        )

    def update_account(self, account_uuid: UUID4, account_data: object) -> Update:
        """
        Updates an account by account_uuid.

        :param account_uuid: UUID4: The UUID of the account.
        :param account_data: object: The data to update the account with.
        :return: Update: An Update statement.
        """
        accounts = self._accounts
        return (
            update(accounts)
            .where(and_(accounts.uuid == account_uuid, accounts.sys_deleted_at == None))
            .values(set_empty_strs_null(account_data))
            .returning(accounts)
        )
