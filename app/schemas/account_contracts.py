from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import TimeStamp


class AccountContracts(BaseModel):
    account_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountContractsCreate(AccountContracts):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class AccountContractsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class AccountContractsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class AccountContractsRes(BaseModel):
    id: int
    uuid: UUID4
    account_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class AccountContractsPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    account_contracts: List[AccountContractsRes]


class AccountContractsDelRes(AccountContractsRes):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
