from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import TimeStamp


class Orders(BaseModel):
    account_uuid: UUID4
    invoice_uuid: Optional[UUID4] = None
    owner_uuid: Optional[UUID4] = None
    approved_on: Optional[date] = None
    transacted_on: Optional[date] = None


class OrdersCreate(Orders):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class OrdersUpdate(BaseModel):
    owner_uuid: Optional[UUID4] = None
    approved_by_uuid: Optional[UUID4] = None
    approved_on: Optional[date] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class OrdersDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class OrdersResponse(BaseModel):
    id: int
    uuid: UUID4
    account_uuid: UUID4
    invoice_uuid: Optional[UUID4] = None
    owner_uuid: Optional[UUID4] = None
    approved_by: Optional[UUID4] = None
    approved_on: Optional[date] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class OrdersPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    orders: Optional[List[OrdersResponse]] = None


class OrdersDelResponse(OrdersResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
