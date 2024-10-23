from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import AddressExists, AddressNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import addresses as s_addresses
from ...services.addresses import AddressesServices
from ...services.authetication import SessionService, TokenService
from ...utilities.set_values import SetField, SetSys
from ...utilities.utilities import Pagination as pg

serv_addresses_r = AddressesServices.ReadService()
serv_addresses_c = AddressesServices.CreateService()
serv_addresses_u = AddressesServices.UpdateService()
serv_addresses_d = AddressesServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=s_addresses.AddressesResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressNotExist])
async def get_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_addresses.AddressesResponse:
    """get one address"""

    async with transaction_manager(db=db):
        return await serv_addresses_r.get_address(
            parent_uuid=account_uuid,
            parent_table="accounts",
            address_uuid=address_uuid,
            db=db,
        )


@router.get(
    "/{account_uuid}/addresses/",
    response_model=s_addresses.AddressesPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressNotExist])
async def get_addresses(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_addresses.AddressesPagResponse:
    """
    Get many addresses by account_uuid.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_addresses_r.get_addresses_ct(
            parent_uuid=account_uuid, parent_table="accounts", db=db
        )
        addresses = await serv_addresses_r.get_addresses(
            parent_uuid=account_uuid,
            parent_table="accounts",
            offset=offset,
            limit=limit,
            db=db,
        )
        has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_addresses.AddressesPagResponse(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            addresses=addresses,
        )


@router.post(
    "/{account_uuid}/addresses/",
    response_model=s_addresses.AddressesResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressExists, AddressNotExist])
async def create_address(
    response: Response,
    account_uuid: UUID4,
    address_data: s_addresses.AddressesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_addresses.AddressesResponse:
    """
    Create one address.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(sys_user=sys_user, data=address_data)
        SetField.set_field_value(
            field="parent_table", value="accounts", data=address_data
        )
        return await serv_addresses_c.create_address(
            parent_uuid=account_uuid, address_data=address_data, db=db
        )


@router.put(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=s_addresses.AddressesResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressNotExist])
async def update_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    address_data: s_addresses.AddressesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_addresses.AddressesResponse:
    """
    Update one address.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(sys_user=sys_user, data=address_data)
        return await serv_addresses_u.update_address(
            parent_uuid=account_uuid,
            parent_table="accounts",
            address_uuid=address_uuid,
            address_data=address_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=s_addresses.AddressesDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressNotExist])
async def soft_del_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_addresses.AddressesDelResponse:
    """
    Soft del one address.
    """

    async with transaction_manager(db=db):
        address_data = s_addresses.AddressesDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(sys_user=sys_user, data=address_data)
        return await serv_addresses_d.soft_del_address(
            parent_uuid=account_uuid,
            parent_table="accounts",
            address_uuid=address_uuid,
            address_data=address_data,
            db=db,
        )
