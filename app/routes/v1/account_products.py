from typing import List, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import (AccProductsExists, AccProductstNotExist,
                           ProductsNotExist)
from ...handlers.handler import handle_exceptions
from ...schemas import account_products as s_account_products
from ...services.account_products import AccountProductsServices
from ...services.authetication import SessionService, TokenService
from ...services.products import ProductsServices
from ...utilities.set_values import SetSys
from ...utilities.utilities import Pagination as pg

serv_acc_products_r = AccountProductsServices.ReadService()
serv_acc_products_c = AccountProductsServices.CreateService()
serv_acc_products_u = AccountProductsServices.UpdateService()
serv_acc_products_d = AccountProductsServices.DelService()
serv_prod_r = ProductsServices.ReadService()
serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsRespone,
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
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsRespone:
    """get one active allowed account product"""

    async with transaction_manager(db=db):
        return await serv_acc_products_r.get_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            db=db,
        )


@router.get(
    "/{account_uuid}/account-products/",
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
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsPagRespone:
    """
    Get all active products linked to the account.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_acc_products_r.get_account_product_ct(
            account_uuid=account_uuid, db=db
        )
        account_products = await serv_acc_products_r.get_account_products(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        product_uuids = []
        for value in account_products:
            product_uuids.append(value.product_uuid)
        products = await serv_prod_r.get_product_by_uuids(
            product_uuids=product_uuids, db=db
        )
        if not isinstance(products, list):
            products = [products]
        has_more = pg.has_more(total_count=total_count, limit=limit, page=page)

        return s_account_products.AccountProductsPagRespone(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            products=products,
        )


@router.post(
    "/{account_uuid}/account-products/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist, AccProductsExists])
async def create_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsCreate:
    """
    Create one link between an account an existing product.

    This does not create a product or an account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=account_product_data, sys_user=sys_user)
        return await serv_acc_products_c.create_account_product(
            account_uuid=account_uuid,
            account_product_data=account_product_data,
            db=db,
        )


@router.put(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def update_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsUpdate:
    """
    Update one link from an account to a product.
    """

    async with transaction_manager(db=db):
        sys_user, token = user_token
        SetSys.sys_updated_by(data=account_product_data, sys_user=sys_user)
        return await serv_acc_products_u.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsDelRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def soft_del_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsDel:
    """
    Soft del one link from the account to a product.
    """

    async with transaction_manager(db=db):
        account_product_data = s_account_products.AccountProductsDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=account_product_data, sys_user=sys_user)
        return await serv_acc_products_d.soft_del_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )
