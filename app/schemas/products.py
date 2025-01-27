from datetime import UTC, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field
from ._variables import ConstrainedStr, TimeStamp


class Products(BaseModel):
    name: ConstrainedStr
    code: Optional[ConstrainedStr] = None
    terms: Optional[ConstrainedStr] = None
    description: Optional[ConstrainedStr] = None
    sys_allowed_price_increase: Optional[bool] = None
    sys_allowed_price_decrease: Optional[bool] = None
    man_allowed_price_increase: Optional[bool] = None
    man_allowed_price_decrease: Optional[bool] = None


class ProductsCreate(Products):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class ProductsUpdate(BaseModel):
    name: Optional[ConstrainedStr] = None
    code: Optional[ConstrainedStr] = None
    terms: Optional[ConstrainedStr] = None
    description: Optional[ConstrainedStr] = None
    sys_allowed_price_increase: Optional[bool] = None
    sys_allowed_price_decrease: Optional[bool] = None
    man_allowed_price_increase: Optional[bool] = None
    man_allowed_price_decrease: Optional[bool] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class ProductsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class ProductsRes(BaseModel):
    id: int
    uuid: UUID4
    name: Optional[ConstrainedStr] = None
    code: Optional[ConstrainedStr] = None
    terms: Optional[ConstrainedStr] = None
    description: Optional[ConstrainedStr] = None
    sys_allowed_price_increase: Optional[bool] = None
    sys_allowed_price_decrease: Optional[bool] = None
    man_allowed_price_increase: Optional[bool] = None
    man_allowed_price_decrease: Optional[bool] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes = True


class ProductsPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    products: Optional[List[ProductsRes]] = None


class ProductsDelRes(ProductsRes):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
