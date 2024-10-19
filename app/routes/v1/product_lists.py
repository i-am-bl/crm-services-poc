from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import ProductListExists, ProductListNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import product_lists as s_product_lists
from ...services.authetication import SessionService, TokenService
from ...services.product_lists import ProductListsServices
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_product_lists_r = ProductListsServices.ReadService()
serv_product_lists_c = ProductListsServices.CreateService()
serv_product_lists_u = ProductListsServices.UpdateService()
serv_product_lists_d = ProductListsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def get_product_list(
    response: Response,
    product_list_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_product_lists.ProductListsResponse:
    """get one product list"""

    async with transaction_manager(db=db):
        product_list = await serv_product_lists_r.get_product_list(
            product_list_uuid=product_list_uuid, db=db
        )
        return product_list


@router.get(
    "/v1/product-management/product-lists/",
    response_model=s_product_lists.ProductListsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def get_product_lists(
    response: Response,
    page: int = Query(default=10, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_product_lists.ProductListsPagResponse:
    """get many product lists"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_product_lists_r.get_product_lists_ct(db=db)
        product_lists = await serv_product_lists_r.get_product_lists(
            limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "product_lists": product_lists,
        }


@router.post(
    "/v1/product-management/product-lists/",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist, ProductListExists])
async def create_product_list(
    response: Response,
    product_list_data: s_product_lists.ProductListsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_product_lists.ProductListsResponse:
    """create product list"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=product_list_data, sys_user=sys_user)
        product_list = await serv_product_lists_c.create_product_list(
            product_list_data=product_list_data, db=db
        )
        return product_list


@router.put(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def update_product_list(
    response: Response,
    product_list_uuid: UUID4,
    product_list_data: s_product_lists.ProductListsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_product_lists.ProductListsResponse:
    """update product list"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=product_list_data, sys_user=sys_user)
        product_list = await serv_product_lists_u.update_product_list(
            product_list_uuid=product_list_uuid,
            product_list_data=product_list_data,
            db=db,
        )
        return product_list


@router.delete(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=s_product_lists.ProductListsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([ProductListNotExist])
async def soft_del_poduct_list(
    response: Response,
    product_list_uuid: UUID4,
    product_list_data: s_product_lists.ProductListsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_product_lists.ProductListsDelResponse:
    """soft del product list"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=product_list_data, sys_user=sys_user)
        product_list = await serv_product_lists_d.soft_del_product_list(
            product_list_uuid=product_list_uuid,
            product_list_data=product_list_data,
            db=db,
        )
        return product_list
