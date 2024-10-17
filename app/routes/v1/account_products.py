from typing import List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import Operations, get_db
from ...schemas import account_products as s_account_products
from ...services.account_products import AccountProductsServices
from ...services.authetication import SessionService
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, AccProductstNotExist, AccProductsExists

serv_acc_products_r = AccountProductsServices.ReadService()
serv_acc_products_c = AccountProductsServices.CreateService()
serv_acc_products_u = AccountProductsServices.UpdateService()
serv_acc_products_d = AccountProductsServices.DelService()
serv_session = SessionService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_200_OK,
)
async def get_account_products(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one active allowed account product"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            account_product = await serv_acc_products_r.get_account_product(
                account_uuid=account_uuid,
                account_product_uuid=account_product_uuid,
                db=db,
            )
            return account_product
    except AccProductstNotExist:
        raise AccProductstNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-products/",
    # response_model=s_account_products.AccountProductsPagRespone,
    status_code=status.HTTP_200_OK,
)
async def get_account_products(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get all active allowed account products"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            offset = pagination_offset(page=page, limit=limit)
            total_count = await serv_acc_products_r.get_account_product_ct(
                account_uuid=account_uuid, db=db
            )
            account_products = await serv_acc_products_r.get_account_products(
                account_uuid=account_uuid, limit=limit, offset=offset, db=db
            )
            return {
                "total": total_count,
                "page": page,
                "limit": limit,
                "has_more": total_count > (page * limit),
                "account_products": account_products,
            }
    except AccProductstNotExist:
        raise AccProductstNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-products/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_201_CREATED,
)
async def create_account_product(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one allowed account product"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=account_product_data, sys_user=sys_user)
            account_product = await serv_acc_products_c.create_account_product(
                account_uuid=account_uuid,
                account_product_data=account_product_data,
                db=db,
            )
            return account_product
    except AccProductstNotExist:
        raise AccProductstNotExist()
    except AccProductsExists:
        raise AccProductsExists()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_200_OK,
)
async def update_account_product(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one account product"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=account_product_data, sys_user=sys_user)
            account_product = await serv_acc_products_u.update_account_product(
                account_uuid=account_uuid,
                account_product_uuid=account_product_uuid,
                account_product_data=account_product_data,
                db=db,
            )
            return account_product
    except AccProductstNotExist:
        raise AccProductstNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsDelRespone,
    status_code=status.HTTP_200_OK,
)
async def soft_del_account_product(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one account product"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=account_product_data, sys_user=sys_user)
            account_product = await serv_acc_products_d.soft_del_account_product(
                account_uuid=account_uuid,
                account_product_uuid=account_product_uuid,
                account_product_data=account_product_data,
                db=db,
            )
            return account_product
    except AccProductstNotExist:
        raise AccProductstNotExist()
    except Exception:
        raise UnhandledException()
