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
from ...services.token import set_auth_cookie
from ...utilities.auth import get_validated_session
from ...utilities import sys_values

router = APIRouter()


@router.get(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=AddressesRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([AddressNotExist])
async def get_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    addresses_read_srvc: ReadSrvc = Depends(services_container["addresses_read"]),
) -> AddressesRes:
    """
    Retrieve a **single address** by account UUID and address UUID.

    This endpoint retrieves a specific address associated with a given account.
    It raises an exception if the address does not exist.

    ### Parameters:
    - **account_uuid** (UUID4): The UUID of the account to which the address belongs.
    - **address_uuid** (UUID4): The UUID of the address to retrieve.

    ### Returns:
    - **AddressesRes**: The address data that corresponds to the provided UUIDs.
    """
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
@set_auth_cookie
@handle_exceptions([AddressNotExist])
async def get_addresses(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    addresses_read_srvc: ReadSrvc = Depends(services_container["addresses_read"]),
) -> AddressesPgRes:
    """
    Retrieve a **list of addresses** for a specific account UUID.

    This endpoint retrieves a paginated list of addresses associated with a specified account UUID.
    It supports pagination through the `page` and `limit` query parameters.

    ### Parameters:
    - **account_uuid** (UUID4): The UUID of the account.
    - **page** (int, optional): The page number for pagination (default is 1).
    - **limit** (int, optional): The number of items per page (default is 10, max 100).

    ### Returns:
    - **AddressesPgRes**: A paginated list of addresses for the provided account UUID.
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
@set_auth_cookie
@handle_exceptions([AddressExists, AddressNotExist])
async def create_address(
    response: Response,
    account_uuid: UUID4,
    address_data: AccountAddressesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    addresses_create_srvc: CreateSrvc = Depends(services_container["addresses_create"]),
) -> AddressesRes:
    """
    **Create a new address** for the specified account UUID.

    This endpoint creates a new address for the given account UUID. The provided address data
    is validated, and any existing address conflicts are handled. The created address is returned
    with a 201 status code.

    ### Parameters:
    - **account_uuid** (UUID4): The UUID of the account to create the address for.
    - **address_data** (AccountAddressesCreate): The address data to be created.

    ### Returns:
    - **AddressesRes**: The created address data.
    """
    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(sys_user_uuid=sys_user.uuid, data=address_data)
        return await addresses_create_srvc.create_address(
            parent_uuid=account_uuid, address_data=address_data, db=db
        )


@router.put(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=AddressesRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([AddressNotExist])
async def update_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    address_data: AddressesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    addresses_update_srvc: UpdateSrvc = Depends(services_container["addresses_update"]),
) -> AddressesRes:
    """
    **Update an existing address** for the specified account and address UUIDs.

    This endpoint updates an existing address, specified by both the account UUID and address UUID.
    The address data is validated, and any necessary updates are applied. It raises an exception
    if the address does not exist.

    ### Parameters:
    - **account_uuid** (UUID4): The UUID of the account the address belongs to.
    - **address_uuid** (UUID4): The UUID of the address to be updated.
    - **address_data** (AddressesUpdate): The updated address data.

    ### Returns:
    - **AddressesRes**: The updated address data.
    """
    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(sys_user_uuid=sys_user.uuid, data=address_data)
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
@set_auth_cookie
@handle_exceptions([AddressNotExist])
async def soft_del_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    addresses_delete_srvc: DelSrvc = Depends(services_container["addresses_delete"]),
) -> None:
    """
    **Soft delete** an address for the specified account UUID and address UUID.

    This endpoint performs a soft deletion of an address, specified by both the account UUID
    and address UUID. The address will be marked as deleted, but not permanently removed
    from the database.

    ### Parameters:
    - **account_uuid** (UUID4): The UUID of the account the address belongs to.
    - **address_uuid** (UUID4): The UUID of the address to be deleted.

    ### Returns:
    - **None**: No content is returned on success (204 No Content).
    """
    async with transaction_manager(db=db):
        address_data = AddressesDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(sys_user_uuid=sys_user.uuid, data=address_data)
        return await addresses_delete_srvc.soft_del_address(
            parent_uuid=account_uuid,
            parent_table="accounts",
            address_uuid=address_uuid,
            address_data=address_data,
            db=db,
        )
