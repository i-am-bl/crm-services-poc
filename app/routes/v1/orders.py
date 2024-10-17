from typing import List

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.orders as s_orders
from app.database.database import get_db
from app.services.orders import OrdersServices
from app.service_utils import pagination_offset

serv_orders_r = OrdersServices.ReadService()
serv_orders_c = OrdersServices.CreateService()
serv_orders_u = OrdersServices.UpdateService()
serv_orders_d = OrdersServices.DelService()
router = APIRouter()


@router.get(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order(order_uuid: UUID4, db: AsyncSession = Depends(get_db)):
    """get one order"""
    async with db.begin():
        order = await serv_orders_r.get_order(order_uuid=order_uuid, db=db)
        return order


@router.get(
    "/v1/order-management/orders/",
    response_model=s_orders.OrdersPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_orders(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many orders"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_orders_r.get_orders_ct(db=db)
        orders = await serv_orders_r.get_orders(limt=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "orders": orders,
        }


@router.post(
    "/v1/order-management/orders/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: s_orders.OrdersCreate, db: AsyncSession = Depends(get_db)
):
    """create one order"""
    async with db.begin():
        order = await serv_orders_c.create_order(order_data=order_data, db=db)
        return order


@router.put(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_200_OK,
)
async def update_order(
    order_uuid: UUID4,
    order_data: s_orders.OrdersUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one order"""
    async with db.begin():
        order = await serv_orders_u.update_order(
            order_uuid=order_uuid, order_data=order_data, db=db
        )
        return order


@router.delete(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_order(
    order_uuid: UUID4,
    order_data: s_orders.OrdersDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete one order"""
    async with db.begin():
        order = await serv_orders_d.soft_del_order(
            order_uuid=order_uuid, order_data=order_data, db=db
        )
        return order
