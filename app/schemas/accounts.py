from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import ConstrainedStr, TimeStamp


class Accounts(BaseModel):
    name: Optional[ConstrainedStr] = None
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountsCreate(Accounts):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class AccountsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class AccountsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class AccountsRes(BaseModel):
    id: int
    uuid: UUID4
    name: Optional[ConstrainedStr] = None
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class AccountsPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    accounts: List[AccountsRes]

    class Config:
        from_attributes = True


class AccountsDelRes(AccountsRes):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
