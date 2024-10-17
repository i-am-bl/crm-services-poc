from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import entities as s_entities
from ...services.authetication import SessionService
from ...services.entities import EntitiesServices
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, EntityNotExist, EntityExists

serv_entities_c = EntitiesServices.CreateService()
serv_entities_r = EntitiesServices.ReadService()
serv_entities_u = EntitiesServices.UpdateService()
serv_entities_d = EntitiesServices.DelService()
serv_session = SessionService()


router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entity(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one entity"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            entity = await serv_entities_r.get_entity(entity_uuid=entity_uuid, db=db)
            return entity
    except EntityNotExist:
        raise EntityNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/entity-management/entities/",
    response_model=s_entities.EntitiesPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entities(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many entities"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            offset = pagination_offset(limit=limit, page=page)
            total_count = await serv_entities_r.get_entity_ct(db=db)
            entities = await serv_entities_r.get_entities(
                limit=limit, offset=offset, db=db
            )
            return {
                "total": total_count,
                "page": page,
                "limit": limit,
                "has_more": total_count > (page * limit),
                "entities": entities,
            }
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/entity-management/entities/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_entity(
    request: Request,
    response: Response,
    entity_data: s_entities.EntitiesCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one entity"""
    try:
        async with db.begin():

            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=entity_data, sys_user=sys_user)
            entity = await serv_entities_c.create_entity(entity_data=entity_data, db=db)
            return entity
    except EntityNotExist:
        raise EntityNotExist()
    except EntityNotExist:
        raise EntityExists()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_200_OK,
)
async def update_entity(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    entity_data: s_entities.EntitiesUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one entity"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=entity_data, sys_user=sys_user)
            entity = await serv_entities_u.update_entity(
                entity_uuid=entity_uuid, entity_data=entity_data, db=db
            )
            return entity
    except EntityNotExist:
        raise EntityNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_entity(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    entity_data: s_entities.EntitiesDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one entity"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=entity_data, sys_user=sys_user)
            entity = await serv_entities_d.soft_del_entity(
                entity_uuid=entity_uuid, entity_data=entity_data, db=db
            )
            return entity
    except EntityNotExist:
        raise EntityNotExist()
    except Exception:
        raise UnhandledException()
