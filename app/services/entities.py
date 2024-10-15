from typing import Annotated, Literal, Optional
from xml.dom import ValidationErr

from fastapi import Depends, Query
from pydantic import UUID4
from sqlalchemy import Select, and_, func, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.messages as msg
import app.models.entities as m_entities
import app.schemas.entities as s_entities
from app.database.database import Operations, get_db
from app.logger import logger
from app.services.utilities import DataUtils as di


class EntitiesModels:
    entities = m_entities.Entities


class EntitiesStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_entity(entity_uuid: UUID4):
            entities = EntitiesModels.entities
            statement = Select(entities).where(entities.uuid == entity_uuid)
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
                .where(entities.uuid == entity_uuid)
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
            di.record_not_exist(model=entity)
            return entity

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
            di.record_not_exist(model=entities)
            return entities

        async def get_entity_ct(self, db: AsyncSession = Depends(get_db)):
            statement = EntitiesStatements.SelStatements.sel_entity_ct()
            entity_ct = await Operations.return_count(
                service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(model=entity_ct)
            return entity_ct

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
            di.record_not_exist(model=entity)
            return entity

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
            di.rec_not_exist_or_soft_del(model=entity)
            return entity

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
            di.record_not_exist(model=entity)
            return entity
