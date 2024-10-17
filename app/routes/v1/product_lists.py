from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.product_lists as s_product_lists
from app.database.database import get_db
from app.services.product_lists import ProductListsServices
from app.service_utils import pagination_offset


serv_product_lists_r = ProductListsServices.ReadService()
serv_product_lists_c = ProductListsServices.CreateService()
serv_product_lists_u = ProductListsServices.UpdateService()
serv_product_lists_d = ProductListsServices.DelService()


router = APIRouter()


@router.get(
    "/v1/product-management/product-lists/{product_list_uuid}",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product_list(
    product_list_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one product list"""
    async with db.begin():
        product_list = await serv_product_lists_r.get_product_list(
            product_list_uuid=product_list_uuid, db=db
        )
        return product_list


@router.get(
    "/v1/product-management/product-lists/",
    response_model=s_product_lists.ProductListsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product_lists(
    page: int = Query(default=10, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many product lists"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_product_lists_r.get_product_lists_ct(db=db)
        product_lists = await serv_product_lists_r.get_product_lists(
            limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "product_lists": product_lists,
        }


@router.post(
    "/v1/product-management/product-lists/",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_list(
    product_list_data: s_product_lists.ProductListsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create product list"""
    async with db.begin():
        product_list = await serv_product_lists_c.create_product_list(
            product_list_data=product_list_data, db=db
        )
        return product_list


@router.put(
    "/v1/product-management/product-lists/{product_list_uuid}",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product_list(
    product_list_uuid: UUID4,
    product_list_data: s_product_lists.ProductListsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update product list"""
    async with db.begin():
        product_list = await serv_product_lists_u.update_product_list(
            product_list_uuid=product_list_uuid,
            product_list_data=product_list_data,
            db=db,
        )
        return product_list


@router.delete(
    "/v1/product-management/product-lists/{product_list_uuid}",
    response_model=s_product_lists.ProductListsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_poduct_list(
    product_list_uuid: UUID4,
    product_list_data: s_product_lists.ProductListsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del product list"""
    async with db.begin():
        product_list = await serv_product_lists_d.soft_del_product_list(
            product_list_uuid=product_list_uuid,
            product_list_data=product_list_data,
            db=db,
        )
        return product_list
