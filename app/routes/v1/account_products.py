from typing import List

from fastapi import APIRouter, Depends, status, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.account_products as s_account_products
from app.database.database import Operations, get_db
from app.services.account_products import AccountProductsServices
from app.service_utils import pagination_offset

serv_acc_products_r = AccountProductsServices.ReadService()
serv_acc_products_c = AccountProductsServices.CreateService()
serv_acc_products_u = AccountProductsServices.UpdateService()
serv_acc_products_d = AccountProductsServices.DelService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_200_OK,
)
async def get_account_products(
    account_uuid: UUID4, account_product_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one active allowed account product"""
    async with db.begin():
        account_product = await serv_acc_products_r.get_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            db=db,
        )
        return account_product


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-products/",
    # response_model=s_account_products.AccountProductsPagRespone,
    status_code=status.HTTP_200_OK,
)
async def get_account_products(
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get all active allowed account products"""
    async with db.begin():
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


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-products/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_201_CREATED,
)
async def create_account_product(
    account_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one allowed account product"""
    async with db.begin():
        account_product = await serv_acc_products_c.create_account_product(
            account_uuid=account_uuid, account_product_data=account_product_data, db=db
        )
        return account_product


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsRespone,
    status_code=status.HTTP_200_OK,
)
async def update_account_product(
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one account product"""
    async with db.begin():
        account_product = await serv_acc_products_u.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )
        return account_product


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/account-products/{account_product_uuid}/",
    response_model=s_account_products.AccountProductsDelRespone,
    status_code=status.HTTP_200_OK,
)
async def soft_del_account_product(
    account_uuid: UUID4,
    account_product_uuid: UUID4,
    account_product_data: s_account_products.AccountProductsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one account product"""
    async with db.begin():
        account_product = await serv_acc_products_d.soft_del_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
            db=db,
        )
        return account_product
