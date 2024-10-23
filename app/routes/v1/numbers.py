from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import NumberExists, NumbersNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import numbers as s_numbers
from ...services.authetication import SessionService, TokenService
from ...services.numbers import NumbersServices
from ...utilities.set_values import SetSys
from ...utilities.utilities import Pagination as pg

router = APIRouter()

serv_num_c = NumbersServices.CreateService()
serv_num_r = NumbersServices.ReadService()
serv_num_u = NumbersServices.UpdateService()
serv_num_d = NumbersServices.DelService()
serv_session = SessionService()
serv_token = TokenService()


@router.get(
    "/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def get_number(
    response: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_numbers.NumbersResponse:
    """get one number by entity"""

    async with transaction_manager(db=db):
        return await serv_num_r.get_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            db=db,
        )


@router.get(
    "/{entity_uuid}/numbers/",
    response_model=s_numbers.NumbersPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def get_numbers(
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_numbers.NumbersPagResponse:
    """
    Get many phone numbers by entity.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_num_r.get_numbers_ct(entity_uuid=entity_uuid, db=db)
        numbers = await serv_num_r.get_numbers(
            entity_uuid=entity_uuid,
            limit=limit,
            offset=offset,
            db=db,
        )
        has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_numbers.NumbersPagResponse(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            numbers=numbers,
        )


@router.post(
    "/{entity_uuid}/numbers/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([NumbersNotExist, NumberExists])
async def create_number(
    response: Response,
    entity_uuid: UUID4,
    number_data: s_numbers.NumbersCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_numbers.NumbersResponse:
    """
    Create one phone number.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=number_data, sys_user=sys_user)
        return await serv_num_c.create_num(
            entity_uuid=entity_uuid, number_data=number_data, db=db
        )


@router.put(
    "/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def update_number(
    response: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    number_data: s_numbers.NumbersUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_numbers.NumbersResponse:
    """
    Update one phone number.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=number_data, sys_user=sys_user)
        return await serv_num_u.update_num(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
            db=db,
        )


@router.delete(
    "/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([NumbersNotExist])
async def soft_del_number(
    response: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_numbers.NumbersDelResponse:
    """
    Soft del one phone number.
    """

    async with transaction_manager(db=db):
        number_data = s_numbers.NumbersDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=number_data, sys_user=sys_user)
        return await serv_num_d.soft_del_num_eng(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
            db=db,
        )
