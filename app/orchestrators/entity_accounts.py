from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.accounts import AccountsCreate
from ..schemas.entity_accounts import (
    AccountEntitiesPgRes,
    EntityAccountParentRes,
    EntityAccountsPgRes,
    EntityAccountsCreate,
)
from ..services import accounts as accounts_srvcs
from ..services import entity_accounts as entity_accounts_srvcs
from ..services import entities as entities_srvcs
from ..utilities import pagination


class EntityAccountsReadOrch:
    def __init__(
        self,
        accounts_read_srvc: accounts_srvcs.ReadSrvc,
        entities_read_srvc: entities_srvcs.ReadSrvc,
        entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc,
    ) -> None:
        self._accounts_read_srvc: accounts_srvcs.ReadSrvc = accounts_read_srvc
        self._entities_read_srvc: entities_srvcs.ReadSrvc = entities_read_srvc
        self._entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc = (
            entity_accounts_read_srvc
        )

    @property
    def accounts_read_srvc(self) -> accounts_srvcs.ReadSrvc:
        return self._accounts_read_srvc

    @property
    def entities_read_srvc(self) -> entities_srvcs.ReadSrvc:
        return self._entities_read_srvc

    @property
    def entity_accounts_read_srvc(self) -> entity_accounts_srvcs.ReadSrvc:
        return self._entity_accounts_read_srvc

    async def paginated_account_entities(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountEntitiesPgRes:
        total_count = await self.entity_accounts_read_srvc.get_account_entities_ct(
            account_uuid=account_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(page=page, limit=limit)
        account_entities = await self.entity_accounts_read_srvc.get_account_entities(
            account_uuid=account_uuid, offset=offset, limit=limit, db=db
        )
        entity_uuids = [account_entity.uuid for account_entity in account_entities]
        entities = await self.entities_read_srvc.get_entities_by_uuids(
            entity_uuids=entity_uuids, db=db
        )
        if not isinstance(entities, list):
            entities = [entities]
        return AccountEntitiesPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=entities
        )

    async def paginated_entity_accounts(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> EntityAccountsPgRes:
        total_count = await self.entity_accounts_read_srvc.get_entity_accounts_ct(
            entity_uuid=entity_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        entity_accounts = await self.entity_accounts_read_srvc.get_entity_accounts(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        account_uuids = [entity_account.uuid for entity_account in entity_accounts]
        accounts = await self.accounts_read_srvc.get_accounts_by_uuids(
            account_uuids=account_uuids, db=db
        )
        if not isinstance(accounts, list):
            accounts = [accounts]
        return EntityAccountsPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=accounts
        )


class EntityAccountsCreateOrch:
    def __init__(
        self,
        accounts_create_srvc: accounts_srvcs.CreateSrvc,
        entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc,
    ):
        self._accounts_create_srvc: accounts_srvcs.CreateSrvc = accounts_create_srvc
        self._entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc = (
            entity_accounts_create_srvc
        )

    @property
    def accounts_create_srvc(self) -> accounts_srvcs.CreateSrvc:
        return self._accounts_create_srvc

    @property
    def entity_accounts_create_srvc(self) -> entity_accounts_srvcs.CreateSrvc:
        return self._entity_accounts_create_srvc

    async def create_account(
        self,
        entity_uuid: UUID4,
        account_data: AccountsCreate,
        entity_account_data: EntityAccountsCreate,
        db: AsyncSession,
    ):
        account = await self._accounts_create_srvc.create_account(
            account_data=account_data, db=db
        )
        await db.flush()
        setattr(entity_account_data, "account_uuid", account.uuid)
        entity_account = await self._entity_accounts_create_srvc.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )

        return EntityAccountParentRes(account=account, entity_account=entity_account)
