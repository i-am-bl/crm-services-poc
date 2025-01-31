from typing import List, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.orchestrators import container as orchs_container
from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AccProductsExists, AccProductstNotExist, ProductsNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...orchestrators.account_products import AccountProductsReadOrch
from ...schemas.account_products import (
    AccountProductsCreate,
    AccountProductsDel,
    AccountProductsInternalCreate,
    AccountProductsInternalUpdate,
    AccountProductsOrchPgRes,
    AccountProductsRes,
    AccountProductsUpdate,
)
from ...services import account_products as account_products_srvcs
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation


router = APIRouter()


@router.get(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=AccountProductsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def get_account_products(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_products_read_srvc: account_products_srvcs.ReadSrvc = Depends(
        services_container["account_products_read"]
    ),
) -> AccountProductsRes:
    """get one active allowed account product"""

    async with transaction_manager(db=db):
        return await account_products_read_srvc.get_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            db=db,
        )


@router.get(
    "/{account_uuid}/account-products/",
    response_model=AccountProductsOrchPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([AccProductstNotExist, ProductsNotExist])
async def get_account_products(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_products_read_orchs: AccountProductsReadOrch = Depends(
        orchs_container["account_products_read_orch"]
    ),
) -> AccountProductsOrchPgRes:
    """
    Get all active products linked to the account.
    """
    async with transaction_manager(db=db):
        return await account_products_read_orchs.paginated_products(
            account_uuid=account_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{account_uuid}/account-products/",
    response_model=AccountProductsRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([AccProductstNotExist, AccProductsExists])
async def create_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_data: AccountProductsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_products_create_srvc: account_products_srvcs.CreateSrvc = Depends(
        services_container["account_products_create"]
    ),
) -> AccountProductsCreate:
    """
    Create one link between an account an existing product.

    This does not create a product or an account.
    """

    sys_user, _ = user_token
    _account_product_data: AccountProductsInternalCreate = internal_schema_validation(
        data=account_product_data,
        schema=AccountProductsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await account_products_create_srvc.create_account_product(
            account_uuid=account_uuid,
            account_product_data=_account_product_data,
            db=db,
        )


@router.put(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=AccountProductsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def update_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: AccountProductsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_products_update_srvc: account_products_srvcs.UpdateSrvc = Depends(
        services_container["account_products_update"]
    ),
) -> AccountProductsUpdate:
    """
    Update one link from an account to a product.
    """
    sys_user, _ = user_token
    _account_product_data: AccountProductsInternalUpdate = internal_schema_validation(
        data=account_product_data,
        schema=AccountProductsInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        return await account_products_update_srvc.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=_account_product_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def soft_del_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_products_delete_srvc: account_products_srvcs.DelSrvc = Depends(
        services_container["account_products_delete"]
    ),
) -> AccountProductsDel:
    """
    Soft del one link from the account to a product.
    """
    sys_user, _ = user_token
    _account_product_data: AccountProductsDel = internal_schema_validation(
        schema=AccountProductsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):
        return await account_products_delete_srvc.soft_del_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=_account_product_data,
            db=db,
        )
