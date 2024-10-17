from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel, field_validator

from app.schemas._variables import ConstrainedDec, TimeStamp


class ProductListItems(BaseModel):
    product_list_id: int
    product_list_uuid: UUID4
    product_id: int
    product_uuid: UUID4

    price: Optional[Decimal] = None
    sys_allowed_price_increase: Optional[bool] = None
    sys_allowed_price_decrease: Optional[bool] = None
    man_allowed_price_increase: Optional[bool] = None
    man_allowed_price_decrease: Optional[bool] = None

    @field_validator("price", mode="before")
    def round_price(cls, value):
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class ProductListItemsCreate(ProductListItems):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class ProductListItemsUpdate(BaseModel):
    price: Optional[ConstrainedDec] = None
    sys_allowed_price_increase: Optional[bool] = None
    sys_allowed_price_decrease: Optional[bool] = None
    man_allowed_price_increase: Optional[bool] = None
    man_allowed_price_decrease: Optional[bool] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None

    @field_validator("price", mode="before")
    def round_price(cls, value):
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class ProductListItemsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class ProductListItemsRespone(ProductListItems):
    id: int
    uuid: UUID4
    sys_created_at: datetime
    sys_updated_at: Optional[datetime]


class ProductListItemsPagRespone(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    product_list_items: Optional[List[ProductListItemsRespone]] = None


class ProductListItemsDelRespone(ProductListItemsRespone):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None
