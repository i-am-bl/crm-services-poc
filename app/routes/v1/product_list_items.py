from typing import List

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.product_list_items as s_product_list_items
from app.database.database import get_db
from app.services.product_list_items import ProductListItemsSerivces
from app.service_utils import pagination_offset

serv_pli_r = ProductListItemsSerivces.ReadService()
serv_pli_c = ProductListItemsSerivces.CreateService()
serv_pli_u = ProductListItemsSerivces.UpdateService()
serv_pli_d = ProductListItemsSerivces.DelService()

router = APIRouter()


@router.get(
    "/v1/product-management/product-lists/{product_list_uuid}/{product_list_item_uuid}/",
    response_model=s_product_list_items.ProductListItemsRespone,
    status_code=status.HTTP_200_OK,
)
async def get_product_list_item(
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one product list item"""
    async with db.begin():
        product_list_item = await serv_pli_r.get_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            db=db,
        )
        return product_list_item


@router.get(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=s_product_list_items.ProductListItemsPagRespone,
    status_code=status.HTTP_200_OK,
)
async def get_product_list_item(
    product_list_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get active product list items by product list"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_pli_r.get_product_list_items_ct(
            product_list_uuid=product_list_uuid, db=db
        )
        product_list_items = await serv_pli_r.get_product_list_items(
            product_list_uuid=product_list_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "product_list_items": product_list_items,
        }


@router.post(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=List[s_product_list_items.ProductListItemsRespone],
    status_code=status.HTTP_201_CREATED,
)
async def create_product_list_items(
    product_list_uuid: UUID4,
    product_list_item_data: List[s_product_list_items.ProductListItemsCreate],
    db: AsyncSession = Depends(get_db),
):
    """create product list item"""
    async with db.begin():
        product_list_item = await serv_pli_c.create_product_list_items(
            product_list_uuid=product_list_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )
        return product_list_item


@router.put(
    "/v1/product-management/product-lists/{product_list_uuid}/{product_list_item_uuid}/",
    response_model=s_product_list_items.ProductListItemsRespone,
    status_code=status.HTTP_200_OK,
)
async def update_product_list_item(
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    product_list_item_data: s_product_list_items.ProductListItemsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update product list item"""
    async with db.begin():
        product_list_item = await serv_pli_u.update_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )
        return product_list_item


@router.delete(
    "/v1/product-management/product-lists/{product_list_uuid}/{product_list_item_uuid}/",
    response_model=s_product_list_items.ProductListItemsDelRespone,
    status_code=status.HTTP_200_OK,
)
async def soft_del_product_list_item(
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    product_list_item_data: s_product_list_items.ProductListItemsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del product list item"""
    async with db.begin():
        product_list_item = await serv_pli_d.soft_del_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )
        return product_list_item
