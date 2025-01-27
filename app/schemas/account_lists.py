from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import TimeStamp
from .product_lists import ProductListsResponse


class AccountLists(BaseModel):
    account_uuid: UUID4
    product_list_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountListsCreate(AccountLists):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class AccountListsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class AccountListsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class AccountListsRes(BaseModel):
    id: int
    uuid: UUID4
    account_uuid: UUID4
    product_list_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class AccountListsPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_moare: bool
    product_lists: Optional[List[ProductListsResponse]] = None


class AccountListsDelRes(AccountListsRes):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
