from typing import List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import Operations, get_db
from ...schemas import products as s_products
from ...services.authetication import SessionService
from ...services.products import ProductsServices
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys

serv_products_r = ProductsServices.ReadService()
serv_products_c = ProductsServices.CreateService()
serv_products_u = ProductsServices.UpdateService()
serv_products_d = ProductsServices.DelService()
serv_session = SessionService()

router = APIRouter()


@router.get(
    "/v1/product-management/products/{product_uuid}",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    request: Request,
    response: Response,
    product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        _ = await serv_session.validate_session(
            request=request, response=response, db=db
        )
        product = await serv_products_r.get_product(product_uuid=product_uuid, db=db)
        return product


@router.get(
    "/v1/product-management/products/",
    response_model=s_products.ProductsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_products(
    request: Request,
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        _ = await serv_session.validate_session(
            request=request, response=response, db=db
        )
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_products_r.get_products_ct(db=db)
        products = await serv_products_r.get_products(limit=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "products": products,
        }


@router.post(
    "/v1/product-management/products/",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
async def create_product(
    request: Request,
    response: Response,
    product_data: s_products.ProductsCreate,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        sys_user = await serv_session.validate_session(
            request=request, response=response, db=db
        )
        SetSys.sys_created_by(data=product_data, sys_user=sys_user)
        product = await serv_products_c.create_product(product_data=product_data, db=db)
        return product


@router.put(
    "/v1/product-management/products/{product_uuid}",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    request: Request,
    response: Response,
    product_uuid: UUID4,
    product_data: s_products.ProductsUpdate,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        sys_user = await serv_session.validate_session(
            request=request, response=response, db=db
        )
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
async def soft_del_product(
    request: Request,
    response: Response,
    product_uuid: UUID4,
    product_data: s_products.ProductsDel,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        sys_user = await serv_session.validate_session(
            request=request, response=response, db=db
        )
        SetSys.sys_deleted_by(data=product_data, sys_user=sys_user)
        product = await serv_products_d.soft_del_product(
            product_uuid=product_uuid, product_data=product_data, db=db
        )
        return product
