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
    AccountsCreate,
    AccountsDel,
    AccountsDelRes,
    AccountsPgRes,
)
from ..statements.accounts import AccountsStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: AccountsStms, db_operations: Operations) -> None:
        self._statements: AccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_account(self, account_uuid: UUID4, db: AsyncSession) -> AccountsRes:
        statement = self._statements.get_account(account_uuid=account_uuid)
        account = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=account, exception=AccsNotExist)

    async def get_accounts_by_uuids(self, account_uuids: List[UUID4], db: AsyncSession):
        statement = self._statements.get_accounts_by_uuids(account_uuids=account_uuids)
        accounts = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=accounts, exception=AccsNotExist)

    async def get_accounts(
        self,
        offset: int,
        limit: int,
        db: AsyncSession,
    ):
        statement = self._statements.get_accounts(offset=offset, limit=limit)
        return await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
        )

    async def get_account_ct(self, db: AsyncSession) -> int:
        statement = self._statements.get_accounts_ct()
        return await self._db_ops.return_count(
            service=cnst.ACCOUNTS_READ_SERVICE,
            statement=statement,
            db=db,
        )

    async def paginated_accounts(
        self, page: int, limit: int, db: AsyncSession
    ) -> AccountsPgRes:
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
    def __init__(self, model: Accounts, db_operations: Operations) -> None:
        self._accounts: Accounts = model
        self._db_ops: Operations = db_operations

    @property
    def accounts(self) -> Accounts:
        return self._accounts

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def create_account(
        self, account_data: AccountsCreate, db: AsyncSession
    ) -> AccountsRes:
        accounts = self._accounts
        account = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_CREATE_SERVICE,
            model=accounts,
            data=account_data,
            db=db,
        )
        return di.record_not_exist(instance=account, exception=AccsNotExist)


class UpdateSrvc:
    def __init__(self, statements: AccountsStms, db_operations: Operations) -> None:
        self._statements: AccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_account(
        self,
        account_uuid: UUID4,
        account_data: AccountsUpdate,
        db: AsyncSession,
    ) -> AccountsRes:
        statement = self._statements.update_account(
            account_uuid=account_uuid, account_data=account_data
        )
        account = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=account, exception=AccsNotExist)


class DelSrvc:
    def __init__(self, statements: AccountsStms, db_operations: Operations) -> None:
        self._statements: AccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def sof_del_account(
        self,
        account_uuid: UUID4,
        account_data: AccountsDel,
        db: AsyncSession,
    ) -> AccountsDelRes:
        statement = self._statements.update_account(
            account_uuid=account_uuid, account_data=account_data
        )
        account = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_UPDATE_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=account, exception=AccsNotExist)
