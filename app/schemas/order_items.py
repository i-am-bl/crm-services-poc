from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field, field_validator

from ..constants.enums import ItemAdjustmentType
from ._variables import ConstrainedDec, TimeStamp


class OrderItems(BaseModel):
    """Represents an individual order item, including details about the product, price, and quantity."""

    order_uuid: UUID4 = Field(..., description="UUID of the associated order.")
    product_list_item_uuid: UUID4 = Field(
        ..., description="UUID of the product list item."
    )
    owner_uuid: Optional[UUID4] = Field(
        None, description="UUID of the owner of the item."
    )
    original_price: ConstrainedDec = Field(
        ..., description="Original price of the item."
    )
    quantity: Optional[int] = Field(1, description="Quantity of the ordered item.")
    adjustment_type: Optional[ItemAdjustmentType] = Field(
        None, description="Type of price adjustment, if any."
    )
    price_adjustment: Optional[ConstrainedDec] = Field(
        None, description="Price adjustment applied, if any."
    )

    @field_validator("original_price", mode="before")
    def round_price(cls, value):
        """Rounds the original price to two decimal places."""
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class OrderItemsCreate(OrderItems):
    """Model for creating a new order item."""

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the order item was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the order item."
    )


class OrderItemsUpdate(BaseModel):
    """Model for updating an existing order item."""

    product_list_item_uuid: Optional[UUID4] = Field(
        None, description="Updated UUID of the product list item."
    )
    owner_uuid: Optional[UUID4] = Field(
        None, description="Updated UUID of the owner of the item."
    )
    quantity: Optional[int] = Field(
        None, description="Updated quantity of the ordered item."
    )
    original_price: Optional[ConstrainedDec] = Field(
        None, description="Updated original price of the item."
    )
    adjustment_type: Optional[ItemAdjustmentType] = Field(
        None, description="Updated adjustment type."
    )
    price_adjustment: Optional[ConstrainedDec] = Field(
        None, description="Updated price adjustment."
    )

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the order item was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the order item."
    )

    @field_validator("original_price", mode="before")
    def round_price(cls, value):
        """Rounds the original price to two decimal places."""
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class OrderItemsDel(BaseModel):
    """Model for marking an order item as deleted."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the order item was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the order item."
    )


class OrderItemsRes(BaseModel):
    """Response model for an order item."""

    id: int = Field(..., description="Database identifier for the order item.")
    uuid: UUID4 = Field(..., description="Unique identifier for the order item.")
    order_uuid: UUID4 = Field(..., description="UUID of the associated order.")
    product_list_item_uuid: UUID4 = Field(
        ..., description="UUID of the product list item."
    )
    owner_uuid: Optional[UUID4] = Field(
        None, description="UUID of the owner of the item."
    )
    quantity: int = Field(..., description="Quantity of the ordered item.")
    original_price: Optional[ConstrainedDec] = Field(
        None, description="Original price of the item."
    )
    adjustment_type: Optional[ItemAdjustmentType] = Field(
        None, description="Type of price adjustment, if any."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp when the order item was created."
    )
    sys_created_by: Optional[UUID4] = Field(
        None, description="UUID of the user who created the order item."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the order item was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the order item."
    )


class OrderItemsPgRes(BaseModel):
    """Paginated response model for order items."""

    total: int = Field(..., description="Total number of order items.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Maximum number of order items per page.")
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    order_items: Optional[List[OrderItemsRes]] = Field(
        None, description="List of order items."
    )


class OrderItemsDelRes(OrderItemsRes):
    """Response model for a deleted order item."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the order item was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the order item."
    )
