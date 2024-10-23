from typing import List, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import ProductListItemExists, ProductListItemNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import product_list_items as s_product_list_items
from ...services.authetication import SessionService, TokenService
from ...services.product_list_items import ProductListItemsSerivces
from ...utilities.set_values import SetSys
from ...utilities.utilities import Pagination as pg

serv_pli_r = ProductListItemsSerivces.ReadService()
serv_pli_c = ProductListItemsSerivces.CreateService()
serv_pli_u = ProductListItemsSerivces.UpdateService()
serv_pli_d = ProductListItemsSerivces.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{product_list_uuid}/product-list-items/{product_list_item_uuid}/",
    response_model=s_product_list_items.ProductListItemsRespone,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def get_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_product_list_items.ProductListItemsRespone:
    """get one product list item"""

    async with transaction_manager(db=db):
        return await serv_pli_r.get_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            db=db,
        )


@router.get(
    "/{product_list_uuid}/product-list-items/",
    response_model=s_product_list_items.ProductListItemsPagRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def get_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_product_list_items.ProductListItemsPagRespone:
    """
    Get active products linked to the product list.

    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_pli_r.get_product_list_items_ct(
            product_list_uuid=product_list_uuid, db=db
        )
        product_list_items = await serv_pli_r.get_product_list_items(
            product_list_uuid=product_list_uuid, limit=limit, offset=offset, db=db
        )
        has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_product_list_items.ProductListItemsPagRespone(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            product_list_items=product_list_items,
        )


@router.post(
    "/{product_list_uuid}/product-list-items/",
    response_model=List[s_product_list_items.ProductListItemsRespone],
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListItemNotExist, ProductListItemExists])
async def create_product_list_items(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_data: List[s_product_list_items.ProductListItemsCreate],
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> List[s_product_list_items.ProductListItemsRespone]:
    """
    Create product list item.

    This will create a link between the an existing product list and product.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by_ls(data=product_list_item_data, sys_user=sys_user)
        return await serv_pli_c.create_product_list_items(
            product_list_uuid=product_list_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )


@router.put(
    "/{product_list_uuid}/product-list-items/{product_list_item_uuid}/",
    response_model=s_product_list_items.ProductListItemsRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def update_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    product_list_item_data: s_product_list_items.ProductListItemsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_product_list_items.ProductListItemsRespone:
    """
    Update product list item.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=product_list_item_data, sys_user=sys_user)
        return await serv_pli_u.update_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )


@router.delete(
    "/{product_list_uuid}/product-list-items/{product_list_item_uuid}/",
    response_model=s_product_list_items.ProductListItemsDelRespone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListItemNotExist])
async def soft_del_product_list_item(
    response: Response,
    product_list_uuid: UUID4,
    product_list_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_product_list_items.ProductListItemsDelRespone:
    """
    Soft del one product list item.

    Removes link between product list and product.
    """

    async with transaction_manager(db=db):
        product_list_item_data = s_product_list_items.ProductListItemsDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=product_list_item_data, sys_user=sys_user)
        return await serv_pli_d.soft_del_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
            db=db,
        )
