from typing import List, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import ProductListItemExists, ProductListItemNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.product_list_items import (
    ProductListItemsCreate,
    ProductListItemsDel,
    ProductListItemsPgRes,
    ProductListItemsRes,
    ProductListItemsUpdate,
)
from ...services.product_list_items import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session

router = APIRouter()


@router.get(
    "/{product_list_uuid}/product-list-items/{product_list_item_uuid}/",
    response_model=ProductListItemsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def get_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    product_list_items_read_srvc: ReadSrvc = Depends(
        service_container["product_list_items_read"]
    ),
) -> ProductListItemsRes:
    """get one product list item"""

    async with transaction_manager(db=db):
        return await product_list_items_read_srvc.get_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            db=db,
        )


@router.get(
    "/{product_list_uuid}/product-list-items/",
    response_model=ProductListItemsPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def get_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    product_list_items_read_srvc: ReadSrvc = Depends(
        service_container["product_list_items_read"]
    ),
) -> ProductListItemsPgRes:
    """
    Get active products linked to the product list.

    """

    async with transaction_manager(db=db):
        return await product_list_items_read_srvc.paginated_product_list_items(
            product_list_uuid=product_list_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{product_list_uuid}/product-list-items/",
    response_model=List[ProductListItemsRes],
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([ProductListItemNotExist, ProductListItemExists])
async def create_product_list_items(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_data: List[ProductListItemsCreate],
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(get_validated_session),
    product_list_items_create_srvc: CreateSrvc = Depends(
        service_container["product_list_items_create"]
    ),
) -> List[ProductListItemsRes]:
    """
    Create product list item.

    This will create a link between the an existing product list and product.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(
            data=product_list_item_data, sys_user_uuid=sys_user.uuid
        )
        return await product_list_items_create_srvc.create_product_list_items(
            product_list_uuid=product_list_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )


@router.put(
    "/{product_list_uuid}/product-list-items/{product_list_item_uuid}/",
    response_model=ProductListItemsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def update_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    product_list_item_data: ProductListItemsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    product_list_items_update_srvc: UpdateSrvc = Depends(
        service_container["product_list_items_update"]
    ),
) -> ProductListItemsRes:
    """
    Update product list item.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(
            data=product_list_item_data, sys_user_uuid=sys_user.uuid
        )
        return await product_list_items_update_srvc.update_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )


@router.delete(
    "/{product_list_uuid}/product-list-items/{product_list_item_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def soft_del_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    product_list_items_delete_srvc: DelSrvc = Depends(
        service_container["product_list_items_delete"]
    ),
) -> None:
    """
    Soft del one product list item.

    Removes link between product list and product.
    """

    async with transaction_manager(db=db):
        product_list_item_data = ProductListItemsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(
            data=product_list_item_data, sys_user_uuid=sys_user.uuid
        )
        return await product_list_items_delete_srvc.soft_del_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )
