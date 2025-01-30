from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AddressExists, AddressNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.addresses import (
    AccountAddressesCreate,
    AddressesDel,
    AddressesDel,
    AddressesPgRes,
    AddressesRes,
    AddressesUpdate,
)
from ...services.addresses import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.authetication import SessionService, TokenService
from ...utilities import sys_values

serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=AddressesRes,
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
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    addresses_read_srvc: ReadSrvc = Depends(services_container["addresses_read"]),
) -> AddressesRes:
    """get one address"""

    async with transaction_manager(db=db):
        return await addresses_read_srvc.get_address(
            parent_uuid=account_uuid,
            parent_table="accounts",
            address_uuid=address_uuid,
            db=db,
        )


@router.get(
    "/{account_uuid}/addresses/",
    response_model=AddressesPgRes,
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
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    addresses_read_srvc: ReadSrvc = Depends(services_container["addresses_read"]),
) -> AddressesPgRes:
    """
    Get many addresses by account_uuid.
    """

    async with transaction_manager(db=db):
        return await addresses_read_srvc.paginated_addresses(
            parent_uuid=account_uuid,
            parent_table="accounts",
            page=page,
            limit=limit,
            db=db,
        )


@router.post(
    "/{account_uuid}/addresses/",
    response_model=AddressesRes,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressExists, AddressNotExist])
async def create_address(
    response: Response,
    account_uuid: UUID4,
    address_data: AccountAddressesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    addresses_create_srvc: CreateSrvc = Depends(services_container["addresses_create"]),
) -> AddressesRes:
    """
    Create one address.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(sys_user=sys_user.uuid, data=address_data)
        return await addresses_create_srvc.create_address(
            parent_uuid=account_uuid, address_data=address_data, db=db
        )


@router.put(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=AddressesRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressNotExist])
async def update_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    address_data: AddressesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    addresses_update_srvc: UpdateSrvc = Depends(services_container["addresses_update"]),
) -> AddressesRes:
    """
    Update one address.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(sys_user=sys_user.uuid, data=address_data)
        return await addresses_update_srvc.update_address(
            parent_uuid=account_uuid,
            parent_table="accounts",
            address_uuid=address_uuid,
            address_data=address_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressNotExist])
async def soft_del_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    addresses_delete_srvc: DelSrvc = Depends(services_container["addresses_delete"]),
) -> None:
    """
    Soft del one address.
    """

    async with transaction_manager(db=db):
        address_data = AddressesDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(sys_user=sys_user.uuid, data=address_data)
        return await addresses_delete_srvc.soft_del_address(
            parent_uuid=account_uuid,
            parent_table="accounts",
            address_uuid=address_uuid,
            address_data=address_data,
            db=db,
        )
