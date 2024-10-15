from datetime import date, datetime
from typing import Optional, List

from pydantic import UUID4, BaseModel

from app.schemas._variables import ConstrainedStr, TimeStamp


class Accounts(BaseModel):
    name: Optional[ConstrainedStr] = None
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountsCreate(Accounts):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class AccountsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class AccountsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class AccountsResponse(Accounts):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class AccountsPagResponse(Accounts):
    total: int
    page: int
    limit: int
    has_more: bool
    accounts: List[AccountsResponse]

    class Config:
        from_attributes = True


class AccountsDelResponse(AccountsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
