from datetime import date, datetime
from typing import Optional, List

from pydantic import UUID4, BaseModel

from app.schemas._variables import TimeStamp


class AccountContracts(BaseModel):
    account_id: int
    account_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None


class AccountContractsCreate(AccountContracts):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class AccountContractsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class AccountContractsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class AccountContractsRepsone(BaseModel):
    id: int
    uuid: UUID4
    account_id: int
    account_uuid: UUID4
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class AccountContractsPagRepsone(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    account_contracts: List[AccountContractsRepsone]


class AccountContractsDelRepsone(AccountContractsRepsone):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True