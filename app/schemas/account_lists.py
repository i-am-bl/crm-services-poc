from datetime import date, datetime
from typing import Optional, List

from pydantic import UUID4, BaseModel

from app.schemas._variables import TimeStamp


class AccountLists(BaseModel):
    account_id: int
    account_uuid: UUID4
    product_list_id: int
    product_list_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountListsCreate(AccountLists):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class AccountListsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class AccountListsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class AccountListsResponse(BaseModel):
    id: int
    uuid: UUID4
    account_uuid: UUID4
    product_list_id: int
    product_list_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class AccountListsPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_moare: bool
    account_lists: Optional[List[AccountListsResponse]] = None


class AccountListsDelResponse(AccountListsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
