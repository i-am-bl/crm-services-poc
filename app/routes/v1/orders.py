from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import OrderExists, OrderNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.orders import (
    OrdersCreate,
    OrdersDel,
    OrdersPgRes,
    OrdersUpdate,
    OrdersRes,
)
from ...services.orders import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session

router = APIRouter()


@router.get(
    "/{order_uuid}/",
    response_model=OrdersRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([OrderNotExist])
async def get_order(
    response: Response,
    order_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    orders_read_srvc: ReadSrvc = Depends(services_container["orders_read"]),
) -> OrdersRes:
    """
    Get one sales order.
    """

    async with transaction_manager(db=db):
        return await orders_read_srvc.get_order(order_uuid=order_uuid, db=db)


@router.get(
    "/",
    response_model=OrdersPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([OrderNotExist])
async def get_orders(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    orders_read_srvc: ReadSrvc = Depends(services_container["orders_read"]),
) -> OrdersPgRes:
    """
    Get many sales orders.
    """

    async with transaction_manager(db=db):
        return await orders_read_srvc.paginated_orders(page=page, limit=limit, db=db)


@router.post(
    "/",
    response_model=OrdersRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([OrderNotExist, OrderExists])
async def create_order(
    response: Response,
    order_data: OrdersCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    orders_create_srvc: CreateSrvc = Depends(services_container["orders_create"]),
) -> OrdersRes:
    """
    Create one sales order.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=order_data, sys_user=sys_user)
        return await orders_create_srvc.create_order(order_data=order_data, db=db)


@router.put(
    "/{order_uuid}/",
    response_model=OrdersRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([OrderNotExist])
async def update_order(
    response: Response,
    order_uuid: UUID4,
    order_data: OrdersUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    orders_update_srvc: UpdateSrvc = Depends(services_container["orders_update"]),
) -> OrdersRes:
    """
    Update one sales order.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=order_data, sys_user=sys_user)
        return await orders_update_srvc.update_order(
            order_uuid=order_uuid, order_data=order_data, db=db
        )


@router.delete(
    "/{order_uuid}/",
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([OrderNotExist])
async def soft_del_order(
    response: Response,
    order_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    orders_delete_srvc: DelSrvc = Depends(services_container["orders_delete"]),
) -> None:
    """
    Soft delete one sales order.
    """

    async with transaction_manager(db=db):
        order_data = OrdersDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=order_data, sys_user=sys_user.uuid)
        await orders_delete_srvc.soft_del_order(
            order_uuid=order_uuid, order_data=order_data, db=db
        )
