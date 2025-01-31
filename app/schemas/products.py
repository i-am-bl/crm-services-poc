from datetime import UTC, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field
from ._variables import ConstrainedStr, TimeStamp


class ProductsCreate(BaseModel):
    """Model representing a product."""

    name: ConstrainedStr = Field(..., description="The name of the product.")
    code: Optional[ConstrainedStr] = Field(
        None, description="The product code (optional)."
    )
    terms: Optional[ConstrainedStr] = Field(
        None, description="Terms associated with the product (optional)."
    )
    description: Optional[ConstrainedStr] = Field(
        None, description="Description of the product (optional)."
    )
    sys_allowed_price_increase: Optional[bool] = Field(
        None, description="Whether price increase is allowed (system-controlled)."
    )
    sys_allowed_price_decrease: Optional[bool] = Field(
        None, description="Whether price decrease is allowed (system-controlled)."
    )
    man_allowed_price_increase: Optional[bool] = Field(
        None, description="Whether price increase is allowed (manufacturer-controlled)."
    )
    man_allowed_price_decrease: Optional[bool] = Field(
        None, description="Whether price decrease is allowed (manufacturer-controlled)."
    )


class ProductsInternalCreate(ProductsCreate):
    """Model for creating a new product, inheriting from `ProductsCreate`.

    Hides system level fields from the client.
    """

    sys_created_at: datetime = Field(
        ...,
        description="The timestamp when the product was created, automatically set.",
    )
    sys_created_by: UUID4 = Field(
        ..., description="The UUID of the user who created the product."
    )


class ProductsUpdate(BaseModel):
    """Model for updating an existing product."""

    name: Optional[ConstrainedStr] = Field(
        None, description="The name of the product (optional for update)."
    )
    code: Optional[ConstrainedStr] = Field(
        None, description="The product code (optional for update)."
    )
    terms: Optional[ConstrainedStr] = Field(
        None, description="Terms associated with the product (optional for update)."
    )
    description: Optional[ConstrainedStr] = Field(
        None, description="Description of the product (optional for update)."
    )
    sys_allowed_price_increase: Optional[bool] = Field(
        None,
        description="Whether price increase is allowed (system-controlled, optional).",
    )
    sys_allowed_price_decrease: Optional[bool] = Field(
        None,
        description="Whether price decrease is allowed (system-controlled, optional).",
    )
    man_allowed_price_increase: Optional[bool] = Field(
        None,
        description="Whether price increase is allowed (manufacturer-controlled, optional).",
    )
    man_allowed_price_decrease: Optional[bool] = Field(
        None,
        description="Whether price decrease is allowed (manufacturer-controlled, optional).",
    )


class ProductsInternalUpdate(ProductsUpdate):
    """Model for updating an existing product.

    Hides system level fields from client.
    """

    sys_updated_at: datetime = Field(
        ...,
        description="The timestamp when the product was last updated, automatically set.",
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who last updated the product."
    )


class ProductsDel(BaseModel):
    """Model for deleting a product."""

    sys_deleted_at: datetime = Field(
        ...,
        description="The timestamp when the product was deleted, automatically set.",
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the product."
    )


class ProductsRes(BaseModel):
    """Response model for a product with detailed attributes."""

    id: int = Field(..., description="The ID of the product.")
    uuid: UUID4 = Field(..., description="The UUID of the product.")
    name: Optional[ConstrainedStr] = Field(None, description="The name of the product.")
    code: Optional[ConstrainedStr] = Field(None, description="The product code.")
    terms: Optional[ConstrainedStr] = Field(
        None, description="Terms associated with the product."
    )
    description: Optional[ConstrainedStr] = Field(
        None, description="Description of the product."
    )
    sys_allowed_price_increase: Optional[bool] = Field(
        None, description="Whether price increase is allowed (system-controlled)."
    )
    sys_allowed_price_decrease: Optional[bool] = Field(
        None, description="Whether price decrease is allowed (system-controlled)."
    )
    man_allowed_price_increase: Optional[bool] = Field(
        None, description="Whether price increase is allowed (manufacturer-controlled)."
    )
    man_allowed_price_decrease: Optional[bool] = Field(
        None, description="Whether price decrease is allowed (manufacturer-controlled)."
    )
    sys_created_at: datetime = Field(
        ..., description="The timestamp when the product was created."
    )
    sys_created_by: UUID4 = Field(
        ..., description="The UUID of the user who created the product."
    )
    sys_updated_at: Optional[datetime] = Field(
        None, description="The timestamp when the product was last updated."
    )
    sys_updated_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who last updated the product."
    )

    class Config:
        from_attributes = True


class ProductsPgRes(BaseModel):
    """Paginated response model for products."""

    total: int = Field(..., description="Total number of products.")
    page: int = Field(..., description="Current page number.")
    limit: int = Field(..., description="Maximum number of products per page.")
    has_more: bool = Field(
        ..., description="Indicates whether there are more pages available."
    )
    products: Optional[List[ProductsRes]] = Field(
        None, description="List of products in the current page."
    )


class ProductsDelRes(ProductsRes):
    """Response model for deleted products."""

    sys_deleted_at: datetime = Field(
        ..., description="The timestamp when the product was deleted."
    )
    sys_deleted_by: Optional[UUID4] = Field(
        None, description="The UUID of the user who deleted the product."
    )

    class Config:
        from_attributes = True
