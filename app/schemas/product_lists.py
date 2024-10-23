from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import ConstrainedStr, TimeStamp


class ProductLists(BaseModel):
    owner_uuid: Optional[UUID4] = None
    name: ConstrainedStr
    start_on: Optional[date]
    end_on: Optional[date]


class ProductListsCreate(ProductLists):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class ProductListsUpdate(ProductLists):
    owner_uuid: Optional[UUID4] = None
    name: Optional[ConstrainedStr] = None
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class ProductListsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class ProductListsResponse(BaseModel):
    id: int
    uuid: UUID4
    owner_uuid: Optional[UUID4] = None
    name: Optional[ConstrainedStr] = None
    start_on: Optional[date]
    end_on: Optional[date]
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime]
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class ProductListsPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    product_lists: Optional[List[ProductListsResponse]] = None


class ProductListsDelResponse(ProductListsResponse):
    sys_deleted_at: Optional[datetime]
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
