from typing import List

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.order_items as s_order_items
from app.database.database import get_db
from app.services.order_items import OrderItemsServices
from app.service_utils import pagination_offset

serv_oi_r = OrderItemsServices.ReadService()
serv_oi_c = OrderItemsServices.CreateService()
serv_oi_u = OrderItemsServices.UpdateService()
serv_oi_d = OrderItemsServices.DelService()

router = APIRouter()


@router.get(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_item(
    order_uuid: UUID4, order_item_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one order item"""
    async with db.begin():
        order_item = await serv_oi_r.get_order_item(
            order_uuid=order_uuid, order_item_uuid=order_item_uuid, db=db
        )
        return order_item


@router.get(
    "/v1/order-management/orders/{order_uuid}/order-items/",
    response_model=s_order_items.OrderItemsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_items(
    order_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get order items by order"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_oi_r.get_order_items_ct(order_uuid=order_uuid, db=db)
        order_items = await serv_oi_r.get_order_items(
            order_uuid=order_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "order_items": order_items,
        }


@router.post(
    "/v1/order-management/orders/{order_uuid}/order-items/",
    response_model=List[s_order_items.OrderItemsResponse],
    status_code=status.HTTP_200_OK,
)
async def create_order_item(
    order_uuid: UUID4,
    order_item_data: List[s_order_items.OrderItemsCreate],
    db: AsyncSession = Depends(get_db),
):
    """create order item"""
    async with db.begin():
        order_item = await serv_oi_c.create_order_item(
            order_uuid=order_uuid, order_item_data=order_item_data, db=db
        )
        return order_item


@router.put(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_order_item(
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    order_item_data: s_order_items.OrderItemsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update order item"""
    async with db.begin():
        order_item = await serv_oi_u.update_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=order_item_data,
            db=db,
        )
        return order_item


@router.delete(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_order_item(
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    order_item_data: s_order_items.OrderItemsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del order item"""
    async with db.begin():
        order_item = await serv_oi_d.soft_del_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=order_item_data,
            db=db,
        )
        return order_item
