from typing import List, Tuple

from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import NonIndividualExists, NonIndividualNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.non_individuals import (
    NonIndividualsCreate,
    NonIndividualsDel,
    NonIndividualsRes,
    NonIndividualsUpdate,
)
from ...services.non_individuals import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session

router = APIRouter()


@router.get(
    "/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=NonIndividualsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([NonIndividualNotExist])
async def get_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    non_invdivuals_read_srvc: ReadSrvc = Depends(
        service_container["non_individuals_read"]
    ),
) -> NonIndividualsRes:
    """get one non_individual"""

    async with transaction_manager(db=db):
        return await non_invdivuals_read_srvc.get_non_individual(
            entity_uuid=entity_uuid, non_individual_uuid=non_individual_uuid, db=db
        )


# Deprecating this, the entities router operations will create all entities.
@router.post(
    "/{entity_uuid}/non-individuals/",
    response_model=NonIndividualsRes,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
    deprecated=True,
)
@set_auth_cookie
@handle_exceptions([NonIndividualNotExist, NonIndividualExists])
async def create_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_data: NonIndividualsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    non_individual_create_srvc: CreateSrvc = Depends(
        service_container["non_individuals_create"]
    ),
) -> NonIndividualsRes:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=non_individual_data, sys_user_uuid=sys_user.uuid)
        return await non_individual_create_srvc.create_non_individual(
            entity_uuid=entity_uuid, non_individual_data=non_individual_data, db=db
        )


@router.put(
    "/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=NonIndividualsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([NonIndividualNotExist])
async def update_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    non_individual_data: NonIndividualsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    non_individuals_update_srvc: UpdateSrvc = Depends(
        service_container["non_individuals_update"]
    ),
) -> NonIndividualsRes:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=non_individual_data, sys_user_uuid=sys_user.uuid)
        return await non_individuals_update_srvc.update_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([NonIndividualNotExist])
async def soft_del_non_individual(
    response: Response,
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    non_individuals_delete_srvc: DelSrvc = Depends(
        service_container["non_individuals_delete"]
    ),
) -> None:

    async with transaction_manager(db=db):
        non_individual_data = NonIndividualsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=non_individual_data, sys_user_uuid=sys_user.uuid)
        return await non_individuals_delete_srvc.soft_del_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
            db=db,
        )
