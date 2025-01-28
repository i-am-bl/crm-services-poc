from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import ProductListExists, ProductListNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.product_lists import (
    ProductListsCreate,
    ProductListsDel,
    ProductListsPgRes,
    ProductListsRes,
    ProductListsUpdate,
)
from ...services.authetication import SessionService, TokenService
from ...services.product_lists import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...utilities import sys_values

serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{product_list_uuid}/",
    response_model=ProductListsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def get_product_list(
    response: Response,
    product_list_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    product_lists_read_srvc: ReadSrvc = Depends(
        service_container["product_lists_read"]
    ),
) -> ProductListsRes:
    """get one product list"""

    async with transaction_manager(db=db):
        return await product_lists_read_srvc.get_product_list(
            product_list_uuid=product_list_uuid, db=db
        )


@router.get(
    "/",
    response_model=ProductListsPgRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def get_product_lists(
    response: Response,
    page: int = Query(default=10, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    product_lists_read_srvc: ReadSrvc = Depends(
        service_container["product_lists_read"]
    ),
) -> ProductListsPgRes:
    """
    Get many product lists.
    """

    async with transaction_manager(db=db):
        return await product_lists_read_srvc.paginated_product_lists(
            page=page, limit=limit, db=db
        )


@router.post(
    "/",
    response_model=ProductListsRes,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist, ProductListExists])
async def create_product_list(
    response: Response,
    product_list_data: ProductListsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    product_lists_create_srvc: CreateSrvc = Depends(
        service_container["product_lists_create"]
    ),
) -> ProductListsRes:
    """
    Create one product list.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=product_list_data, sys_user=sys_user.uuid)
        return await product_lists_create_srvc.create_product_list(
            product_list_data=product_list_data, db=db
        )


@router.put(
    "/{product_list_uuid}/",
    response_model=ProductListsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def update_product_list(
    response: Response,
    product_list_uuid: UUID4,
    product_list_data: ProductListsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    product_lists_update_srvc: UpdateSrvc = Depends(
        service_container["product_lists_update"]
    ),
) -> ProductListsRes:
    """
    Update one product list.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=product_list_data, sys_user=sys_user.uuid)
        return await product_lists_update_srvc.update_product_list(
            product_list_uuid=product_list_uuid,
            product_list_data=product_list_data,
            db=db,
        )


@router.delete(
    "/{product_list_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def soft_del_poduct_list(
    response: Response,
    product_list_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
    product_lists_delete_srvc: DelSrvc = Depends(
        service_container["product_lists_delete"]
    ),
) -> None:
    """
    Soft del one product list.
    """

    async with transaction_manager(db=db):
        product_list_data = ProductListsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=product_list_data, sys_user=sys_user.uuid)
        await product_lists_delete_srvc.soft_del_product_list(
            product_list_uuid=product_list_uuid,
            product_list_data=product_list_data,
            db=db,
        )
