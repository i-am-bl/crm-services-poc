from typing import List

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.products as s_products
from app.database.database import Operations, get_db
from app.services.products import ProductsServices
from app.service_utils import pagination_offset

serv_products_r = ProductsServices.ReadService()
serv_products_c = ProductsServices.CreateService()
serv_products_u = ProductsServices.UpdateService()
serv_products_d = ProductsServices.DelService()

router = APIRouter()


@router.get(
    "/v1/product-management/products/{product_uuid}",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product(product_uuid: UUID4, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        product = await serv_products_r.get_product(product_uuid=product_uuid, db=db)
        return product


@router.get(
    "/v1/product-management/products/",
    response_model=s_products.ProductsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_products(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
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
    product_data: s_products.ProductsCreate, db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        product = await serv_products_c.create_product(product_data=product_data, db=db)
        return product


@router.put(
    "/v1/product-management/products/{product_uuid}",
    response_model=s_products.ProductsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_uuid: UUID4,
    product_data: s_products.ProductsUpdate,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
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
    product_uuid: UUID4,
    product_data: s_products.ProductsDel,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        product = await serv_products_d.soft_del_product(
            product_uuid=product_uuid, product_data=product_data, db=db
        )
        return product
