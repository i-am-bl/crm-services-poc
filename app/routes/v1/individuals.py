from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import IndividualExists, IndividualNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.individuals import (
    IndividualsCreate,
    IndividualsUpdate,
    IndividualsRes,
    IndividualsDel,
)
from ...services.individuals import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session

router = APIRouter()


@router.get(
    "/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=IndividualsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([IndividualNotExist])
async def get_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    individuals_read_srvc: ReadSrvc = Depends(services_container["individuals_read"]),
) -> IndividualsRes:
    """get one individual"""

    async with transaction_manager(db=db):
        return await individuals_read_srvc.get_individual(
            entity_uuid=entity_uuid, individual_uuid=individual_uuid, db=db
        )


@router.post(
    "/{entity_uuid}/individuals/",
    response_model=IndividualsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([IndividualNotExist, IndividualExists])
async def create_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_data: IndividualsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    individuals_create_srvc: CreateSrvc = Depends(
        services_container["individuals_create"]
    ),
) -> IndividualsRes:
    """create one individual"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=individual_data, sys_user=sys_user.uuid)
        return await individuals_create_srvc.create_individual(
            entity_uuid=entity_uuid, individual_data=individual_data, db=db
        )


@router.put(
    "/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=IndividualsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([IndividualNotExist])
async def update_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    individual_data: IndividualsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(get_validated_session),
    individuals_update_srvc: UpdateSrvc = Depends(
        services_container["individuals_update"]
    ),
) -> IndividualsRes:
    """update one individual"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=individual_data, sys_user=sys_user.uuid)
        return await individuals_update_srvc.update_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=individual_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/individuals/{individual_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([IndividualNotExist])
async def soft_del_individual(
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    individuals_delete_srvc: DelSrvc = Depends(
        services_container["individuals_delete"]
    ),
) -> None:
    """soft del one entity"""

    async with transaction_manager(db=db):
        individual_data = IndividualsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=individual_data, sys_user=sys_user.uuid)
        return await individuals_delete_srvc.soft_del_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=individual_data,
            db=db,
        )
