from typing import List, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AccProductsExists, AccProductstNotExist, ProductsNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.account_products import (
    AccountProductsCreate,
    AccountProductsDel,
    AccountProductsPgRes,
    AccountProductsPgProductsRes,
    AccountProductsRes,
    AccountProductsUpdate,
)
from ...services import account_products as account_products_srvcs
from ...services.authetication import SessionService, TokenService
from ...services import products as products_srvcs
from ...utilities.set_values import SetSys
from ...utilities import pagination
from ...utilities import sys_values

serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=AccountProductsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def get_account_products(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
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
    response_model=AccountProductsPgProductsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist, ProductsNotExist])
async def get_account_products(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    account_products_read_srvc: account_products_srvcs.ReadSrvc = Depends(
        services_container["account_products_read"]
    ),
    products_read_srvcs: products_srvcs.ReadSrvc = Depends(
        services_container["products_read"]
    ),
) -> AccountProductsPgProductsRes:
    """
    Get all active products linked to the account.
    """
    # TODO: need an orchestrator for this
    async with transaction_manager(db=db):
        offset = pagination.page_offset(page=page, limit=limit)
        total_count = await account_products_read_srvc.get_account_product_ct(
            account_uuid=account_uuid, db=db
        )
        account_products = await account_products_read_srvc.get_account_products(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        product_uuids = []
        for value in account_products:
            product_uuids.append(value.product_uuid)
        products = await products_read_srvcs.get_product_by_uuids(
            product_uuids=product_uuids, db=db
        )
        if not isinstance(products, list):
            products = [products]
        has_more = pagination.has_more_items(
            total_count=total_count, limit=limit, page=page
        )

        return AccountProductsPgProductsRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            products=products,
        )


@router.post(
    "/{account_uuid}/account-products/",
    response_model=AccountProductsRes,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist, AccProductsExists])
async def create_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_data: AccountProductsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    account_products_create_srvc: account_products_srvcs.CreateSrvc = Depends(
        services_container["account_products_create"]
    ),
) -> AccountProductsCreate:
    """
    Create one link between an account an existing product.

    This does not create a product or an account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=account_product_data, sys_user=sys_user.uuid)
        return await account_products_create_srvc.create_account_product(
            account_uuid=account_uuid,
            account_product_data=account_product_data,
            db=db,
        )


@router.put(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=AccountProductsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def update_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: AccountProductsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    account_products_update_srvc: account_products_srvcs.UpdateSrvc = Depends(
        services_container["account_products_update"]
    ),
) -> AccountProductsUpdate:
    """
    Update one link from an account to a product.
    """

    async with transaction_manager(db=db):
        sys_user, token = user_token
        sys_values.sys_updated_by(data=account_product_data, sys_user=sys_user.uuid)
        return await account_products_update_srvc.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def soft_del_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    account_products_delete_srvc: account_products_srvcs.DelSrvc = Depends(
        services_container["account_products_delete"]
    ),
) -> AccountProductsDel:
    """
    Soft del one link from the account to a product.
    """

    async with transaction_manager(db=db):
        account_product_data = AccountProductsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=account_product_data, sys_user=sys_user.uuid)
        return await account_products_delete_srvc.soft_del_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )
