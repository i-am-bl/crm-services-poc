from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import EntityAccExists, EntityAccNotExist
from ..models.entity_accounts import EntityAccounts

from ..schemas.entity_accounts import (
    EntityAccountsCreate,
    EntityAccountsDel,
    EntityAccountsDelRes,
    EntityAccountsRes,
    EntityAccountsUpdate,
)
from ..statements.entity_accounts import EntityAccountsStms
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: EntityAccounts, db_operations: Operations) -> None:
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntityAccountsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_uuid: UUID4,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        statement = self._statements.get_entity_account(
            entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid
        )
        entity_account: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        statement = self._statements.get_account_entity(
            account_uuid=account_uuid, entity_account_uuid=entity_account_uuid
        )
        entity_account: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_account_entities(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EntityAccountsRes]:
        statement = self._statements.get_account_entities(
            account_uuid=account_uuid, limit=limit, offset=offset
        )
        entity_account: List[EntityAccountsRes] = await self._db_ops.return_all_rows(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_entity_accounts(
        self,
        entity_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EntityAccountsRes]:
        statement = self._statements.get_entity_accounts(
            entity_uuid=entity_uuid, limit=limit, offset=offset
        )
        entity_account = await self._db_ops.return_all_rows(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_entity_accounts_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        statement = self._statements.get_entity_account_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )

    async def get_account_entities_ct(
        self,
        account_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        statement = self._statements.get_account_entities_ct(account_uuid=account_uuid)
        return await self._db_ops.return_count(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )


class CreateSrvc:
    def __init__(
        self,
        statements: EntityAccounts,
        db_operations: Operations,
        model: EntityAccounts,
    ) -> None:
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations
        self._model: EntityAccounts = model

    @property
    def statements(self) -> EntityAccountsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> EntityAccounts:
        return self._model

    async def create_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_data: EntityAccountsCreate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        statement = self._statements.get_entity_account_by_parent(
            entity_uuid=entity_uuid,
            account_uuid=entity_account_data.account_uuid,
        )
        entity_accounts = self._model

        entity_account_exists: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV, statement=statement, db=db
        )

        di.record_exists(instance=entity_account_exists, exception=EntityAccExists)

        entity_account: EntityAccountsRes = await self._db_ops.add_instance(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV,
            model=entity_accounts,
            data=entity_account_data,
            db=db,
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def create_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_data: EntityAccountsCreate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        statement = self._statements.get_entity_account_by_parent(
            entity_uuid=entity_account_data.entity_uuid,
            account_uuid=account_uuid,
        )
        entity_accounts = self._model

        entity_account_exists: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV, statement=statement, db=db
        )

        di.record_exists(instance=entity_account_exists, exception=EntityAccExists)

        entity_account: EntityAccountsRes = await self._db_ops.add_instance(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV,
            model=entity_accounts,
            data=entity_account_data,
            db=db,
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)


class UpdateSrvc:
    def __init__(self, statements: EntityAccounts, db_operations: Operations) -> None:
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntityAccountsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsUpdate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        statement = self._statements.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def update_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsUpdate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        statement = self._statements.update_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)


class DelSrvc:
    def __init__(self, statements: EntityAccounts, db_operations: Operations) -> None:
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntityAccountsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsDel,
        db: AsyncSession,
    ) -> EntityAccountsDelRes:
        statement = self._statements.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account: EntityAccountsDelRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def soft_del_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsDel,
        db: AsyncSession,
    ) -> EntityAccountsDelRes:
        statement = self._statements.update_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account: EntityAccountsDelRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)
