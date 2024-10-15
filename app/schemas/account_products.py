from datetime import date, datetime
from typing import Optional, List

from pydantic import UUID4, BaseModel
from sqlalchemy import Boolean

from app.schemas._variables import TimeStamp


class AccountProducts(BaseModel):
    account_id: int
    account_uuid: UUID4
    product_id: int
    product_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountProductsCreate(AccountProducts):
    sys_created_at: datetime = TimeStamp
    sys_created_at: Optional[int] = None


class AccountProductsUpdate(BaseModel):
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class AccountProductsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class AccountProductsRespone(AccountProducts):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class AccountProductsPagRespone(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    account_products: Optional[List[AccountProductsRespone]] = None


class AccountProductsDelRespone(AccountProductsRespone):
    sys_deleted_at: Optional[datetime] = None
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
