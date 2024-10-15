from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.schemas._variables import ConstrainedStr, TimeStamp


class EntityAccounts(BaseModel):
    entity_id: int
    entity_uuid: UUID4
    account_id: int
    account_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class EntityAccountsCreate(EntityAccounts):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class EntityAccountsAccountCreate(BaseModel):
    entity_id: int
    entity_uuid: UUID4
    account_id: Optional[int] = None
    account_uuid: Optional[UUID4] = None
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class EntityAccountsUpdate(BaseModel):
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class EntityAccountsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class EntityAccountsResponse(EntityAccounts):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class EntityAccountsPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    entity_accounts: Optional[List[EntityAccountsResponse]] = None


class EntityAccountsDelResponse(EntityAccountsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
