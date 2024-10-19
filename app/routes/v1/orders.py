from typing import List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import OrderExists, OrderNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import orders as s_orders
from ...services.authetication import SessionService, TokenService
from ...services.orders import OrdersServices
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_orders_r = OrdersServices.ReadService()
serv_orders_c = OrdersServices.CreateService()
serv_orders_u = OrdersServices.UpdateService()
serv_orders_d = OrdersServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderNotExist])
async def get_order(
    response: Response,
    order_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_orders.OrdersResponse:
    """get one order"""

    async with transaction_manager(db=db):
        order = await serv_orders_r.get_order(order_uuid=order_uuid, db=db)
        return order


@router.get(
    "/v1/order-management/orders/",
    response_model=s_orders.OrdersPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderNotExist])
async def get_orders(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_orders.OrdersPagResponse:
    """get many orders"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_orders_r.get_orders_ct(db=db)
        orders = await serv_orders_r.get_orders(limt=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "orders": orders,
        }


@router.post(
    "/v1/order-management/orders/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderNotExist, OrderExists])
async def create_order(
    response: Response,
    order_data: s_orders.OrdersCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_orders.OrdersResponse:
    """create one order"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=order_data, sys_user=sys_user)
        order = await serv_orders_c.create_order(order_data=order_data, db=db)
        return order


@router.put(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderNotExist])
async def update_order(
    response: Response,
    order_uuid: UUID4,
    order_data: s_orders.OrdersUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_orders.OrdersResponse:
    """update one order"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=order_data, sys_user=sys_user)
        order = await serv_orders_u.update_order(
            order_uuid=order_uuid, order_data=order_data, db=db
        )
        return order


@router.delete(
    "/v1/order-management/orders/{order_uuid}/",
    response_model=s_orders.OrdersDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderNotExist])
async def soft_del_order(
    response: Response,
    order_uuid: UUID4,
    order_data: s_orders.OrdersDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_orders.OrdersDelResponse:
    """soft delete one order"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=order_data, sys_user=sys_user)
        order = await serv_orders_d.soft_del_order(
            order_uuid=order_uuid, order_data=order_data, db=db
        )
        return order
