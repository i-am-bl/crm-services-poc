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
    IndividualsInternalUpdate,
    IndividualsUpdate,
    IndividualsRes,
    IndividualsDel,
)
from ...services.individuals import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

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


# Deprecating this, the entities router operations will create all entities.
# TODO: Remove this.
@router.post(
    "/{entity_uuid}/individuals/",
    response_model=IndividualsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    deprecated=True,
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

    sys_user, _ = user_token
    async with transaction_manager(db=db):
        sys_values.sys_created_by(data=individual_data, sys_user_uuid=sys_user.uuid)
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

    sys_user, _ = user_token
    _individual_data: IndividualsInternalUpdate = internal_schema_validation(
        data=individual_data,
        schema=IndividualsInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):

        return await individuals_update_srvc.update_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=_individual_data,
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
    sys_user, _ = user_token
    _individual_data: IndividualsDel = internal_schema_validation(
        schema=IndividualsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        return await individuals_delete_srvc.soft_del_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=_individual_data,
            db=db,
        )
