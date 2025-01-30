from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import NumberExists, NumbersNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.numbers import (
    NumbersCreate,
    NumbersDel,
    NumbersPgRes,
    NumbersRes,
    NumbersUpdate,
)
from ...services.numbers import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session

router = APIRouter()


@router.get(
    "/{entity_uuid}/numbers/{number_uuid}/",
    response_model=NumbersRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def get_number(
    response: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(get_validated_session),
    numbers_read_srvc: ReadSrvc = Depends(services_container["numbers_read"]),
) -> NumbersRes:
    """get one number by entity"""

    async with transaction_manager(db=db):
        return await numbers_read_srvc.get_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            db=db,
        )


@router.get(
    "/{entity_uuid}/numbers/",
    response_model=NumbersPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def get_numbers(
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    numbers_read_srvc: ReadSrvc = Depends(services_container["numbers_read"]),
) -> NumbersPgRes:
    """
    Get many phone numbers by entity.
    """

    async with transaction_manager(db=db):
        return await numbers_read_srvc.paginated_numbers(
            entity_uuid=entity_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{entity_uuid}/numbers/",
    response_model=NumbersRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([NumbersNotExist, NumberExists])
async def create_number(
    response: Response,
    entity_uuid: UUID4,
    number_data: NumbersCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    numbers_create_srvc: CreateSrvc = Depends(services_container["numbers_create"]),
) -> NumbersRes:
    """
    Create one phone number.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=number_data, sys_user=sys_user.uuid)
        return await numbers_create_srvc.create_number(
            entity_uuid=entity_uuid, number_data=number_data, db=db
        )


@router.put(
    "/{entity_uuid}/numbers/{number_uuid}/",
    response_model=NumbersRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def update_number(
    response: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    number_data: NumbersUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    numbers_update_srvc: UpdateSrvc = Depends(services_container["numbers_update"]),
) -> NumbersRes:
    """
    Update one phone number.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=number_data, sys_user=sys_user.uuid)
        return await numbers_update_srvc.update_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/numbers/{number_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def soft_del_number(
    response: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    numbers_delete_srvc: DelSrvc = Depends(services_container["numbers_delete"]),
) -> None:
    """
    Soft del one phone number.
    """

    async with transaction_manager(db=db):
        number_data = NumbersDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=number_data, sys_user=sys_user.uuid)
        return await numbers_delete_srvc.soft_delete_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
            db=db,
        )
