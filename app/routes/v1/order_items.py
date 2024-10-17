from typing import List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import order_items as s_order_items
from ...services.authetication import SessionService
from ...services.order_items import OrderItemsServices
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, OrderItemExists, OrderItemNotExist


serv_oi_r = OrderItemsServices.ReadService()
serv_oi_c = OrderItemsServices.CreateService()
serv_oi_u = OrderItemsServices.UpdateService()
serv_oi_d = OrderItemsServices.DelService()
serv_session = SessionService()

router = APIRouter()


@router.get(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_item(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one order item"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            order_item = await serv_oi_r.get_order_item(
                order_uuid=order_uuid, order_item_uuid=order_item_uuid, db=db
            )
            return order_item
    except OrderItemNotExist:
        raise OrderItemNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/order-management/orders/{order_uuid}/order-items/",
    response_model=s_order_items.OrderItemsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_items(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get order items by order"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            offset = pagination_offset(page=page, limit=limit)
            total_count = await serv_oi_r.get_order_items_ct(
                order_uuid=order_uuid, db=db
            )
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
    except OrderItemNotExist:
        raise OrderItemNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/order-management/orders/{order_uuid}/order-items/",
    response_model=List[s_order_items.OrderItemsResponse],
    status_code=status.HTTP_200_OK,
)
async def create_order_item(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    order_item_data: List[s_order_items.OrderItemsCreate],
    db: AsyncSession = Depends(get_db),
):
    """create order item"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by_ls(data=order_item_data, sys_user=sys_user)
            order_item = await serv_oi_c.create_order_item(
                order_uuid=order_uuid, order_item_data=order_item_data, db=db
            )
            return order_item
    except OrderItemExists:
        raise OrderItemExists()
    except OrderItemNotExist:
        raise OrderItemNotExist()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_order_item(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    order_item_data: s_order_items.OrderItemsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update order item"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=order_item_data, sys_user=sys_user)
            order_item = await serv_oi_u.update_order_item(
                order_uuid=order_uuid,
                order_item_uuid=order_item_uuid,
                order_item_data=order_item_data,
                db=db,
            )
            return order_item
    except OrderItemNotExist:
        raise OrderItemNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_order_item(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    order_item_data: s_order_items.OrderItemsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del order item"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=order_item_data, sys_user=sys_user)
            order_item = await serv_oi_d.soft_del_order_item(
                order_uuid=order_uuid,
                order_item_uuid=order_item_uuid,
                order_item_data=order_item_data,
                db=db,
            )
            return order_item
    except OrderItemNotExist:
        raise OrderItemNotExist()
    except Exception:
        raise UnhandledException()
