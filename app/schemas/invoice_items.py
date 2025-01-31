from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from typing import Annotated, List, Optional

from pydantic import UUID4, BaseModel, Field, field_validator

from ..constants.enums import ItemAdjustmentType
from ._variables import ConstrainedDec, TimeStamp


class InvoiceItemsCreate(BaseModel):
    """Represents an invoice item, including product and pricing details."""

    invoice_uuid: UUID4 = Field(..., description="UUID of the associated invoice.")
    order_item_uuid: UUID4 = Field(
        ..., description="UUID of the associated order item."
    )
    product_list_item_uuid: UUID4 = Field(
        ..., description="UUID of the associated product list item."
    )
    owner_uuid: Optional[UUID4] = Field(
        None, description="UUID of the owner responsible for the item."
    )
    quantity: int = Field(1, description="Quantity of the item in the invoice.")
    original_price: Optional[ConstrainedDec] = Field(
        None, description="Original price of the item before adjustments."
    )
    adjustment_type: Annotated[Optional[ItemAdjustmentType], None] = Field(
        None, description="Type of price adjustment applied to the item."
    )
    price_adjustment: Optional[ConstrainedDec] = Field(
        None, description="Adjustment amount applied to the price."
    )

    @field_validator("original_price", mode="before")
    @classmethod
    def round_price(cls, value):
        """Ensures the original price is a Decimal rounded to two decimal places."""
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a numeric value")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class InvoiceItemsInternalCreate(InvoiceItemsCreate):
    """Model for creating an invoice item.

    Hiding system level fields from the client.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the item was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="UUID of the user who created the item."
    )


class InvoiceItemsUpdate(BaseModel):
    """Model for updating an invoice item."""

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the item was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the item."
    )


class InvoiceItemsDel(BaseModel):
    """Model for marking an invoice item as deleted."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the item was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the item."
    )


class InvoiceItemsRes(BaseModel):
    """Response model for an invoice item."""

    id: int = Field(..., description="Database identifier for the invoice item.")
    uuid: UUID4 = Field(..., description="Unique identifier for the invoice item.")
    invoice_uuid: UUID4 = Field(..., description="UUID of the associated invoice.")
    order_item_uuid: UUID4 = Field(
        ..., description="UUID of the associated order item."
    )
    product_list_item_uuid: UUID4 = Field(
        ..., description="UUID of the associated product list item."
    )
    owner_uuid: Optional[UUID4] = Field(
        None, description="UUID of the owner responsible for the item."
    )
    quantity: int = Field(..., description="Quantity of the item in the invoice.")
    original_price: Optional[ConstrainedDec] = Field(
        None, description="Original price of the item before adjustments."
    )
    adjustment_type: Annotated[Optional[ItemAdjustmentType], None] = Field(
        None, description="Type of price adjustment applied to the item."
    )
    price_adjustment: Optional[ConstrainedDec] = Field(
        None, description="Adjustment amount applied to the price."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp when the item was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the item."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the item was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the item."
    )

    class Config:
        from_attributes = True


class InvoiceItemsPgRes(BaseModel):
    """Paginated response model for invoice items."""

    total: int = Field(..., description="Total number of invoice items.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Number of records per page.")
    has_more: bool = Field(
        ..., description="Indicates if there are more records available."
    )
    invoice_items: Optional[List[InvoiceItemsRes]] = Field(
        None, description="List of invoice items."
    )


class InvoiceItemsDelRes(InvoiceItemsRes):
    """Response model for a deleted invoice item."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the item was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the item."
    )

    class Config:
        from_attributes = True
