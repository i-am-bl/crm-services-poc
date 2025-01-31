from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field, field_validator

from ._variables import ConstrainedDec, TimeStamp


class ProductListItemsCreate(BaseModel):
    """Represents a product item in a product list, including pricing and allowed adjustments."""

    product_list_uuid: UUID4 = Field(
        ..., description="UUID of the associated product list."
    )
    product_uuid: UUID4 = Field(..., description="UUID of the associated product.")

    price: Optional[Decimal] = Field(
        None, description="Price of the product list item."
    )
    sys_allowed_price_increase: Optional[bool] = Field(
        None, description="Flag indicating if price increase is allowed by the system."
    )
    sys_allowed_price_decrease: Optional[bool] = Field(
        None, description="Flag indicating if price decrease is allowed by the system."
    )
    man_allowed_price_increase: Optional[bool] = Field(
        None,
        description="Flag indicating if price increase is allowed by the manufacturer.",
    )
    man_allowed_price_decrease: Optional[bool] = Field(
        None,
        description="Flag indicating if price decrease is allowed by the manufacturer.",
    )

    @field_validator("price", mode="before")
    def round_price(cls, value):
        """Rounds the price to two decimal places."""
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class ProductListItemsInternalCreate(ProductListItemsCreate):
    """Model for creating a new product list item.

    Hides system level fields from client.
    """

    sys_created_at: datetime = Field(
        TimeStamp, description="Timestamp when the product list item was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="UUID of the user who created the product list item."
    )


class ProductListItemsUpdate(BaseModel):
    """Model for updating an existing product list item."""

    price: Optional[ConstrainedDec] = Field(
        None, description="Updated price of the product list item."
    )
    sys_allowed_price_increase: Optional[bool] = Field(
        None, description="Updated flag for price increase allowed by the system."
    )
    sys_allowed_price_decrease: Optional[bool] = Field(
        None, description="Updated flag for price decrease allowed by the system."
    )
    man_allowed_price_increase: Optional[bool] = Field(
        None, description="Updated flag for price increase allowed by the manufacturer."
    )
    man_allowed_price_decrease: Optional[bool] = Field(
        None, description="Updated flag for price decrease allowed by the manufacturer."
    )

    @field_validator("price", mode="before")
    def round_price(cls, value):
        """Rounds the price to two decimal places."""
        if isinstance(value, (float, int)):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            raise ValueError("Price must be a number")
        return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


class ProductListItemsInternalUpdate(ProductListItemsUpdate):
    """Model for updating an existing product list item.

    Hides system level fields from client.
    """

    sys_updated_at: datetime = Field(
        TimeStamp, description="Timestamp when the product list item was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the product list item."
    )


class ProductListItemsDel(BaseModel):
    """Model for marking a product list item as deleted."""

    sys_deleted_at: datetime = Field(
        TimeStamp, description="Timestamp when the product list item was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the product list item."
    )


class ProductListItemsRes(BaseModel):
    """Response model for a product list item."""

    id: int = Field(..., description="Database identifier for the product list item.")
    uuid: UUID4 = Field(..., description="Unique identifier for the product list item.")
    product_list_uuid: UUID4 = Field(
        ..., description="UUID of the associated product list."
    )
    product_uuid: UUID4 = Field(..., description="UUID of the associated product.")
    price: Optional[Decimal] = Field(
        None, description="Price of the product list item."
    )
    sys_allowed_price_increase: Optional[bool] = Field(
        None, description="Flag for price increase allowed by the system."
    )
    sys_allowed_price_decrease: Optional[bool] = Field(
        None, description="Flag for price decrease allowed by the system."
    )
    man_allowed_price_increase: Optional[bool] = Field(
        None, description="Flag for price increase allowed by the manufacturer."
    )
    man_allowed_price_decrease: Optional[bool] = Field(
        None, description="Flag for price decrease allowed by the manufacturer."
    )
    sys_created_at: datetime = Field(
        ..., description="Timestamp when the product list item was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="UUID of the user who created the product list item."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the product list item was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="UUID of the user who last updated the product list item."
    )

    class Config:
        from_attributes = True


class ProductListItemsPgRes(BaseModel):
    """Paginated response model for product list items."""

    total: int = Field(..., description="Total number of product list items.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(
        ..., description="Maximum number of product list items per page."
    )
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    product_list_items: Optional[List[ProductListItemsRes]] = Field(
        None, description="List of product list items."
    )


class ProductListItemsDelRes(ProductListItemsRes):
    """Response model for a deleted product list item."""

    sys_deleted_at: datetime = Field(
        ..., description="Timestamp when the product list item was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="UUID of the user who deleted the product list item."
    )

    class Config:
        from_attributes = True
