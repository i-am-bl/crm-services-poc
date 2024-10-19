from typing import List

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import ProductsExists, ProductsNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import products as s_products
from ...services.authetication import SessionService, TokenService
from ...services.products import ProductsServices
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_products_r = ProductsServices.ReadService()
serv_products_c = ProductsServices.CreateService()
serv_products_u = ProductsServices.UpdateService()
serv_products_d = ProductsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/v1/product-management/products/{product_uuid}",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def get_product(
    response: Response,
    product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_products.ProductsResponse:

    async with transaction_manager(db=db):
        product = await serv_products_r.get_product(product_uuid=product_uuid, db=db)
        return product


@router.get(
    "/v1/product-management/products/",
    response_model=s_products.ProductsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def get_products(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_products.ProductsPagResponse:

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_products_r.get_products_ct(db=db)
        products = await serv_products_r.get_products(limit=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "products": products,
        }


@router.post(
    "/v1/product-management/products/",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductsNotExist, ProductsExists])
async def create_product(
    response: Response,
    product_data: s_products.ProductsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_products.ProductsResponse:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=product_data, sys_user=sys_user)
        product = await serv_products_c.create_product(product_data=product_data, db=db)
        return product


@router.put(
    "/v1/product-management/products/{product_uuid}",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def update_product(
    response: Response,
    product_uuid: UUID4,
    product_data: s_products.ProductsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_products.ProductsResponse:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=product_data, sys_user=sys_user)
        product = await serv_products_u.update_product(
            product_uuid=product_uuid, product_data=product_data, db=db
        )
        return product


@router.delete(
    "/v1/product-management/products/{product_uuid}",
    response_model=s_products.ProductsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def soft_del_product(
    response: Response,
    product_uuid: UUID4,
    product_data: s_products.ProductsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_products.ProductsDelResponse:

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=product_data, sys_user=sys_user)
        product = await serv_products_d.soft_del_product(
            product_uuid=product_uuid, product_data=product_data, db=db
        )
        return product
