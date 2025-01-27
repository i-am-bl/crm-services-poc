from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import TimeStamp


class Invoices(BaseModel):
    order_uuid: UUID4
    sys_value_status_uuid: Optional[UUID4] = None
    transacted_on: Optional[date] = None
    posted_on: Optional[date] = None
    paid_on: Optional[date] = None


class InvoicesCreate(Invoices):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class InvoicesUpdate(BaseModel):
    sys_value_status_uuid: Optional[UUID4] = None
    transacted_on: Optional[date] = None
    posted_on: Optional[date] = None
    paid_on: Optional[date] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None


class InvoicesDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class InvoicesRes(BaseModel):
    id: int
    uuid: UUID4
    order_uuid: UUID4
    sys_value_status_uuid: Optional[UUID4] = None
    transacted_on: Optional[date] = None
    posted_on: Optional[date] = None
    paid_on: Optional[date] = None
    sys_created_at: Optional[datetime] = None
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class InvoicesPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    invoices: Optional[List[InvoicesRes]] = None


class InvoicesDelRes(InvoicesRes):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
