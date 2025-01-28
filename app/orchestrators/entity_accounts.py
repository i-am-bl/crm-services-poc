from pydantic import UUID4
from ..schemas.entity_accounts import AccountEntitiesPgRes, EntityAccountsPgRes
from ..services import accounts as accounts_srvcs
from ..services import entity_accounts as entity_accounts_srvcs
from ..services import entities as entities_srvcs
from sqlalchemy.ext.asyncio import AsyncSession
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
        if not isinstance(entities, list):
            entities = [entities]
        entity_uuids = [account_entity.uuid for account_entity in account_entities]
        entities = await self.entities_read_srvc.get_entities_by_uuids(
            entity_uuids=entity_uuids, db=db
        )
        return AccountEntitiesPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=entities
        )

    async def paginated_entity_accounts(self) -> EntityAccountsPgRes:
        return EntityAccountsPgRes()
