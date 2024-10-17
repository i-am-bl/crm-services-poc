from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import product_lists as s_product_lists
from ...services.authetication import SessionService
from ...services.product_lists import ProductListsServices
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, ProductListExists, ProductListNotExist

serv_product_lists_r = ProductListsServices.ReadService()
serv_product_lists_c = ProductListsServices.CreateService()
serv_product_lists_u = ProductListsServices.UpdateService()
serv_product_lists_d = ProductListsServices.DelService()
serv_session = SessionService()

router = APIRouter()


@router.get(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product_list(
    request: Request,
    response: Response,
    product_list_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one product list"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            product_list = await serv_product_lists_r.get_product_list(
                product_list_uuid=product_list_uuid, db=db
            )
            return product_list
    except ProductListNotExist:
        raise ProductListNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/product-management/product-lists/",
    response_model=s_product_lists.ProductListsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product_lists(
    request: Request,
    response: Response,
    page: int = Query(default=10, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many product lists"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            offset = pagination_offset(page=page, limit=limit)
            total_count = await serv_product_lists_r.get_product_lists_ct(db=db)
            product_lists = await serv_product_lists_r.get_product_lists(
                limit=limit, offset=offset, db=db
            )
            return {
                "total": total_count,
                "page": page,
                "limit": limit,
                "has_more": total_count > (page * limit),
                "product_lists": product_lists,
            }
    except ProductListNotExist:
        raise ProductListNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/product-management/product-lists/",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_list(
    request: Request,
    response: Response,
    product_list_data: s_product_lists.ProductListsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create product list"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=product_list_data, sys_user=sys_user)
            product_list = await serv_product_lists_c.create_product_list(
                product_list_data=product_list_data, db=db
            )
            return product_list
    except ProductListExists:
        raise ProductListExists()
    except ProductListNotExist:
        raise ProductListNotExist()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=s_product_lists.ProductListsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product_list(
    request: Request,
    response: Response,
    product_list_uuid: UUID4,
    product_list_data: s_product_lists.ProductListsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update product list"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=product_list_data, sys_user=sys_user)
            product_list = await serv_product_lists_u.update_product_list(
                product_list_uuid=product_list_uuid,
                product_list_data=product_list_data,
                db=db,
            )
            return product_list
    except ProductListNotExist:
        raise ProductListNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/product-management/product-lists/{product_list_uuid}/",
    response_model=s_product_lists.ProductListsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_poduct_list(
    request: Request,
    response: Response,
    product_list_uuid: UUID4,
    product_list_data: s_product_lists.ProductListsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del product list"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=product_list_data, sys_user=sys_user)
            product_list = await serv_product_lists_d.soft_del_product_list(
                product_list_uuid=product_list_uuid,
                product_list_data=product_list_data,
                db=db,
            )
            return product_list
    except ProductListNotExist:
        raise ProductListNotExist()
    except Exception:
        raise UnhandledException()
