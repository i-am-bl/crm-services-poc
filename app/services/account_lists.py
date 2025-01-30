from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..exceptions import AccListExists, AccListNotExist
from ..models.account_lists import AccountLists
from ..schemas.account_lists import (
    AccountListsCreate,
    AccountListsDel,
    AccountListsDelRes,
    AccountListsUpdate,
    AccountListsRes,
    AccountListsOrchPgRes,
)
from ..statements.account_lists import AccountListsStms
from ..database.operations import Operations
from ..utilities import pagination
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Read service class for account lists.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountListsStms.
    varType: AccountListsStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(self, statements: AccountListsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadService class.

        :param statements: An instance of AccountListsStms.
        :type statements: AccountListsStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def get_account_list(
        self,
        account_uuid: UUID4,
        account_list_uuid: UUID4,
        db: AsyncSession,
    ) -> AccountListsRes:
        """
        Retrieves a specific account list for a given account UUID and account list UUID.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_list_uuid: The UUID of the account list.
        :type account_list_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The account list data.
        :rtype: AccountListsRes
        :raises AccListNotExist: If the account list does not exist.
        """
        statement = self._statements.get_account_list(
            account_uuid=account_uuid, account_list_uuid=account_list_uuid
        )
        account_list: AccountListsRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account_list, exception=AccListNotExist)

    async def get_account_lists(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[AccountLists]:
        """
        Retrieves a list of account lists for a given account UUID, with pagination support.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param limit: The maximum number of records to retrieve.
        :type limit: int
        :param offset: The starting point for retrieving records.
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of account lists.
        :rtype: List[AccountLists]
        :raises AccListNotExist: If no account lists are found.
        """
        statement = self._statements.get_account_lists_account(
            account_uuid=account_uuid, limit=limit, offset=offset
        )
        account_lists: List[AccountLists] = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account_lists, exception=AccListNotExist)

    async def get_account_list_ct(self, account_uuid: UUID4, db: AsyncSession) -> int:
        """
        Retrieves the count of account lists for a given account UUID.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The count of account lists for the specified account.
        :rtype: int
        """
        statement = self._statements.get_account_list_count(account_uuid=account_uuid)
        return await self._db_ops.return_count(
            service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_account_lists(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountListsOrchPgRes:
        """
        Retrieves a paginated list of account lists for a given account UUID.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param page: The current page number.
        :type page: int
        :param limit: The maximum number of records per page.
        :type limit: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A paginated result with total count, page, limit, and data.
        :rtype: AccountListsOrchPgRes
        :raises AccListNotExist: If no account lists are found for pagination.
        """
        offset: int = pagination.page_offset(page=page, limit=limit)
        total_count: int = await self.get_account_list_ct(
            account_uuid=account_uuid, db=db
        )
        account_lists = await self.get_account_lists(account_uuid=account_uuid, db=db)
        has_more: bool = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        return AccountListsOrchPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            data=None,  # TODO: return actual data once logic for 'product lists' is clarified
        )


class CreateSrvc:
    """
    Create service class for account lists.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountListsStms.
    varType: AccountListsStms
    ivar: _account_lists: The model for account lists.
    varType: AccountLists
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(
        self,
        statements: AccountListsStms,
        model: AccountLists,
        db_operations: Operations,
    ) -> None:
        """
        Initializes the CreateService class.

        :param statements: An instance of AccountListsStms.
        :type statements: AccountListsStms
        :param model: The model for account lists.
        :type model: AccountLists
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._account_lists = model
        self._db_ops = db_operations

    async def create_account_list(
        self,
        account_uuid: UUID4,
        account_list_data: AccountListsCreate,
        db: AsyncSession,
    ) -> AccountListsRes:
        """
        Creates a new account list for a given account UUID and account list data.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_list_data: The data for the account list to be created.
        :type account_list_data: AccountListsCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The created account list.
        :rtype: AccountListsRes
        :raises AccListExists: If the account list already exists.
        :raises AccListNotExist: If the account list creation fails.
        """
        statement = self._statements.get_account_lists_product_list(
            account_uuid=account_uuid,
            product_list_uuid=account_list_data.product_list_uuid,
        )
        account_list_exists = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_LISTS_CREATE_SERVICE, statement=statement, db=db
        )
        record_exists(instance=account_list_exists, exception=AccListExists)

        account_list: AccountListsRes = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_LISTS_CREATE_SERVICE,
            model=self._account_lists,
            data=account_list_data,
            db=db,
        )
        return record_not_exist(instance=account_list, exception=AccListNotExist)


class UpdateSrvc:
    """
    Update service class for account lists.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountListsStms.
    varType: AccountListsStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(self, statements: AccountListsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateService class.

        :param statements: An instance of AccountListsStms.
        :type statements: AccountListsStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def update_account_list(
        self,
        account_uuid: UUID4,
        account_list_uuid: UUID4,
        account_list_data: AccountListsUpdate,
        db: AsyncSession,
    ) -> AccountListsRes:
        """
        Updates an account list in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_list_uuid: The UUID of the account list to be updated.
        :type account_list_uuid: UUID4
        :param account_list_data: The new data for the account list.
        :type account_list_data: AccountListsUpdate
        :param db: The database session.
        :type db: AsyncSession
        :return: The updated account list.
        :rtype: AccountListsRes
        :raises AccListNotExist: If the account list does not exist.
        """
        statement = self._statements.update_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
        )
        account_list: AccountListsRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_LISTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account_list, exception=AccListNotExist)


class DelSrvc:
    """
    Delete service class for account lists.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountListsStms.
    varType: AccountListsStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(self, statements: AccountListsStms, db_operations: Operations) -> None:
        """
        Initializes the DeleteService class.

        :param statements: An instance of AccountListsStms.
        :type statements: AccountListsStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def soft_del_account_list(
        self,
        account_uuid: UUID4,
        account_list_uuid: UUID4,
        account_list_data: AccountListsDel,
        db: AsyncSession,
    ) -> AccountListsDelRes:
        """
        Soft deletes an account list in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_list_uuid: The UUID of the account list to be deleted.
        :type account_list_uuid: UUID4
        :param account_list_data: The data to update for the account list.
        :type account_list_data: AccountListsDel
        :param db: The database session.
        :type db: AsyncSession
        :return: The soft-deleted account list.
        :rtype: AccountListsDelRes
        :raises AccListNotExist: If the account list does not exist.
        """
        statement = self._statements.update_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
        )
        account_list: AccountListsDelRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_LISTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account_list, exception=AccListNotExist)
