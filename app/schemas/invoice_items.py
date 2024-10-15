from datetime import UTC, date, datetime
from decimal import ROUND_DOWN, Decimal
from typing import Annotated, List, Literal, Optional

from pydantic import UUID4, BaseModel, field_validator

import app.constants as cnst
from app.schemas._variables import ConstrainedDec, TimeStamp


class InvoiceItems(BaseModel):
    invoice_id: int
    invoice_uuid: UUID4
    order_item_id: int
    order_item_uuid: UUID4
    product_list_item_id: int
    product_list_item_uuid: UUID4
    owner_id: Optional[int] = None
    adjusted_by_id: Optional[int] = None
    original_price: Optional[ConstrainedDec] = None
    adjustment_type: Optional[Literal["dollar", "percentage"]] = None
    price_adjustment: Optional[ConstrainedDec] = None

    @field_validator("original_price", mode="before")
    def round_price(cls, value):
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class InvoiceItemsCreate(InvoiceItems):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[int] = None


class InvoiceItemsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[int] = None


class InvoiceItemsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class InvoiceItemsResponse(BaseModel):
    id: int
    uuid: UUID4
    invoice_id: int
    invoice_uuid: UUID4
    order_item_id: int
    order_item_uuid: UUID4
    product_list_item_id: int
    product_list_item_uuid: UUID4
    owner_id: Optional[int] = None
    adjusted_by_id: Optional[int] = None
    original_price: Optional[ConstrainedDec] = None
    # TODO: migrate literals to a constants file
    adjustment_type: Optional[Literal["dollar", "percentage"]] = None
    price_adjustment: Optional[ConstrainedDec] = None
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class InvoiceItemsPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    invoice_items: Optional[List[InvoiceItemsResponse]] = None


class InvoiceItemsDelResponse(InvoiceItemsResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None

    class Config:
        from_attributes = True
