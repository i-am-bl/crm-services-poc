from typing import List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import orders as s_orders
from ...services.authetication import SessionService
from ...services.orders import OrdersServices
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, OrderExists, OrderNotExist

serv_orders_r = OrdersServices.ReadService()
serv_orders_c = OrdersServices.CreateService()
serv_orders_u = OrdersServices.UpdateService()
serv_orders_d = OrdersServices.DelService()
serv_session = SessionService()
router = APIRouter()


@router.get(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one order"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            order = await serv_orders_r.get_order(order_uuid=order_uuid, db=db)
            return order
    except OrderNotExist:
        raise OrderNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/order-management/orders/",
    response_model=s_orders.OrdersPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_orders(
    request: Request,
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many orders"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
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
    except OrderNotExist:
        raise OrderNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/order-management/orders/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    request: Request,
    response: Response,
    order_data: s_orders.OrdersCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one order"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=order_data, sys_user=sys_user)
            order = await serv_orders_c.create_order(order_data=order_data, db=db)
            return order
    except OrderExists:
        raise OrderExists()
    except OrderNotExist:
        raise OrderNotExist()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_200_OK,
)
async def update_order(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    order_data: s_orders.OrdersUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one order"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=order_data, sys_user=sys_user)
            order = await serv_orders_u.update_order(
                order_uuid=order_uuid, order_data=order_data, db=db
            )
            return order
    except OrderNotExist:
        raise OrderNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_order(
    request: Request,
    response: Response,
    order_uuid: UUID4,
    order_data: s_orders.OrdersDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete one order"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=order_data, sys_user=sys_user)
            order = await serv_orders_d.soft_del_order(
                order_uuid=order_uuid, order_data=order_data, db=db
            )
            return order
    except OrderNotExist:
        raise OrderNotExist()
    except Exception:
        raise UnhandledException()
