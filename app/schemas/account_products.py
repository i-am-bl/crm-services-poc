from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import TimeStamp
from .products import ProductsRes


class AccountProducts(BaseModel):
    account_uuid: UUID4
    product_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountProductsCreate(AccountProducts):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class AccountProductsUpdate(BaseModel):
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class AccountProductsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class AccountProductsRes(BaseModel):
    id: int
    uuid: UUID4
    account_uuid: UUID4
    product_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class AccountProductsOrchPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    data: Optional[List[ProductsRes]] = None


class AccountProductsPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    # TODO: Standardize this to be data
    account_products: Optional[List[AccountProductsRes]] = None


class AccountProductsDelRes(AccountProductsRes):
    sys_deleted_at: Optional[datetime] = None
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
