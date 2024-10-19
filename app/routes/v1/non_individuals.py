from typing import List

from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import NonIndividualExists, NonIndividualNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import non_individuals as s_non_individuals
from ...services.authetication import SessionService, TokenService
from ...services.non_individuals import NonIndividualsServices
from ...utilities.sys_users import SetSys

serv_non_indiv_r = NonIndividualsServices.ReadService()
serv_non_indiv_c = NonIndividualsServices.CreateService()
serv_non_indiv_u = NonIndividualsServices.UpdateService()
serv_non_indiv_d = NonIndividualsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()


router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=s_non_individuals.NonIndividualsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([NonIndividualNotExist])
async def get_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_non_individuals.NonIndividualsResponse:
    """get one non_individual"""

    async with transaction_manager(db=db):
        non_individual = await serv_non_indiv_r.get_non_individual(
            entity_uuid=entity_uuid, non_individual_uuid=non_individual_uuid, db=db
        )
        return non_individual


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/",
    response_model=s_non_individuals.NonIndividualsResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([NonIndividualNotExist, NonIndividualExists])
async def create_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_data: s_non_individuals.NonIndividualsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_non_individuals.NonIndividualsResponse:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=non_individual_data, sys_user=sys_user)
        non_individual = await serv_non_indiv_c.create_non_individual(
            entity_uuid=entity_uuid, non_individual_data=non_individual_data, db=db
        )
        return non_individual


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=s_non_individuals.NonIndividualsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([NonIndividualNotExist])
async def update_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    non_individual_data: s_non_individuals.NonIndividualsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_non_individuals.NonIndividualsResponse:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=non_individual_data, sys_user=sys_user)
        non_individual = await serv_non_indiv_u.update_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
            db=db,
        )
        return non_individual


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=s_non_individuals.NonIndividualsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([NonIndividualNotExist])
async def soft_del_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    non_individual_data: s_non_individuals.NonIndividualsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_non_individuals.NonIndividualsDelResponse:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=non_individual_data, sys_user=sys_user)
        non_individual = await serv_non_indiv_d.soft_del_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
            db=db,
        )
        return non_individual
