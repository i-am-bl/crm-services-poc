from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from posixpath import ismount
from typing import List, Literal, Optional

from click import Option
from pydantic import UUID4, BaseModel, field_validator

from app.schemas._variables import ConstrainedDec, TimeStamp


class OrderItems(BaseModel):
    order_id: int
    order_uuid: UUID4
    product_list_item_id: int
    product_list_item_uuid: UUID4
    owner_id: Optional[int] = None
    adjusted_by_id: Optional[int] = None
    original_price: ConstrainedDec
    # TODO: refactor these options to source from constants file
    adjustment_type: Optional[Literal["dollar", "percentage"]] = None
    price_adjustment: Optional[ConstrainedDec] = None

    @field_validator("original_price", mode="before")
    def round_price(cls, value):
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class OrderItemsCreate(OrderItems):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class OrderItemsUpdate(BaseModel):
    product_list_item_id: Optional[int] = None
    product_list_item_uuid: Optional[UUID4] = None
    owner_id: Optional[int] = None
    adjusted_by_id: Optional[int] = None
    original_price: Optional[ConstrainedDec] = None
    adjustment_type: Optional[Literal["dollar", "percentage"]] = None
    price_adjustment: Optional[ConstrainedDec] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None

    @field_validator("original_price", mode="before")
    def round_price(cls, value):
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class OrderItemsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class OrderItemsResponse(BaseModel):
    id: int
    uuid: UUID4
    order_id: int
    order_uuid: UUID4
    product_list_item_id: int
    product_list_item_uuid: UUID4
    owner_id: Optional[int] = None
    adjusted_by_id: Optional[int]
    original_price: Optional[ConstrainedDec] = None
    adjustment_type: Optional[Literal["dollar", "percentage"]] = None
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None


class OrderItemsPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    order_items: Optional[List[OrderItemsResponse]] = None


class OrderItemsDelResponse(OrderItemsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None
