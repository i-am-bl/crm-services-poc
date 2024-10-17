from datetime import UTC, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, StringConstraints

from app.schemas._variables import ConstrainedStr, TimeStamp


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
    sys_created_by: Optional[int] = None


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
    sys_updated_by: Optional[int] = None


class ProductsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class ProductsResponse(Products):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProductsPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    products: Optional[List[ProductsResponse]] = None


class ProductsDelResponse(ProductsResponse):
    sys_updated_at: Optional[datetime]
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int]

    class Config:
        from_attributes = True
