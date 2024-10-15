from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, routing, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.schemas.entities as s_entities
from app.database.database import get_db
from app.logger import logger
from app.services.entities import EntitiesServices
from app.service_utils import pagination_offset
from app.services.oauth2 import AuthService

serv_entities_c = EntitiesServices.CreateService()
serv_entities_r = EntitiesServices.ReadService()
serv_entities_u = EntitiesServices.UpdateService()
serv_entities_d = EntitiesServices.DelService()


router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entity(entity_uuid: UUID4, db: AsyncSession = Depends(get_db)):
    """get one entity"""
    async with db.begin():
        entity = await serv_entities_r.get_entity(entity_uuid=entity_uuid, db=db)
        return entity


@router.get(
    "/v1/entity-management/entities/",
    response_model=s_entities.EntitiesPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entities(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many entities"""
    async with db.begin():
        offset = pagination_offset(limit=limit, page=page)
        total_count = await serv_entities_r.get_entity_ct(db=db)
        entities = await serv_entities_r.get_entities(limit=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "entities": entities,
        }


@router.post(
    "/v1/entity-management/entities/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_entity(
    entity_data: s_entities.EntitiesCreate,
    db: AsyncSession = Depends(get_db),
    user_uuid: UUID4 = Depends(AuthService.get_current_user),
):
    """create one entity"""
    async with db.begin():
        entity = await serv_entities_c.create_entity(entity_data=entity_data, db=db)
        return entity


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_200_OK,
)
async def update_entity(
    entity_uuid: UUID4,
    entity_data: s_entities.EntitiesUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one entity"""
    async with db.begin():
        entity = await serv_entities_u.update_entity(
            entity_uuid=entity_uuid, entity_data=entity_data, db=db
        )
        return entity


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_entity(
    entity_uuid: UUID4,
    entity_data: s_entities.EntitiesDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one entity"""
    async with db.begin():
        entity = await serv_entities_d.soft_del_entity(
            entity_uuid=entity_uuid, entity_data=entity_data, db=db
        )
        return entity
