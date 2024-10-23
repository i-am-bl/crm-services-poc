from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import IndividualExists, IndividualNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import individuals as s_individuals
from ...services.authetication import SessionService, TokenService
from ...services.individuals import IndividualsServices
from ...utilities.set_values import SetSys

serv_individuals_r = IndividualsServices.ReadService()
serv_individuals_c = IndividualsServices.CreateService()
serv_individuals_u = IndividualsServices.UpdateService()
serv_individuals_d = IndividualsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([IndividualNotExist])
async def get_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_individuals.IndividualsResponse:
    """get one individual"""

    async with transaction_manager(db=db):
        return await serv_individuals_r.get_individual(
            entity_uuid=entity_uuid, individual_uuid=individual_uuid, db=db
        )


@router.post(
    "/{entity_uuid}/individuals/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([IndividualNotExist, IndividualExists])
async def create_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_data: s_individuals.IndividualsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_individuals.IndividualsResponse:
    """create one individual"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=individual_data, sys_user=sys_user)
        return await serv_individuals_c.create_individual(
            entity_uuid=entity_uuid, individual_data=individual_data, db=db
        )


@router.put(
    "/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([IndividualNotExist])
async def update_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    individual_data: s_individuals.IndividualsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_individuals.IndividualsResponse:
    """update one individual"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=individual_data, sys_user=sys_user)
        return await serv_individuals_u.update_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=individual_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([IndividualNotExist])
async def soft_del_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_individuals.IndividualsDelResponse:
    """soft del one entity"""

    async with transaction_manager(db=db):
        individual_data = s_individuals.IndividualsDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=individual_data, sys_user=sys_user)
        return await serv_individuals_d.soft_del_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=individual_data,
            db=db,
        )
