from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import EntityNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import entities as s_entities
from ...services.authetication import SessionService, TokenService
from ...services.entities import EntitiesServices
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_entities_c = EntitiesServices.CreateService()
serv_entities_r = EntitiesServices.ReadService()
serv_entities_u = EntitiesServices.UpdateService()
serv_entities_d = EntitiesServices.DelService()
serv_session = SessionService()
serv_token = TokenService()


router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist])
async def get_entity(
    entity_uuid: UUID4,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesResponse:
    """get one entity"""

    async with transaction_manager(db=db):
        entity = await serv_entities_r.get_entity(entity_uuid=entity_uuid, db=db)
        return entity


@router.get(
    "/v1/entity-management/entities/",
    response_model=s_entities.EntitiesPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist])
async def get_entities(
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesPagResponse:
    """get many entities"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(limit=limit, page=page)

        total_count = await serv_entities_r.get_entity_ct(db=db)
        entities = await serv_entities_r.get_entities(limit=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "entities": entities,
        }


@router.post(
    "/v1/entity-management/entities/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist])
async def create_entity(
    response: Response,
    entity_data: s_entities.EntitiesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesResponse:
    """create one entity"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token

        SetSys.sys_created_by(data=entity_data, sys_user=sys_user)
        entity = await serv_entities_c.create_entity(entity_data=entity_data, db=db)
        return entity


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist])
async def update_entity(
    response: Response,
    entity_uuid: UUID4,
    entity_data: s_entities.EntitiesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesResponse:
    """update one entity"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token

        SetSys.sys_updated_by(data=entity_data, sys_user=sys_user)
        entity = await serv_entities_u.update_entity(
            entity_uuid=entity_uuid, entity_data=entity_data, db=db
        )
        return entity


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/",
    response_model=s_entities.EntitiesDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist])
async def soft_del_entity(
    response: Response,
    entity_uuid: UUID4,
    entity_data: s_entities.EntitiesDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesDel:
    """soft del one entity"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token

        SetSys.sys_deleted_by(data=entity_data, sys_user=sys_user)
        entity = await serv_entities_d.soft_del_entity(
            entity_uuid=entity_uuid, entity_data=entity_data, db=db
        )
        return entity
