from datetime import UTC, date, datetime
from decimal import ROUND_DOWN, Decimal
from typing import Annotated, List, Literal, Optional

from pydantic import UUID4, BaseModel, field_validator

from ..constants import constants as cnst
from ._variables import ConstrainedDec, TimeStamp


class InvoiceItems(BaseModel):
    invoice_uuid: UUID4
    order_item_uuid: UUID4
    product_list_item_uuid: UUID4
    owner_uuid: Optional[UUID4] = None
    adjusted_by: Optional[UUID4] = None
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
    sys_created_by: Optional[UUID4] = None


class InvoiceItemsUpdate(BaseModel):
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class InvoiceItemsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class InvoiceItemsResponse(BaseModel):
    id: int
    uuid: UUID4
    invoice_uuid: UUID4
    order_item_uuid: UUID4
    product_list_item_uuid: UUID4
    owner_uuid: Optional[UUID4] = None
    adjusted_by: Optional[UUID4] = None
    original_price: Optional[ConstrainedDec] = None
    # TODO: migrate literals to a constants file
    adjustment_type: Optional[Literal["dollar", "percentage"]] = None
    price_adjustment: Optional[ConstrainedDec] = None
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

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
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes = True
