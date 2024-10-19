from typing import List

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import AccProductsExists, AccProductstNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import account_products as s_account_products
from ...services.account_products import AccountProductsServices
from ...services.authetication import SessionService, TokenService
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_acc_products_r = AccountProductsServices.ReadService()
serv_acc_products_c = AccountProductsServices.CreateService()
serv_acc_products_u = AccountProductsServices.UpdateService()
serv_acc_products_d = AccountProductsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def get_account_products(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsRespone:
    """get one active allowed account product"""

    async with transaction_manager(db=db):
        account_product = await serv_acc_products_r.get_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            db=db,
        )
        return account_product


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-products/",
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def get_account_products(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsPagRespone:
    """get all active allowed account products"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_acc_products_r.get_account_product_ct(
            account_uuid=account_uuid, db=db
        )
        account_products = await serv_acc_products_r.get_account_products(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, limit=limit, page=page),
            "account_products": account_products,
        }


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-products/",
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsCreate:
    """create one allowed account product"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=account_product_data, sys_user=sys_user)
        account_product = await serv_acc_products_c.create_account_product(
            account_uuid=account_uuid,
            account_product_data=account_product_data,
            db=db,
        )
        return account_product


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsUpdate:
    """update one account product"""

    async with transaction_manager(db=db):
        sys_user, token = user_token
        SetSys.sys_updated_by(data=account_product_data, sys_user=sys_user)
        account_product = await serv_acc_products_u.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )
        return account_product


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsDelRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccProductstNotExist])
async def soft_del_account_product(
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_products.AccountProductsDel:
    """soft del one account product"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=account_product_data, sys_user=sys_user)
        account_product = await serv_acc_products_d.soft_del_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )
        return account_product
