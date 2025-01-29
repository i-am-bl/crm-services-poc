from typing import Annotated, Literal, Optional, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...constants.enums import EntityTypes
from ...database.database import get_db, transaction_manager
from ...exceptions import (
    EntityDataInvalid,
    EntityIndivDataInvalid,
    EntityNonIndivDataInvalid,
    EntityNotExist,
    EntityTypeInvalid,
    IndividualNotExist,
    NonIndividualNotExist,
)
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.entities import (
    EntitiesCreate,
    EntitiesDel,
    EntitiesPgRes,
    EntitiesCombinedRes,
)
from ...services.authetication import SessionService, TokenService
from ...services.entities import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...utilities import sys_values
from ...utilities.utilities import Pagination as pg

serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{entity_uuid}/",
    response_model=EntitiesCombinedRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist])
async def get_entity(
    entity_uuid: UUID4,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
    entities_read_srvc: ReadSrvc = Depends(services_container["entities_read"]),
) -> EntitiesCombinedRes:
    """
    Get one entity by entity_uuid.

    A type is not needed.
    Response will conditionally return the applicable payload.
    """
    # TODO: Refactor how we are handling conditional responses.
    async with transaction_manager(db=db):
        entity = await entities_read_srvc.get_entity(entity_uuid=entity_uuid, db=db)
        if entity.type == EntityTypes.ENTITY_INDIVIDUAL:
            # TODO: refactor service and how we aggregate conditionally
            individual = await serv_indiv_r.get_individual(
                entity_uuid=entity.uuid, db=db
            )
            return EntitiesCombinedRes(entity=entity, individual=individual)
        elif entity.type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            # TODO: Refactor how we are handling conditional responses.
            non_individual = await serv_non_indiv_r.get_non_individual(
                entity_uuid=entity.uuid, db=db
            )

            return EntitiesCombinedRes(entity=entity, non_individual=non_individual)


@router.get(
    "/",
    response_model=EntitiesPgRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist, EntityTypeInvalid])
async def get_entities(
    response: Response,
    entity_type: Annotated[
        EntityTypes,
        Literal[EntityTypes.ENTITY_INDIVIDUAL, EntityTypes.ENTITY_NON_INDIVIDUAL],
    ],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entities_read_srvc: ReadSrvc = Depends(services_container["entities_read"]),
) -> EntitiesPgRes:
    """
    Retrieve a list of entity by either individual or non-individual.
    """
    # TODO: revisit this all together
    async with transaction_manager(db=db):
        offset = pg.pagination_offset(limit=limit, page=page)
        if entity_type == EntityTypes.ENTITY_INDIVIDUAL:
            total_count = await serv_indiv_r.get_individuals_ct(db=db)
            individuals = await serv_indiv_r.get_individuals(
                limit=limit, offset=offset, db=db
            )
            has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
            return EntitiesPgRes(
                total=total_count,
                page=page,
                limit=limit,
                has_more=has_more,
                individuals=individuals,
            )
        elif entity_type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            total_count = await serv_non_indiv_r.get_non_individuals_ct(db=db)
            non_individuals = await serv_non_indiv_r.get_non_individuals(
                limit=limit, offset=offset, db=db
            )
            has_more = (pg.has_more(total_count=total_count, page=page, limit=limit),)
            return EntitiesPgRes(
                total=total_count,
                page=page,
                limit=limit,
                has_more=has_more,
                non_individuals=non_individuals,
            )
        else:
            raise EntityTypeInvalid()


@router.post(
    "/",
    response_model=EntitiesCombinedRes,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist, EntityTypeInvalid])
async def create_entity(
    response: Response,
    entity_type: Annotated[
        EntityTypes,
        Literal[EntityTypes.ENTITY_INDIVIDUAL, EntityTypes.ENTITY_NON_INDIVIDUAL],
    ],
    individual_data: Optional[s_indiv.IndividualsCreate] = None,
    non_individual_data: Optional[s_non_indiv.NonIndividualsCreate] = None,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entities_creates_srvc: CreateSrvc = Depends(services_container["entities_create"]),
) -> EntitiesCombinedRes:
    # TODO: Revisit this all together
    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_data = EntitiesCreate(type=entity_type)
        sys_values.sys_created_by(data=entity_data, sys_user=sys_user.uuid)
        entity = await entities_creates_srvc.create_entity(
            entity_data=entity_data, db=db
        )
        await db.flush()
        if entity_type == EntityTypes.ENTITY_INDIVIDUAL:
            if not individual_data:
                raise EntityIndivDataInvalid()
            else:
                sys_values.sys_created_by(sys_user=sys_user.uuid, data=individual_data)
                setattr(individual_data, "entity_uuid", entity.uuid)
                individual = await serv_indiv_c.create_individual(
                    entity_uuid=entity.uuid, individual_data=individual_data, db=db
                )
                await db.flush()
                return EntitiesCombinedRes(entity=entity, individual=individual)
        elif entity_type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            if not non_individual_data:
                raise EntityNonIndivDataInvalid()
            else:
                sys_values.sys_created_by(
                    sys_user=sys_user.uuid, data=non_individual_data
                )
                setattr(non_individual_data, "entity_uuid", entity.uuid)
                non_individual = (
                    await serv_non_indiv_c.create_non_individual(
                        entity_uuid=entity.uuid,
                        non_individual_data=non_individual_data,
                        db=db,
                    ),
                )
                return EntitiesCombinedRes(entity=entity, non_individual=non_individual)
        elif entity_type not in [
            EntityTypes.ENTITY_INDIVIDUAL,
            EntityTypes.ENTITY_NON_INDIVIDUAL,
        ]:
            raise EntityTypeInvalid()


@router.put(
    "/{entity_uuid}/",
    response_model=EntitiesCombinedRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions(
    [
        EntityNotExist,
        IndividualNotExist,
        NonIndividualNotExist,
        EntityIndivDataInvalid,
        EntityNonIndivDataInvalid,
        EntityDataInvalid,
    ]
)
async def update_entity(
    response: Response,
    entity_uuid: UUID4,
    entity_type: Annotated[
        EntityTypes,
        Literal[EntityTypes.ENTITY_INDIVIDUAL, EntityTypes.ENTITY_NON_INDIVIDUAL],
    ],
    individual_data: Optional[s_indiv.IndividualsUpdate] = None,
    non_individual_data: Optional[s_non_indiv.NonIndividualsUpdate] = None,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entities_read_srvc: ReadSrvc = Depends(services_container["entities_read"]),
) -> EntitiesCombinedRes:
    """
    Update one entity by entity_uuid.
    """
    # TODO: Revisit this logic
    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity = await entities_read_srvc.get_entity(entity_uuid=entity_uuid, db=db)
        await db.flush()
        if entity_type == EntityTypes.ENTITY_INDIVIDUAL:
            if not individual_data:
                raise EntityIndivDataInvalid()
            else:
                SetSys.sys_updated_by(data=individual_data, sys_user=sys_user)
                individual = await serv_indiv_u.update_individual(
                    entity_uuid=entity_uuid,
                    individual_data=individual_data,
                    db=db,
                )
                return EntitiesCombinedRes(entity=entity, individual=individual)
        elif entity_type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            if not non_individual_data:
                raise EntityNonIndivDataInvalid()
            else:
                SetSys.sys_updated_by(data=non_individual_data, sys_user=sys_user)
                non_individual = await serv_non_indiv_u.update_non_individual(
                    entity_uuid=entity_uuid,
                    non_individual_data=non_individual_data,
                    db=db,
                )
                return EntitiesCombinedRes(entity=entity, non_individual=non_individual)
        elif entity_type not in [
            EntityTypes.ENTITY_INDIVIDUAL,
            EntityTypes.ENTITY_NON_INDIVIDUAL,
        ]:
            raise EntityTypeInvalid()
        else:
            raise EntityDataInvalid()


@router.delete(
    "/{entity_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@serv_token.set_auth_cookie
@handle_exceptions(
    [
        EntityNotExist,
        IndividualNotExist,
        NonIndividualNotExist,
    ]
)
async def soft_del_entity(
    response: Response,
    entity_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entities_delete_srvc: DelSrvc = Depends(services_container["entities_delete"]),
) -> None:
    """
    Soft del one entity by entity_uuid.
    """
    # TODO: revisit this logic
    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_data = EntitiesDel()
        SetSys.sys_deleted_by(data=entity_data, sys_user=sys_user)
        entity = await entities_delete_srvc.soft_del_entity(
            entity_uuid=entity_uuid, entity_data=entity_data, db=db
        )
        await db.flush()
        if entity.type == EntityTypes.ENTITY_INDIVIDUAL:
            individual_data = s_indiv.IndividualsDel()
            SetSys.sys_deleted_by(data=individual_data, sys_user=sys_user)
            await serv_indiv_d.soft_del_individual(
                entity_uuid=entity_uuid, individual_data=individual_data, db=db
            )
        elif entity.type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            non_individual_data = s_non_indiv.NonIndividualsDel()
            sys_values.sys_deleted_by(data=non_individual_data, sys_user=sys_user.uuid)
            await serv_non_indiv_d.soft_del_non_individual(
                entity_uuid=entity_uuid, non_individual_data=non_individual_data, db=db
            )
