from typing import List, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import OrderItemNotExist, OrderItemExists
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.order_items import (
    OrderItemsCreate,
    OrderItemsDel,
    OrderItemsInternalCreate,
    OrderItemsInternalUpdate,
    OrderItemsPgRes,
    OrderItemsRes,
    OrderItemsUpdate,
)
from ...services.order_items import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=OrderItemsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def get_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    order_items_read_srvc: ReadSrvc = Depends(services_container["order_items_read"]),
) -> OrderItemsRes:
    """
    Get one order item.
    """

    async with transaction_manager(db=db):
        return await order_items_read_srvc.get_order_item(
            order_uuid=order_uuid, order_item_uuid=order_item_uuid, db=db
        )


@router.get(
    "/{order_uuid}/order-items/",
    response_model=OrderItemsPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def get_order_items(
    response: Response,
    order_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    order_items_read_srvc: ReadSrvc = Depends(services_container["order_items_read"]),
) -> OrderItemsPgRes:
    """
    Get order items by order.
    """

    async with transaction_manager(db=db):
        return await order_items_read_srvc.paginated_order_items(
            order_uuid=order_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{order_uuid}/order-items/",
    response_model=List[OrderItemsRes],
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([OrderItemNotExist, OrderItemExists])
async def create_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_data: List[OrderItemsCreate],
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    order_items_create_srvc: CreateSrvc = Depends(
        services_container["order_items_create"]
    ),
) -> List[OrderItemsRes]:
    """
    Create order item.
    """

    sys_user, _ = user_token
    _order_item_data: List[OrderItemsInternalCreate] = internal_schema_validation(
        data=order_item_data,
        schema=OrderItemsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await order_items_create_srvc.create_order_item(
            order_uuid=order_uuid, order_item_data=_order_item_data, db=db
        )


@router.put(
    "/{order_uuid}/order-items/{order_item_uuid}/",
    response_model=OrderItemsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def update_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    order_item_data: OrderItemsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    order_items_update_srvc: UpdateSrvc = Depends(
        services_container["order_items_update"]
    ),
) -> OrderItemsRes:
    """
    Update order item.
    """

    sys_user, _ = user_token
    _order_item_data: OrderItemsInternalUpdate = internal_schema_validation(
        data=order_item_data,
        schema=OrderItemsInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await order_items_update_srvc.update_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=_order_item_data,
            db=db,
        )


@router.delete(
    "/{order_uuid}/order-items/{order_item_uuid}/",
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([OrderItemNotExist])
async def soft_del_order_item(
    response: Response,
    order_uuid: UUID4,
    order_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    order_items_delete_srvc: DelSrvc = Depends(
        services_container["order_items_delete"]
    ),
) -> None:
    """
    Soft del order item.
    """

    sys_user, _ = user_token
    _order_item_data: OrderItemsDel = internal_schema_validation(
        schema=OrderItemsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await order_items_delete_srvc.soft_del_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=_order_item_data,
            db=db,
        )
