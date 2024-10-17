from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.schemas._variables import ConstrainedStr, TimeStamp


class ProductLists(BaseModel):
    owner_id: int
    name: ConstrainedStr
    start_on: Optional[date]
    end_on: Optional[date]


class ProductListsCreate(ProductLists):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class ProductListsUpdate(ProductLists):
    owner_id: Optional[int] = None
    name: Optional[ConstrainedStr] = None
    start_on: Optional[date] = None
    end_on: Optional[date] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class ProductListsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class ProductListsResponse(ProductLists):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[int]
    sys_updated_at: Optional[datetime]
    sys_updated_by: Optional[int]

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
    sys_deleted_by: Optional[int]

    class Config:
        from_attributes = True
