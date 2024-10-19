from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..constants import messages as msg
from ..database.database import Operations, get_db
from ..exceptions import EntityNotExist
from ..models import entities as m_entities
from ..schemas import entities as s_entities
from ..utilities.logger import logger
from ..utilities.utilities import DataUtils as di


class EntitiesModels:
    entities = m_entities.Entities


class EntitiesStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_entity(entity_uuid: UUID4):
            entities = EntitiesModels.entities
            statement = Select(entities).where(
                and_(entities.uuid == entity_uuid, entities.sys_deleted_at == None)
            )
            return statement

        @staticmethod
        def sel_entities(limit: int, offset: int):
            entities = EntitiesModels.entities
            statement = (
                Select(entities)
                .where(entities.sys_deleted_at == None)
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_entity_ct():
            entities = EntitiesModels.entities
            statement = (
                Select(func.count())
                .select_from(entities)
                .where(entities.sys_deleted_at == None)
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_entity(entity_uuid: UUID4, entity_data: object):
            entities = EntitiesModels.entities
            statement = (
                update(entities)
                .where(
                    and_(entities.uuid == entity_uuid, entities.sys_deleted_at == None)
                )
                .values(di.set_empty_strs_null(entity_data))
                .returning(entities)
            )
            return statement


class EntitiesServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_entity(
            self, entity_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = EntitiesStatements.SelStatements.sel_entity(
                entity_uuid=entity_uuid
            )
            entity = await Operations.return_one_row(
                service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=entity, exception=entity)

        async def get_entities(
            self,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntitiesStatements.SelStatements.sel_entities(
                limit=limit, offset=offset
            )
            entities = await Operations.return_all_rows(
                service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(instance=entities, exception=EntityNotExist)
            return entities

        async def get_entity_ct(self, db: AsyncSession = Depends(get_db)):
            statement = EntitiesStatements.SelStatements.sel_entity_ct()
            return await Operations.return_count(
                service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_entity(
            self,
            entity_data: s_entities.EntitiesCreate,
            db: AsyncSession = Depends(get_db),
        ):
            entities = EntitiesModels.entities
            entity = await Operations.add_instance(
                service=cnst.ENTITIES_CREATE_SERV,
                model=entities,
                data=entity_data,
                db=db,
            )
            return di.record_not_exist(instance=entity, exception=EntityNotExist)

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_entity(
            self,
            entity_uuid: UUID4,
            entity_data: s_entities.EntitiesUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntitiesStatements.UpdateStatements.update_entity(
                entity_uuid=entity_uuid, entity_data=entity_data
            )
            entity = await Operations.return_one_row(
                service=cnst.ENTITIES_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=entity, exception=EntityNotExist)

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_entity(
            self,
            entity_uuid: UUID4,
            entity_data: s_entities.EntitiesDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntitiesStatements.UpdateStatements.update_entity(
                entity_uuid=entity_uuid, entity_data=entity_data
            )
            entity = await Operations.return_one_row(
                service=cnst.ENTITIES_DEL_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=entity, exception=EntityNotExist)
