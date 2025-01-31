from re import A
from token import OP
from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import AccsNotExist
from ..models.accounts import Accounts
from ..schemas.accounts import (
    AccountsRes,
    AccountsUpdate,
    AccountsInternalCreate,
    AccountsDel,
    AccountsDelRes,
    AccountsPgRes,
)
from ..statements.accounts import AccountsStms
from ..utilities import pagination
from ..utilities.data import record_not_exist


class ReadSrvc:
    """
    Service for reading account data from the database.

    This class provides methods to retrieve account information from the database, including:
    - A single account by UUID
    - Multiple accounts by a list of UUIDs
    - A paginated list of accounts

    :param statements: The statements used to query account data.
    :type statements: AccountsStms
    :param db_operations: The database operations object used for querying and returning data.
    :type db_operations: Operations
    """

    def __init__(self, statements: AccountsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the given database statements and operations.

        :param statements: The statements used to query account data.
        :type statements: AccountsStms
        :param db_operations: The database operations object used for querying and returning data.
        :type db_operations: Operations
        """
        self._statements: AccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountsStms:
        """
        Returns the statements object for account data queries.

        :return: The statements object for querying account data.
        :rtype: AccountsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def get_account(self, account_uuid: UUID4, db: AsyncSession) -> AccountsRes:
        """
        Retrieves a single account from the database by its UUID.

        :param account_uuid: The UUID of the account to retrieve.
        :type account_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The retrieved account data.
        :rtype: AccountsRes
        :raises AccsNotExist: If the account does not exist.
        """
        statement = self._statements.get_account(account_uuid=account_uuid)
        account = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account, exception=AccsNotExist)

    async def get_accounts_by_uuids(self, account_uuids: List[UUID4], db: AsyncSession):
        """
        Retrieves multiple accounts from the database by a list of UUIDs.

        :param account_uuids: The list of UUIDs for the accounts to retrieve.
        :type account_uuids: List[UUID4]
        :param db: The database session.
        :type db: AsyncSession
        :return: The list of retrieved account data.
        :rtype: List[AccountsRes]
        :raises AccsNotExist: If the accounts do not exist.
        """
        statement = self._statements.get_accounts_by_uuids(account_uuids=account_uuids)
        accounts = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=accounts, exception=AccsNotExist)

    async def get_accounts(self, offset: int, limit: int, db: AsyncSession):
        """
        Retrieves a paginated list of accounts from the database.

        :param offset: The number of records to skip for pagination.
        :type offset: int
        :param limit: The maximum number of records to return.
        :type limit: int
        :param db: The database session.
        :type db: AsyncSession
        :return: The list of accounts within the given pagination parameters.
        :rtype: List[AccountsRes]
        """
        statement = self._statements.get_accounts(offset=offset, limit=limit)
        return await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
        )

    async def get_account_ct(self, db: AsyncSession) -> int:
        """
        Retrieves the total count of accounts in the database.

        :param db: The database session.
        :type db: AsyncSession
        :return: The total count of accounts.
        :rtype: int
        """
        statement = self._statements.get_accounts_ct()
        return await self._db_ops.return_count(
            service=cnst.ACCOUNTS_READ_SERVICE,
            statement=statement,
            db=db,
        )

    async def paginated_accounts(
        self, page: int, limit: int, db: AsyncSession
    ) -> AccountsPgRes:
        """
        Retrieves a paginated list of accounts, including metadata such as the total count and pagination details.

        :param page: The page number for pagination.
        :type page: int
        :param limit: The maximum number of accounts per page.
        :type limit: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A paginated response with account data and pagination metadata.
        :rtype: AccountsPgRes
        """
        total_count = await self.get_account_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        accounts = await self.get_accounts(offset=offset, limit=limit, db=db)
        return AccountsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            accounts=accounts,
        )


class CreateSrvc:
    """
    Service for creating new accounts in the database.

    This class provides functionality to create an account in the database.

    :param model: The model used for the account data.
    :type model: Accounts
    :param db_operations: The database operations object used for adding data.
    :type db_operations: Operations
    """

    def __init__(self, model: Accounts, db_operations: Operations) -> None:
        """
        Initializes the CreateSrvc class with the provided model and database operations.

        :param model: The model used for the account data.
        :type model: Accounts
        :param db_operations: The database operations object used for adding data.
        :type db_operations: Operations
        """
        self._accounts: Accounts = model
        self._db_ops: Operations = db_operations

    @property
    def accounts(self) -> Accounts:
        """
        Returns the accounts model.

        :return: The accounts model.
        :rtype: Accounts
        """
        return self._accounts

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def create_account(
        self, account_data: AccountsInternalCreate, db: AsyncSession
    ) -> AccountsRes:
        """
        Creates a new account in the database.

        :param account_data: The data required to create the new account.
        :type account_data: AccountsInternalCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The result of the account creation operation.
        :rtype: AccountsRes
        :raises AccsNotExist: If the account could not be created.
        """
        accounts = self._accounts
        account = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_CREATE_SERVICE,
            model=accounts,
            data=account_data,
            db=db,
        )
        return record_not_exist(instance=account, exception=AccsNotExist)


class UpdateSrvc:
    """
    Service for updating existing accounts in the database.

    This class provides functionality to update an existing account in the database.

    :param statements: The SQL statements used for account data updates.
    :type statements: AccountsStms
    :param db_operations: The database operations object used for updating data.
    :type db_operations: Operations
    """

    def __init__(self, statements: AccountsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for account data updates.
        :type statements: AccountsStms
        :param db_operations: The database operations object used for updating data.
        :type db_operations: Operations
        """
        self._statements: AccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountsStms:
        """
        Returns the accounts update SQL statements.

        :return: The accounts update SQL statements.
        :rtype: AccountsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def update_account(
        self,
        account_uuid: UUID4,
        account_data: AccountsUpdate,
        db: AsyncSession,
    ) -> AccountsRes:
        """
        Updates an existing account in the database.

        :param account_uuid: The UUID of the account to update.
        :type account_uuid: UUID4
        :param account_data: The updated account data.
        :type account_data: AccountsUpdate
        :param db: The database session.
        :type db: AsyncSession
        :return: The updated account data.
        :rtype: AccountsRes
        :raises AccsNotExist: If the account does not exist to be updated.
        """
        statement = self._statements.update_account(
            account_uuid=account_uuid, account_data=account_data
        )
        account = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account, exception=AccsNotExist)


class DelSrvc:
    """
    Service for performing soft deletions of accounts in the database.

    This class provides functionality to perform a soft deletion of an account in the database.

    :param statements: The SQL statements used for account data updates.
    :type statements: AccountsStms
    :param db_operations: The database operations object used for performing deletions.
    :type db_operations: Operations
    """

    def __init__(self, statements: AccountsStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for account data updates.
        :type statements: AccountsStms
        :param db_operations: The database operations object used for performing deletions.
        :type db_operations: Operations
        """
        self._statements: AccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountsStms:
        """
        Returns the accounts delete SQL statements.

        :return: The accounts delete SQL statements.
        :rtype: AccountsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def sof_del_account(
        self,
        account_uuid: UUID4,
        account_data: AccountsDel,
        db: AsyncSession,
    ) -> AccountsDelRes:
        """
        Performs a soft deletion of an account in the database.

        :param account_uuid: The UUID of the account to delete.
        :type account_uuid: UUID4
        :param account_data: The data required to mark the account as deleted.
        :type account_data: AccountsDel
        :param db: The database session.
        :type db: AsyncSession
        :return: The result of the soft deletion operation.
        :rtype: AccountsDelRes
        :raises AccsNotExist: If the account does not exist to be deleted.
        """
        statement = self._statements.update_account(
            account_uuid=account_uuid, account_data=account_data
        )
        account = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account, exception=AccsNotExist)
