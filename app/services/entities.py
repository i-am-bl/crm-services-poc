from typing import List

from pydantic import UUID4
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import EntityNotExist
from ..models.entities import Entities
from ..schemas.entities import (
    EntitiesCreate,
    EntitiesDel,
    EntitiesDelRes,
    EntitiesPgRes,
    EntitiesRes,
    EntitiesUpdate,
)
from ..statements.entities import EntitiesStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: EntitiesStms, db_operations: Operations) -> None:
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntitiesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_entity(self, entity_uuid: UUID4, db: AsyncSession) -> EntitiesRes:
        statement: Select = self._statements.get_entity(entity_uuid=entity_uuid)
        entity: EntitiesRes = await self._db_ops.return_one_row(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entity, exception=EntityNotExist)

    async def get_entities_by_uuids(self, entity_uuids: List[UUID4], db: AsyncSession):
        statement: Select = self._statements.get_entities_by_uuids(
            entity_uuids=entity_uuids
        )
        entities: List[EntitiesRes] = await self._db_ops.return_all_rows_and_values(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entities, exception=EntityNotExist)

    async def get_entities(
        self,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EntitiesRes]:
        statement: Select = self._statements.get_entities(limit=limit, offset=offset)
        entities: List[EntitiesRes] = await self._db_ops.return_all_rows(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )
        di.record_not_exist(instance=entities, exception=EntityNotExist)
        return entities

    async def get_entity_ct(self, db: AsyncSession) -> int:
        statement: Select = self._statements.get_entity_ct()
        return await self._db_ops.return_count(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )

    async def paginated_entities(
        self, page: int, limit: int, db: AsyncSession
    ) -> EntitiesPgRes:
        total_count: int = self.get_entity_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        entities = await self.get_entities(offset=offset, limit=limit, db=db)
        return EntitiesPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=entities
        )


class CreateSrvc:
    def __init__(
        self, statements: EntitiesStms, db_operations: Operations, model: Entities
    ) -> None:
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Entities = model

    @property
    def statements(self) -> EntitiesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def create_entity(
        self,
        entity_data: EntitiesCreate,
        db: AsyncSession,
    ) -> EntitiesRes:
        entities = self._model
        entity: EntitiesRes = await self._db_ops.add_instance(
            service=cnst.ENTITIES_CREATE_SERV,
            model=entities,
            data=entity_data,
            db=db,
        )
        return di.record_not_exist(instance=entity, exception=EntityNotExist)


class UpdateSrvc:
    def __init__(self, statements: EntitiesStms, db_operations: Operations) -> None:
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntitiesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_entity(
        self,
        entity_uuid: UUID4,
        entity_data: EntitiesUpdate,
        db: AsyncSession,
    ):
        statement: update = self._statements.update_entity(
            entity_uuid=entity_uuid, entity_data=entity_data
        )
        entity: EntitiesRes = await Operations.return_one_row(
            service=cnst.ENTITIES_UPDATE_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entity, exception=EntityNotExist)


class DelSrvc:
    def __init__(self, statements: EntitiesStms, db_operations: Operations) -> None:
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntitiesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_entity(
        self,
        entity_uuid: UUID4,
        entity_data: EntitiesDel,
        db: AsyncSession,
    ):
        statement: update = self._statements.update_entity(
            entity_uuid=entity_uuid, entity_data=entity_data
        )
        entity: EntitiesDelRes = await self._db_ops.return_one_row(
            service=cnst.ENTITIES_DEL_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=entity, exception=EntityNotExist)
