from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import ProductsExists, ProductsNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.products import (
    ProductsCreate,
    ProductsDel,
    ProductsInternalCreate,
    ProductsInternalUpdate,
    ProductsPgRes,
    ProductsUpdate,
    ProductsRes,
)
from ...services.products import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{product_uuid}",
    response_model=ProductsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def get_product(
    response: Response,
    product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    products_read_srvc: ReadSrvc = Depends(services_container["products_read"]),
) -> ProductsRes:

    async with transaction_manager(db=db):
        return await products_read_srvc.get_product(product_uuid=product_uuid, db=db)


@router.get(
    "/",
    response_model=ProductsPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def get_products(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    products_read_srvc: ReadSrvc = Depends(services_container["products_read"]),
) -> ProductsPgRes:
    """
    Get many active products.
    """

    async with transaction_manager(db=db):
        return await products_read_srvc.paginated_products(
            page=page, limit=limit, db=db
        )


@router.post(
    "/",
    response_model=ProductsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([ProductsNotExist, ProductsExists])
async def create_product(
    response: Response,
    product_data: ProductsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    products_create_srvc: CreateSrvc = Depends(services_container["products_create"]),
) -> ProductsRes:
    """
    Create one product.
    """
    sys_user, _ = user_token
    _product_data: ProductsInternalCreate = internal_schema_validation(
        data=product_data,
        schema=ProductsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):
        return await products_create_srvc.create_product(
            product_data=_product_data, db=db
        )


@router.put(
    "/{product_uuid}",
    response_model=ProductsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def update_product(
    response: Response,
    product_uuid: UUID4,
    product_data: ProductsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    products_update_srvc: UpdateSrvc = Depends(services_container["products_update"]),
) -> ProductsRes:
    """
    Update one product.
    """
    sys_user, _ = user_token
    _product_data: ProductsInternalUpdate = internal_schema_validation(
        data=product_data,
        schema=ProductsInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await products_update_srvc.update_product(
            product_uuid=product_uuid, product_data=_product_data, db=db
        )


@router.delete(
    "/{product_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([ProductsNotExist])
async def soft_del_product(
    response: Response,
    product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    products_delete_srvc: DelSrvc = Depends(services_container["products_delete"]),
) -> None:
    """
    Soft del one product.
    """
    sys_user, _ = user_token
    _product_data: ProductsDel = internal_schema_validation(
        schema=ProductsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await products_delete_srvc.soft_del_product(
            product_uuid=product_uuid, product_data=_product_data, db=db
        )
