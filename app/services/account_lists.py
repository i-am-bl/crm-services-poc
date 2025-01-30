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
    def __init__(self, statements: AccountListsStms, db_operations: Operations) -> None:
        self._statements: AccountListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountListsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_account_list(
        self,
        account_uuid: UUID4,
        account_list_uuid: UUID4,
        db: AsyncSession,
    ) -> AccountListsRes:
        statement = self._statements.get_account_list(
            account_uuid=account_uuid, account_list_uuid=account_list_uuid
        )
        account_list = await self._db_ops.return_one_row(
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
        statement = self._statements.get_account_lists_account(
            account_uuid=account_uuid, limit=limit, offset=offset
        )
        account_lists: List[AccountLists] = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account_lists, exception=AccListNotExist)

    async def get_account_list_ct(self, account_uuid: UUID4, db: AsyncSession) -> int:
        statement = self._statements.get_account_list_count(account_uuid=account_uuid)
        return await self._db_ops.return_count(
            service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_account_lists(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountListsOrchPgRes:

        offset: int = pagination.page_offset(page=page, limit=limit)
        total_count: int = await self.get_account_list_ct(
            account_uuid=account_uuid, db=db
        )
        account_lists = await self.get_account_lists(account_uuid=account_uuid, db=db)
        has_more: bool = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        # TODO: research the product lists in this context.
        return AccountListsOrchPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_moare=has_more,
            data=None,
        )


class CreateSrvc:
    def __init__(
        self,
        statements: AccountListsStms,
        model: AccountLists,
        db_operations: Operations,
    ) -> None:
        self._statements: AccountListsStms = statements
        self._account_lists: AccountLists = model
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountListsStms:
        return self._statements

    @property
    def account_lists(self) -> AccountLists:
        return self._account_lists

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def create_account_list(
        self,
        account_uuid: UUID4,
        account_list_data: AccountListsCreate,
        db: AsyncSession,
    ) -> AccountListsRes:
        account_lists = self._account_lists
        statement = self._statements.get_account_lists_product_list(
            account_uuid=account_uuid,
            product_list_uuid=account_list_data.product_list_uuid,
        )
        account_list_exists = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_LISTS_CREATE_SERVICE, statement=statement, db=db
        )
        record_exists(instance=account_list_exists, exception=AccListExists)

        account_list = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_LISTS_CREATE_SERVICE,
            model=account_lists,
            data=account_list_data,
            db=db,
        )
        return record_not_exist(instance=account_list, exception=AccListNotExist)


class UpdateSrvc:
    def __init__(self, statements: AccountListsStms, db_operations: Operations) -> None:
        self._statements: AccountListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountListsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_account_list(
        self,
        account_uuid: UUID4,
        account_list_uuid: UUID4,
        account_list_data: AccountListsUpdate,
        db: AsyncSession,
    ) -> AccountListsRes:
        statement = self._statements.update_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
        )
        account_list = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_LISTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account_list, exception=AccListNotExist)


class DelSrvc:
    def __init__(self, statements: AccountListsStms, db_operations: Operations) -> None:
        self._statements: AccountListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self):
        return self._statements

    @property
    def db_operations(self):
        return self._db_ops

    async def soft_del_account_list(
        self,
        account_uuid: UUID4,
        account_list_uuid: UUID4,
        account_list_data: AccountListsDel,
        db: AsyncSession,
    ) -> AccountListsDelRes:
        statement = self._statements.update_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
        )
        account_list = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_LISTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=account_list, exception=AccListNotExist)
