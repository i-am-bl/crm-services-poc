from typing import List

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import OrderItemExists, OrderItemNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import order_items as s_order_items
from ...services.authetication import SessionService, TokenService
from ...services.order_items import OrderItemsServices
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_oi_r = OrderItemsServices.ReadService()
serv_oi_c = OrderItemsServices.CreateService()
serv_oi_u = OrderItemsServices.UpdateService()
serv_oi_d = OrderItemsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def get_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_order_items.OrderItemsResponse:
    """get one order item"""

    async with transaction_manager(db=db):
        order_item = await serv_oi_r.get_order_item(
            order_uuid=order_uuid, order_item_uuid=order_item_uuid, db=db
        )
        return order_item


@router.get(
    "/v1/order-management/orders/{order_uuid}/order-items/",
    response_model=s_order_items.OrderItemsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def get_order_items(
    response: Response,
    order_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> List[s_order_items.OrderItemsPagResponse]:
    """get order items by order"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_oi_r.get_order_items_ct(order_uuid=order_uuid, db=db)
        order_items = await serv_oi_r.get_order_items(
            order_uuid=order_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "order_items": order_items,
        }


@router.post(
    "/v1/order-management/orders/{order_uuid}/order-items/",
    response_model=List[s_order_items.OrderItemsResponse],
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderItemNotExist, OrderItemExists])
async def create_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_data: List[s_order_items.OrderItemsCreate],
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> List[s_order_items.OrderItemsResponse]:
    """create order item"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by_ls(data=order_item_data, sys_user=sys_user)
        order_item = await serv_oi_c.create_order_item(
            order_uuid=order_uuid, order_item_data=order_item_data, db=db
        )
        return order_item


@router.put(
    "/v1/order-management/orders/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=s_order_items.OrderItemsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def update_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    order_item_data: s_order_items.OrderItemsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_order_items.OrderItemsResponse:
    """update order item"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=order_item_data, sys_user=sys_user)
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
@serv_token.set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def soft_del_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    order_item_data: s_order_items.OrderItemsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_order_items.OrderItemsDelResponse:
    """soft del order item"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=order_item_data, sys_user=sys_user)
        order_item = await serv_oi_d.soft_del_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=order_item_data,
            db=db,
        )
        return order_item
