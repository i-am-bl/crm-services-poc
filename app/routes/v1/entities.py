from typing import Annotated, Literal, Optional, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...constants.enums import EntityTypes
from ...database.database import get_db, transaction_manager
from ...exceptions import (EntityDataInvalid, EntityIndivDataInvalid,
                           EntityNonIndivDataInvalid, EntityNotExist,
                           EntityTypeInvalid, IndividualNotExist,
                           NonIndividualNotExist)
from ...handlers.handler import handle_exceptions
from ...schemas import entities as s_entities
from ...schemas import individuals as s_indiv
from ...schemas import non_individuals as s_non_indiv
from ...services.authetication import SessionService, TokenService
from ...services.entities import EntitiesServices
from ...services.individuals import IndividualsServices
from ...services.non_individuals import NonIndividualsServices
from ...utilities.logger import logger
from ...utilities.set_values import SetField, SetSys
from ...utilities.utilities import Pagination as pg

serv_entities_c = EntitiesServices.CreateService()
serv_entities_r = EntitiesServices.ReadService()
serv_entities_u = EntitiesServices.UpdateService()
serv_entities_d = EntitiesServices.DelService()
serv_indiv_c = IndividualsServices.CreateService()
serv_indiv_r = IndividualsServices.ReadService()
serv_indiv_u = IndividualsServices.UpdateService()
serv_indiv_d = IndividualsServices.DelService()
serv_non_indiv_c = NonIndividualsServices.CreateService()
serv_non_indiv_r = NonIndividualsServices.ReadService()
serv_non_indiv_u = NonIndividualsServices.UpdateService()
serv_non_indiv_d = NonIndividualsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{entity_uuid}/",
    response_model=s_entities.EntitiesCombinedResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityNotExist])
async def get_entity(
    entity_uuid: UUID4,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entities.EntitiesCombinedResponse:
    """
    Get one entity by entity_uuid.

    A type is not needed.
    Response will conditionally return the applicable payload.
    """

    async with transaction_manager(db=db):
        entity = await serv_entities_r.get_entity(entity_uuid=entity_uuid, db=db)
        if entity.type == EntityTypes.ENTITY_INDIVIDUAL:
            individual = await serv_indiv_r.get_individual(
                entity_uuid=entity.uuid, db=db
            )
            return s_entities.EntitiesCombinedResponse(
                entity=entity, individual=individual
            )
        elif entity.type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            non_individual = await serv_non_indiv_r.get_non_individual(
                entity_uuid=entity.uuid, db=db
            )

            return s_entities.EntitiesCombinedResponse(
                entity=entity, non_individual=non_individual
            )


@router.get(
    "/",
    response_model=s_entities.EntitiesPagResponse,
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
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entities.EntitiesPagResponse:
    """
    Retrieve a list of entity by either individual or non-individual.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(limit=limit, page=page)
        if entity_type == EntityTypes.ENTITY_INDIVIDUAL:
            total_count = await serv_indiv_r.get_individuals_ct(db=db)
            individuals = await serv_indiv_r.get_individuals(
                limit=limit, offset=offset, db=db
            )
            has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
            return s_entities.EntitiesPagResponse(
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
            return s_entities.EntitiesPagResponse(
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
    response_model=s_entities.EntitiesCombinedResponse,
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesCombinedResponse:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_data = s_entities.EntitiesCreate(type=entity_type)
        SetSys.sys_created_by(data=entity_data, sys_user=sys_user)
        entity = await serv_entities_c.create_entity(entity_data=entity_data, db=db)
        await db.flush()
        if entity_type == EntityTypes.ENTITY_INDIVIDUAL:
            if not individual_data:
                raise EntityIndivDataInvalid()
            else:
                SetSys.sys_created_by(sys_user=sys_user, data=individual_data)
                SetField.set_field_value(
                    field="entity_uuid", value=entity.uuid, data=individual_data
                )
                individual = await serv_indiv_c.create_individual(
                    entity_uuid=entity.uuid, individual_data=individual_data, db=db
                )
                await db.flush()
                return s_entities.EntitiesCombinedResponse(
                    entity=entity, individual=individual
                )
        elif entity_type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            if not non_individual_data:
                raise EntityNonIndivDataInvalid()
            else:
                SetSys.sys_created_by(sys_user=sys_user, data=non_individual_data)
                SetField.set_field_value(
                    field="entity_uuid", value=entity.uuid, data=non_individual_data
                )
                non_individual = (
                    await serv_non_indiv_c.create_non_individual(
                        entity_uuid=entity.uuid,
                        non_individual_data=non_individual_data,
                        db=db,
                    ),
                )
                return s_entities.EntitiesCombinedResponse(
                    entity=entity, non_individual=non_individual
                )
        elif entity_type not in [
            EntityTypes.ENTITY_INDIVIDUAL,
            EntityTypes.ENTITY_NON_INDIVIDUAL,
        ]:
            raise EntityTypeInvalid()


@router.put(
    "/{entity_uuid}/",
    response_model=s_entities.EntitiesCombinedResponse,
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesCombinedResponse:
    """
    Update one entity by entity_uuid.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity = await serv_entities_r.get_entity(entity_uuid=entity_uuid, db=db)
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
                return s_entities.EntitiesCombinedResponse(
                    entity=entity, individual=individual
                )
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
                return s_entities.EntitiesCombinedResponse(
                    entity=entity, non_individual=non_individual
                )
        elif entity_type not in [
            EntityTypes.ENTITY_INDIVIDUAL,
            EntityTypes.ENTITY_NON_INDIVIDUAL,
        ]:
            raise EntityTypeInvalid()
        else:
            raise EntityDataInvalid()


@router.delete(
    "/{entity_uuid}/",
    response_model=s_entities.EntitiesCombinedDelResponse,
    status_code=status.HTTP_200_OK,
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_entities.EntitiesCombinedDelResponse:
    """
    Soft del one entity by entity_uuid.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_data = s_entities.EntitiesDel()
        SetSys.sys_deleted_by(data=entity_data, sys_user=sys_user)
        entity = await serv_entities_d.soft_del_entity(
            entity_uuid=entity_uuid, entity_data=entity_data, db=db
        )
        await db.flush()
        if entity.type == EntityTypes.ENTITY_INDIVIDUAL:
            individual_data = s_indiv.IndividualsDel()
            SetSys.sys_deleted_by(data=individual_data, sys_user=sys_user)
            individual = await serv_indiv_d.soft_del_individual(
                entity_uuid=entity_uuid, individual_data=individual_data, db=db
            )
            return s_entities.EntitiesCombinedDelResponse(
                entity=entity, individual=individual
            )
        elif entity.type == EntityTypes.ENTITY_NON_INDIVIDUAL:
            non_individual_data = s_non_indiv.NonIndividualsDel()
            SetSys.sys_deleted_by(data=non_individual_data, sys_user=sys_user)
            non_individual = await serv_non_indiv_d.soft_del_non_individual(
                entity_uuid=entity_uuid, non_individual_data=non_individual_data, db=db
            )
            return s_entities.EntitiesCombinedDelResponse(
                entity=entity, non_individual=non_individual
            )
